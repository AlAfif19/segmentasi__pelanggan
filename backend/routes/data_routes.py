from flask import Blueprint

from controllers.data_controller import embedded_data_action

data_bp = Blueprint("data", __name__)

data_bp.get("/embedded")(embedded_data_action)
