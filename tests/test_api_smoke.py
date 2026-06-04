import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_segmentation_pipeline_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.post("/api/segmentation/run")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["data"]["status"] in {"completed", "database_unavailable", "no_data"}
    assert payload["data"]["segment_levels"] == ["Low", "Medium", "High"]


def test_download_endpoint_streams_browser_attachment():
    app = create_app()
    client = app.test_client()

    response = client.post("/api/download/", json={"format": "csv"})

    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")
    assert "segmentation_result.csv" in response.headers["Content-Disposition"]
    assert response.mimetype == "text/csv"
