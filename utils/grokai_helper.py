import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def recommend_careers(subjects=None, interests=None, leisure_activities=None, 
                     work_environment=None, salary_expectations=None, 
                     industry_preference=None, considered_careers=None):
    """
    Recommend careers based on all collected user data
    """
    prompt = f"""
You are a career guidance AI.
Based on the following information, suggest 3 career options from these roles:
Frontend Developer, Backend Developer, Full Stack Developer, Data Analyst, 
Data Scientist, DevOps Engineer, Cybersecurity Analyst

User Information:
- Strong subjects: {subjects or 'Not provided'}
- Interests: {interests or 'Not provided'}
- Leisure activities: {leisure_activities or 'Not provided'}
- Preferred work environment: {work_environment or 'Not provided'}
- Salary expectations: {salary_expectations or 'Not provided'}
- Industry preference: {industry_preference or 'Not provided'}
- Previously considered careers: {considered_careers or 'Not provided'}

Return ONLY JSON like:
{{
  "careers": [
    {{"role": "Role Name", "reason": "Why suitable based on user profile"}},
    {{"role": "Role Name", "reason": "Why suitable based on user profile"}},
    {{"role": "Role Name", "reason": "Why suitable based on user profile"}}
  ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.choices[0].message.content.strip()
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= 0:
            return json.loads(text[start:end+1])
    except Exception as e:
        print(f"Error in recommend_careers: {e}")
    
    # Fallback if LLM fails
    return {
        "careers": [
            {"role": "Frontend Developer", "reason": "Good match based on your profile"},
            {"role": "Backend Developer", "reason": "Suitable for your interests"},
            {"role": "Full Stack Developer", "reason": "Combines multiple skills"}
        ]
    }
