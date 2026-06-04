import csv
import json
from io import BytesIO, StringIO

from openpyxl import Workbook
from repositories import mysql_repository
from services.result_service import get_results


def export_result(file_format, include_metadata=True, include_evaluation=True):
    file_format = file_format.lower()
    if file_format not in {"csv", "excel", "json"}:
        file_format = "csv"

    result = get_results(page=1, per_page=100)
    if mysql_repository.is_ready():
        total = mysql_repository.count_customers_result()
        customers = mysql_repository.get_customers(limit=max(total, 1), offset=0)
    else:
        customers = result["customers"]

    suffix = "xlsx" if file_format == "excel" else file_format
    filename = f"segmentation_result.{suffix}"
    payload = {
        "metadata": result["summary"] if include_metadata else None,
        "evaluation": result["evaluation"] if include_evaluation else None,
        "customers": customers,
    }

    if file_format == "json":
        content = json.dumps(payload, indent=2, default=str).encode("utf-8")
        return BytesIO(content), "application/json", filename

    fieldnames = (
        list(customers[0].keys())
        if customers
        else [
            "customer_id",
            "name",
            "recency",
            "frequency",
            "monetary",
            "lrfmc_combination",
            "cluster",
            "segment_label",
            "recommendation",
        ]
    )

    if file_format == "excel":
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Segmentation Result"
        sheet.append(fieldnames)
        for row in customers:
            sheet.append([row.get(field) for field in fieldnames])
        stream = BytesIO()
        workbook.save(stream)
        stream.seek(0)
        return stream, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename

    text_stream = StringIO()
    writer = csv.DictWriter(text_stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(customers)
    return BytesIO(text_stream.getvalue().encode("utf-8-sig")), "text/csv", filename
