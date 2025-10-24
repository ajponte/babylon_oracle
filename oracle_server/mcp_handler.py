"""MCP parsing and execution."""

import re
from oracle_server.tools import weather, calculator

# todo: https://github.com/ajponte/babylon/issues/38
# A simple in-memory conversation history
# pylint: disable=global-variable-not-assigned
conversation_history = []


def handle_mcp_request(data):
    """Handle MCP request."""
    global conversation_history

    user_input = data.get("user_input", "")
    conversation_history.append(f"User: {user_input}")

    # Simple regex to find tool calls like [tool_name(param1=value1, param2=value2)]
    tool_call_match = re.search(r"\[(\w+)\((.*)\)\]", user_input)

    if tool_call_match:
        tool_name = tool_call_match.group(1)
        tool_params_str = tool_call_match.group(2)

        # Simple parsing of params
        try:
            tool_params = dict(p.split("=") for p in tool_params_str.split(", "))
        except ValueError:
            return {"response": "Invalid tool parameters."}

        if tool_name == "get_weather":
            result = weather.get_weather(**tool_params)
        elif tool_name == "calculate":
            result = calculator.calculate(**tool_params)
        else:
            result = "Unknown tool."

        conversation_history.append(f"Tool: {result}")
        return {"response": result}

    conversation_history.append("Assistant: I can help with that.")
    return {"response": "I can help with that."}
