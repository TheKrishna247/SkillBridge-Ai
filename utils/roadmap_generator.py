ROADMAPS = {
    "Frontend Developer": [
        ("HTML", "CSS"),
        ("CSS", "JavaScript"),
        ("JavaScript", "React"),
        ("React", "Projects")
    ],
    
    "Backend Developer": [
        ("Python", "SQL"),
        ("SQL", "API Development"),
        ("API Development", "Database Design"),
        ("Database Design", "Git"),
        ("Git", "Projects")
    ],
    
    "Full Stack Developer": [
        ("HTML", "CSS"),
        ("CSS", "JavaScript"),
        ("JavaScript", "React"),
        ("React", "Node.js"),
        ("Node.js", "SQL"),
        ("SQL", "Git"),
        ("Git", "Projects")
    ],

    "Data Analyst": [
        ("Python", "SQL"),
        ("SQL", "Excel"),
        ("Excel", "Data Visualization"),
        ("Data Visualization", "Statistics"),
        ("Statistics", "Projects")
    ],

    "Data Scientist": [
        ("Python", "Statistics"),
        ("Statistics", "Pandas"),
        ("Pandas", "SQL"),
        ("SQL", "Machine Learning"),
        ("Machine Learning", "Deep Learning"),
        ("Deep Learning", "Projects")
    ],

    "DevOps Engineer": [
        ("Linux", "Git"),
        ("Git", "Docker"),
        ("Docker", "CI/CD"),
        ("CI/CD", "Cloud"),
        ("Cloud", "Projects")
    ],
    
    "Cybersecurity Analyst": [
        ("Networking", "Linux"),
        ("Linux", "Security Basics"),
        ("Security Basics", "OWASP"),
        ("OWASP", "Security Tools"),
        ("Security Tools", "Projects")
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
