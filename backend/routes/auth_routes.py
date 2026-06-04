from flask import Blueprint

from controllers.auth_controller import login_action, logout_action

auth_bp = Blueprint("auth", __name__)

auth_bp.post("/login")(login_action)
auth_bp.post("/logout")(logout_action)
