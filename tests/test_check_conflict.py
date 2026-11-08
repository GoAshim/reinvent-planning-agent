from src.tools import search_sessions, check_conflict

sessions = search_sessions(
    day="2026-12-01",
    limit=20,
)

conflicting_pair = None
non_conflicting_pair = None

for first_session in sessions:
    for second_session in sessions:
        if first_session["id"] == second_session["id"]:
            continue

        result = check_conflict(
            first_session_id=first_session["id"],
            second_session_id=second_session["id"]
        )

        if (
            result["conflict"] and
            conflicting_pair is None
        ):
            conflicting_pair = (
                first_session,
                second_session,
                result
            )

        if (
            not result["conflict"] and
            non_conflicting_pair is None
        ):
            non_conflicting_pair = (
                first_session,
                second_session,
                result
            )

        if (
            conflicting_pair is not None
            and 
            non_conflicting_pair is not None
        ):
            break

    if (
        conflicting_pair is not None
        and 
        non_conflicting_pair is not None
    ):
        break

# Validation
assert conflicting_pair is not None
assert non_conflicting_pair is not None

print("Conflicting pair:")
print(conflicting_pair[0]["title"])
print(conflicting_pair[1]["title"])
print(conflicting_pair[2])

print("\nNon-conflicting pair:")
print(non_conflicting_pair[0]["title"])
print(non_conflicting_pair[1]["title"])
print(non_conflicting_pair[2])

missing_result = check_conflict(
    first_session_id="not-a-real-session",
    second_session_id=sessions[0]["id"],
)
assert "error" in missing_result
print(f"\nMissing session result: {missing_result}")

print("\nAll check_conflict tool tests passed.")
