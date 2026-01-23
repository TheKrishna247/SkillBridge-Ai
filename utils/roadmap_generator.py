ROADMAPS = {
    # More structured (branching) graphs to better resemble roadmap.sh.
    "Frontend Developer": [
        ("Front-end", "Internet"),
        ("Internet", "How does the Internet work?"),
        ("Internet", "HTTP"),
        ("Internet", "DNS"),
        ("Internet", "Browsers"),

        ("Front-end", "HTML"),
        ("HTML", "Semantic HTML"),
        ("HTML", "Forms & Validation"),
        ("HTML", "Accessibility (a11y)"),

        ("Front-end", "CSS"),
        ("CSS", "Selectors & Specificity"),
        ("CSS", "Flexbox"),
        ("CSS", "Grid"),
        ("CSS", "Responsive Design"),

        ("Front-end", "JavaScript"),
        ("JavaScript", "ES6+"),
        ("JavaScript", "DOM"),
        ("JavaScript", "Fetch / Async"),

        ("Front-end", "Version Control"),
        ("Version Control", "Git"),
        ("Version Control", "GitHub"),

        ("Front-end", "Package Managers"),
        ("Package Managers", "npm"),
        ("Package Managers", "pnpm / yarn"),

        ("Front-end", "Framework"),
        ("Framework", "React"),
        ("React", "State Management"),
        ("React", "Routing"),

        ("Front-end", "Testing"),
        ("Testing", "Unit Testing"),
        ("Testing", "E2E Testing"),

        ("Front-end", "Projects"),
        ("Projects", "Portfolio"),
    ],

    "Backend Developer": [
        ("Back-end", "Programming Language"),
        ("Programming Language", "Python"),
        ("Programming Language", "Java / Node / Go (optional)"),

        ("Back-end", "Databases"),
        ("Databases", "SQL Basics"),
        ("Databases", "PostgreSQL / MySQL"),
        ("Databases", "Indexing"),

        ("Back-end", "APIs"),
        ("APIs", "REST"),
        ("APIs", "Auth (JWT / Sessions)"),
        ("APIs", "Rate Limiting"),

        ("Back-end", "Caching"),
        ("Caching", "Redis"),

        ("Back-end", "Dev Practices"),
        ("Dev Practices", "Git"),
        ("Dev Practices", "Testing"),
        ("Dev Practices", "Logging & Monitoring"),

        ("Back-end", "Deployment"),
        ("Deployment", "Docker"),
        ("Deployment", "Cloud Basics"),

        ("Back-end", "Projects"),
    ],

    "Full Stack Developer": [
        ("Full-stack", "Front-end"),
        ("Front-end", "HTML"),
        ("Front-end", "CSS"),
        ("Front-end", "JavaScript"),
        ("JavaScript", "React"),

        ("Full-stack", "Back-end"),
        ("Back-end", "APIs"),
        ("Back-end", "Databases"),
        ("Databases", "SQL"),

        ("Full-stack", "Dev Practices"),
        ("Dev Practices", "Git"),
        ("Dev Practices", "Testing"),

        ("Full-stack", "Deployment"),
        ("Deployment", "Docker"),
        ("Deployment", "CI/CD"),

        ("Full-stack", "Projects"),
        ("Projects", "Portfolio"),
    ],

    "Data Analyst": [
        ("Data Analyst", "Foundations"),
        ("Foundations", "Spreadsheets"),
        ("Foundations", "Statistics"),
        ("Foundations", "Data Literacy"),

        ("Data Analyst", "SQL"),
        ("SQL", "Joins"),
        ("SQL", "Window Functions"),
        ("SQL", "Data Modeling Basics"),

        ("Data Analyst", "Python (optional but strong)"),
        ("Python (optional but strong)", "Pandas"),
        ("Python (optional but strong)", "Data Cleaning"),

        ("Data Analyst", "Visualization"),
        ("Visualization", "Tableau / Power BI"),
        ("Visualization", "Dashboards"),
        ("Visualization", "Storytelling"),

        ("Data Analyst", "Analytics"),
        ("Analytics", "KPIs & Metrics"),
        ("Analytics", "A/B Testing Basics"),

        ("Data Analyst", "Projects"),
        ("Projects", "Portfolio"),
    ],

    "Data Scientist": [
        ("Data Scientist", "Math & Stats"),
        ("Math & Stats", "Probability"),
        ("Math & Stats", "Statistics"),
        ("Math & Stats", "Linear Algebra (basics)"),

        ("Data Scientist", "Python"),
        ("Python", "Pandas"),
        ("Python", "NumPy"),
        ("Python", "Data Viz (Matplotlib/Seaborn)"),

        ("Data Scientist", "SQL"),

        ("Data Scientist", "Machine Learning"),
        ("Machine Learning", "Supervised Learning"),
        ("Machine Learning", "Unsupervised Learning"),
        ("Machine Learning", "Model Evaluation"),

        ("Data Scientist", "MLOps Basics"),
        ("MLOps Basics", "Experiment Tracking"),
        ("MLOps Basics", "Deployment"),

        ("Data Scientist", "Projects"),
        ("Projects", "Portfolio"),
    ],

    "DevOps Engineer": [
        ("DevOps", "Linux"),
        ("Linux", "Networking Basics"),
        ("Linux", "Shell Scripting"),

        ("DevOps", "Version Control"),
        ("Version Control", "Git"),

        ("DevOps", "Containers"),
        ("Containers", "Docker"),
        ("Containers", "Kubernetes (optional)"),

        ("DevOps", "CI/CD"),
        ("CI/CD", "Pipelines"),
        ("CI/CD", "Testing in CI"),

        ("DevOps", "Cloud"),
        ("Cloud", "AWS / Azure / GCP"),
        ("Cloud", "IaC (Terraform)"),

        ("DevOps", "Observability"),
        ("Observability", "Monitoring"),
        ("Observability", "Logging"),

        ("DevOps", "Projects"),
    ],

    "Cybersecurity Analyst": [
        ("Cybersecurity", "Foundations"),
        ("Foundations", "Networking"),
        ("Foundations", "Linux"),
        ("Foundations", "Security Basics"),

        ("Cybersecurity", "Web Security"),
        ("Web Security", "OWASP Top 10"),
        ("Web Security", "Burp Suite (basics)"),

        ("Cybersecurity", "Blue Team"),
        ("Blue Team", "SIEM Basics"),
        ("Blue Team", "Log Analysis"),

        ("Cybersecurity", "Tools"),
        ("Tools", "Nmap"),
        ("Tools", "Wireshark"),

        ("Cybersecurity", "Projects"),
        ("Projects", "Write-ups / Portfolio"),
    ],
}

