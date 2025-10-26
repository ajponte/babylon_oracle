"""Main Flask application."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from oracle_server.mcp_handler import handle_mcp_request
import logging

app = Flask(__name__)
CORS(app)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request_info():
    """Logs information about the incoming request."""
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    """Chat endpoint."""
    if request.method == "OPTIONS":
        # Pre-flight request. Reply successfully:
        return "", 200
    
    app.logger.info("Received request for /chat")
    data = request.get_json()
    app.logger.debug("Request data: %s", data)
    response = handle_mcp_request(data)
    app.logger.debug("Response data: %s", response)
    return jsonify(response)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
