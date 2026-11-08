from src.tools import search_sessions

# ------- Test 1: Search for valid sessions as list of tuples ------- 
# sessions = search_sessions("2026-12-01")
# print(f"Number of sessions found on 2026-12-01: {len(sessions)}")

# print("\n First 5 sessions on 2026-12-01")
# for session in sessions[:5]:
#     print(session)


# ------- Test 2: Search for no sessions ------- 
# sessions = search_sessions("2026-12-10")
# print(f"Number of sessions found on 2026-12-10: {len(sessions)}")

# ------- Test 3: Search for valid sessions with day ------- 
# all_sessions = search_sessions("2026-12-01")
# print(f"Number of sessions found on 2026-12-01: {len(all_sessions)}")

# print("\n First 5 sessions on 2026-12-01")
# for session in all_sessions[:5]:
#     print(
#         session["id"],
#         session["title"],
#         session["day"],
#         session["start_time"],
#         session["level"]
#     )

# ------- Test 4: Search for valid sessions with day and level ------- 
# all_sessions = search_sessions("2026-12-01")
# level_300_sessions = search_sessions("2026-12-01", 300)
# no_sessions = search_sessions("2026-12-11", 400)
# print(f"\nNumber of sessions found on 2026-12-01: {len(all_sessions)}")
# print(f"\nNumber of 300 level sessions found on 2026-12-01: {len(level_300_sessions)}")
# print(f"\nNumber of 400 level sessions found on 2026-12-11: {len(no_sessions)}")

# print("\n First 5 level 300 sessions on 2026-12-01")
# for session in level_300_sessions[:5]:
#     print(
#         session["id"],
#         session["title"],
#         session["day"],
#         session["start_time"],
#         session["level"]
#     )

# ------- Test 5: Search for valid sessions with day, level, and session_type ------- 
# all_sessions = search_sessions(day="2026-12-02")
# level_300_sessions = search_sessions(
#     day="2026-12-02", 
#     level=300
# )
# workshops_1202 = search_sessions(
#     day="2026-12-02", 
#     session_type="workshop"
# )
# level_300_workshops_1201 = search_sessions(
#     day="2026-12-01", 
#     level=300,
#     session_type="workshop"
# )
# level_300_workshops_all = search_sessions(
#     level=300,
#     session_type="workshop"
# )
# no_sessions_by_day = search_sessions(day="2026-12-11")
# no_sessions_by_level = search_sessions(day="2026-12-01",level=1000)
# no_sessions_by_type = search_sessions(day="2026-12-01",session_type=1000)

# print(f"\nNumber of sessions found: {len(all_sessions)}")
# print(f"\nNumber of 300 level sessions: {len(level_300_sessions)}")
# print(f"\nNumber of workshop sessions: {len(workshops_1202)}")
# print(f"\nNumber of level 300 workshop sessions on 12-01: {len(level_300_workshops_1201)}")
# print(f"\nNumber of level 300 workshop sessions for all 5 days: {len(level_300_workshops_all)}")

# print(f"\nNumber of sessions found on a wrong date: {len(no_sessions_by_day)}")
# print(f"\nNumber of sessions found with wrong level: {len(no_sessions_by_level)}")
# print(f"\nNumber of sessions found with wrong type: {len(no_sessions_by_type)}")

# print("\n First 3 level 300 workshop sessions on 2026-12-01")
# for session in level_300_workshops_1201[:5]:
#     print(
#         session["id"],
#         session["title"],
#         session["day"],
#         session["start_time"],
#         session["level"]
#     )

# ------- Test 6: Search for sessions with limit ------- 
# all_sessions = search_sessions()
# five_sessions = search_sessions(
#     day="2026-12-02", 
#     level=300,
#     limit=5
# )
# large_limit = search_sessions(
#     limit=2000
# )

# print(f"\nNumber of sessions found: {len(all_sessions)}")
# print(f"\nNumber of 300 level sessions: {len(five_sessions)}")
# print(f"\nNumber of workshop sessions: {len(large_limit)}")

# ------- Test 7: Search for sessions with keyword ------- 
# bedrock_sessions = search_sessions(keyword="bedrock")
# bedrock_workshops = search_sessions(
#     keyword="bedrock", 
#     session_type="workshop",
#     limit=5
# )
# bedrock_level_300 = search_sessions(
#     keyword="observability", 
#     day="2026-12-02", 
# )

# print(f"\nNumber of bedrock sessions found: {len(bedrock_sessions)}")
# print(f"\nNumber of bedrock workshop sessions: {len(bedrock_workshops)}")
# print(f"\nNumber of observability sessions on 12-02: {len(bedrock_level_300)}")

# ------- Test 8: limit test ------- 
# try:
#     search_sessions(limit=0)
# except ValueError as error:
#     print(f"Error: {error}")

# try:
#     search_sessions(limit=55)
# except ValueError as error:
#     print(f"Error: {error}")

# try:
#     search_sessions(limit="ten")
# except TypeError as error:
#     print(f"Error: {error}")

# ------- Test 9: test with assertion ------- 
all_sessions = search_sessions(limit=20)
assert len(all_sessions) == 20

five_sessions = search_sessions(
    day="2026-12-02", 
    level=300,
    limit=5
)
assert len(five_sessions) <= 5
assert all(
    session["level"] == 300
    for session in five_sessions
)

workshops = search_sessions(
    session_type="workshop", 
    limit=15
)
assert len(workshops) <= 15
assert all(
    session["session_type"] == "workshop"
    for session in workshops
)

no_sessions = search_sessions(keyword="Missouri is called as Show Me state")
assert len(no_sessions) == 0

print("All search_session tool tests passed.")
