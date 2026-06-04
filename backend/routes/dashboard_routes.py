from flask import Blueprint

from controllers.dashboard_controller import dashboard_action

dashboard_bp = Blueprint("dashboard", __name__)

dashboard_bp.get("/")(dashboard_action)
