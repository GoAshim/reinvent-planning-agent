# Import libraries
import json
import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
json_path = project_root / "data" / "sessions.json"
database_path = project_root / "data" / "sessions.db"

with json_path.open("r", encoding="utf-8") as file:
    sessions = json.load(file)

connection = sqlite3.connect(database_path)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS sessions")

cursor.execute(
    """
    CREATE TABLE sessions(
        id TEXT PRIMARY KEY,
        base_id TEXT NOT NULL,
        title TEXT NOT NULL,
        session_type TEXT NOT NULL,
        level INTEGER NOT NULL,
        day TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        venue TEXT NOT NULL,
        description TEXT NOT NULL,
        walk_up_only INTEGER NOT NULL
    )
    """
)

for session in sessions:
    cursor.execute(
        """
        INSERT INTO sessions(
            id,
            base_id,
            title,
            session_type,
            level,
            day,
            start_time,
            end_time,
            venue,
            description,
            walk_up_only
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session["id"],
            session["base_id"],
            session["title"],
            session["session_type"],
            session["level"],
            session["day"],
            session["start_time"],
            session["end_time"],
            session["venue"],
            session["description"],
            session["walk_up_only"]
        ),
    )

connection.commit()

cursor.execute("SELECT COUNT(*) FROM sessions")
session_count = cursor.fetchone()[0]

connection.close()

print(f"Database created at: {database_path}")
print(f"Number of sessions loaded to the database: {session_count}")