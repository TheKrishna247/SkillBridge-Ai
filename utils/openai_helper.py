import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def recommend_careers(subjects, interests):
    prompt = f"""
You are a career guidance AI.
Based on strong subjects and interests, suggest 3 career options.

Strong subjects: {subjects}
Interests: {interests}

Return ONLY JSON like:
{{
  "careers": [
    {{"role": "Role Name", "reason": "Why suitable"}},
    {{"role": "Role Name", "reason": "Why suitable"}},
    {{"role": "Role Name", "reason": "Why suitable"}}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content.strip()
    start = text.find("{")
    end = text.rfind("}")
    return json.loads(text[start:end+1])
