import csv
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from services.crispdm_service import SCALER_COMPARISON_CONFIGS, run_pipeline, select_global_scaler


PERIODS = [
    ("1_month", "1 bulan"),
    ("3_months", "3 bulan"),
    ("6_months", "6 bulan"),
    ("1_year", "1 tahun"),
]
CANDIDATES = {"logfm_standard", "logfm_robust"}
OUTPUT_DIR = ROOT / "docs" / "research"


def main():
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    rows = []
    for period_code, period_label in PERIODS:
        result = run_pipeline(period_code, SCALER_COMPARISON_CONFIGS)
        for candidate in result["model_candidates"]:
            if candidate["name"] not in CANDIDATES:
                continue
            rows.append(
                {
                    "period": period_code,
                    "period_label": period_label,
                    "name": candidate["name"],
                    "scaler": candidate["scaler"],
                    "optimal_k": candidate["optimal_k"],
                    "silhouette_score": candidate["silhouette_score"],
                    "davies_bouldin_index": candidate["davies_bouldin_index"],
                    "calinski_harabasz_index": candidate["calinski_harabasz_index"],
                }
            )
        print(f"Evaluated {period_label}")

    selection = select_global_scaler(rows)
    score_by_key = {
        (row["period"], row["scaler"]): row["period_score"]
        for row in selection["rows"]
    }
    for row in rows:
        row["period_score"] = score_by_key[(row["period"], row["scaler"])]
        row["global_winner"] = row["scaler"] == selection["winner"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "scaler-comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    markdown = [
        "# Perbandingan Scaler Global",
        "",
        "Transformasi kedua kandidat sama: `log1p` pada Frequency dan Monetary, winsorization 1%.",
        "",
        "| Periode | Scaler | K | Silhouette | DBI | CHI | Skor periode |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        markdown.append(
            f"| {row['period_label']} | {row['scaler']} | {row['optimal_k']} | "
            f"{row['silhouette_score']:.4f} | {row['davies_bouldin_index']:.4f} | "
            f"{row['calinski_harabasz_index']:.2f} | {row['period_score']:.4f} |"
        )
    markdown.extend(
        [
            "",
            "## Skor Global",
            "",
            *[
                f"- {scaler}: {score:.4f}"
                for scaler, score in sorted(selection["scores"].items())
            ],
            "",
            f"**Scaler terpilih: {selection['winner']}**",
            "",
        ]
    )
    (OUTPUT_DIR / "scaler-comparison.md").write_text("\n".join(markdown), encoding="utf-8")
    print(f"Winner: {selection['winner']}")


if __name__ == "__main__":
    main()
