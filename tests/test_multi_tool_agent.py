from src.agent import run_agent_loop

response = run_agent_loop(
    "Find two level-300 workshops on Amazon Bedrock "
    "on December 2, 2026. Get their full details. "
    "and also check whether they conflict."
)

message = response["output"]["message"]
print(f"Full response message:\n {message}")

text_blocks = [
    block["text"]
    for block in message["content"]
    if "text" in block
]

assert response["stopReason"] == "end_turn"
assert len(text_blocks) > 0

final_text = "\n".join(text_blocks)

print(f"Final response: {final_text}")

print("\nMulti-tool agent test passed.")