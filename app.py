import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# -----------------------------
st.set_page_config(page_title="SkillBridge AI", layout="centered")

# Add to your imports at the top
from utils.career_suggester import suggest_careers_llm

from roles_skills import ROLES_SKILLS
from roadmap_links import ROADMAP_LINKS
from utils.resume_parser import extract_text
from utils.ats_score import calculate_ats_score
from utils.resource_retriever import get_resources
from utils.agent import get_agent_response  # Using new agent
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
    q1, q2, q3 = st.columns(3)

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
    if "show_resume_uploader" not in st.session_state:
        st.session_state.show_resume_uploader = False

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
    
    # Get response from enhanced agent
    agent_response = get_agent_response(user_input)
    
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
            # Set flag to show resume uploader in next render
            st.session_state.show_resume_uploader = True
            
        elif action == "generate_roadmap":
            # Generate roadmap for target role
            target_role = st.session_state.agent_state.get("target_role", "Developer")
            
            # Import roadmap generator
            from utils.roadmap_generator import generate_roadmap_mermaid
            
            roadmap = generate_roadmap_mermaid(target_role)
            if roadmap:
                st.session_state.chat.append({
                    "role": "assistant", 
                    "content": f"## 🗺️ Roadmap for {target_role}\n\n{roadmap}\n\n**Next Steps:**\n1. Follow the roadmap step by step\n2. Use SkillBridge to check your progress\n3. Build projects for each skill"
                })
            else:
                st.session_state.chat.append({
                    "role": "assistant", 
                    "content": f"📚 **Learning Resources for {target_role}:**\n\n1. YouTube tutorials\n2. FreeCodeCamp\n3. Coursera/Udemy courses\n4. Build 2-3 projects\n5. Contribute to open source"
                })
            
            # Offer to continue to SkillBridge
            st.session_state.chat.append({
                "role": "assistant",
                "content": "Would you like to analyze your skills with SkillBridge? (Yes/No)"
            })
            
        elif action == "suggest_careers":
            # Use LLM to suggest careers based on collected data
            from utils.grokai_helper import recommend_careers
            
            # Get user data from agent state
            interests = st.session_state.agent_state.get("interests", "")
            subjects = st.session_state.agent_state.get("strong_subjects", "")
            
            if interests or subjects:
                careers_data = recommend_careers(subjects, interests)
                if careers_data and "careers" in careers_data:
                    career_text = "## 🎯 Suggested Career Options:\n\n"
                    for i, career in enumerate(careers_data["careers"], 1):
                        career_text += f"{i}. **{career.get('role', 'Role')}**\n"
                        career_text += f"   - {career.get('reason', 'Suitable based on your profile')}\n\n"
                    
                    career_text += "\n**Choose one to view the roadmap!**"
                    st.session_state.chat.append({"role": "assistant", "content": career_text})
                else:
                    st.session_state.chat.append({
                        "role": "assistant", 
                        "content": "Based on your profile, consider:\n1. **Data Analyst** - Good with numbers\n2. **Web Developer** - Creative + technical\n3. **Digital Marketer** - Communication skills"
                    })
        
        elif action == "ask_skill":
            # Manual skill input mode
            st.session_state.skill_input_mode = True
            st.session_state.current_skill_step = "enter_skill"
            
        # Update agent state with any updates
        updates = agent_response.get("update_state", {})
        for key, value in updates.items():
            if value is not None:
                st.session_state.agent_state[key] = value
        
        # Show options if available
        if options and next_question:
            options_text = "\n".join([f"- {opt}" for opt in options])
            st.session_state.chat.append({
                "role": "assistant",
                "content": f"{next_question}\n\n{options_text}"
            })
    
    st.rerun()

# ✅ Resume Uploader (if triggered)
if st.session_state.get("show_resume_uploader", False):
    st.markdown("### 📄 Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        key="resume_uploader"
    )
    
    if uploaded_file:
        # Extract text from resume
        from utils.resume_parser import extract_text
        resume_text = extract_text(uploaded_file)
        
        if resume_text and len(resume_text) > 50:
            st.session_state.agent_state["resume_text"] = resume_text
            st.session_state.agent_state["has_resume"] = True
            
            # Calculate ATS score
            target_role = st.session_state.agent_state.get("target_role")
            from utils.ats_score import calculate_ats_score
            
            ats_result = calculate_ats_score(resume_text, target_role)
            
            # Show results
            st.success(f"✅ Resume uploaded successfully!")
            st.metric("ATS Score", f"{ats_result['score']}/100", ats_result['grade'])
            
            # Show suggestions
            if ats_result.get("suggestions"):
                st.warning("**Improvement Suggestions:**")
                for suggestion in ats_result["suggestions"]:
                    st.write(f"- {suggestion}")
            
            # Extract skills
            from utils.resume_parser import extract_skills_from_text
            skills = extract_skills_from_text(resume_text)
            
            if skills:
                st.info(f"**Skills detected:** {', '.join(skills)}")
                st.session_state.agent_state["detected_skills"] = skills
                
                # Ask for proficiency
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": f"I detected these skills in your resume: {', '.join(skills)}\n\nPlease rate your proficiency for each (Beginner/Intermediate/Advanced):"
                })
            
            # Reset uploader flag
            st.session_state.show_resume_uploader = False
            st.rerun()
    
    # Cancel button
    if st.button("Cancel Upload"):
        st.session_state.show_resume_uploader = False
        st.session_state.chat.append({
            "role": "assistant",
            "content": "Resume upload cancelled. How else can I help you?"
        })
        st.rerun()

# ✅ Manual Skill Input (if triggered)
if st.session_state.get("skill_input_mode", False):
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
                    "content": "Add another skill? (Yes/No)"
                })
                
                # Reset
                st.session_state.skill_input_mode = False
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                st.session_state.skill_input_mode = False
                st.session_state.chat.append({
                    "role": "assistant",
                    "content": "Skill input cancelled."
                })
                st.rerun()


