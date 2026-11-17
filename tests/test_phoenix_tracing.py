"""Send one multi-tool agent run to Phoenix so its trace can be inspected.

Start the Phoenix server first, in a separate terminal:
    phoenix serve

Then run:
    python -m tests.test_phoenix_tracing

Open http://localhost:6006, select the "reinvent-agent-local" project,
and open the newest trace. Expect one agent span containing model call
spans and one span per tool call (search_sessions, get_session_details,
check_conflict).
"""

import sys
import uuid
import urllib.request
from urllib.error import URLError

PHOENIX_URL = "http://localhost:6006"


def phoenix_is_running() -> bool:
    """Return True if the local Phoenix server answers on PHOENIX_URL."""
    try:
        with urllib.request.urlopen(PHOENIX_URL, timeout=3):
            return True
    except (URLError, OSError):
        return False


def test_phoenix_tracing():
    if not phoenix_is_running():
        sys.exit(
            f"Phoenix is not reachable at {PHOENIX_URL}. "
            "Run 'phoenix serve' in another terminal first."
        )

    # Import after the check, because importing strands_agent
    # sets up the tracing pipeline to Phoenix
    from src.strands_agent import run_strands_agent, tracer_provider

    # This prompt should make the agent call all three tools
    prompt = (
        "Find two level 300 workshops about Amazon Bedrock on "
        "December 2, get their full details, and check whether "
        "they conflict."
    )
    print(f"User: {prompt}\n")

    response = run_strands_agent(
        user_prompt=prompt,
        session_id=str(uuid.uuid4()),
    )
    print(f"Agent: {response}\n")

    # Make sure every span has been sent before the script exits
    tracer_provider.force_flush()

    print(
        f"Done. Open {PHOENIX_URL}, select the 'reinvent-agent-local' "
        "project, and open the newest trace."
    )


if __name__ == "__main__":
    test_phoenix_tracing()
