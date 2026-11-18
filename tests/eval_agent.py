"""Run the Strands agent on tests/agent_cases.json and score it with code checks.

Usage:
    python -m tests.eval_agent            # every case, 1 run each
    python -m tests.eval_agent 3          # every case, 3 runs each
    python -m tests.eval_agent 3 002 007  # only cases 002 and 007, 3 runs each

Every answer and tool call is saved to tests/eval_results.json for review.
"""

import json
import re
import sys
from pathlib import Path

from strands import Agent
from src.strands_agent import model, tools, SYSTEM_PROMPT
from src.tools import get_session_details

CASES_PATH = Path(__file__).parent / "agent_cases.json"
RESULTS_PATH = Path(__file__).parent / "eval_results.json"

# Matches every ID format in sessions.db, e.g. AIM101-S, AIM2210, GHJ308-S-R1
SESSION_ID_PATTERN = re.compile(r"\b[A-Z]{3}\d{3,4}(?:-[A-Z0-9]+)*\b")


def run_case(prompt: str, case_id: str) -> dict:
    """Run a fresh agent (no memory) and return its answer, tool calls and cycle count."""
    agent = Agent(
        model=model, 
        tools=tools, 
        system_prompt=SYSTEM_PROMPT, 
        callback_handler=None,
        name=f"eval-{case_id}",
        trace_attributes={"eval.case_id": case_id},
    )
    result = agent(prompt)
    tool_calls = [
        block["toolUse"]
        for message in agent.messages
        for block in message["content"]
        if "toolUse" in block
    ]
    return {
        "answer": str(result),
        "tool_calls": [{"name": c["name"], "input": c["input"]} for c in tool_calls],
        "cycles": result.metrics.cycle_count,
    }


def matches(session: dict, rules: dict) -> bool:
    """True if the session satisfies every rule (keyword is a case-insensitive substring)."""
    for key, value in rules.items():
        if key == "keyword":
            text = f"{session['title']} {session['description']}".lower()
            if value.lower() not in text:
                return False
        elif session[key] != value:
            return False
    return True


def check(expect: dict, run: dict) -> list[str]:
    """Return a list of failure reasons. An empty list means the run passed."""
    answer = run["answer"]
    called = {c["name"] for c in run["tool_calls"]}
    looked_up = {c["input"].get("session_id") for c in run["tool_calls"]}
    missing_ids = set(expect.get("missing_ids", []))

    mentioned = set(SESSION_ID_PATTERN.findall(answer)) - missing_ids
    details = {sid: get_session_details(sid) for sid in mentioned}
    real = {sid: d for sid, d in details.items() if "error" not in d}
    failures = []

    invented = sorted(set(details) - set(real))
    if invented:
        failures.append(f"invented session IDs: {invented}")

    for tool_name in expect.get("tools_called", []):
        if tool_name not in called:
            failures.append(f"did not call {tool_name}")

    for sid in expect.get("must_mention_ids", []):
        if sid not in answer:
            failures.append(f"did not mention {sid}")

    for text in expect.get("must_contain", []):
        if text not in answer:
            failures.append(f"answer does not contain '{text}'")

    if len(real) < expect.get("min_sessions", 0):
        failures.append(f"only {len(real)} sessions, expected at least {expect['min_sessions']}")
    if len(real) > expect.get("max_sessions", len(real)):
        failures.append(f"{len(real)} sessions, expected at most {expect['max_sessions']}")

    for sid, session in real.items():
        if not matches(session, expect.get("constraints", {})):
            failures.append(f"{sid} breaks constraints {expect['constraints']}")

    # Each topic must be covered by a different session
    unused = dict(real)
    for topic in expect.get("topics", []):
        hit = next((sid for sid, s in unused.items() if matches(s, topic)), None)
        if hit is None:
            failures.append(f"no session matches topic {topic}")
        else:
            unused.pop(hit)

    for sid in missing_ids:
        if sid not in answer or sid not in looked_up:
            failures.append(f"did not look up and report missing ID {sid}")

    if expect.get("expect_no_results") and real:
        failures.append(f"expected no sessions but got {sorted(real)}")

    return failures


def main():
    runs_per_case = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    only_ids = set(sys.argv[2:])

    cases = json.loads(CASES_PATH.read_text())
    if only_ids:
        cases = [c for c in cases if c["id"] in only_ids]

    results, total_passed, total_runs = [], 0, 0

    for case in cases:
        passed = 0
        for attempt in range(1, runs_per_case + 1):
            try:
                run = run_case(case["prompt"], case["id"])
                failures = check(case["expect"], run)
            except Exception as error:
                run, failures = {"answer": "", "tool_calls": [], "cycles": 0}, [f"crashed: {error!r}"]

            passed += not failures
            results.append({"id": case["id"], "attempt": attempt, "failures": failures, **run})
            status = "PASS" if not failures else "FAIL: " + "; ".join(failures)
            print(f"{case['id']} run {attempt} ({run['cycles']} cycles): {status}")

        print(f"--> {case['id']} {case['category']}: {passed}/{runs_per_case} passed\n")
        total_passed += passed
        total_runs += runs_per_case

    print(f"OVERALL: {total_passed}/{total_runs} runs passed")
    RESULTS_PATH.write_text(json.dumps(results, indent=2))
    print(f"Answers and tool calls saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
