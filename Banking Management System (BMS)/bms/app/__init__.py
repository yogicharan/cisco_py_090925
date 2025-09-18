import os
from flask import Flask, jsonify
from .config import Config
from .db import init_db
from .logger import setup_logging
from .exceptions import AppError
from .routes import bp as api_bp


def create_app(config: Config = None):
    config = config or Config.from_env()
    setup_logging(config)
    app = Flask(__name__)
    app.config.from_object(config)

    # init db and other extensions
    init_db(app, config.SQLALCHEMY_DATABASE_URI)

    # register blueprints
    app.register_blueprint(api_bp, url_prefix="/bms")

    # centralized exception handler
    @app.errorhandler(AppError)
    def handle_app_error(err):
        payload = {"error": err.name, "message": err.message}
        return jsonify(payload), err.status_code

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        # minimal exposure; real app would log stacktrace and more details
        app.logger.exception("Unhandled exception")
        return jsonify({"error": "internal_error", "message": "An internal error occurred."}), 500

    return app
