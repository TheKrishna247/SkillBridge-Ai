import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# -----------------------------
st.set_page_config(page_title="SkillBridge AI", layout="centered")

from roles_skills import ROLES_SKILLS
from roadmap_links import ROADMAP_LINKS
from utils.resume_parser import extract_text
from utils.ats_score import calculate_ats_score
from utils.resource_retriever import get_resources
from utils.agent import agent_decide
from utils.internet_search import search_web

# -----------------------------
# CHAT INIT (AFTER PAGE CONFIG)
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = [
        {"role": "assistant", "content": "Hi! I’m SkillBridge AI. Choose Roadmap or SkillBridge to begin."}
    ]

# -----------------------------
# CUSTOM CSS (UI UPGRADE)
# -----------------------------
st.markdown("""
<style>

/* =========================
   GLOBAL UI (KEEP THIS)
   ========================= */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 950px;
}

h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
}

.small-label {
    opacity: 0.75;
    font-size: 0.95rem;
}

.header-card {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 26px;
    background: rgba(255,255,255,0.03);
    margin-top: 14px;
    margin-bottom: 22px;
}

.mode-card {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 22px;
    background: rgba(255,255,255,0.04);
    transition: 0.2s ease-in-out;
    min-height: 190px;
}
.mode-card:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(255,255,255,0.25);
    background: rgba(255,255,255,0.06);
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.82rem;
    border: 1px solid rgba(255,255,255,0.18);
    opacity: 0.9;
}

button[kind="secondary"] {
    border-radius: 14px !important;
    padding: 0.65rem 1rem !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    background: rgba(255,255,255,0.04) !important;
}
button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

/* =========================
   CHAT UI (ADD THIS)
   ========================= */

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.chat-row {
    display: flex;
    width: 100%;
}

.chat-user {
    justify-content: flex-end;
}

.chat-ai {
    justify-content: flex-start;
}

.chat-bubble {
    max-width: 70%;
    padding: 12px 14px;
    border-radius: 16px;
    line-height: 1.45;
    word-wrap: break-word;
}

/* USER */
.user-bubble {
    background: #F4D7DE;
    color: #2B1B1E;
    border-radius: 16px 16px 2px 16px;
    border: 1px solid #E8BFC9;
}

/* AI */
.ai-bubble {
    background: #E5E7EB;
    color: #111827;
    border-radius: 16px 16px 16px 2px;
}




</style>
""", unsafe_allow_html=True)




# -----------------------------
# SESSION STATE
# -----------------------------
if "screen" not in st.session_state:
    st.session_state.screen = "home"

if "chat" not in st.session_state:
    st.session_state.chat = []

if "target_role" not in st.session_state:
    st.session_state.target_role = None

# -----------------------------
# QUESTION LIMIT CONTROL (NEW)
# -----------------------------
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "max_questions" not in st.session_state:
    st.session_state.max_questions = 5  # set 3/4/5


# -----------------------------
# AGENT STATE (NEW)
# -----------------------------
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "step": "START",
        "mode": None,            # "roadmap" or "skillbridge"
        "target_role": None,     # selected career role
        "resume_needed": None    # True / False
    }

def add_assistant(msg):
    st.session_state.chat.append({"role": "assistant", "content": msg})

def add_user(msg):
    st.session_state.chat.append({"role": "user", "content": msg})

def question_limit_reached():
    return st.session_state.question_count >= st.session_state.max_questions

def reset_app():
    st.session_state.screen = "home"

    # reset chat to default welcome message
    st.session_state.chat = [
        {"role": "assistant", "content": "Hi! I’m SkillBridge AI. Choose Roadmap or SkillBridge to begin."}
    ]

    # reset old UI role
    st.session_state.target_role = None

    # reset agent state
    st.session_state.agent_state = {
        "step": "START",
        "mode": None,
        "target_role": None,
        "resume_needed": None
    }

    # reset question limit counter (NEW)
    st.session_state.question_count = 0


# -----------------------------
# SIDEBAR (Modern)
# -----------------------------
with st.sidebar:
    st.markdown("## 🔥 Phoenix")
    st.markdown("### SkillBridge AI")

    # ✅ Creator section
    st.markdown("**Creator:**")
    st.markdown("Krishna Tomar")
    st.markdown("Avanish Pathak")

    st.markdown("---")

    st.markdown("**Modes Available:**")
    st.markdown("- 🗺 Roadmap Generator")
    st.markdown("- 🧠 SkillBridge Resume Analyzer")
    st.markdown("---")

    if st.button("🔄 Reset Assistant"):
        reset_app()
        st.rerun()

# -----------------------------
# HEADER
# -----------------------------
st.markdown("## 🔥 SkillBridge AI Assistant")
st.markdown("<div class='small-label'>Your AI Career Guide for Roadmaps and Skill Gaps</div>", unsafe_allow_html=True)
st.markdown("---")



