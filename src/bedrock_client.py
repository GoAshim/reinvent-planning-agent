# Import libraries
import time
import boto3
from src.tool_definitions import SEARCH_SESSIONS_TOOL

MODEL_ID = (
    "us.anthropic.claude-haiku-4-5-20251001-v1:0"
)
session = boto3.Session(
    profile_name="reinvent"
)
bedrock_client = session.client(
    "bedrock-runtime"
)

def ask_model(prompt: str) -> dict:
    """
    Send one text prompt to Amazon Bedrock

    Args:
        prompt: User's question
    
    Returns:
        The complete response from Bedrock Converse API
    """

    start_time = time.perf_counter()

    response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=[{

                "role": "user",
                "content": [{
                    "text":prompt,                        
                }]
        }],
        inferenceConfig={
            "maxTokens":300,
            "temperature":0,
        },
    )

    elapsed_seconds = time.perf_counter() - start_time
    print(f"Latency: {elapsed_seconds:.2f} seconds")

    return response


def request_with_search_tool(prompt: str) -> dict:
    """
    
    """

    start_time = time.perf_counter()

    response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=[{
                "role": "user",
                "content": [{
                    "text":prompt,                        
                }]
        }],
        inferenceConfig={
            "maxTokens":300,
            "temperature":0,
        },
        toolConfig={
            "tools": [
                SEARCH_SESSIONS_TOOL
            ]
        }
    )

    elapsed_seconds = time.perf_counter() - start_time
    print(f"Latency: {elapsed_seconds:.2f} seconds")

    return response
