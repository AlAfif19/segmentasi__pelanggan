"""Reconstruct and render the actual production K-Means model trace."""

from datetime import date, datetime
from pathlib import Path
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from repositories import mysql_repository
from services.crispdm_service import (
    PRODUCTION_MODEL_CONFIG,
    _category_score,
    _days_between,
    _minmax,
    calculate_loyalty,
)


ANALYSIS_DATE = date(2026, 6, 7)
N_CLUSTERS = 4
RANDOM_STATE = 42
N_INIT = 30
FEATURE_NAMES = ("loyalty", "recency", "frequency", "monetary", "category")
INITIALIZATION_NOTE = (
    "Jejak ini adalah satu inisialisasi K-Means++ yang dapat direproduksi "
    "dengan random_state=42. Nilai probabilitas adalah bobot D(x)^2 pada "
    "tahap pemilihan terkait; ini bukan rekaman internal inisialisasi yang "
    "dipertahankan scikit-learn dari n_init=30."
)


def _prepare_actual_data():
    import numpy as np
    from sklearn.preprocessing import StandardScaler

    source_rows = mysql_repository.get_lrfmc_source_rows(
        None,
        ANALYSIS_DATE,
        ANALYSIS_DATE,
    )
    source_rows = sorted(source_rows, key=lambda row: str(row["customer_id"]))
    if not source_rows:
        raise RuntimeError("Database tidak berisi data pelanggan untuk dianalisis")

    loyalty_values = [
        calculate_loyalty(
            ANALYSIS_DATE,
            row["active_date"],
            row.get("first_transaction"),
            row.get("last_transaction_all"),
        )["days"]
        for row in source_rows
    ]
    observed_recency = [
        _days_between(ANALYSIS_DATE, row["last_transaction"], default=None)
        for row in source_rows
        if row["last_transaction"]
    ]
    recency_fill = max(observed_recency) + 30 if observed_recency else 999
    recency_days = [
        _days_between(
            ANALYSIS_DATE,
            row["last_transaction"],
            default=recency_fill,
        )
        for row in source_rows
    ]
    frequencies = [float(row["frequency"] or 0) for row in source_rows]
    monetary_values = [float(row["monetary"] or 0) for row in source_rows]
    average_payments = [
        monetary_values[index] / frequencies[index]
        if frequencies[index] > 0
        else 0.0
        for index in range(len(source_rows))
    ]
    category_scores = [
        _category_score(
            row["category"],
            row.get("monthly_fee"),
            average_payments[index],
        )
        for index, row in enumerate(source_rows)
    ]

    loyalty_normalized = _minmax(loyalty_values)
    recency_scores = _minmax(recency_days, invert=True)
    frequency_normalized = _minmax(frequencies)
    monetary_normalized = _minmax(monetary_values)
    category_normalized = _minmax(category_scores)

    raw_matrix = np.asarray(
        [
            [
                loyalty_values[index],
                recency_scores[index],
                frequencies[index],
                monetary_values[index],
                category_scores[index],
            ]
            for index in range(len(source_rows))
        ],
        dtype=float,
    )
    business_matrix = np.asarray(
        [
            [
                loyalty_normalized[index],
                recency_scores[index],
                frequency_normalized[index],
                monetary_normalized[index],
                category_normalized[index],
            ]
            for index in range(len(source_rows))
        ],
        dtype=float,
    )

    model_ready = raw_matrix.copy()
    if PRODUCTION_MODEL_CONFIG["transform"] == "log1p_frequency_monetary":
        model_ready[:, 2] = np.log1p(model_ready[:, 2])
        model_ready[:, 3] = np.log1p(model_ready[:, 3])

    winsor = PRODUCTION_MODEL_CONFIG["winsor"]
    for column in range(model_ready.shape[1]):
        lower = np.quantile(model_ready[:, column], winsor)
        upper = np.quantile(model_ready[:, column], 1 - winsor)
        if lower < upper:
            model_ready[:, column] = np.clip(
                model_ready[:, column],
                lower,
                upper,
            )

    if PRODUCTION_MODEL_CONFIG["scaler"] != "StandardScaler":
        raise RuntimeError("Extractor hanya mendukung konfigurasi produksi StandardScaler")
    scaled_matrix = StandardScaler().fit_transform(model_ready)
    return source_rows, raw_matrix, business_matrix, scaled_matrix


