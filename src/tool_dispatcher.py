"""Route tool calls from the model to the Python functions that run them.

When the model asks to use a tool, the agent loop passes the tool's name and
input here. This module looks up the matching function in src.tools, calls
it, and returns the result so it can be sent back to the model.

To add a tool: write the function in src.tools, add its spec to
src.tool_definitions, and add a branch for it in execute_tool.
"""
from src.tools import search_sessions, get_session_details, check_conflict

def execute_tool(
        tool_name: str,
        tool_input: dict,
):
    """Run the tool the model asked for and return its result.

    Args:
        tool_name: Name of the tool, matching the "name" in its tool spec,
            e.g. "search_sessions".
        tool_input: Arguments the model chose for the tool, as a dict of
            parameter names to values, e.g. {"day": "2026-12-01", "level": 300}.
            They are passed to the function as keyword arguments.

    Returns:
        A dict, ready to send to the model as a JSON tool result:
            search_sessions: {"sessions": [...]}, wrapping the list of
                session dicts, because Bedrock requires a JSON object.
            get_session_details and check_conflict: the dict the tool
                returns. If a session ID is not found, this is a dict with
                a single "error" key.

    Raises:
        ValueError: If tool_name is not a known tool, or if the tool rejects
            an input value (e.g. a limit outside 1 to 20).
        TypeError: If tool_input has a parameter the tool does not accept,
            or if limit is not an integer.
    """
    if tool_name == "search_sessions":
        # Only the search_sessions tool returns a list, so 
        # I am converting it to JSON object before returning 
        # it back to the agent loop.
        return {"sessions": search_sessions(**tool_input)}
 
    if tool_name == "get_session_details":
        return get_session_details(**tool_input)

    if tool_name == "check_conflict":
        return check_conflict(**tool_input)

    raise ValueError(
        f"Unknown tool: {tool_name}"
    )