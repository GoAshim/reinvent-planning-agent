import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "data" / "memory.db"
if not db_path.exists():
    raise SystemExit(f"No memory database found at {db_path}")

with sqlite3.connect(db_path) as conn:
    rows = conn.execute(
        """
        SELECT session_id, role, content, created_at
        FROM messages
        ORDER BY id
        """
    ).fetchall()

for session_id, role, content, created_at in rows:
    preview = content.replace("\n", " ")[:80]
    print(f"{session_id[:8]}  {role:<9}  {created_at}  {preview}")

print(f"\nTotal rows: {len(rows)}")
