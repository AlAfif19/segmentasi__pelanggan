from flask import Blueprint

from controllers.download_controller import download_action

download_bp = Blueprint("download", __name__)

download_bp.post("/")(download_action)
