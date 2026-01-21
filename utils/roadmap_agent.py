MAX_QUESTIONS = 6

def roadmap_agent(user_input, state):
    """
    state = {
        "step": 1,
        "question_count": 0,
        "knows_role": None,
        "role": None,
        "subjects": [],
        "interests": [],
        "work_type": None,
        "experience": None,
        "time": None
    }
    """

    # Safety stop
    if state["question_count"] >= MAX_QUESTIONS:
        state["step"] = "generate"
        return None, state

    # STEP 1
    if state["step"] == 1:
        state["question_count"] += 1
        state["step"] = 2
        return "Do you already know your target job role? (Yes / No)", state

    # STEP 2
    if state["step"] == 2:
        state["question_count"] += 1

        if "yes" in user_input.lower():
            state["knows_role"] = True
            state["step"] = 3
            return "What is your target job role?", state
        else:
            state["knows_role"] = False
            state["step"] = 4
            return "What are your strongest subjects?", state

    # STEP 3 — Known role
    if state["step"] == 3:
        state["role"] = user_input
        state["question_count"] += 1
        state["step"] = 6
        return "What is your experience level? (Beginner / Intermediate / Advanced)", state

    # STEP 4 — Discovery
    if state["step"] == 4:
        state["subjects"] = user_input.split(",")
        state["question_count"] += 1
        state["step"] = 5
        return "What are your interests? (Web, Data, AI, Security, Cloud, Design)", state

    # STEP 5
    if state["step"] == 5:
        state["interests"] = user_input.split(",")
        state["question_count"] += 1
        state["step"] = 6
        return "What kind of work do you enjoy? (Coding / Analysis / Design / Security)", state

    # STEP 6
    if state["step"] == 6:
        state["experience"] = user_input
        state["question_count"] += 1
        state["step"] = "generate"
        return None, state
