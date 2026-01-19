def calculate_ats_score(resume_text, role_skills=None):
    text = resume_text.lower()
    score = 0

    sections = {
        "projects": 10,
        "experience": 10,
        "education": 5,
        "skills": 10,
        "certification": 5
    }

    for sec, pts in sections.items():
        if sec in text:
            score += pts

    if "linkedin" in text:
        score += 5
    if "github" in text:
        score += 5

    if role_skills:
        matched = 0
        for skill in role_skills:
            if skill.lower() in text:
                matched += 1
        if len(role_skills) > 0:
            score += int((matched / len(role_skills)) * 50)

    return min(100, score)
