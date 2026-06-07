import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app import create_app
from services.crispdm_service import resolve_period


def test_resolve_period_uses_calendar_month_boundaries():
    analysis_date = date(2026, 6, 7)

    assert resolve_period("1_month", analysis_date)["start_date"] == date(2026, 5, 7)
    assert resolve_period("3_months", analysis_date)["start_date"] == date(2026, 3, 7)
    assert resolve_period("6_months", analysis_date)["start_date"] == date(2025, 12, 7)
    assert resolve_period("1_year", analysis_date)["start_date"] == date(2025, 6, 7)
    assert resolve_period("all", analysis_date)["start_date"] is None


def test_resolve_period_rejects_unknown_code():
    try:
        resolve_period("2_years", date(2026, 6, 7))
    except ValueError as error:
        assert "Periode tidak valid" in str(error)
    else:
        raise AssertionError("Unknown period must be rejected")


def test_segmentation_endpoint_passes_selected_period_to_pipeline():
    app = create_app()
    client = app.test_client()

    with patch(
        "controllers.segmentation_controller.run_pipeline",
        return_value={"status": "completed", "segment_levels": ["Low", "Medium", "High"]},
    ) as run_pipeline:
        response = client.post("/api/segmentation/run", json={"period": "3_months"})

    assert response.status_code == 200
    run_pipeline.assert_called_once_with("3_months")


def test_segmentation_endpoint_rejects_invalid_period():
    app = create_app()
    client = app.test_client()

    response = client.post("/api/segmentation/run", json={"period": "2_years"})

    assert response.status_code == 400
    assert "Periode tidak valid" in response.get_json()["message"]
