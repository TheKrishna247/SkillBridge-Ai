import sys
from pathlib import Path

# Add parent directory to path to import roles_skills
sys.path.append(str(Path(__file__).parent.parent))
from roles_skills import ROLES_SKILLS

def calculate_readiness(user_skills, target_role):
    """
    Calculate how ready the user is for the target job (0-100%)
    
    Args:
        user_skills: dict of {skill: proficiency_level} where proficiency_level is "Beginner", "Intermediate", or "Advanced"
        target_role: string role name from ROLES_SKILLS
    
    Returns:
        dict with:
            - readiness_percentage: float (0-100)
            - matched_skills: list of skills user has
            - missing_skills: list of skills user needs
            - breakdown: dict with detailed breakdown
    """
    if not target_role or target_role not in ROLES_SKILLS:
        return {
            "readiness_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "breakdown": {}
        }
    
    required_skills = ROLES_SKILLS[target_role]
    user_skills_lower = {k.lower(): v for k, v in user_skills.items()}
    
    matched_skills = []
    missing_skills = []
    skill_scores = {}
    
    # Proficiency weights
    proficiency_weights = {
        "Beginner": 0.3,
        "Intermediate": 0.7,
        "Advanced": 1.0
    }
    
    # Check each required skill
    for required_skill in required_skills:
        required_lower = required_skill.lower()
        matched = False
        
        # Check for exact or partial match
        for user_skill, proficiency in user_skills_lower.items():
            if required_lower in user_skill or user_skill in required_lower:
                matched = True
                weight = proficiency_weights.get(proficiency, 0.5)
                skill_scores[required_skill] = weight
                matched_skills.append({
                    "skill": required_skill,
                    "proficiency": proficiency,
                    "score": weight
                })
                break
        
        if not matched:
            missing_skills.append(required_skill)
            skill_scores[required_skill] = 0
    
    # Calculate readiness percentage
    if not required_skills:
        readiness_percentage = 0
    else:
        total_score = sum(skill_scores.values())
        max_possible_score = len(required_skills) * 1.0  # All skills at Advanced level
        readiness_percentage = (total_score / max_possible_score) * 100
    
    # Create breakdown
    breakdown = {
        "total_required_skills": len(required_skills),
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "skill_scores": skill_scores,
        "by_proficiency": {
            "Advanced": len([s for s in matched_skills if s["proficiency"] == "Advanced"]),
            "Intermediate": len([s for s in matched_skills if s["proficiency"] == "Intermediate"]),
            "Beginner": len([s for s in matched_skills if s["proficiency"] == "Beginner"])
        }
    }
    
    return {
        "readiness_percentage": round(readiness_percentage, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "breakdown": breakdown
    }
