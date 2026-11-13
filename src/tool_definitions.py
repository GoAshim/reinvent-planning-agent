SEARCH_SESSIONS_TOOL = {
    "toolSpec": {
        "name": "search_sessions",
        "description": (
            "Search AWS re:Invent conference sessions using "
            "optional keyword, date, level, session type, "
            "and result limit filters."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Text to find in session title or description."
                    },
                    "day": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD, from 2026-11-30 to 2026-12-04."
                    },
                    "level": {
                        "type": "integer",
                        "enum": [100, 200, 300, 400, 500],
                        "description":"Session level such as 200, 300, or 400."
                    },
                    "session_type": {
                        "type": "string",
                        "enum": [
                            "Breakout_session", "Builders_session", "bootcamp",
                            "chalk_talk", "code_talk", "exam_prep",
                            "gamified_learning", "lab", "lightning_talk", "workshop"
                        ],
                        "description": "Session format such as workshop, lab, or code_talk."
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "description": "Maximum number of records in the result from 1 to 20"
                    }
                },
                "required":[]
            }
        }
    }
}

GET_SESSION_DETAILS_TOOL = {
    "toolSpec": {
        "name": "get_session_details",
        "description": (
            "Get full details of one AWS re:Invent session by its ID, "
            "including the description. Use an ID returned by search_sessions."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Exact, case-sensitive session ID such as AIM256-S or CON304-R1."
                    }
                },
                "required": ["session_id"]
            }
        }
    }
}

CHECK_CONFLICT_TOOL = {
    "toolSpec": {
        "name": "check_conflict",
        "description": (
            "Check whether two AWS re:Invent sessions overlap in time. "
            "Use IDs returned by search_sessions."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "first_session_id": {
                        "type": "string",
                        "description": "Exact, case-sensitive ID of the first session."
                    },
                    "second_session_id": {
                        "type": "string",
                        "description": "Exact, case-sensitive ID of the second session."
                    }
                },
                "required": ["first_session_id", "second_session_id"]
            }
        }
    }
}

AGENT_TOOLS = [
    SEARCH_SESSIONS_TOOL,
    GET_SESSION_DETAILS_TOOL,
    CHECK_CONFLICT_TOOL,
]