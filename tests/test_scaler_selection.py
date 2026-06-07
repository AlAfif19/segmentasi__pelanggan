import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from services.crispdm_service import select_global_scaler


def test_select_global_scaler_aggregates_period_scores():
    rows = [
        {"period": "1_month", "scaler": "StandardScaler", "silhouette_score": 0.7, "davies_bouldin_index": 0.5, "calinski_harabasz_index": 100},
        {"period": "1_month", "scaler": "RobustScaler", "silhouette_score": 0.8, "davies_bouldin_index": 0.4, "calinski_harabasz_index": 120},
        {"period": "3_months", "scaler": "StandardScaler", "silhouette_score": 0.6, "davies_bouldin_index": 0.6, "calinski_harabasz_index": 90},
        {"period": "3_months", "scaler": "RobustScaler", "silhouette_score": 0.7, "davies_bouldin_index": 0.5, "calinski_harabasz_index": 110},
    ]

    result = select_global_scaler(rows)

    assert result["winner"] == "RobustScaler"
    assert result["scores"]["RobustScaler"] > result["scores"]["StandardScaler"]


def test_select_global_scaler_prefers_standard_on_complete_tie():
    rows = [
        {"period": "1_month", "scaler": "StandardScaler", "silhouette_score": 0.7, "davies_bouldin_index": 0.5, "calinski_harabasz_index": 100},
        {"period": "1_month", "scaler": "RobustScaler", "silhouette_score": 0.7, "davies_bouldin_index": 0.5, "calinski_harabasz_index": 100},
    ]

    result = select_global_scaler(rows)

    assert result["winner"] == "StandardScaler"
