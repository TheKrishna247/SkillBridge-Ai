import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def suggest_careers_llm(user_data):
    """Use LLM to suggest careers based on user profile"""
    
    prompt = f"""
    Based on this user profile:
    - Interests: {user_data.get('interests', 'Not specified')}
    - Strong Subjects: {user_data.get('strong_subjects', 'Not specified')}
    - Leisure Activities: {user_data.get('leisure', 'Not specified')}
    - Work Preference: {user_data.get('work_env', 'Not specified')}
    
    Suggest 3 suitable career options with:
    1. Role name
    2. Why it's suitable
    3. Expected salary range
    4. Growth prospects
    
    Format the response clearly with bullet points.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}],
        )
        
        return response.choices[0].message.content
    except:
        return """Based on your profile, I suggest:
        
        1. **Data Analyst**
           - Why: Good with numbers and analysis
           - Salary: ₹4-8 LPA
           - Growth: High demand in tech companies
        
        2. **Frontend Developer**
           - Why: Creative and technical
           - Salary: ₹5-10 LPA
           - Growth: Always needed for web development
        
        3. **Digital Marketer**
           - Why: Good communication skills
           - Salary: ₹3-6 LPA
           - Growth: Essential for all businesses"""