"""MCP Server"""

from mcp.server.sdk import McpServer, api_route
from pydantic import BaseModel


class HelloWorldRequest(BaseModel):
    """HelloWorldRequest"""

    name: str


class HelloWorldResponse(BaseModel):
    """HelloWorldResponse"""

    message: str


class MyMcpServer(McpServer):
    """MyMcpServer"""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    @api_route("/hello_world")
    def hello_world(self, request: HelloWorldRequest) -> HelloWorldResponse:
        """hello_world"""
        return HelloWorldResponse(message=f"Hello, {request.name}!")
