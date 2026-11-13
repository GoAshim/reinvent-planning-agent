from src.bedrock_client import request_with_search_tool
from src.tool_dispatcher import execute_tool

response = request_with_search_tool(
    "Find up to five 300 level workshops about "
    "Amazon Bedrock on December 2, 2026."
)

message = response["output"]["message"]
content_blocks = message["content"]

tool_request = next(
    block["toolUse"]
    for block in content_blocks
    if "toolUse" in block
)

tool_name = tool_request['name']
tool_input = tool_request['input']
print(f"Tool name: {tool_name}")
print(f"Tool input: {tool_input}")

tool_result = execute_tool(
    tool_name=tool_name,
    tool_input=tool_input,
)

print(f"Number of results returned: {len(tool_result)}")
for session in tool_result:
    print(
        session["id"],
        session["title"],
        session["session_type"],
        session["level"],
        session["day"],
    )

assert tool_name == "search_sessions"
assert len(tool_result) <= 5
assert all(
    session["level"] == 300
    for session in tool_result
)
assert all(
    session["session_type"] == "workshop"
    for session in tool_result
)
assert all(
    session["day"] == "2026-12-02"
    for session in tool_result
)

print("\n Tool dispatcher tests passed")

