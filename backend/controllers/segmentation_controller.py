from services.crispdm_service import run_pipeline
from utils.response import ok


def run_segmentation_action():
    return ok(run_pipeline(), "Segmentasi selesai")
