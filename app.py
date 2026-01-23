import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# -----------------------------
st.set_page_config(page_title="SkillBridge AI", layout="centered")

# Add to your imports at the top
from roles_skills import ROLES_SKILLS
from roadmap_links import ROADMAP_LINKS
from utils.resume_parser import extract_text
from utils.ats_detailed import get_detailed_ats_analysis
from utils.resource_retriever import get_resources
from utils.agent import get_agent_response, agent  # Using new agent
from utils.internet_search import search_web
from utils.dynamic_career_agent import (
    create_initial_state,
    run_career_discovery
)

import re
import difflib


def _normalize_role_text(text: str) -> str:
    text = (text or "").strip().lower()
    # Keep alphanumerics, turn the rest into spaces, collapse whitespace.
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def resolve_role(user_text: str, allowed_roles: list[str] | None = None) -> str | None:
    """
    Convert freeform user input (any casing / minor variations) into a canonical role name.

    - If allowed_roles is provided, only returns one of those roles.
    """
    if not user_text:
        return None

    canonical_roles = list(ROADMAP_LINKS.keys())
    allowed = allowed_roles or canonical_roles

    norm = _normalize_role_text(user_text)
    if not norm:
        return None

    # Canonical normalization map + a few common aliases.
    aliases: dict[str, str] = {}
    for role in canonical_roles:
        aliases[_normalize_role_text(role)] = role

    # Common user variations
    aliases.update({
        "frontend": "Frontend Developer",
        "front end": "Frontend Developer",
        "front end developer": "Frontend Developer",
        "backend": "Backend Developer",
        "back end": "Backend Developer",
        "back end developer": "Backend Developer",
        "fullstack": "Full Stack Developer",
        "full stack": "Full Stack Developer",
        "full stack developer": "Full Stack Developer",
        "data analyst": "Data Analyst",
        "data analytics": "Data Analyst",
        "data scientist": "Data Scientist",
        "devops": "DevOps Engineer",
        "dev ops": "DevOps Engineer",
        "cyber security": "Cybersecurity Analyst",
        "cybersecurity": "Cybersecurity Analyst",
        "security analyst": "Cybersecurity Analyst",
    })

    # 1) Exact alias hit
    candidate = aliases.get(norm)
    if candidate and candidate in allowed:
        return candidate

    # 2) Substring match against canonical role names (helps when user types extra words)
    for role in allowed:
        role_norm = _normalize_role_text(role)
        if role_norm and (norm == role_norm or norm in role_norm or role_norm in norm):
            return role

    # 3) Fuzzy match (typos, small differences)
    allowed_norms = { _normalize_role_text(r): r for r in allowed }
    close = difflib.get_close_matches(norm, list(allowed_norms.keys()), n=1, cutoff=0.75)
    if close:
        return allowed_norms[close[0]]

    return None

