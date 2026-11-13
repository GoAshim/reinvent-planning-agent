"""Agents that answer re:Invent 2026 questions using tools.

Both agents send the user's prompt to the model through the Amazon Bedrock
Converse API. They run the tools the model asks for and send the results
back, until the model writes its final answer.

- run_single_tool_agent: allows at most one round of tool calls. A simple
  version for learning how tool use works.
- run_agent_loop: repeats the call-tool-reply cycle until the model is done
  or an iteration limit is reached. Use this one for real questions.
"""

from src.bedrock_client import (
    MODEL_ID,
    bedrock_client,
)
from src.tool_definitions import AGENT_TOOLS
from src.tool_dispatcher import execute_tool

def run_single_tool_agent(
        user_prompt: str,
) -> dict:
    """Answer a prompt with at most one tool call.

    Sends the prompt to the model. If the model answers directly, that
    response is returned. If it asks for a tool, the first tool it requested
    is run, the result is sent back, and the model's second response is
    returned. Any further tool requests in that second response are not run.

    Args:
        user_prompt: The user's question, e.g.
            "Find level 300 workshops on 2026-12-01."

    Returns:
        The raw Bedrock Converse response dict. The answer text is in
        response["output"]["message"]["content"], and response["stopReason"]
        says why the model stopped.

    Raises:
        Exception: Any error from the Bedrock call or from the tool is not
            caught and is passed to the caller.
    """

    messages = [{
        "role": "user",
        "content": [{
            "text": user_prompt,
        }]
    }]

    first_response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=messages,
        toolConfig={
            "tools": AGENT_TOOLS,
        },
        inferenceConfig={
            "maxTokens":500,
            "temperature":0,
        },
    )

    assistant_message = first_response["output"]["message"]

    messages.append(assistant_message)

    if first_response["stopReason"] != "tool_use":
        return first_response

    tool_use = next(
        block["toolUse"]
        for block in assistant_message["content"]
        if "toolUse" in block
    )

    tool_result = execute_tool(
        tool_name=tool_use["name"],
        tool_input=tool_use["input"],
    )

    messages.append({
        "role": "user",
        "content": [{
            "toolResult": {
                "toolUseId": tool_use["toolUseId"],
                "content": [{
                    "json": tool_result,
                }]
            }
        }]
    })

    final_response = bedrock_client.converse(
        modelId=MODEL_ID,
        messages=messages,
        toolConfig={
            "tools": AGENT_TOOLS,
        },
        inferenceConfig={
            "maxTokens":500,
            "temperature":0,
        },
    )

    return final_response


def run_agent_loop(
        user_prompt: str,
        max_iteration: int = 5,
) -> dict:
    """Answer a prompt by letting the model call tools as many times as needed.

    Each iteration sends the conversation to the model. If the model asks
    for tools, every requested tool is run and all results are sent back
    together in the next message. The loop ends when the model finishes
    its answer (stop reason "end_turn").

    If a tool raises an error, the error message is sent back to the model
    as a tool result with status "error", so the model can correct its
    input and try again. Progress (iteration, stop reason, token usage and
    tool calls) is printed to the console.

    Args:
        user_prompt: The user's question, e.g.
            "Find level 300 workshops on 2026-12-01."
        max_iteration: Maximum number of calls to the model. Defaults to 5.

    Returns:
        The raw Bedrock Converse response dict from the final call. The
        answer text is in response["output"]["message"]["content"].

    Raises:
        RuntimeError: If the model stops for any reason other than
            "end_turn" or "tool_use" (e.g. "max_tokens"), or if it is still
            calling tools after max_iteration model calls.
    """
    messages = [{
        "role": "user",
        "content": [{
            "text": user_prompt,
        }]
    }]

    for iteration in range(1, max_iteration + 1):
        print(f"\nAgent iteration: {iteration}")

        response = bedrock_client.converse(
            modelId=MODEL_ID,
            messages=messages,
            toolConfig={
                "tools": AGENT_TOOLS,
            },
            inferenceConfig={
                "maxTokens":4096,
                "temperature":0,
            },
        )

        stop_reason = response["stopReason"]
        assistant_message = response["output"]["message"]
        print(f"Stop reason: {stop_reason}")
        print(f"Usage: {response['usage']}")

        messages.append(assistant_message)

        if stop_reason == "end_turn":
            return response

        if stop_reason != "tool_use":
            raise RuntimeError(
                f"Unexpected stop reason: {stop_reason}"
            )

        tool_result_blocks = []
        for content_block in assistant_message["content"]:
            if "toolUse" not in content_block:
                continue

            tool_use = content_block["toolUse"]
            print(f"Tool name: {tool_use['name']}")
            print(f"Tool input: {tool_use['input']}")

            try:
                tool_result = execute_tool(
                    tool_name=tool_use["name"],
                    tool_input=tool_use["input"],
                )

                print(f"Tool result: {tool_result}")

                tool_result_bloc = {
                    "toolResult": {
                        "toolUseId": tool_use["toolUseId"],
                        "content": [{
                            "json": tool_result,
                        }]
                    }
                }

            except Exception as error:
                tool_result_bloc = {
                    "toolResult": {
                        "toolUseId": tool_use["toolUseId"],
                        "content": [{
                            "text": str(error),
                        }],
                        "status":"error",
                    }
                }

            tool_result_blocks.append(tool_result_bloc)

        messages.append({
            "role":"user",
            "content":tool_result_blocks
        })

    raise RuntimeError("Agent exceeded the maximum number of iterations allowed.")
