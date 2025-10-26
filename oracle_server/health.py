"""
Custom /health route.
"""
from flask import Flask

def health():
    """
    A simple health route.
    :return: Tuple of OK message and HTTP 200 status.
    """
    # Simple health check for now.
    return "OK", 200


def setup_health_route(flask_app: Flask):
    """
    Set up a /health route.

    :param flask_app: The app.
    """
    flask_app.add_url_rule("/health", view_func=health)
