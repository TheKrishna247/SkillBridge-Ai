from dotenv import load_dotenv
load_dotenv()


from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CAREER_COACH_SYSTEM_PROMPT = """
You are a professional career coach.

Your mission:
Identify the user's best-fit tech career role.

You must gather information about:
1. Interests
2. Technical skills
3. Experience level
4. Salary expectations

Rules:
- Ask ONLY one question at a time.
- Be conversational and human-like.
- Adapt questions based on previous answers.
- Never repeat a question.
- Do NOT explain your reasoning.
- Do NOT list options unless necessary.
- When you have enough information, say EXACTLY:
  "I have enough information to suggest career roles."
"""


def create_initial_state():
    return {
        "mode": "career_discovery",
        "facts": {
            "interests": None,
            "skills": None,
            "experience": None,
            "salary": None
        },
        "conversation": [],
        "done": False,
        "turns": 0,
        "max_turns": 8
    }


def run_career_discovery(user_input, state):
    # Safety stop
    if state["done"]:
        return None, state

    # Build LLM messages
    messages = [
        {"role": "system", "content": CAREER_COACH_SYSTEM_PROMPT}
    ]

    for msg in state["conversation"]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_input})

    # Call LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.6
    )

    assistant_reply = response.choices[0].message.content.strip()

    # Store conversation
    state["conversation"].append({"role": "user", "content": user_input})
    state["conversation"].append({"role": "assistant", "content": assistant_reply})

    # Light fact extraction
    text = user_input.lower()
    facts = state["facts"]

    if facts["interests"] is None and any(x in text for x in ["web", "data", "ai", "security", "cloud"]):
        facts["interests"] = user_input

    if facts["skills"] is None and any(x in text for x in ["python", "java", "sql", "javascript", "react"]):
        facts["skills"] = user_input

    if facts["experience"] is None and any(x in text for x in ["beginner", "intermediate", "advanced", "year"]):
        facts["experience"] = user_input

    if facts["salary"] is None and any(x in text for x in ["salary", "lpa", "₹", "$"]):
        facts["salary"] = user_input

    # Stop conditions
    if "I have enough information to suggest career roles." in assistant_reply:
        state["done"] = True

    if all(facts.values()):
        state["done"] = True

    state["turns"] += 1
    if state["turns"] >= state["max_turns"]:
        state["done"] = True

    return assistant_reply, state