# -----------------------------
# HOME SCREEN
# -----------------------------
if st.session_state.screen == "home":
    if len(st.session_state.chat) == 0:
        add_assistant("Hi! I’m SkillBridge AI. Choose Roadmap or SkillBridge to begin.")

    # ✅ Put text INSIDE the rectangle
    st.markdown("""
    <div class='header-card'>
        <h2 style='text-align:center; margin:0;'>Choose an option</h2>
        <p style='text-align:center; opacity:0.7; margin-top:6px;'>Select one to continue</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="mode-card">
            <div class="badge">Career Roadmap</div>
            <h2 style="margin-top:12px;">🗺 Roadmap</h2>
            <p style="opacity:0.8; font-size:0.95rem;">
                Get a structured learning path based on your goal.
                Perfect if you want direction and clarity.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="mode-card">
            <div class="badge">Skill Gap + ATS</div>
            <h2 style="margin-top:12px;">🧠 SkillBridge</h2>
            <p style="opacity:0.8; font-size:0.95rem;">
                Upload your resume, get ATS score, identify missing skills,
                and receive a personalized improvement plan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ✅ Chat section
    st.markdown("---")

    # ✅ Chat Title + Clear Chat button
    colA, colB = st.columns([3, 1])

    with colA:
        st.markdown("### 💬 Chat Assistant")

    with colB:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat = [
                {"role": "assistant", "content": "Chat cleared. How can I help you now?"}
            ]
            st.rerun()

    # ✅ Quick Replies
    st.markdown("**Quick Replies:**")
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("🗺 Roadmap", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I want Roadmap"})
            st.session_state.agent_state["mode"] = "roadmap"
            st.session_state.agent_state["step"] = "ROADMAP_FLOW"
            st.rerun()


    with q2:
        if st.button("🧠 SkillBridge", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I want SkillBridge"})
            st.session_state.agent_state["mode"] = "skillbridge"
            st.session_state.agent_state["step"] = "SKILLBRIDGE_FLOW"
            st.rerun()


    with q3:
        if st.button("📄 Upload Resume", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I have a resume"})
            st.session_state.agent_state["mode"] = "skillbridge"
            st.session_state.agent_state["resume_needed"] = True
            st.session_state.agent_state["step"] = "WAITING_FOR_RESUME_UPLOAD"
            st.rerun()


    with q4:
        if st.button("🎯 Suggest Careers", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I am uncertain about job role"})
            st.session_state.agent_state["mode"] = "roadmap"
            st.session_state.agent_state["step"] = "ROADMAP_FLOW"
            st.rerun()


    
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for msg in st.session_state.chat:
        role_class = "chat-user" if msg["role"] == "user" else "chat-ai"
        bubble_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"

        st.markdown(f"""
            <div class="chat-row {role_class}">
                <div class="chat-bubble {bubble_class}">
                    {msg["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ✅ Chat input
    user_input = st.chat_input("Type here...")

    if user_input:
        # store user message
        st.session_state.chat.append({"role": "user", "content": user_input})

        # build memory text for agent
        memory_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat])

        # call agent with state
        decision = agent_decide(user_input, memory_text, st.session_state.agent_state)

        # update state from agent response
        updates = decision.get("updates", {})
        for k, v in updates.items():
            if v is not None:
                st.session_state.agent_state[k] = v

        # update current step
        st.session_state.agent_state["step"] = decision.get(
            "next_step",
            st.session_state.agent_state["step"]
        )

        # store assistant message
        assistant_msg = decision.get("assistant_message", "Okay.")
        hints = decision.get("answer_hints", [])
        if hints:
            assistant_msg += "\n\nHint options:\n" + "\n".join([f"• {h}" for h in hints])

        if decision.get("next_step") == "ASK":
            st.session_state.agent_state["question_count"] += 1


        st.session_state.chat.append({"role": "assistant", "content": assistant_msg})

        # -----------------------------
        # STEP 5: WEB SEARCH TOOL CALL
        # -----------------------------
        if decision.get("should_web_search") and decision.get("web_search_query"):
            query = decision["web_search_query"]

            st.session_state.chat.append({
                "role": "assistant",
                "content": f"🔎 Searching the web for: {query}"
            })


            results = search_web(query, max_results=5)

            if results:
                formatted_results = ""
                for i, r in enumerate(results, 1):
                    formatted_results += (
                        f"{i}) {r['title']}\n"
                        f"{r['url']}\n"
                        f"{r['snippet']}\n\n"
                    )

                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "✅ Here are the top web results:\n\n" + formatted_results
                })
            else:
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "⚠️ I tried searching, but I couldn’t fetch results right now."
                })

        st.rerun()

