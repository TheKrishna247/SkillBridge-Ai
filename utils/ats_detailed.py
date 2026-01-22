import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from roles_skills import ROLES_SKILLS

def get_detailed_ats_analysis(resume_text, target_role=None):
    """
    Generate comprehensive ATS analysis with detailed breakdown
    """
    text = resume_text.lower()
    analysis = {
        "score": 0,
        "grade": "Needs Improvement",
        "breakdown": {},
        "suggestions": [],
        "strengths": [],
        "weaknesses": [],
        "section_analysis": {},
        "keyword_analysis": {},
        "formatting_analysis": {}
    }
    
    # === SECTION ANALYSIS (40 points) ===
    sections = {
        "Contact Information": {"keywords": ["contact", "email", "phone", "address", "linkedin"], "found": False, "score": 10},
        "Professional Summary": {"keywords": ["summary", "objective", "profile", "about"], "found": False, "score": 8},
        "Work Experience": {"keywords": ["experience", "employment", "work history", "career"], "found": False, "score": 10},
        "Education": {"keywords": ["education", "degree", "university", "college", "qualification"], "found": False, "score": 6},
        "Skills": {"keywords": ["skills", "technical skills", "competencies", "expertise"], "found": False, "score": 8},
        "Projects": {"keywords": ["projects", "project", "portfolio", "achievements"], "found": False, "score": 6},
        "Certifications": {"keywords": ["certifications", "certificate", "courses", "training"], "found": False, "score": 4}
    }
    
    section_found = []
    section_missing = []
    section_score = 0
    
    for section_name, section_data in sections.items():
        found = any(keyword in text for keyword in section_data["keywords"])
        sections[section_name]["found"] = found
        if found:
            section_found.append(section_name)
            section_score += section_data["score"]
        else:
            section_missing.append(section_name)
    
    analysis["section_analysis"] = {
        "found": section_found,
        "missing": section_missing,
        "score": section_score,
        "max_score": 52
    }
    analysis["score"] += section_score
    
    # === FORMATTING ANALYSIS (25 points) ===
    formatting_score = 0
    formatting_issues = []
    formatting_strengths = []
    
    # Word count check
    word_count = len(resume_text.split())
    if 300 <= word_count <= 600:
        formatting_score += 8
        formatting_strengths.append("Optimal length (300-600 words)")
    elif 200 <= word_count < 300:
        formatting_score += 5
        formatting_issues.append(f"Resume is short ({word_count} words)")
    elif word_count > 600:
        formatting_score += 3
        formatting_issues.append(f"Resume is long ({word_count} words)")
    else:
        formatting_issues.append(f"Resume is very short ({word_count} words)")
    
    # Bullet points
    bullet_chars = ["•", "*", "-", "→", "▸"]
    has_bullets = any(char in resume_text for char in bullet_chars)
    if has_bullets:
        formatting_score += 5
        formatting_strengths.append("Good use of bullet points")
    else:
        formatting_issues.append("Use bullet points for better readability")
    
    # Action verbs
    action_verbs = [
        "developed", "created", "managed", "improved", "increased", "led",
        "designed", "implemented", "optimized", "built", "delivered", "achieved",
        "collaborated", "analyzed", "solved", "executed", "launched", "maintained"
    ]
    verb_count = sum(1 for verb in action_verbs if verb in text)
    if verb_count >= 8:
        formatting_score += 7
        formatting_strengths.append("Strong action verbs")
    elif verb_count >= 5:
        formatting_score += 5
        formatting_strengths.append("Good use of action verbs")
    elif verb_count >= 3:
        formatting_score += 3
    else:
        formatting_issues.append("Add more action verbs")
    
    # Quantifiable achievements
    numbers = re.findall(r'\b\d+\b', resume_text)
    quantifiable_count = sum(1 for num in numbers if len(num) <= 4)  # Avoid years/dates
    
    if quantifiable_count >= 5:
        formatting_score += 5
        formatting_strengths.append("Good quantifiable achievements")
    elif quantifiable_count >= 3:
        formatting_score += 3
    else:
        formatting_issues.append("Add quantifiable achievements (numbers, percentages)")
    
    analysis["formatting_analysis"] = {
        "score": formatting_score,
        "max_score": 25,
        "word_count": word_count,
        "bullet_points": has_bullets,
        "action_verbs": verb_count,
        "quantifiable_achievements": quantifiable_count,
        "issues": formatting_issues,
        "strengths": formatting_strengths
    }
    analysis["score"] += formatting_score
    
    # === KEYWORD ANALYSIS (35 points) ===
    keyword_score = 0
    matched_skills = []
    missing_skills = []
    
    if target_role and target_role in ROLES_SKILLS:
        required_skills = ROLES_SKILLS[target_role]
        
        for skill in required_skills:
            skill_lower = skill.lower()
            if skill_lower in text or any(word in text for word in skill_lower.split()):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        if matched_skills:
            match_percentage = (len(matched_skills) / len(required_skills)) * 35
            keyword_score += match_percentage
    
    # Generic keywords
    generic_keywords = ["team", "leadership", "communication", "problem solving", "project", "results"]
    found_generic = [kw for kw in generic_keywords if kw in text]
    keyword_score += min(len(found_generic) * 2, 10)  # Max 10 points for generic
    
    analysis["keyword_analysis"] = {
        "score": keyword_score,
        "max_score": 35,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "generic_keywords": found_generic,
        "target_role": target_role
    }
    analysis["score"] += keyword_score
    
    # === FINAL SCORE & GRADE ===
    analysis["score"] = min(100, int(analysis["score"]))
    
    if analysis["score"] >= 85:
        analysis["grade"] = "Excellent"
        grade_emoji = "🟢"
    elif analysis["score"] >= 70:
        analysis["grade"] = "Good"
        grade_emoji = "🟡"
    elif analysis["score"] >= 50:
        analysis["grade"] = "Fair"
        grade_emoji = "🟠"
    else:
        analysis["grade"] = "Needs Improvement"
        grade_emoji = "🔴"
    
    analysis["grade_emoji"] = grade_emoji
    
    # === GENERATE SUGGESTIONS ===
    suggestions = []
    strengths = []
    weaknesses = []
    
    # Section suggestions
    if section_missing:
        for section in section_missing[:3]:  # Top 3 missing sections
            suggestions.append(f"Add '{section}' section")
            weaknesses.append(f"Missing '{section}' section")
    
    # Found sections are strengths
    for section in section_found[:3]:
        strengths.append(f"Has '{section}' section")
    
    # Formatting suggestions
    if formatting_issues:
        suggestions.extend(formatting_issues[:3])
        weaknesses.extend(formatting_issues[:2])
    
    if formatting_strengths:
        strengths.extend(formatting_strengths[:3])
    
    # Keyword suggestions
    if missing_skills:
        suggestions.append(f"Add role-specific skills: {', '.join(missing_skills[:3])}")
        weaknesses.append(f"Missing key skills for {target_role}" if target_role else "Missing key skills")
    
    if matched_skills:
        strengths.append(f"Has relevant skills: {', '.join(matched_skills[:3])}")
    
    # Contact info check
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.search(email_pattern, resume_text):
        suggestions.append("Ensure email address is clearly visible")
        weaknesses.append("Email not found")
    else:
        strengths.append("Email address present")
    
    if "linkedin" not in text and "linkedin.com" not in resume_text:
        suggestions.append("Add LinkedIn profile URL")
        weaknesses.append("LinkedIn URL missing")
    else:
        strengths.append("LinkedIn profile included")
    
    if "github" not in text and "github.com" not in resume_text:
        suggestions.append("Add GitHub profile URL (if applicable)")
    
    analysis["suggestions"] = suggestions[:8]  # Top 8 suggestions
    analysis["strengths"] = strengths[:5]  # Top 5 strengths
    analysis["weaknesses"] = weaknesses[:5]  # Top 5 weaknesses
    
    return analysis