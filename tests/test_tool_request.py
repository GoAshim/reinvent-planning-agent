from src.bedrock_client import request_with_search_tool

response = request_with_search_tool(
    "Find up to five 300 level workshops about "
    "Amazon Bedrock on December 2, 2026."
)
# response = request_with_search_tool(
#     "Describe Macroeconomics in two sentences"
# )

message = response["output"]["message"]
content_blocks = message["content"]

print(f"\nStop reason: {response['stopReason']}")
print(f"Content blocks: {content_blocks}")
print(f"Token usage: {response['usage']}")

tool_requests = [
    block["toolUse"]
    for block in content_blocks
    if "toolUse" in block
]

assert response["stopReason"] == "tool_use"
assert len(tool_requests) == 1

tool_request = tool_requests[0]

print(f"\nTool-use ID: {tool_request['toolUseId']}")
print(f"Tool name: {tool_request['name']}")
print(f"Tool input: {tool_request['input']}")

assert tool_request["name"] == "search_sessions"

print("\n Tool request tests passed")

