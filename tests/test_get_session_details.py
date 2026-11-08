from src.tools import get_session_details, search_sessions

search_result = search_sessions(
    keyword="Bedrock",
    limit=1
)

valid_session_id = search_result[0]["id"]

session = get_session_details(session_id=valid_session_id)

assert session is not None
assert session["id"] == valid_session_id
assert session["description"] != ""

print("Valid session:")
print(f"id: {session["id"]}")
print(f"title: {session["title"]}")
print(f"description: {session["description"]}")

invalid_session = get_session_details(session_id="invalid-session-id")
assert invalid_session is None
print("\nInvalid session: {invalid_session}")

print("\nAll tests of get_session_details tool passed.")