# Import libraries
import json
from pathlib import Path
from collections import Counter

json_path = Path("data/sessions.json")

# Open the JSON file
with json_path.open("r", encoding="utf-8") as file:
    sessions = json.load(file)

# --------- Validation Round 1 ---------
print(f"Top-level Python type: {type(sessions).__name__}")
print(f"Number of records: {len(sessions)}")
print()

first_session = sessions[0]
print("Fields from the first session record in file:")
for field in first_session:
    print(f"- {field}")

print()
print("All fields and values of the first session in the file:")
print(json.dumps(first_session, indent=2))

# --------- Validation Round 2 ---------
expected_fields = set(sessions[0].keys())
records_with_different_fields = []

for session in sessions:
    current_session_fields = set(session.keys())
    if current_session_fields != expected_fields:
        records_with_different_fields.append(session["id"])

print(f"Number of records: {len(sessions)}")
print(f"Expected fields: {sorted(expected_fields)}")
print(f"Records with different fields: {len(records_with_different_fields)}")

print()
print("Session types:")
print(sorted({session["session_type"] for session in sessions}))

print()
print("Levels:")
print(sorted({session["level"] for session in sessions}))

print()
print("Days:")
print(sorted({session["day"] for session in sessions}))

print()
print("Walk-up Only:")
print(sorted({session["walk_up_only"] for session in sessions}))

# --------- Validation Round 3 ---------
session_ids = [session["id"] for session in sessions]
id_counts = Counter(session_ids)

duplicate_ids = [
    session_id for session_id, count in id_counts.items()
        if count > 1
]

print(f"Number of records: {len(sessions)}")
print(f"Unique IDs: {len(set(session_ids))}")
print(f"Duplicate IDs: {len(duplicate_ids)}")

print()
print("Missing of empty values by field:")

for field in sessions[0].keys():
    missing_count = sum(
        1
        for session in sessions
        if session[field] is None or session[field] == ""
    )

    print(f"- {field}: {missing_count}")

