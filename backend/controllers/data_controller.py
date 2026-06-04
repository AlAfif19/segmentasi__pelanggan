from services.embedded_data_service import preview_sources
from utils.response import ok


def embedded_data_action():
    return ok(preview_sources())