def _build_segment_mapping(labels, business_matrix):
    cluster_scores = {}
    for cluster in sorted(set(int(label) for label in labels)):
        members = business_matrix[labels == cluster]
        cluster_scores[cluster] = float(members.mean(axis=1).mean())

    ranked_clusters = sorted(cluster_scores, key=cluster_scores.get)
    mapping = {}
    for rank, cluster in enumerate(ranked_clusters):
        ratio = rank / max(len(ranked_clusters) - 1, 1)
        if ratio <= 0.34:
            mapping[cluster] = "Low-Value"
        elif ratio <= 0.67:
            mapping[cluster] = "Medium-Value"
        else:
            mapping[cluster] = "High-Value"
    return mapping


def _build_probability_steps(source_rows, scaled_matrix):
    import numpy as np
    from sklearn.cluster import kmeans_plusplus

    _, selected_indices = kmeans_plusplus(
        scaled_matrix,
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_local_trials=1,
    )
    steps = []
    for selection_index, customer_index in enumerate(selected_indices):
        step = {
            "selection": selection_index + 1,
            "customer_id": str(source_rows[int(customer_index)]["customer_id"]),
            "customer_name": source_rows[int(customer_index)]["name"],
            "nearest_d_squared": None,
            "total_d_squared": None,
            "selected_probability": None,
        }
        if selection_index:
            selected_centers = scaled_matrix[selected_indices[:selection_index]]
            squared_distances = (
                (scaled_matrix[:, np.newaxis, :] - selected_centers[np.newaxis, :, :])
                ** 2
            ).sum(axis=2)
            nearest_squared = squared_distances.min(axis=1)
            total_squared = float(nearest_squared.sum())
            selected_squared = float(nearest_squared[int(customer_index)])
            step.update(
                {
                    "nearest_d_squared": selected_squared,
                    "total_d_squared": total_squared,
                    "selected_probability": selected_squared / total_squared,
                }
            )
        steps.append(step)
    return steps


def _raw_lrfmc(values):
    return {
        feature: float(values[index])
        for index, feature in enumerate(FEATURE_NAMES)
    }


def build_actual_model_trace():
    """Build a read-only trace of the actual all-data production model."""
    import numpy as np
    from sklearn.cluster import KMeans

    database_analysis_date = mysql_repository.get_analysis_date()
    if isinstance(database_analysis_date, datetime):
        database_analysis_date = database_analysis_date.date()
    if database_analysis_date != ANALYSIS_DATE:
        raise RuntimeError(
            "Tanggal analisis database tidak sesuai: "
            f"diharapkan {ANALYSIS_DATE.isoformat()}, "
            f"didapat {database_analysis_date}"
        )

    source_rows, raw_matrix, business_matrix, scaled_matrix = (
        _prepare_actual_data()
    )
    model = KMeans(
        n_clusters=N_CLUSTERS,
        init="k-means++",
        random_state=RANDOM_STATE,
        n_init=N_INIT,
    ).fit(scaled_matrix)
    labels = model.labels_
    segment_mapping = _build_segment_mapping(labels, business_matrix)
    distances = np.linalg.norm(
        scaled_matrix[:, np.newaxis, :]
        - model.cluster_centers_[np.newaxis, :, :],
        axis=2,
    )

    assignments = []
    for index in range(min(20, len(source_rows))):
        nearest_cluster = int(np.argmin(distances[index]))
        assignments.append(
            {
                "customer_id": str(source_rows[index]["customer_id"]),
                "customer_name": source_rows[index]["name"],
                "raw_lrfmc": _raw_lrfmc(raw_matrix[index]),
                "distances": [
                    float(distance) for distance in distances[index]
                ],
                "nearest_cluster": nearest_cluster,
                "segment_label": segment_mapping[nearest_cluster],
            }
        )

    centroid_profiles = []
    cluster_counts = []
    for cluster in range(N_CLUSTERS):
        member_indexes = np.flatnonzero(labels == cluster)
        cluster_counts.append(int(len(member_indexes)))
        centroid_profiles.append(
            {
                "cluster": cluster,
                "raw_lrfmc": _raw_lrfmc(
                    raw_matrix[member_indexes].mean(axis=0)
                ),
                "customer_count": int(len(member_indexes)),
                "segment_label": segment_mapping[cluster],
            }
        )

    return {
        "analysis_date": ANALYSIS_DATE.isoformat(),
        "k": N_CLUSTERS,
        "iteration": int(model.n_iter_),
        "inertia": float(model.inertia_),
        "cluster_counts": cluster_counts,
        "initialization_note": INITIALIZATION_NOTE,
        "probability_steps": _build_probability_steps(
            source_rows,
            scaled_matrix,
        ),
        "assignments": assignments,
        "centroid_profiles": centroid_profiles,
    }