# -----------------------------
# ROADMAP MODE
# -----------------------------
elif st.session_state.screen == "roadmap_choice":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 🗺 Roadmap Mode")
    st.write("Step 1/2: Choose how you want to proceed")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ I know my job role"):
            add_user("I know my job role")
            add_assistant("Select your job role below.")
            st.session_state.screen = "roadmap_known"
            st.rerun()

    with col2:
        if st.button("❓ I am uncertain"):
            add_user("I am uncertain about job role")
            add_assistant("No problem. Tell me your strong subjects and interests.")
            st.session_state.screen = "roadmap_uncertain"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.screen == "roadmap_known":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 🗺 Roadmap Generator")
    st.write("Step 2/2: Select your target role")

    role = st.selectbox("Select Job Role", list(ROADMAP_LINKS.keys()))

    if st.button("🚀 Generate Roadmap Link"):
        add_user(f"My job role is {role}")
        add_assistant(f"✅ Roadmap Link for **{role}**:\n\n{ROADMAP_LINKS[role]}")
        add_assistant("Follow the roadmap step-by-step. You can also use SkillBridge to check your gaps.")
        st.session_state.screen = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.screen == "roadmap_uncertain":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### ❓ Career Discovery")
    st.write("Tell me your strengths and interests (I will suggest roles)")

    subjects = st.multiselect(
        "Strong Subjects",
        ["Maths", "Physics", "Chemistry", "Computer Science", "Statistics", "English"]
    )

    interests = st.multiselect(
        "Interests",
        ["Web Development", "Data", "AI/ML", "Cybersecurity", "Cloud", "Design"]
    )

    st.info("For hackathon demo: This section can be upgraded with AI role prediction + top 3 suggestions.")

    if st.button("🔍 Suggest Careers (Basic)"):
        add_user(f"My strong subjects: {subjects}, interests: {interests}")
        add_assistant("Here are some roles you can explore:")

        # Basic mapping (fast + safe)
        if "Web Development" in interests:
            add_assistant("**Frontend Developer** → Good for UI + coding.")
            add_assistant("**Full Stack Developer** → Frontend + Backend combined.")
        if "Data" in interests or "AI/ML" in interests:
            add_assistant("**Data Analyst** → Python + SQL + dashboards.")
            add_assistant("**Data Scientist** → ML + statistics + advanced projects.")
        if "Cybersecurity" in interests:
            add_assistant("**Cybersecurity Analyst** → Networking + security fundamentals.")
        if "Cloud" in interests:
            add_assistant("**DevOps Engineer** → Linux + Docker + cloud deployment.")

        add_assistant("Now choose one role from Roadmap Generator.")
        st.session_state.screen = "roadmap_known"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SKILLBRIDGE MODE
# -----------------------------
elif st.session_state.screen == "skillbridge_goal":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 🧠 SkillBridge")
    st.write("Step 1/3: Choose your target career")

    role = st.selectbox("Choose Target Career", list(ROLES_SKILLS.keys()))

    if st.button("Next ➜"):
        st.session_state.target_role = role
        add_user(f"I want to become {role}")
        add_assistant("Do you have a resume?")
        st.session_state.screen = "skillbridge_resume_choice"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.screen == "skillbridge_resume_choice":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Resume Check")
    st.write("Step 2/3: Select one option")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Yes, I have a resume"):
            add_user("Yes, I have a resume")
            add_assistant("Upload your resume now.")
            st.session_state.screen = "skillbridge_upload"
            st.rerun()

    with col2:
        if st.button("❌ No, I don't have a resume"):
            add_user("No, I don't have a resume")
            add_assistant("No worries. Tell me your skills and projects.")
            st.session_state.screen = "skillbridge_no_resume"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.screen == "skillbridge_upload":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Upload Resume")
    st.write("Step 3/3: Upload resume to analyze ATS + gaps")

    uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

    if uploaded:
        resume_text = extract_text(uploaded)

        st.success("✅ Resume extracted successfully!")
        st.text_area("Extracted Resume Text", resume_text, height=200)

        role = st.session_state.target_role
        role_skills = ROLES_SKILLS[role]

        ats = calculate_ats_score(resume_text, role_skills)

        st.subheader("📌 ATS Score")
        st.progress(ats / 100)
        st.write(f"Your ATS Score: **{ats}/100**")

        st.subheader("❌ Missing Skills + Best Resources")
        missing = [s for s in role_skills if s.lower() not in resume_text.lower()]

        if missing:
            for skill in missing:
                st.markdown(f"### 🔴 {skill.title()}")
                res = get_resources(skill)
                if res:
                    st.markdown(f"- 📘 **Course**: {res['course']}")
                    st.markdown(f"- 🎥 **Video**: {res['video']}")
                    st.markdown(f"- 🧠 **Practice**: {res['practice']}")
                else:
                    st.markdown("- ⚠️ No curated resource found yet.")
        else:
            st.success("You are already role-ready 🎉")

        st.markdown("---")
        if st.button("⬅ Back"):
            st.session_state.screen = "skillbridge_resume_choice"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.screen == "skillbridge_no_resume":
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("### 🧾 No Resume Mode")
    st.write("Tell me your current skills + projects and I’ll guide you.")

    skills = st.text_area("Your Skills (example: Python, SQL, Excel)")
    projects = st.text_area("Your Projects (example: Attendance system, Portfolio website)")

    if st.button("Generate Plan"):
        add_user(f"My skills: {skills} | Projects: {projects}")
        add_assistant("✅ Great! Here is your next action plan:")
        add_assistant("1) Build 2 strong projects for your target role.")
        add_assistant("2) Create a 1-page ATS resume.")
        add_assistant("3) Upload resume again for ATS + skill gap analysis.")
        st.session_state.screen = "home"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)