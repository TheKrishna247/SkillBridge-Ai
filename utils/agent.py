import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are SkillBridge AI Assistant.
Guide the user like Airtel Thanks help interface.

Rules:
1) Ask only ONE question at a time
2) Decide between Roadmap or SkillBridge
3) When enough info is collected, return final answer
Return JSON only in format:
{
  "intent": "roadmap" or "skillbridge",
  "next_question": "string or null",
  "final_answer": "string or null"
}
"""

def agent_decide(user_message, memory):
    prompt = f"""
Conversation so far:
{memory}

User message:
{user_message}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.4,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    text = response.choices[0].message.content.strip()
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end+1])
