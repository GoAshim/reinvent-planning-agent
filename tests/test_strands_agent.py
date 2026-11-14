from src.strands_agent import run_strands_agent

response_text = run_strands_agent(
    "Find two level-300 workshops on Amazon Bedrock "
    "on December 2, 2026. Get their full details. "
    "and also check whether they conflict."
)

print(f"Final response:\n{response_text}")
print("\nStrands agent test passed.")