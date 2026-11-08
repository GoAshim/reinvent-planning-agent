# Import libraries
import sqlite3
from pathlib import Path
from datetime import time

project_root = Path(__file__).resolve().parent.parent
database_path = project_root / "data" / "sessions.db"

def search_sessions(
        keyword=None,
        day=None, 
        level=None, 
        session_type=None,
        limit=20
) -> list[dict]:
    """Search re:Invent 2026 sessions using optional filters.

    All filters are combined with AND. A filter left as None is not applied,
    so calling with no arguments returns the first `limit` sessions overall.
    Results are sorted by day, then start time, then title.

    Args:
        keyword: Case-insensitive text to look for in the session title or
            description, e.g. "serverless". Matches partial words.
        day: Exact date in "YYYY-MM-DD" format. Valid values are
            "2026-11-30" through "2026-12-04".
        level: Exact session level as an integer: 100, 200, 300, 400 or 500
            (100 = introductory, 500 = expert).
        session_type: Exact session type, case-sensitive. One of
            "Breakout_session", "Builders_session", "bootcamp", "chalk_talk",
            "code_talk", "exam_prep", "gamified_learning", "lab",
            "lightning_talk", "workshop".
        limit: Maximum number of sessions to return, from 1 to 20.
            Defaults to 20.

    Returns:
        A list of dicts, one per matching session, with the keys:
        id, title, session_type, level, day, start_time ("HH:MM"),
        end_time ("HH:MM"), venue, and walk_up_only (1 if the session
        is walk-up only, 0 otherwise). The list is empty if nothing matches.

    Raises:
        TypeError: If limit is not an integer.
        ValueError: If limit is outside the range 1 to 20.
    """

    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("limit must be a number")
    
    if limit < 1 or limit > 20:
        raise ValueError("limit must be between 1 and 20")

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT 
            id, 
            title, 
            session_type,
            level, 
            day, 
            start_time, 
            end_time,
            venue,
            walk_up_only
        FROM sessions
        WHERE 1 = 1
    """

    parameters = []

    if keyword is not None:
        query += " AND (title LIKE ? OR description LIKE ?)"
        keyword_pattern = f"%{keyword}%"
        parameters.extend(
            [
                keyword_pattern,
                keyword_pattern
            ]
        )

    if day is not None:
        parameters.append(day)
        query += " AND day = ?"

    if level is not None:
        parameters.append(level)
        query += " AND level = ?"

    if session_type is not None:
        parameters.append(session_type)
        query += " AND session_type = ?"

    query += " ORDER BY day, start_time, title" 
    query += " LIMIT ?"
    parameters.append(limit)
    cursor.execute(query, parameters)

    rows = cursor.fetchall()
    sessions = [dict(row) for row in rows]
    # sessions = cursor.fetchall()

    connection.close()

    return sessions


def get_session_details(
        session_id: str
) -> dict | None:
    """Get the full details of one re:Invent 2026 session by its ID.

    Use this after search_sessions to get the information search results
    leave out, such as the description and base_id.

    Args:
        session_id: Exact session ID, case-sensitive, as returned by
            search_sessions, e.g. "AIM256-S" or "CON304-R1".

    Returns:
        A dict with the keys: id, base_id, title, session_type, level, day
        ("YYYY-MM-DD"), start_time ("HH:MM"), end_time ("HH:MM"), venue,
        description, and walk_up_only (1 if the session is walk-up only,
        0 otherwise).

        base_id is the session code without its suffix (e.g. "CON304" for
        "CON304-R1"). Repeats of the same session share a base_id.

        Returns None if no session has this ID.
    """

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT 
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
        FROM sessions
        WHERE id = ?
    """
    cursor.execute(query, (session_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None
    
    return dict(row)


def check_conflict(
        first_session_id: str,
        second_session_id: str,
) -> dict:
    """Check whether two re:Invent 2026 sessions overlap in time.

    Two sessions conflict only if they are on the same day and their time
    ranges overlap. Sessions that touch end-to-start (one ends at 10:00 and
    the other starts at 10:00) do not conflict. Travel time between venues
    is not taken into account.

    Args:
        first_session_id: Exact ID of the first session, case-sensitive,
            e.g. "AIM256-S".
        second_session_id: Exact ID of the second session, case-sensitive,
            e.g. "CON304-R1".

    Returns:
        On success, a dict with the keys:
            conflict: True if the sessions overlap, False otherwise.
            reason: A short explanation, e.g. "Session times overlap."
            first_session: Title of the first session.
            second_session: Title of the second session.

        If either ID does not match a session, a dict with a single
        "error" key naming the missing ID. If both are missing, only the
        first one is reported.
    """

    first_session = get_session_details(first_session_id)
    second_session = get_session_details(second_session_id)

    if first_session is None:
        return {
            "error": f"Session not found for id: {first_session_id}"
        }

    if second_session is None:
        return {
            "error": f"Session not found for id: {second_session_id}"
        }

    if first_session["day"] != second_session["day"]:
        return {
            "conflict": False,
            "reason": "Sessions occur on different days.",
            "first_session": first_session["title"],
            "second_session": second_session["title"]
        }

    first_session_starts_at = time.fromisoformat(
        first_session["start_time"]
    )
    second_session_starts_at = time.fromisoformat(
        second_session["start_time"]
    )
    first_session_ends_at = time.fromisoformat(
        first_session["end_time"]
    )
    second_session_ends_at = time.fromisoformat(
        second_session["end_time"]
    )

    # Check conflict
    conflict = (
        first_session_starts_at < second_session_ends_at
        and
        second_session_starts_at < first_session_ends_at
    )

    return {
        "conflict": conflict,
        "reason": (
            "Session times overlap."
            if conflict
            else "Session times do not overlap."
        ),
        "first_session": first_session["title"],
        "second_session": second_session["title"]
    }

