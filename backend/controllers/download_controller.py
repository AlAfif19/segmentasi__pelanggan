from flask import request, send_file

from services.download_service import export_result


def download_action():
    payload = request.get_json(silent=True) or {}
    stream, mimetype, filename = export_result(
        payload.get("format", "csv"),
        include_metadata=payload.get("include_metadata", True),
        include_evaluation=payload.get("include_evaluation", True),
    )
    return send_file(
        stream,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
        max_age=0,
    )
