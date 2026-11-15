import sqlite3
from contextlib import closing
from pathlib import Path

# Use the existing data directory for the memory database
project_root = Path(__file__).resolve().parent.parent
db_path = project_root / "data" / "memory.db"

class SQLiteShortTermMemory:
    def __init__(self):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create the table for conversational turns if it doesn't exist."""
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def get_context(self, session_id: str) -> list[dict]:
        """
        Retrieve the short-term memory / context 
        window for the current session from the 
        table.
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT 
                    role, 
                    content 
                FROM messages 
                WHERE session_id = ? 
                ORDER BY id ASC
                """,
                (session_id,)
            )
            return [
                {"role": row["role"], "content": row["content"]} 
                for row in cursor.fetchall()
            ]


    def save_turn(self, session_id: str, user_prompt: str, agent_response: str):
        """
        Append the latest turn of conversation 
        to the session's short-term memory / 
        context window in the table.
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(
                """
                INSERT INTO messages (
                    session_id, 
                    role, 
                    content
                ) 
                VALUES (?, ?, ?)
                """,
                (session_id, "user", user_prompt)
            )
            conn.execute(
                """
                INSERT INTO messages (
                    session_id, 
                    role, 
                    content
                ) 
                VALUES (?, ?, ?)
                """,
                (session_id, "assistant", agent_response)
            )


class SQLiteLongTermMemory:
    def __init__(self):
        # We reuse the same db_path defined at the top of your memory.py file
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create the key-value table for durable user preferences."""
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        user_id TEXT NOT NULL,
                        preference_key TEXT NOT NULL,
                        preference_value TEXT NOT NULL,
                        PRIMARY KEY (user_id, preference_key)
                    )
                """
            )

    def get_user_profile(self, user_id: str) -> str:
        """
        Fetch the long-term memory and 
        format them for the system prompt.
        """
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            cursor = conn.execute(
                """
                    SELECT 
                        preference_key, 
                        preference_value 
                    FROM user_preferences 
                    WHERE user_id = ?
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            
            # If we know nothing about this user yet, 
            # return an empty string
            if not rows:
                return ""
            
            # Translate the database rows into a 
            # list of preference key and value 
            # for the LLM
            profile_lines = [f"- {row[0]}: {row[1]}" for row in rows]
            return "\nBackground Knowledge about this user:\n" + "\n".join(profile_lines)

    def set_preference(self, user_id: str, key: str, value: str):
        """Insert or update a specific long-term preference."""
        with closing(sqlite3.connect(self.db_path)) as conn, conn:
            conn.execute(
                """
                    INSERT INTO user_preferences (
                        user_id, 
                        preference_key, 
                        preference_value
                    ) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, preference_key) DO UPDATE SET preference_value=excluded.preference_value
                """, 
                (user_id, key, value)
            )