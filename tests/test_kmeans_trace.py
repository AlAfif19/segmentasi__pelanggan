import importlib.util
from pathlib import Path
import unicodedata

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "generate_kmeans_trace.py"


def _load_trace_module():
    assert SCRIPT_PATH.exists(), "K-Means trace extractor has not been implemented"
    spec = importlib.util.spec_from_file_location("generate_kmeans_trace", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_trace():
    module = _load_trace_module()
    return module, module.build_actual_model_trace()


def test_trace_is_deterministic():
    trace_module, trace = _build_trace()
    assert trace_module.build_actual_model_trace() == trace


def test_trace_matches_actual_production_model_metrics():
    _, trace = _build_trace()
    assert trace["analysis_date"] == "2026-06-07"
    assert trace["k"] == 4
    assert trace["iteration"] == 4
    assert trace["inertia"] == pytest.approx(295.6958481887592)
    assert trace["cluster_counts"] == [83, 83, 344, 9]


def test_probability_steps_reproduce_weighted_kmeans_plus_plus():
    _, trace = _build_trace()
    steps = trace["probability_steps"]

    assert [step["customer_id"] for step in steps] == [
        "10036056",
        "10276409",
        "10105764",
        "10072037",
    ]
    assert steps[0]["nearest_d_squared"] is None
    assert steps[0]["total_d_squared"] is None
    assert steps[0]["selected_probability"] is None
    assert all(step["customer_name"] for step in steps)

    expected = [
        (13.48952934274697, 10597.089886415639, 0.001272946581309944),
        (40.88828001294015, 2721.368454902594, 0.015024896735052244),
        (7.00851197462216, 2393.84676405324, 0.002927719551587091),
    ]
    for step, (distance_squared, total, probability) in zip(steps[1:], expected):
        assert step["nearest_d_squared"] == pytest.approx(distance_squared)
        assert step["total_d_squared"] == pytest.approx(total)
        assert step["selected_probability"] == pytest.approx(probability)
        assert step["selected_probability"] == pytest.approx(
            step["nearest_d_squared"] / step["total_d_squared"]
        )

    assert "satu inisialisasi" in trace["initialization_note"].lower()
    assert "n_init=30" in trace["initialization_note"]


def test_first_twenty_assignments_are_exact_and_use_distance_argmin():
    _, trace = _build_trace()
    assignments = trace["assignments"]
    expected = [
        ("10000128", 0, "Low-Value"),
        ("10000647", 2, "High-Value"),
        ("10000648", 0, "Low-Value"),
        ("10000649", 2, "High-Value"),
        ("10000650", 2, "High-Value"),
        ("10000651", 2, "High-Value"),
        ("10000653", 0, "Low-Value"),
        ("10000654", 2, "High-Value"),
        ("10000655", 2, "High-Value"),
        ("10000657", 2, "High-Value"),
        ("10000658", 2, "High-Value"),
        ("10000659", 0, "Low-Value"),
        ("10000660", 0, "Low-Value"),
        ("10000661", 2, "High-Value"),
        ("10000663", 2, "High-Value"),
        ("10000664", 2, "High-Value"),
        ("10000665", 0, "Low-Value"),
        ("10000666", 2, "High-Value"),
        ("10000667", 0, "Low-Value"),
        ("10000668", 2, "High-Value"),
    ]

    assert [
        (row["customer_id"], row["nearest_cluster"], row["segment_label"])
        for row in assignments
    ] == expected
    assert assignments[0]["customer_name"] == "Aswin / Batagor"
    assert len(assignments) == 20
    assert [row["customer_id"] for row in assignments] == sorted(
        row["customer_id"] for row in assignments
    )

    for row in assignments:
        assert set(row["raw_lrfmc"]) == {
            "loyalty",
            "recency",
            "frequency",
            "monetary",
            "category",
        }
        assert len(row["distances"]) == 4
        assert row["nearest_cluster"] == min(
            range(4), key=lambda cluster: row["distances"][cluster]
        )

    assert assignments[0]["raw_lrfmc"] == {
        "loyalty": 0.0,
        "recency": 0.0,
        "frequency": 0.0,
        "monetary": 0.0,
        "category": 1.45,
    }
    assert assignments[1]["raw_lrfmc"]["monetary"] == 1100000.0


def test_centroid_profiles_match_actual_cluster_counts_and_labels():
    _, trace = _build_trace()
    profiles = trace["centroid_profiles"]

    assert [
        (row["cluster"], row["customer_count"], row["segment_label"])
        for row in profiles
    ] == [
        (0, 83, "Low-Value"),
        (1, 83, "Medium-Value"),
        (2, 344, "High-Value"),
        (3, 9, "Low-Value"),
    ]
    assert sum(row["customer_count"] for row in profiles) == 519
    assert profiles[2]["raw_lrfmc"]["monetary"] == pytest.approx(
        1069912.7906976745
    )


def test_rendered_markdown_has_indonesian_tables_and_expected_rows():
    trace_module, trace = _build_trace()
    markdown = trace_module.render_markdown_tables(trace)

    assert "## Probabilitas Inisialisasi K-Means++" in markdown
    assert "## Assignment 20 Pelanggan" in markdown
    assert "## Update Centroid Akhir" in markdown
    assert "bukan rekaman internal" in markdown
    assert "Nama Pelanggan" in markdown
    assert "Probabilitas (%)" in markdown
    assert "Aswin / Batagor" in markdown
    assert not any(unicodedata.category(char) == "Cf" for char in markdown)
    assert "Rp 1.100.000" in markdown
    assert "0,2153" in markdown

    sections = markdown.split("\n## ")
    probability = next(section for section in sections if "Probabilitas" in section)
    assignments = next(section for section in sections if "Assignment" in section)
    centroids = next(section for section in sections if "Update Centroid" in section)
    assert sum(line.startswith("|") for line in probability.splitlines()) == 6
    assert sum(line.startswith("|") for line in assignments.splitlines()) == 22
    assert sum(line.startswith("|") for line in centroids.splitlines()) == 6