def clean_text(text):
    """Remove HTML tags and clean text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\-\:\;\(\)\@]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
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

if "target_role" not in st.session_state:
    st.session_state.target_role = None

# -----------------------------
# AGENT STATE (NEW)
# -----------------------------
if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "step": "START",
        "resume_needed": None,

        "question_count": 0,
        "max_questions": 4,   # you can set 3/4/5
        "mode": "roadmap",
        "target_role": None,
        "experience": None,
        "time_per_day": None,
        "goal_timeline": None
    }



def add_assistant(msg):
    st.session_state.chat.append({"role": "assistant", "content": msg})

def add_user(msg):
    st.session_state.chat.append({"role": "user", "content": msg})

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
    "resume_needed": None,

    "question_count": 0,
    "max_questions": 4,
    "mode": "roadmap",
    "target_role": None,
    "experience": None,
    "time_per_day": None,
    "goal_timeline": None
}


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
    st.markdown("- 🧠 SkillBridge")
    st.markdown("- 🔍 Resume Analyzer")
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
    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("🗺 Roadmap", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I want Roadmap"})
            # Reset and set agent state
            st.session_state.agent_state["mode"] = "roadmap"
            st.session_state.agent_state["step"] = "roadmap_start"
            # Trigger agent response immediately with session state sync
            agent_response = get_agent_response("I want Roadmap", st.session_state.agent_state)
            # Always ensure we have a response
            if not agent_response or not agent_response.get("response"):
                # Fallback response
                st.session_state.chat.append({
                    "role": "assistant", 
                    "content": "Great! Let's create your career roadmap.\n\n**Do you know exactly what job profile you want to become?**"
                })
                st.session_state.agent_state["step"] = "roadmap_choice"
            else:
                response_text = agent_response.get("response", "")
                if response_text:
                    st.session_state.chat.append({"role": "assistant", "content": response_text})
                # Update session state with agent's update_state
                if "update_state" in agent_response:
                    for key, value in agent_response["update_state"].items():
                        if value is not None:
                            # Map "step" to "step" in session state
                            if key == "step":
                                st.session_state.agent_state["step"] = value
                            else:
                                st.session_state.agent_state[key] = value
                # Also sync agent's internal state back to session state
                if hasattr(agent, 'state'):
                    if agent.state.get("current_step"):
                        st.session_state.agent_state["step"] = agent.state["current_step"]
                    if agent.state.get("mode"):
                        st.session_state.agent_state["mode"] = agent.state["mode"]
            st.rerun()

    with q2:
        if st.button("🧠 SkillBridge", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I want SkillBridge"})
            # Reset and set agent state
            st.session_state.agent_state["mode"] = "skillbridge"
            st.session_state.agent_state["step"] = "skillbridge_start"
            # Trigger agent response immediately with session state sync
            agent_response = get_agent_response("I want SkillBridge", st.session_state.agent_state)
            # Always ensure we have a response
            if not agent_response or not agent_response.get("response"):
                # Fallback response
                st.session_state.chat.append({
                    "role": "assistant", 
                    "content": "Great! Let's bridge your skill gap.\n\n**What job profile do you want to target?**"
                })
                st.session_state.agent_state["step"] = "ask_target_role"
            else:
                response_text = agent_response.get("response", "")
                if response_text:
                    st.session_state.chat.append({"role": "assistant", "content": response_text})
                # Update session state with agent's update_state
                if "update_state" in agent_response:
                    for key, value in agent_response["update_state"].items():
                        if value is not None:
                            # Map "step" to "step" in session state
                            if key == "step":
                                st.session_state.agent_state["step"] = value
                            else:
                                st.session_state.agent_state[key] = value
                # Also sync agent's internal state back to session state
                if hasattr(agent, 'state'):
                    if agent.state.get("current_step"):
                        st.session_state.agent_state["step"] = agent.state["current_step"]
                    if agent.state.get("mode"):
                        st.session_state.agent_state["mode"] = agent.state["mode"]
            st.rerun()

    with q3:
        if st.button("🔍 Resume Analyzer", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "I want to analyze my resume"})
            st.session_state.agent_state["mode"] = "ats_score"
            st.session_state.agent_state["step"] = "ATS_SCORE_FLOW"
            st.session_state.show_ats_uploader = True
            # Clear any existing target role for standalone ATS
            if "target_role" in st.session_state.agent_state:
                st.session_state.agent_state["target_role"] = None
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


    if "show_resume_uploader" not in st.session_state:
        st.session_state.show_resume_uploader = False
    
    if "show_ats_uploader" not in st.session_state:
        st.session_state.show_ats_uploader = False

    if "skill_input_mode" not in st.session_state:
        st.session_state.skill_input_mode = False

    if "current_skill_step" not in st.session_state:
        st.session_state.current_skill_step = "enter_skill"

    if "temp_skill" not in st.session_state:
        st.session_state.temp_skill = ""
    # ============ END OF ADDITION ============

    # ✅ Chat input
    # ✅ Chat input section


user_input = st.chat_input("Type here...")
if user_input:
    # Store user message
    st.session_state.chat.append({"role": "user", "content": user_input})
    # =============================
    # Career Discovery Trigger
    # =============================
    if user_input.lower() in ["career discovery", "discover career", "career help"]:
        st.session_state.agent_state = create_initial_state()
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Great! Let’s figure out the best career path for you.\n\nWhat kind of work do you enjoy doing?"
        })
        st.rerun()

    # Check if user is selecting a career from suggestions
    suggested_careers = st.session_state.agent_state.get("suggested_careers", [])
    selected_from_suggestions = resolve_role(user_input, allowed_roles=suggested_careers) if suggested_careers else None
    if selected_from_suggestions:
        st.session_state.agent_state["target_role"] = selected_from_suggestions
        st.session_state.agent_state["step"] = "generate_roadmap"
        # Generate roadmap directly
        from utils.roadmap_generator import generate_roadmap_mermaid, generate_roadmap_markdown
        roadmap = generate_roadmap_mermaid(selected_from_suggestions)
        details = generate_roadmap_markdown(selected_from_suggestions)
        if roadmap:
            roadmap_msg = f"## 🗺️ Roadmap for {selected_from_suggestions}\n\n"
            roadmap_msg += f"{roadmap}\n\n"
            if details:
                roadmap_msg += f"{details}\n\n"
            roadmap_msg += "**Next Steps:**\n1. Follow the roadmap step by step\n2. Use SkillBridge to check your progress\n3. Build projects for each skill"
            st.session_state.chat.append({"role": "assistant", "content": roadmap_msg})
        else:
            st.session_state.chat.append({
                "role": "assistant", 
                "content": f"📚 **Learning Path for {selected_from_suggestions}:**\n\n1. Learn fundamentals\n2. Build projects\n3. Practice coding\n4. Get certifications"
            })
        st.session_state.chat.append({
            "role": "assistant",
            "content": "**Would you like to analyze your current skills with SkillBridge?** Type 'Yes' to continue."
        })
        st.rerun()
    
    # Check if user wants to continue to SkillBridge after roadmap
    if "yes" in user_input.lower() and st.session_state.agent_state.get("mode") == "roadmap":
        target_role = st.session_state.agent_state.get("target_role")
        if target_role:
            st.session_state.agent_state["mode"] = "skillbridge"
            st.session_state.agent_state["step"] = "skillbridge_start"
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"Great! Let's analyze your skills for **{target_role}**.\n\n**Do you have a resume?**"
            })
            st.rerun()
    # =============================
    # Career Discovery Mode Handler
    # =============================
    if st.session_state.agent_state.get("mode") == "career_discovery":

        reply, st.session_state.agent_state = run_career_discovery(
            user_input,
            st.session_state.agent_state
        )

        if reply:
            st.session_state.chat.append({
                "role": "assistant",
                "content": reply
            })

        # Stop here – do NOT let old agent logic run
        st.rerun()

    # Get response from enhanced agent (sync with session state)
    agent_response = get_agent_response(user_input, st.session_state.agent_state)
    
    if agent_response:
        response_text = agent_response.get("response", "")
        action = agent_response.get("action", "")
        next_question = agent_response.get("next_question", "")
        options = agent_response.get("options", [])
        
        # Add assistant response to chat
        if response_text:
            st.session_state.chat.append({"role": "assistant", "content": response_text})
        
        # Handle different actions
        if action == "upload_resume":
            # Set flag to show unified resume uploader in next render
            st.session_state.show_resume_uploader = True
            
        elif action == "generate_roadmap" or action == "show_roadmap":
            # Generate roadmap for target role
            target_role = st.session_state.agent_state.get("target_role")
            
            if not target_role:
                # Try to resolve from freeform user input (case-insensitive, minor variations).
                resolved = resolve_role(user_input)
                if resolved:
                    target_role = resolved
                    st.session_state.agent_state["target_role"] = resolved
            
            if target_role:
                # Import roadmap generator
                from utils.roadmap_generator import generate_roadmap_mermaid, generate_roadmap_markdown
                
                roadmap = generate_roadmap_mermaid(target_role)
                details = generate_roadmap_markdown(target_role)
                if roadmap:
                    roadmap_msg = f"## 🗺️ Roadmap for {target_role}\n\n"
                    roadmap_msg += f"{roadmap}\n\n"
                    if details:
                        roadmap_msg += f"{details}\n\n"
                    roadmap_msg += "**Next Steps:**\n"
                    roadmap_msg += "1. Follow the roadmap step by step\n"
                    roadmap_msg += "2. Use SkillBridge to check your progress\n"
                    roadmap_msg += "3. Build projects for each skill\n"
                    roadmap_msg += "4. Practice regularly and track your progress"
                    
                    st.session_state.chat.append({
                        "role": "assistant", 
                        "content": roadmap_msg
                    })
                else:
                    # Fallback if roadmap not available
                    st.session_state.chat.append({
                        "role": "assistant", 
                        "content": f"📚 **Learning Path for {target_role}:**\n\n1. Learn fundamentals\n2. Build projects\n3. Practice coding\n4. Get certifications\n5. Build portfolio"
                    })
                
                # Offer to continue to SkillBridge
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "**Would you like to analyze your current skills with SkillBridge?**\n\nThis will help you see how ready you are for this role and identify what skills you need to learn.\n\nType 'Yes' to continue to SkillBridge or 'No' to finish."
                })
            else:
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "Please select a target role first."
                })
            
        elif action == "suggest_careers":
            # Use LLM to suggest careers based on ALL collected data
            from utils.grokai_helper import recommend_careers
            
            # Get all user data from agent state
            interests = st.session_state.agent_state.get("interests")
            subjects = st.session_state.agent_state.get("strong_subjects")
            leisure = st.session_state.agent_state.get("leisure_activities")
            work_env = st.session_state.agent_state.get("work_environment")
            salary = st.session_state.agent_state.get("salary_expectations")
            industry = st.session_state.agent_state.get("industry_preference")
            considered = st.session_state.agent_state.get("considered_careers")
            
            careers_data = recommend_careers(
                subjects=subjects,
                interests=interests,
                leisure_activities=leisure,
                work_environment=work_env,
                salary_expectations=salary,
                industry_preference=industry,
                considered_careers=considered
            )
            
            if careers_data and "careers" in careers_data:
                career_text = "## 🎯 Suggested Career Options:\n\n"
                career_options = []
                for i, career in enumerate(careers_data["careers"], 1):
                    role_name = career.get('role', 'Role')
                    career_text += f"{i}. **{role_name}**\n"
                    career_text += f"   - {career.get('reason', 'Suitable based on your profile')}\n\n"
                    career_options.append(role_name)
                
                career_text += "\n**Choose one to view the roadmap!**"
                st.session_state.chat.append({"role": "assistant", "content": career_text})
                # Store career options for selection
                st.session_state.agent_state["suggested_careers"] = career_options
            else:
                st.session_state.chat.append({
                    "role": "assistant", 
                    "content": "Based on your profile, consider:\n1. **Data Analyst** - Good with numbers\n2. **Web Developer** - Creative + technical\n3. **Digital Marketer** - Communication skills"
                })
        
        elif action == "calculate_readiness":
            # Calculate readiness after skills are confirmed
            from utils.readiness_calculator import calculate_readiness
            
            target_role = st.session_state.agent_state.get("target_role")
            user_skills = st.session_state.agent_state.get("skills", {})
            
            if target_role and user_skills:
                readiness_result = calculate_readiness(user_skills, target_role)
                st.session_state.agent_state["readiness_result"] = readiness_result
                
                # Show readiness results
                readiness_msg = f"## 📊 Your Readiness for {target_role}\n\n"
                readiness_msg += f"**Readiness: {readiness_result['readiness_percentage']}%**\n\n"
                
                if readiness_result["matched_skills"]:
                    readiness_msg += f"**Matched Skills ({len(readiness_result['matched_skills'])}):**\n"
                    for skill_info in readiness_result["matched_skills"]:
                        readiness_msg += f"- {skill_info['skill']} ({skill_info['proficiency']})\n"
                    readiness_msg += "\n"
                
                if readiness_result["missing_skills"]:
                    readiness_msg += f"**Missing Skills ({len(readiness_result['missing_skills'])}):**\n"
                    for skill in readiness_result["missing_skills"]:
                        readiness_msg += f"- {skill}\n"
                    readiness_msg += "\n"
                
                st.session_state.chat.append({"role": "assistant", "content": readiness_msg})
                
                # Show learning resources for missing skills
                if readiness_result["missing_skills"]:
                    st.session_state.agent_state["step"] = "show_learning_resources"
                    st.rerun()
        
        elif action == "ask_skill":
            # Manual skill input mode
            st.session_state.skill_input_mode = True
            st.session_state.current_skill_step = "enter_skill"
        
        elif action == "ats_score":
            # Standalone ATS score flow
            st.session_state.show_ats_uploader = True
            st.session_state.agent_state["mode"] = "ats_score"
            # Clear any existing target role for standalone ATS
            if "target_role" in st.session_state.agent_state:
                st.session_state.agent_state["target_role"] = None
            
        # Update agent state with any updates
        updates = agent_response.get("update_state", {})
        for key, value in updates.items():
            if value is not None:
                st.session_state.agent_state[key] = value
        
        # Also sync back from agent to session state  <-- ADD THIS
        if hasattr(agent, 'state'):
            for key in ["mode", "current_step", "target_role", "interests", "strong_subjects", 
                       "leisure_activities", "work_environment", "salary_expectations", 
                       "industry_preference", "considered_careers", "suggested_careers"]:
                if key in agent.state and agent.state[key] is not None:
                    st.session_state.agent_state[key] = agent.state[key]
        
        # Show options if available
        if options and next_question:
            options_text = "\n".join([f"- {opt}" for opt in options])
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"{next_question}\n\n{options_text}"
            })
        
        # Show options if available
        if options and next_question:
            options_text = "\n".join([f"- {opt}" for opt in options])
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"{next_question}\n\n{options_text}"
            })
    
    st.rerun()

# ✅ Unified Resume Uploader with ATS Analysis (works for both SkillBridge and standalone ATS)
resume_uploader_active = st.session_state.get("show_resume_uploader", False) or st.session_state.get("show_ats_uploader", False)

if resume_uploader_active:
    st.markdown("---")
    
    # Determine if this is for SkillBridge or standalone ATS
    is_skillbridge = st.session_state.get("show_resume_uploader", False)
    is_ats_only = st.session_state.get("show_ats_uploader", False)
    
    if is_ats_only:
        st.markdown("### 📊 ATS Score Analyzer")
        st.markdown("Upload your resume to get an instant ATS compatibility score and improvement suggestions.")
    else:
        st.markdown("### 📄 Upload Your Resume")
        st.markdown("Upload your resume to analyze ATS compatibility and identify skill gaps.")
    
    # Get target role - either from agent state (SkillBridge) or from selectbox (standalone ATS)
    target_role_from_state = st.session_state.agent_state.get("target_role")
    
    # Show role selector if not already set (or for standalone ATS)
    if not target_role_from_state or is_ats_only:
        target_role_selected = st.selectbox(
            "**Select target job role for role-specific analysis (Optional):**",
            ["None", "Frontend Developer", "Backend Developer", "Full Stack Developer", 
             "Data Analyst", "Data Scientist", "DevOps Engineer", "Cybersecurity Analyst"],
            key="resume_target_role"
        )
        
        if target_role_selected == "None":
            target_role_selected = None
        else:
            # Store in agent state if it's SkillBridge flow
            if is_skillbridge:
                st.session_state.agent_state["target_role"] = target_role_selected
    else:
        target_role_selected = target_role_from_state
        st.info(f"**Target Role:** {target_role_selected}")
    
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, TXT, or Image)", 
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        key="unified_resume_uploader"
    )
    
    if uploaded_file:
        # Extract text from resume
        from utils.resume_parser import extract_text
        from utils.ats_detailed import get_detailed_ats_analysis
        from utils.resume_parser import extract_skills_from_text
        
        resume_text = extract_text(uploaded_file)
        resume_text = clean_text(resume_text)
        
        if resume_text and len(resume_text) > 50:
            # Show analysis progress
            with st.spinner("🔍 Analyzing your resume..."):
                import time
                time.sleep(1)  # Simulate analysis time
                
                # Calculate ATS score
                ats_result = get_detailed_ats_analysis(resume_text, target_role_selected)
                
                # Store resume text
                st.session_state.agent_state["resume_text"] = resume_text
                st.session_state.agent_state["has_resume"] = True

        if resume_text and len(resume_text) > 50:
            # Store resume text
            st.session_state.agent_state["resume_text"] = resume_text
            st.session_state.agent_state["has_resume"] = True
            
            # Calculate ATS score with detailed analysis
            from utils.ats_detailed import get_detailed_ats_analysis
            ats_result = get_detailed_ats_analysis(resume_text, target_role_selected)
            
            # Display comprehensive ATS results
            st.markdown("---")
            st.markdown("## 📊 ATS Score Analysis")
            st.success(f"✅ Resume uploaded and analyzed successfully!")
            
            # Score Display with enhanced formatting
            score_color = {
                "Excellent": "🟢",
                "Good": "🟡",
                "Fair": "🟠",
                "Needs Improvement": "🔴"
            }.get(ats_result['grade'], "⚪")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"### {ats_result['score']}/100")
                st.markdown(f"**{score_color} {ats_result['grade']}**")
            with col2:
                if target_role_selected:
                    st.info(f"**Target Role:**\n{target_role_selected}")
                else:
                    st.info("**No target role selected**\n(Select a role for better analysis)")
            with col3:
                word_count = len(resume_text.split())
                st.metric("Word Count", word_count)
            
            # Skills Analysis Section
            if target_role_selected and ats_result.get("missing_skills"):
                st.markdown("---")
                st.markdown("### 🔍 Skills Analysis")
                
                missing_skills = ats_result["missing_skills"]
                matched_skills = ats_result.get("matched_skills", [])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"#### ❌ Missing Skills ({len(missing_skills)})")
                    for skill in missing_skills:
                        st.write(f"• {skill}")
                    if missing_skills:
                        total_skills = len(matched_skills) + len(missing_skills)
                        match_percentage = (len(matched_skills) / total_skills) * 100 if total_skills > 0 else 0
                        st.progress(match_percentage / 100)
                        st.caption(f"Skill Match: {match_percentage:.1f}%")
                
                with col2:
                    if matched_skills:
                        st.markdown(f"#### ✅ Matched Skills ({len(matched_skills)})")
                        for skill in matched_skills:
                            st.write(f"• {skill}")
                    else:
                        st.info("No skills matched. Consider adding relevant keywords.")
            
            # Detected Skills from Resume
            detected_skills = extract_skills_from_text(resume_text)
            if detected_skills:
                st.markdown("---")
                st.markdown("### 🎯 Skills Detected in Resume")
                st.info(f"{', '.join(detected_skills)}")
                st.session_state.agent_state["detected_skills"] = detected_skills
            
            # Improvement Suggestions with expander
            if ats_result.get("suggestions"):
                st.markdown("---")
                with st.expander("💡 **Improvement Suggestions**", expanded=True):
                    for i, suggestion in enumerate(ats_result["suggestions"], 1):
                        st.markdown(f"**{i}.** {suggestion}")
            
            # Add comprehensive results to chat with better formatting
            score_msg = f"## 📊 ATS Score Analysis\n\n"
            score_msg += f"### **Overall Score: {ats_result['score']}/100** {ats_result.get('grade_emoji', '⚪')} {ats_result['grade']}\n\n"
            
            # Score breakdown (if detailed analysis is available)
            if 'section_analysis' in ats_result:
                score_msg += "### 📈 **Score Breakdown**\n"
                score_msg += f"- **Sections:** {ats_result['section_analysis']['score']}/{ats_result['section_analysis']['max_score']} points\n"
                score_msg += f"- **Formatting:** {ats_result['formatting_analysis']['score']}/{ats_result['formatting_analysis']['max_score']} points\n"
                score_msg += f"- **Keywords:** {ats_result['keyword_analysis']['score']}/{ats_result['keyword_analysis']['max_score']} points\n\n"
                
                # Strengths
                if ats_result.get('strengths'):
                    score_msg += "### ✅ **Strengths:**\n"
                    for strength in ats_result['strengths'][:3]:
                        score_msg += f"- {strength}\n"
                    score_msg += "\n"
                
                # Weaknesses
                if ats_result.get('weaknesses'):
                    score_msg += "### ⚠️ **Areas for Improvement:**\n"
                    for weakness in ats_result['weaknesses'][:3]:
                        score_msg += f"- {weakness}\n"
                    score_msg += "\n"
                
                # Section analysis
                if ats_result['section_analysis']['found']:
                    score_msg += "### 📋 **Sections Found:**\n"
                    for section in ats_result['section_analysis']['found'][:5]:
                        score_msg += f"✅ {section}\n"
                    score_msg += "\n"
                
                # Missing sections
                if ats_result['section_analysis']['missing']:
                    score_msg += "### ❌ **Missing Sections:**\n"
                    for section in ats_result['section_analysis']['missing'][:3]:
                        score_msg += f"- {section}\n"
                    score_msg += "\n"
            else:
                # Fallback to basic analysis
                score_msg += "### 📋 **Analysis Summary**\n"
                if target_role_selected:
                    score_msg += f"**Target Role:** {target_role_selected}\n\n"
            
            # Skills analysis (if target role specified)
            if target_role_selected:
                if ats_result.get("matched_skills"):
                    score_msg += f"### 🎯 **Matched Skills for {target_role_selected}:**\n"
                    for skill in ats_result.get("matched_skills", [])[:5]:
                        score_msg += f"- ✅ {skill}\n"
                    score_msg += "\n"
                
                if ats_result.get("missing_skills"):
                    score_msg += f"### ❌ **Missing Skills for {target_role_selected}:**\n"
                    for skill in ats_result.get("missing_skills", [])[:5]:
                        score_msg += f"- {skill}\n"
                    score_msg += "\n"
            
            # Detailed suggestions
            if ats_result.get('suggestions'):
                score_msg += "### 💡 **Actionable Suggestions:**\n"
                for i, sug in enumerate(ats_result['suggestions'][:5], 1):
                    score_msg += f"{i}. {sug}\n"
            
            # Metrics
            word_count = len(resume_text.split())
            score_msg += f"\n**📊 Metrics:**\n"
            score_msg += f"- **Word Count:** {word_count}\n"
            if 200 <= word_count <= 600:
                score_msg += f"- **Length:** Good (200-600 words)\n"
            elif word_count < 200:
                score_msg += f"- **Length:** Too short (aim for 200-600 words)\n"
            else:
                score_msg += f"- **Length:** Too long (aim for 200-600 words)\n"
            
            st.session_state.chat.append({
                "role": "assistant",
                "content": score_msg
            })
            
            # For SkillBridge flow, set up proficiency confirmation
            if is_skillbridge and detected_skills and target_role_selected:
                st.session_state.agent_state["step"] = "confirm_skills"
                st.session_state.agent_state["skills_to_confirm"] = detected_skills
                st.session_state.agent_state["target_role"] = target_role_selected
                
                # Add message to chat
                skill_list = ", ".join(detected_skills[:5])
                if len(detected_skills) > 5:
                    skill_list += f" and {len(detected_skills)-5} more"
                
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": f"**Resume analysis complete!**\n\nI detected these skills: {skill_list}\n\nPlease rate your proficiency for each skill (we'll ask one by one)."
                })
            
            # Reset uploader flags
            st.session_state.show_resume_uploader = False
            st.session_state.show_ats_uploader = False
            st.rerun()
    
    # Cancel button
    cancel_key = "cancel_unified_resume"
    if st.button("Cancel", key=cancel_key):
        st.session_state.show_resume_uploader = False
        st.session_state.show_ats_uploader = False
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Resume upload cancelled. How else can I help you?"
        })
        st.rerun()

# ✅ Proficiency Confirmation (for SkillBridge with resume)
if st.session_state.agent_state.get("step") == "confirm_skills":
    skills_to_confirm = st.session_state.agent_state.get("skills_to_confirm", [])
    confirmed_skills = st.session_state.agent_state.get("skills", {})
    
    if skills_to_confirm:
        st.markdown("---")
        st.markdown("### ✅ Confirm Your Skills")
        
        # Get next skill to confirm
        remaining_skills = [s for s in skills_to_confirm if s not in confirmed_skills]
        
        if remaining_skills:
            current_skill = remaining_skills[0]
            st.markdown(f"**Skill: {current_skill}**")
            
            proficiency = st.selectbox(
                f"Rate your proficiency in {current_skill}:",
                ["Beginner", "Intermediate", "Advanced"],
                key=f"proficiency_{current_skill}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm", key=f"confirm_{current_skill}"):
                    if "skills" not in st.session_state.agent_state:
                        st.session_state.agent_state["skills"] = {}
                    st.session_state.agent_state["skills"][current_skill] = proficiency
                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": f"✅ Confirmed: {current_skill} ({proficiency})"
                    })
                    # Check if more skills to confirm
                    remaining_skills = [s for s in skills_to_confirm if s not in st.session_state.agent_state.get("skills", {})]
                    if not remaining_skills:
                        # All skills confirmed, calculate readiness
                        st.session_state.agent_state["step"] = "calculate_readiness"
                    st.rerun()
            
            with col2:
                if st.button("Skip", key=f"skip_{current_skill}"):
                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": f"⏭️ Skipped: {current_skill}"
                    })
                    st.rerun()
        else:
            # All skills confirmed, calculate readiness
            st.success("✅ All skills confirmed!")
            st.session_state.agent_state["step"] = "calculate_readiness"
            st.rerun()
# ✅ Readiness Calculation (after skills confirmed)
if st.session_state.agent_state.get("step") == "calculate_readiness":
    target_role = st.session_state.agent_state.get("target_role")
    user_skills = st.session_state.agent_state.get("skills", {})
    
    if target_role and user_skills:
        from utils.readiness_calculator import calculate_readiness
        
        readiness_result = calculate_readiness(user_skills, target_role)
        st.session_state.agent_state["readiness_result"] = readiness_result
        
        st.markdown("---")
        st.markdown("## 📊 Your Readiness Analysis")
        
        # Display readiness percentage
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Readiness", f"{readiness_result['readiness_percentage']}%")
            st.progress(readiness_result['readiness_percentage'] / 100)
        
        with col2:
            st.info(f"**Target Role:** {target_role}")
            st.caption(f"{len(readiness_result['matched_skills'])}/{len(readiness_result['matched_skills']) + len(readiness_result['missing_skills'])} skills matched")
        
        # Show matched skills
        if readiness_result["matched_skills"]:
            with st.expander(f"✅ Matched Skills ({len(readiness_result['matched_skills'])})", expanded=True):
                for skill_info in readiness_result["matched_skills"]:
                    st.write(f"- **{skill_info['skill']}** ({skill_info['proficiency']})")
        
        # Show missing skills with resources
        if readiness_result["missing_skills"]:
            with st.expander(f"📚 Missing Skills & Learning Resources ({len(readiness_result['missing_skills'])})", expanded=True):
                for skill in readiness_result["missing_skills"]:
                    st.markdown(f"#### {skill}")
                    from utils.resource_retriever import get_resources
                    resources = get_resources(skill)
                    if resources:
                        if resources.get("course"):
                            st.markdown(f"📖 **Course:** [{resources['course'].split('/')[-1]}]({resources['course']})")
                        if resources.get("video"):
                            st.markdown(f"🎥 **Video:** [Watch Tutorial]({resources['video']})")
                        if resources.get("practice"):
                            st.markdown(f"💻 **Practice:** [Practice Here]({resources['practice']})")
                    else:
                        st.markdown(f"💡 Search online for '{skill} tutorial'")
                    st.markdown("---")
        
        # Add completion button
        if st.button("✅ Complete SkillBridge Analysis"):
            st.session_state.agent_state["step"] = "completed"
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"## ✅ SkillBridge Analysis Complete!\n\nYou are **{readiness_result['readiness_percentage']}%** ready for {target_role}.\n\nContinue learning the missing skills and check back later!"
            })
            st.rerun()




# ✅ Manual Skill Input (if triggered - for SkillBridge without resume)
if st.session_state.get("skill_input_mode", False):
    st.markdown("---")
    st.markdown("### 🧠 Manual Skill Input")
    
    current_step = st.session_state.get("current_skill_step", "enter_skill")
    
    if current_step == "enter_skill":
        skill = st.text_input("Enter a skill (e.g., Python, React, SQL):")
        
        if skill:
            st.session_state.temp_skill = skill
            st.session_state.current_skill_step = "enter_proficiency"
            st.rerun()
    
    elif current_step == "enter_proficiency":
        skill = st.session_state.get("temp_skill", "Unknown Skill")
        proficiency = st.selectbox(
            f"Proficiency level for {skill}:",
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Skill"):
                # Add to agent state
                if "skills" not in st.session_state.agent_state:
                    st.session_state.agent_state["skills"] = {}
                
                st.session_state.agent_state["skills"][skill] = proficiency
                
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": f"Added: {skill} ({proficiency})"
                })
                
                # Ask if more skills
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "Add another skill? (Yes/No) Or type 'Done' when finished."
                })
                
                # Reset to enter next skill
                st.session_state.current_skill_step = "enter_skill"
                st.session_state.temp_skill = ""
                st.rerun()
        
        with col2:
            if st.button("Done Adding Skills"):
                # Calculate readiness when done
                target_role = st.session_state.agent_state.get("target_role")
                user_skills = st.session_state.agent_state.get("skills", {})
                
                if target_role and user_skills:
                    from utils.readiness_calculator import calculate_readiness
                    readiness_result = calculate_readiness(user_skills, target_role)
                    st.session_state.agent_state["readiness_result"] = readiness_result
                    
                    # Display readiness (similar to above)
                    st.markdown("---")
                    st.markdown("## 📊 Your Readiness Analysis")
                    st.metric("Readiness", f"{readiness_result['readiness_percentage']}%")
                    
                    if readiness_result["missing_skills"]:
                        st.markdown("### ❌ Missing Skills & Learning Resources")
                        for skill in readiness_result["missing_skills"]:
                            st.write(f"**{skill}**")
                            from utils.resource_retriever import get_resources
                            resources = get_resources(skill)
                            if resources:
                                with st.expander(f"📚 Learning Resources for {skill}"):
                                    if resources.get("course"):
                                        st.write(f"📖 Course: {resources['course']}")
                                    if resources.get("video"):
                                        st.write(f"🎥 Video: {resources['video']}")
                                    if resources.get("practice"):
                                        st.write(f"💻 Practice: {resources['practice']}")
                
                st.session_state.skill_input_mode = False
                st.rerun()
            
            if st.button("Cancel"):
                st.session_state.skill_input_mode = False
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "Skill input cancelled."
                })
                st.rerun()