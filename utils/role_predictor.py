def predict_role(subjects, interests, work_type):
    interests = " ".join(interests).lower()

    if "web" in interests:
        return "Frontend Developer"
    if "data" in interests or "statistics" in interests:
        return "Data Analyst"
    if "ai" in interests:
        return "Data Scientist"
    if "security" in interests:
        return "Cybersecurity Analyst"
    if "cloud" in interests:
        return "DevOps Engineer"

    return "Software Engineer"
