from services.embedded_data_service import get_summary
from services.evaluation_service import calculate_metrics
from utils.response import ok


def dashboard_action():
    return ok({"summary": get_summary(), "evaluation": calculate_metrics()})
