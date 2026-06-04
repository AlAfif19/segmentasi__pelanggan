def ok(data=None, message="success"):
    return {"status": "success", "message": message, "data": data or {}}


def fail(message, status="error"):
    return {"status": status, "message": message, "data": {}}