def _format_decimal(value, decimals):
    if value is None:
        return "-"
    text = f"{float(value):,.{decimals}f}"
    return text.replace(",", "_").replace(".", ",").replace("_", ".")


def _format_rupiah(value, decimals=0):
    return f"Rp {_format_decimal(value, decimals)}"


def _markdown_table(headers, rows):
    def clean(value):
        text = str(value).replace("|", r"\|")
        return "".join(
            char for char in text if unicodedata.category(char) != "Cf"
        )

    lines = [
        "| " + " | ".join(clean(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend(
        "| " + " | ".join(clean(value) for value in row) + " |"
        for row in rows
    )
    return "\n".join(lines)


def render_markdown_tables(trace):
    """Render the probability, assignment, and centroid tables in Indonesian."""
    probability_rows = []
    for step in trace["probability_steps"]:
        probability_rows.append(
            [
                step["selection"],
                step["customer_id"],
                step["customer_name"],
                _format_decimal(step["nearest_d_squared"], 6),
                _format_decimal(step["total_d_squared"], 6),
                _format_decimal(
                    None
                    if step["selected_probability"] is None
                    else step["selected_probability"] * 100,
                    6,
                ),
            ]
        )

    assignment_rows = []
    for row in trace["assignments"]:
        raw = row["raw_lrfmc"]
        assignment_rows.append(
            [
                row["customer_id"],
                row["customer_name"],
                _format_decimal(raw["loyalty"], 2),
                _format_decimal(raw["recency"], 4),
                _format_decimal(raw["frequency"], 0),
                _format_rupiah(raw["monetary"]),
                _format_decimal(raw["category"], 2),
                *[_format_decimal(distance, 4) for distance in row["distances"]],
                row["nearest_cluster"],
                row["segment_label"],
            ]
        )

    centroid_rows = []
    for row in trace["centroid_profiles"]:
        raw = row["raw_lrfmc"]
        centroid_rows.append(
            [
                row["cluster"],
                _format_decimal(raw["loyalty"], 2),
                _format_decimal(raw["recency"], 4),
                _format_decimal(raw["frequency"], 2),
                _format_rupiah(raw["monetary"], 2),
                _format_decimal(raw["category"], 4),
                row["customer_count"],
                row["segment_label"],
            ]
        )

    sections = [
        "## Probabilitas Inisialisasi K-Means++",
        "",
        trace["initialization_note"],
        "",
        _markdown_table(
            [
                "Pemilihan",
                "No. Pelanggan",
                "Nama Pelanggan",
                "D(x)^2 Terdekat",
                "Total D(x)^2",
                "Probabilitas (%)",
            ],
            probability_rows,
        ),
        "",
        "## Assignment 20 Pelanggan",
        "",
        (
            "Jarak dihitung pada ruang model terstandardisasi; nilai LRFMC "
            "ditampilkan dalam satuan bisnis."
        ),
        "",
        _markdown_table(
            [
                "Customer ID",
                "Nama Pelanggan",
                "L",
                "R",
                "F",
                "M",
                "C",
                "Jarak C0",
                "Jarak C1",
                "Jarak C2",
                "Jarak C3",
                "Cluster",
                "Segmen",
            ],
            assignment_rows,
        ),
        "",
        "## Update Centroid Akhir",
        "",
        (
            "Centroid interpretasi adalah rata-rata LRFMC mentah anggota "
            "cluster; assignment tetap menggunakan ruang terstandardisasi."
        ),
        "",
        _markdown_table(
            [
                "Cluster",
                "Rata-rata L",
                "Rata-rata R",
                "Rata-rata F",
                "Rata-rata M",
                "Rata-rata C",
                "Jumlah Pelanggan",
                "Segmen",
            ],
            centroid_rows,
        ),
    ]
    return "\n".join(sections)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render_markdown_tables(build_actual_model_trace()))


if __name__ == "__main__":
    main()
