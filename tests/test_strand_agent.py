import uuid
from src.strands_agent import run_strands_agent

# Conversation with short-term memory
# Generate a unique ID for this specific test run
session_id1 = str(uuid.uuid4())
print(f"--- Starting Test Session: {session_id1} ---\n")

# Turn 1: Establish the context in the database
prompt_1 = "Find me one level 300 workshop about Agent on December 1."
print(f"User: {prompt_1}")
response_1 = run_strands_agent(
    session_id=session_id1,
    user_prompt=prompt_1,
)
print(f"Agent: {response_1}\n")

# Turn 2: The Pronoun Test
prompt_2 = "What time does it start?"
print(f"User: {prompt_2}")
response_2 = run_strands_agent(
    session_id=session_id1,
    user_prompt=prompt_2,
)
print(f"Agent: {response_2}\n")
