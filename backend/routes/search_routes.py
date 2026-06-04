from flask import Blueprint

from controllers.search_controller import search_action

search_bp = Blueprint("search", __name__)

search_bp.get("/")(search_action)
