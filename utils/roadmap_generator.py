ROADMAPS = {
    "Frontend Developer": [
        ("HTML", "CSS"),
        ("CSS", "JavaScript"),
        ("JavaScript", "React"),
        ("React", "Projects")
    ],

    "Data Scientist": [
        ("Python", "Statistics"),
        ("Statistics", "Pandas"),
        ("Pandas", "SQL"),
        ("SQL", "Machine Learning"),
        ("Machine Learning", "Projects")
    ],

    "DevOps Engineer": [
        ("Linux", "Git"),
        ("Git", "Docker"),
        ("Docker", "CI/CD"),
        ("CI/CD", "Cloud"),
        ("Cloud", "Projects")
    ]
}

def generate_roadmap_mermaid(role):
    edges = ROADMAPS.get(role)

    if not edges:
        return None

    diagram = "```mermaid\ngraph TD\n"

    for src, dst in edges:
        diagram += f"    {src.replace(' ', '_')} --> {dst.replace(' ', '_')}\n"

    diagram += "```"
    return diagram
