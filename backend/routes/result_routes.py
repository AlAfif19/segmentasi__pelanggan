from flask import Blueprint

from controllers.result_controller import result_action

result_bp = Blueprint("result", __name__)

result_bp.get("/")(result_action)
