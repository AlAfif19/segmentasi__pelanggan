from flask import request

from services.auth_service import login, logout
from utils.response import fail, ok


def login_action():
    payload = request.get_json(silent=True) or {}
    result = login(payload.get("username", ""), payload.get("password", ""))
    if not result:
        return fail("Username atau password salah"), 401
    return ok(result, "Login berhasil")


def logout_action():
    return ok(logout(), "Logout berhasil")
