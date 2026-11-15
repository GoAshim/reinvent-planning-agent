import uuid
from src.strands_agent import run_strands_agent_with_LTM, lt_memory

def test_long_term_memory():
    # Define a user ID representing
    # the user logging into the app
    user_id = f"user_{uuid.uuid4()}"
    
    # SESSION 1: The user states a preference
    session_1 = str(uuid.uuid4())
    print(f"--- Starting Session 1: The Preference ---")
    
    prompt_1 = """
        Hi, I'm planning my re:Invent schedule. 
        Please remember for all future searches 
        that I only want to attend Level 400 
        (Expert) sessions.
        Suggest me a session on observability.
    """
    print(f"User: {prompt_1}")
    
    response_1 = run_strands_agent_with_LTM(
        user_id=user_id,
        session_id=session_1,
        user_prompt=prompt_1,
    )
    print(f"Agent: {response_1}\n")

    # Check if the model called the tool to 
    # save user preference to the database
    user_profile = lt_memory.get_user_profile(user_id)
    print(f"Long-term memory from the database: {user_profile}")

    
    # SESSION 2: A completely new conversation on a different day
    session_2 = str(uuid.uuid4())
    print(f"--- Starting Session 2: The Retrieval ---")
    
    # The user doesn't mention Level 400 any more
    prompt_2 = "Can you find me a workshop on Amazon Bedrock?"
    print(f"User: {prompt_2}")
    
    # We pass the SAME user_id, but a NEW session_id
    response_2 = run_strands_agent_with_LTM(
        user_id=user_id,
        session_id=session_2,
        user_prompt=prompt_2,
    )
    print(f"Agent: {response_2}\n")

    # Check if the user preference is still the same
    user_profile = lt_memory.get_user_profile(user_id)
    print(f"Long-term memory from the database: {user_profile}")

    
    # SESSION 3: A completely new conversation on a different day
    session_3 = str(uuid.uuid4())
    print(f"--- Starting Session 3: The Override ---")
    
    # The user mention a level 200 session, which  
    # is different from the preference stored in  
    # the long-term memory
    prompt_3 = "Can you find me a level 200 session on memory?"
    print(f"User: {prompt_3}")
    
    # We pass the SAME user_id, but a NEW session_id
    response_3 = run_strands_agent_with_LTM(
        user_id=user_id,
        session_id=session_3,
        user_prompt=prompt_3,
    )
    print(f"Agent: {response_3}\n")

    # Check if the user preference is still the same
    user_profile = lt_memory.get_user_profile(user_id)
    print(f"Long-term memory from the database: {user_profile}")


    # SESSION 4: The user changes the preference
    session_4 = str(uuid.uuid4())
    print(f"--- Starting Session 4: Add a new Preference ---")
    
    prompt_4 = """
        Please remember for all future searches 
        that I don't want to attend sessions in
        MGM Grand.
        Suggest me a session on AgentCore.
    """
    print(f"User: {prompt_4}")
    
    response_4 = run_strands_agent_with_LTM(
        user_id=user_id,
        session_id=session_4,
        user_prompt=prompt_4,
    )
    print(f"Agent: {response_4}\n")

    # Check if the model called the tool to 
    # save user preference to the database
    user_profile = lt_memory.get_user_profile(user_id)
    print(f"Long-term memory from the database: {user_profile}")


    # SESSION 5: The user changes the preference
    session_5 = str(uuid.uuid4())
    print(f"--- Starting Session 5: Modify preference ---")
    
    prompt_5 = """
        Remember for all future searches that
        I only want to attend Level 300 sessions.
        Suggest me a session on AgentCore.
    """
    print(f"User: {prompt_5}")
    
    response_5 = run_strands_agent_with_LTM(
        user_id=user_id,
        session_id=session_5,
        user_prompt=prompt_5,
    )
    print(f"Agent: {response_5}\n")

    # Check if the model called the tool to 
    # save user preference to the database
    user_profile = lt_memory.get_user_profile(user_id)
    print(f"Long-term memory from the database: {user_profile}")


    # SESSION 6: Start conversation with a new user

    # Define a new user ID representing
    # a different user logging into the app
    user_id_1 = f"user_{uuid.uuid4()}"
    
    session_6 = str(uuid.uuid4())
    print(f"--- Starting Session 6 ---")
    
    prompt_6 = """
        Suggest me a session on observability.
    """
    print(f"User: {prompt_6}")
    
    response_6 = run_strands_agent_with_LTM(
        user_id=user_id_1,
        session_id=session_6,
        user_prompt=prompt_6,
    )
    print(f"Agent: {response_6}\n")

    # Expect an empty profile for the new user 
    user_profile = lt_memory.get_user_profile(user_id_1)
    print(f"Long-term memory from the database: {user_profile}")


if __name__ == "__main__":
    test_long_term_memory()