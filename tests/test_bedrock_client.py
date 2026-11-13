from src.bedrock_client import ask_model

response = ask_model(prompt="Explain what is an AI agent in two sentences.")

message = response["output"]["message"]
text = message["content"][0]["text"]

print(f"Model response:\n {text}")
print(f"\nRole: {message['role']}")
print(f"\nStop reason: {response['stopReason']}")
print(f"\nUsage: {response['usage']}")

# assert message["role"] == "assistant"
# assert text != ""
# assert response["stopReason"] == "end_turn"
# assert response["usage"]["inputTokens"] > 0
# assert response["usage"]["outputTokens"] > 0

# print("\nBedrock client test passed.")

print("\nTop-level response keys:")
print(response.keys())

print("\nOutput:")
print(response["output"])

print("\nMessage:")
print(response["output"]["message"])

print("\nContent blocks:")
print(response["output"]["message"]["content"])

print("\nMetrics:")
print(response["metrics"])
