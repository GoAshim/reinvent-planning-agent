from src.tools import (
    search_sessions,
    get_session_details,
    check_conflict,
)

# Test search_sessions tool
search_results = search_sessions(
    keyword="Observability",
    level=300,
    limit=5
)
assert 1 <= len(search_results) <= 5

# Test get_session_details tool
selected_session_id = search_results[0]["id"]
session_details = get_session_details(
    session_id=selected_session_id
)
assert session_details is not None
assert session_details["id"] == selected_session_id
assert session_details["level"] == 300
assert session_details["description"] != ""

# Test 1 for check_conflict tool
same_day_sessions = search_sessions(
    day=session_details["day"],
    limit=20,
)
comparison_session = next(
    session
    for session in same_day_sessions
    if session["id"] != selected_session_id
)
conflict_result = check_conflict(
    first_session_id=selected_session_id,
    second_session_id=comparison_session["id"],
)

assert "conflict" in conflict_result
assert isinstance(conflict_result["conflict"], bool)

# Test 2 for check_conflict tool
different_day_sessions = search_sessions(
    day="2026-12-04",
    limit=1,
)
different_day_result = check_conflict(
    first_session_id=selected_session_id,
    second_session_id=different_day_sessions[0]["id"],
)

assert different_day_result["conflict"] is False
assert (
    different_day_result["reason"] 
    == "Sessions occur on different days."
)

# Print test results
print(f"Search results: {len(search_results)}")
print(f"Selected session: {session_details["title"]}")
print(f"Same day comparison: {conflict_result}")
print(f"Different day comparison: {different_day_result}")

print("\nAll integration tests passed.")
