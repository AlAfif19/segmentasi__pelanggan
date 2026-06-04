from functools import wraps

from flask import request

from utils.response import fail


def require_token(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return fail("Token tidak valid"), 401
        return handler(*args, **kwargs)

    return wrapper
