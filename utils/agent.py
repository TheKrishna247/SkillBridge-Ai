import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ALLOWED_STEPS = ["ASK", "GENERATE"]

SYSTEM_PROMPT = """
You are SkillBridge AI, a strict roadmap generator.

Your job:
- Ask only 3 to 5 questions total.
- Ask only ONE question at a time.
- Provide hints/options for what the user can answer.
- After 3-5 questions OR when enough info is collected, STOP asking and generate a full roadmap.

You MUST output ONLY valid JSON in this schema:

{
  "assistant_message": "string",
  "next_step": "ASK|GENERATE",
  "question": "string|null",
  "answer_hints": ["string", "string"] or [],
  "updates": {
    "mode": "roadmap|skillbridge|null",
    "target_role": "string|null",
    "experience": "beginner|intermediate|advanced|null",
    "time_per_day": "string|null",
    "goal_timeline": "string|null"
  },
  "should_web_search": true|false,
  "web_search_query": "string|null"
}

Hard Rules:
- Use state.question_count and state.max_questions.
- If question_count >= max_questions => next_step MUST be "GENERATE"
- Ask questions ONLY from this list (in this order):
  1) target_role
  2) experience
  3) time_per_day
  4) goal_timeline
- If user already provided an answer, do NOT ask again.
- When next_step="ASK":
  - Fill question
  - Fill answer_hints (2 to 5 hints)
  - assistant_message must include question + short hints
- When next_step="GENERATE":
  - assistant_message must contain the FULL roadmap content (roadmap.sh style sections + checklist + projects)
- Do NOT output markdown outside JSON.
"""


def safe_json_parse(text: str):
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except Exception:
        return None


def agent_decide(user_message: str, memory_text: str, state: dict):
    prompt = f"""
Conversation so far:
{memory_text}

Current state:
{json.dumps(state)}

User message:
{user_message}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    raw = response.choices[0].message.content
    data = safe_json_parse(raw)

    # Fallback if model returns invalid JSON
    if not data:
        return {
            "assistant_message": "What role do you want to become?\nHint: choose one option below.",
            "next_step": "ASK",
            "question": "What role do you want to become?",
            "answer_hints": [
                "Frontend Developer",
                "Backend Developer",
                "Full Stack Developer",
                "Data Analyst",
                "DevOps Engineer"
            ],
            "updates": {
                "mode": "roadmap",
                "target_role": None,
                "experience": None,
                "time_per_day": None,
                "goal_timeline": None
            },
            "should_web_search": False,
            "web_search_query": None
        }

    # Guardrails
    if data.get("next_step") not in ALLOWED_STEPS:
        data["next_step"] = "ASK"

    # Ensure keys exist (safety)
    data.setdefault("assistant_message", "Okay.")
    data.setdefault("question", None)
    data.setdefault("answer_hints", [])
    data.setdefault("should_web_search", False)
    data.setdefault("web_search_query", None)
    data.setdefault("updates", {})

    return data
