# Import libraries
from strands import Agent
from src.strands_tools import search_sessions, get_session_details, check_conflict
from src.bedrock_client import MODEL_ID, session
from strands.models import BedrockModel

# Initialize a Bedrock model with the Haiku model id 
# and the SSO session defined in bedrock_client.py
model = BedrockModel(
    model_id=MODEL_ID,
    boto_session=session,
)

# Initialize the Strands agent with the model, tools, 
# and a system prompt.
agent = Agent(
    model=model,
    tools=[
        search_sessions,
        get_session_details,
        check_conflict,
    ],
    system_prompt=
    """
    You are a helpful AWS re:Invent 2026 
    session planning assistant.
    """
)

def run_strands_agent(user_prompt: str) -> str:
    """
    Answer user prompt by letting Strands 
    manage the agent loop.
    """
    response = agent(user_prompt)
    return str(response)
