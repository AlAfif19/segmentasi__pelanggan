from flask import request

from services.crispdm_service import run_pipeline
from utils.response import fail, ok


def run_segmentation_action():
    payload = request.get_json(silent=True) or {}
    try:
        return ok(run_pipeline(payload.get("period", "all")), "Segmentasi selesai")
    except ValueError as error:
        return fail(str(error)), 400
