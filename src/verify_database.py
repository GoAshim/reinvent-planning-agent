# Import libraries
import json
import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
database_path = project_root / "data" / "sessions.db"

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sessions")
session_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT id) FROM sessions")
unique_id_count = cursor.fetchone()[0]

cursor.execute(
    """
    SELECT id, title, day, start_time, level, walk_up_only
    FROM sessions
    ORDER BY day, start_time
    LIMIT 3
    """
)
sample_sessions = cursor.fetchall()

cursor.execute(
    """
    SELECT walk_up_only, COUNT(*)
    FROM sessions
    GROUP BY walk_up_only
    ORDER BY walk_up_only
    """
)
walk_up_only_sessions = cursor.fetchall()

connection.close()

print(f"Database at: {database_path}")
print(f"Number of sessions: {session_count}")
print(f"Number of unique sessions: {unique_id_count}")

print()
print("First 3 sessions:")
for session in sample_sessions:
    print(session)

print()
print("Walk-up sessions:")
for value, count in walk_up_only_sessions:
    print(f"{value}: {count}")