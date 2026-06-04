import secrets

from repositories import mysql_repository
from werkzeug.security import check_password_hash


def login(username, password):
    if not mysql_repository.is_ready():
        return None

    user = mysql_repository.find_user_by_username(username)
    if user and check_password_hash(user["password_hash"], password):
        return {
            "token": secrets.token_urlsafe(32),
            "user": {"username": user["username"], "role": user["role"]},
        }
    return None


def logout():
    return {"logged_out": True}
