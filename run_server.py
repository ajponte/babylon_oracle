"""Run the MCP server."""

from oracle_server.app import app

if __name__ == "__main__":
    app.run(debug=True)
