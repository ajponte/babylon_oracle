"""Main Flask application."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from oracle_server.mcp_handler import handle_mcp_request

app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    """Chat endpoint."""
    data = request.get_json()
    response = handle_mcp_request(data)
    return jsonify(response)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
