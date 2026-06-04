from flask import request

from services.search_service import search_customers
from utils.response import ok


def search_action():
    rows = search_customers(
        keyword=request.args.get("keyword", ""),
        category=request.args.get("category", "name"),
        segment=request.args.get("segment", "all"),
    )
    return ok({"rows": rows, "count": len(rows)})
