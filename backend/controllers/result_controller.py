from flask import request

from services.result_service import get_results
from utils.response import ok


def result_action():
    return ok(
        get_results(
            page=request.args.get("page", 1),
            per_page=request.args.get("per_page", 10),
            keyword=request.args.get("keyword", ""),
            category=request.args.get("category", "name"),
            segment=request.args.get("segment", "all"),
            payment_status=request.args.get("payment_status", "all"),
        )
    )
