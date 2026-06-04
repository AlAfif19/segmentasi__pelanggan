import sys
from pathlib import Path

from flask import Flask
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import Config
from middleware.error_handler import register_error_handlers
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.data_routes import data_bp
from routes.download_routes import download_bp
from routes.result_routes import result_bp
from routes.search_routes import search_bp
from routes.segmentation_routes import segmentation_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(data_bp, url_prefix="/api/data")
    app.register_blueprint(segmentation_bp, url_prefix="/api/segmentation")
    app.register_blueprint(result_bp, url_prefix="/api/result")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(download_bp, url_prefix="/api/download")
    register_error_handlers(app)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "app": app.config["APP_NAME"]}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=Config.APP_DEBUG, use_reloader=False)
