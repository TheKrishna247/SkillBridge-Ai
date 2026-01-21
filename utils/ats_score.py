def calculate_ats_score(resume_text, target_role=None):
    """
    Calculate ATS score for resume
    Returns score (0-100) and improvement suggestions
    """
    text = resume_text.lower()
    score = 0
    suggestions = []
    
    # 1. Check for essential sections (30 points)
    sections = {
        "contact information": 10,
        "summary/objective": 5,
        "work experience": 10,
        "education": 5,
        "skills": 10,
        "projects": 5
    }
    
    for section, points in sections.items():
        if section in text or section.replace(" ", "") in text:
            score += points
        else:
            suggestions.append(f"Add '{section.title()}' section")
    
    # 2. Formatting checks (20 points)
    if len(resume_text) > 300 and len(resume_text) < 800:
        score += 10  # Good length
    elif len(resume_text) <= 300:
        suggestions.append("Resume is too short - add more details")
    else:
        suggestions.append("Resume is too long - keep it concise")
    
    # Check for bullet points
    if "•" in resume_text or "*" in resume_text or "- " in resume_text:
        score += 5
    
    # Check for action verbs
    action_verbs = ["developed", "created", "managed", "improved", "increased", "led"]
    verb_count = sum(1 for verb in action_verbs if verb in text)
    if verb_count >= 3:
        score += 5
    
    # 3. Role-specific keywords (30 points)
    if target_role:
        role_skills = {
            "frontend developer": ["html", "css", "javascript", "react", "git"],
            "backend developer": ["python", "sql", "api", "database", "git"],
            "data analyst": ["python", "sql", "excel", "data visualization", "statistics"],
            "devops engineer": ["linux", "docker", "aws", "ci/cd", "git"],
            "cybersecurity analyst": ["networking", "linux", "security", "owasp"]
        }
        
        required_skills = role_skills.get(target_role.lower(), [])
        matched = sum(1 for skill in required_skills if skill in text)
        
        if required_skills:
            match_percentage = (matched / len(required_skills)) * 30
            score += match_percentage
            
            if matched < len(required_skills):
                missing = [s for s in required_skills if s not in text]
                suggestions.append(f"Add keywords: {', '.join(missing)}")
    
    # 4. Additional points (20 points)
    if "linkedin" in text:
        score += 5
    if "github" in text:
        score += 5
    if "@" in resume_text and ".com" in resume_text:
        score += 5  # Has email
    if any(word in text for word in ["bachelor", "master", "degree", "diploma"]):
        score += 5
    
    # Cap score at 100
    score = min(100, int(score))
    
    # Generate grade
    if score >= 80:
        grade = "Excellent"
    elif score >= 60:
        grade = "Good"
    elif score >= 40:
        grade = "Fair"
    else:
        grade = "Needs Improvement"
    
    return {
        "score": score,
        "grade": grade,
        "suggestions": suggestions[:5]  # Top 5 suggestions
    }