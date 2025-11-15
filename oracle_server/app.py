"""App factory."""

import logging
from http import HTTPStatus
import sys

import datetime as dt
from pathlib import Path
from typing import Any
from connexion import FlaskApp  # type: ignore
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from werkzeug.exceptions import NotFound

from flask import request, jsonify

from oracle_server.config.config import (
    update_config_from_environment,
    update_config_from_secrets,
)
from oracle_server.health import setup_health_route
from oracle_server.logger import logs

DEFAULT_SWAGGER_API_SOURCE = "_api.yml"


def create_app() -> FlaskApp:
    """
    Create a new Flask app.

    :return: The new Flask app.
    """
    spec_path = get_api_spec_path(DEFAULT_SWAGGER_API_SOURCE)
    print(f"full spec path: {spec_path}")
    app = FlaskApp(__name__)
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_ROUTING,
        allow_origins=["*"],  # Allows all origins, replace with specific origins for production
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    print("Successfully create flask app from connexion factory.")
    try:
        app.add_api(
            specification=spec_path,
            pythonic_params=True,
            validate_responses=True,
            strict_validation=True,
            options={"swagger_ui_path": "/ui"},
        )
        print("Successfully added API spec")
    except Exception as e:
        logging.error("Failed to load OpenAPI spec: %s", e)
        sys.exit(1)  # Exit the application gracefully

    flask_app = app.app
    _setup_logging(app)
    _setup_config(app)

    cors_origins = flask_app.config.get("CORS_ORIGINS", "http://localhost:3000").split(",")
    flask_app.logger.debug(f"CORS_ORIGINS: {cors_origins}")
    # CORS(app.app, resources={r"/api/*": {"origins": cors_origins}})

    setup_health_route(flask_app)
    _setup_http_error_handling(app)

    return app


def get_api_spec_path(filename: str) -> Path:
    """
    Returns a pathlib.Path object for a given API spec filename.

    This function assumes the API specification files are located in the
    './api_spec/' directory relative to the current working directory.

    :param filename: The name of the API specification file (e.g., "test-api.yml").

    :return: Path: A Path object representing the full path to the API spec file.
    """
    # Get the base directory of the project (parent of the current file's directory)
    base_dir = Path(__file__).parent.parent

    # Construct the full path to the API spec file
    api_spec_path = base_dir / "api_spec" / filename

    # Return the Path object
    return api_spec_path


# todo: Update for https://github.com/ajponte/babylon/issues/40
# pylint: disable=unused-argument
def decode_token(token) -> dict:
    """
    Decode token method for bearer auth scheme.
    This is the function registered with the spec's `securitySchemes`.

    :param token: Bearer token.
    :return: Dict containing possible user info.
    """
    # todo
    return {}


def _setup_logging(
    app: FlaskApp,
):
    """
    Setup logging.
    """
    # Init logs
    logs.init_app(app.app, log_level="DEBUG", log_type="stream")

    # For request logging
    @app.app.after_request
    def after_request(response):
        """
        Application logging.

        :param response: Application response.
        :return: response
        """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            dt.datetime.now().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response


def _setup_http_error_handling(app):
    _handle_error_unknown(app)
    # Add a catch-all handler for any exception that isn't handled by a more specific handler.
    _handle_base_exception(app)
    # Handler for 404 errors. This is to catch issues with connexion/swagger integration.
    _handle_not_found(app)


def _handle_error_unknown(app: FlaskApp):
    """
    Hande a response from the server when an unknown error is encountered.
    """

    @app.app.errorhandler(500)
    def error(e: Any | None):
        resp = {
            "message": f"Unknown server error: {str(e)}",
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        }
        return jsonify(resp)


def _handle_not_found(app: FlaskApp):
    """
    Handle 404 Not Found errors.
    """

    @app.app.errorhandler(NotFound)
    def handle_not_found_error(e):
        resp = {"message": f"Not Found: {str(e)}", "status": HTTPStatus.NOT_FOUND}
        return jsonify(resp), 404


def _handle_base_exception(app: FlaskApp):
    """
    Handle any base exception and return a generic 500 error response.
    """

    @app.app.errorhandler(Exception)
    def handle_base_exception(e):
        resp = {
            "message": f"A base exception was caught: {str(e)}",
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        }
        return jsonify(resp), 500


def _setup_config(app: FlaskApp):
    """
    Set up the flask app config.

    :param app: The connexion app.
    """
    config: dict[str, Any] = {}
    update_config_from_environment(config)
    update_config_from_secrets(config)
    app.app.config.from_mapping(config)
