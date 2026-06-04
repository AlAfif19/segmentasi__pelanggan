from flask import Blueprint

from controllers.segmentation_controller import run_segmentation_action

segmentation_bp = Blueprint("segmentation", __name__)

segmentation_bp.post("/run")(run_segmentation_action)