ROADMAP_DETAILS = {
    "Frontend Developer": [
        (
            "Foundations",
            [
                "Understand how the internet works (requests, responses, DNS, hosting).",
                "Learn how browsers render HTML, CSS, and JavaScript.",
            ],
        ),
        (
            "HTML",
            [
                "Learn basic tags, attributes, and document structure.",
                "Practice semantic HTML (header, nav, main, section, article, footer).",
                "Build a few static pages (portfolio, landing page).",
            ],
        ),
        (
            "CSS",
            [
                "Master the box model, positioning, and common layouts.",
                "Learn Flexbox and CSS Grid for modern layout systems.",
                "Practice responsive design (mobile‑first) and media queries.",
            ],
        ),
        (
            "JavaScript",
            [
                "Understand variables, functions, loops, and objects (ES6+).",
                "Manipulate the DOM and handle events.",
                "Work with APIs using fetch / async‑await.",
            ],
        ),
        (
            "Framework (React)",
            [
                "Learn components, props, and state.",
                "Understand hooks, routing, and basic state management.",
                "Build 2–3 complete React projects (e.g., dashboard, e‑commerce UI).",
            ],
        ),
        (
            "Tooling",
            [
                "Use Git and GitHub for version control.",
                "Learn npm / yarn / pnpm and basic bundlers (Vite, Webpack, or CRA).",
            ],
        ),
        (
            "Testing & Performance",
            [
                "Write basic unit tests (Jest / React Testing Library).",
                "Understand Lighthouse and basic performance optimization.",
            ],
        ),
        (
            "Projects & Portfolio",
            [
                "Ship a polished portfolio site showcasing at least 3 projects.",
                "Deploy using Netlify, Vercel, or similar hosting.",
            ],
        ),
    ],
    "Backend Developer": [
        (
            "Language & Syntax",
            [
                "Choose one primary backend language (Python / Node / Java / Go).",
                "Learn syntax, control flow, functions, and modules.",
            ],
        ),
        (
            "Databases",
            [
                "Understand relational databases and SQL fundamentals.",
                "Practice joins, aggregations, and indexing.",
            ],
        ),
        (
            "APIs",
            [
                "Build REST APIs with a framework (e.g., FastAPI, Django, Express).",
                "Implement authentication and authorization (sessions / JWT).",
            ],
        ),
        (
            "Architecture & Patterns",
            [
                "Learn MVC / layered architecture basics.",
                "Understand error handling, logging, and configuration management.",
            ],
        ),
        (
            "Deployment",
            [
                "Containerize simple services using Docker.",
                "Deploy to a cloud provider (Render, Railway, AWS, etc.).",
            ],
        ),
        (
            "Projects",
            [
                "Build at least 2 real‑world style APIs (e.g., blog, task manager).",
                "Add authentication, pagination, and basic permissions.",
            ],
        ),
    ],
    "Full Stack Developer": [
        (
            "Front‑end Stack",
            [
                "Cover the full Frontend Developer path (HTML, CSS, JS, React).",
                "Practice building responsive, accessible UIs.",
            ],
        ),
        (
            "Back‑end Stack",
            [
                "Choose a backend framework (Node/Express, Django, etc.).",
                "Connect your API to a database and expose REST endpoints.",
            ],
        ),
        (
            "Integration",
            [
                "Connect frontend apps to your backend APIs.",
                "Handle auth flows end‑to‑end (login, signup, protected routes).",
            ],
        ),
        (
            "DevOps Basics",
            [
                "Use Git for collaboration (branches, PRs).",
                "Set up simple CI and deployment pipelines.",
            ],
        ),
    ],
    "Data Analyst": [
        (
            "Business & Data Foundations",
            [
                "Understand basic business metrics (revenue, conversion, churn, etc.).",
                "Learn how to translate questions into data problems.",
            ],
        ),
        (
            "Spreadsheets",
            [
                "Become comfortable with Excel or Google Sheets.",
                "Practice formulas, pivot tables, and charts.",
            ],
        ),
        (
            "SQL",
            [
                "Practice CRUD operations, joins, and aggregations.",
                "Learn window functions and subqueries for analytics.",
            ],
        ),
        (
            "Analytics Tools",
            [
                "Pick one BI tool (Power BI / Tableau / Looker Studio).",
                "Create interactive dashboards and reports.",
            ],
        ),
        (
            "Statistics",
            [
                "Review descriptive statistics and probability basics.",
                "Understand hypothesis testing and confidence intervals.",
            ],
        ),
        (
            "Projects",
            [
                "Do at least 2 end‑to‑end case studies (data cleaning → analysis → dashboard).",
                "Publish your work on GitHub or a portfolio site.",
            ],
        ),
    ],
    "Data Scientist": [
        (
            "Math & Stats",
            [
                "Strengthen knowledge of probability, statistics, and linear algebra basics.",
                "Focus on concepts behind common ML algorithms.",
            ],
        ),
        (
            "Python for Data",
            [
                "Practice with NumPy, Pandas, and Matplotlib/Seaborn.",
                "Work on EDA (exploratory data analysis) projects.",
            ],
        ),
        (
            "Machine Learning",
            [
                "Learn supervised vs unsupervised learning.",
                "Implement models with scikit‑learn (regression, classification, clustering).",
            ],
        ),
        (
            "Model Evaluation & Tuning",
            [
                "Use proper metrics (accuracy, F1, ROC‑AUC, etc.).",
                "Learn cross‑validation and basic hyperparameter tuning.",
            ],
        ),
        (
            "Deployment Basics",
            [
                "Expose simple models via an API (FastAPI / Flask).",
                "Understand model versioning and experiment tracking.",
            ],
        ),
    ],
    "DevOps Engineer": [
        (
            "Systems & Linux",
            [
                "Get comfortable using Linux CLI daily.",
                "Understand processes, permissions, and basic networking.",
            ],
        ),
        (
            "Source Control & CI",
            [
                "Use Git effectively (branching, merging, rebasing).",
                "Set up CI pipelines (GitHub Actions, GitLab CI, etc.).",
            ],
        ),
        (
            "Containers & Orchestration",
            [
                "Containerize apps with Docker.",
                "Learn container registries and basic Kubernetes concepts.",
            ],
        ),
        (
            "Cloud & IaC",
            [
                "Pick one cloud provider (AWS / Azure / GCP).",
                "Automate infrastructure with Terraform or similar tools.",
            ],
        ),
    ],
    "Cybersecurity Analyst": [
        (
            "Networking & OS",
            [
                "Understand TCP/IP, ports, and common protocols.",
                "Get comfortable with Linux and basic administration tasks.",
            ],
        ),
        (
            "Security Fundamentals",
            [
                "Learn core security concepts (CIA triad, threats, and vulnerabilities).",
                "Study common attack types (phishing, injection, XSS, etc.).",
            ],
        ),
        (
            "Tools & Platforms",
            [
                "Practice with Nmap, Wireshark, and basic SIEM tools.",
                "Explore vulnerability scanning and simple incident response labs.",
            ],
        ),
        (
            "Web & Application Security",
            [
                "Study OWASP Top 10 and common mitigation strategies.",
                "Do hands‑on labs (e.g., intentionally vulnerable web apps).",
            ],
        ),
    ],
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


def generate_roadmap_markdown(role: str) -> str | None:
    """
    Return a detailed, sectioned markdown roadmap (similar in spirit to roadmap.sh).
    """
    sections = ROADMAP_DETAILS.get(role)
    if not sections:
        return None

    lines: list[str] = []
    for title, bullets in sections:
        lines.append(f"### {title}")
        for item in bullets:
            lines.append(f"- {item}")
        lines.append("")  # blank line between sections

    return "\n".join(lines).strip()
