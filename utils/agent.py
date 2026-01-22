import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SkillBridgeAgent:
    def __init__(self):
        self.state = {
            "mode": None,  # "roadmap" or "skillbridge"
            "roadmap_choice": None,  # "know_profile" or "not_clear"
            "has_resume": None,
            "target_role": None,
            "interests": None,
            "strong_subjects": None,
            "leisure_activities": None,
            "work_environment": None,
            "salary_expectations": None,
            "industry_preference": None,
            "considered_careers": None,
            "current_step": "start",
            "question_count": 0
        }
        
    def get_response(self, user_input, session_state=None):
        """Main function to get agent response"""
        
        # Sync with session state if provided
        if session_state:
            # Always sync mode and step if they exist in session state (even if None/empty)
            if "mode" in session_state:
                self.state["mode"] = session_state["mode"]
            if "step" in session_state:
                self.state["current_step"] = session_state["step"]
            if "target_role" in session_state:
                self.state["target_role"] = session_state.get("target_role")
            if "roadmap_choice" in session_state:
                self.state["roadmap_choice"] = session_state.get("roadmap_choice")
            if "interests" in session_state:
                self.state["interests"] = session_state.get("interests")
            if "strong_subjects" in session_state:
                self.state["strong_subjects"] = session_state.get("strong_subjects")
            if "leisure_activities" in session_state:
                self.state["leisure_activities"] = session_state.get("leisure_activities")
            if "work_environment" in session_state:
                self.state["work_environment"] = session_state.get("work_environment")
            if "salary_expectations" in session_state:
                self.state["salary_expectations"] = session_state.get("salary_expectations")
            if "industry_preference" in session_state:
                self.state["industry_preference"] = session_state.get("industry_preference")
            if "considered_careers" in session_state:
                self.state["considered_careers"] = session_state.get("considered_careers")
        
        # Clean user input
        user_input_clean = user_input.lower().strip()
        
        # === START: Determine mode ===
        if self.state["mode"] is None:
            if "roadmap" in user_input_clean:
                self.state["mode"] = "roadmap"
                self.state["current_step"] = "roadmap_start"
                return self._roadmap_response(user_input)
            elif "skillbridge" in user_input_clean or "skill" in user_input_clean:
                self.state["mode"] = "skillbridge"
                self.state["current_step"] = "skillbridge_start"
                return self._skillbridge_response(user_input)
            elif "ats" in user_input_clean or "score" in user_input_clean or "resume" in user_input_clean or "analyzer" in user_input_clean:
                self.state["mode"] = "ats_score"
                self.state["current_step"] = "ats_upload"
                return {
                    "response": "## 📊 ATS Score Analyzer\n\nI'll analyze your resume for ATS compatibility. **Please upload your resume using the uploader below.**\n\nI'll check:\n- Formatting & structure\n- Keywords & skills\n- Section completeness\n- Length optimization\n- Contact information\n\nUpload your resume (PDF, DOCX, TXT, or Image) to get started!",
                    "action": "ats_score",
                    "update_state": {"mode": "ats_score", "step": "ats_upload"}
                }
            else:
                return {
                    "response": "Welcome! Please choose:\n1. **Roadmap** - Get career path\n2. **SkillBridge** - Analyze your skills\n3. **ATS Score** - Check resume ATS compatibility\n\nType 'Roadmap', 'SkillBridge', or 'ATS Score' to begin.",
                    "action": "ask",
                    "options": ["Roadmap", "SkillBridge", "ATS Score"]
                }
        
        # === Route based on mode ===
        if self.state["mode"] == "roadmap":
            response = self._roadmap_response(user_input)
            # Ensure we always return a valid response
            if not response or not response.get("response"):
                # Fallback response
                if self.state["current_step"] == "roadmap_start" or not self.state.get("current_step"):
                    self.state["current_step"] = "roadmap_choice"
                    return {
                        "response": "Great! Let's create your career roadmap.\n\n**Do you know exactly what job profile you want to become?**",
                        "action": "ask",
                        "options": ["Yes, I know my target job", "No, I'm not clear about career options"],
                        "update_state": {"step": "roadmap_choice"}
                    }
            return response
        elif self.state["mode"] == "ats_score":
            return {
                "response": "Please upload your resume using the uploader above to get your ATS score.",
                "action": "ats_score",
                "options": []
            }
        else:
            return self._skillbridge_response(user_input)
    
    def _roadmap_response(self, user_input):
        """Handle roadmap flow according to architecture"""
        
        # Step 1: Ask if user knows their job profile
        if self.state["current_step"] == "roadmap_start":
            self.state["current_step"] = "roadmap_choice"
            return {
                "response": "Great! Let's create your career roadmap.\n\n**Do you know exactly what job profile you want to become?**",
                "action": "ask",
                "options": ["Yes, I know my target job", "No, I'm not clear about career options"],
                "update_state": {"step": "roadmap_choice"}
            }
        
        # Step 2: Handle choice
        elif self.state["current_step"] == "roadmap_choice":
            if "yes" in user_input.lower() or "know" in user_input.lower():
                self.state["roadmap_choice"] = "know_profile"
                self.state["current_step"] = "ask_role"
                return {
                    "response": "Perfect! **What is your target job role?**",
                    "action": "ask",
                    "options": ["Frontend Developer", "Backend Developer", "Full Stack Developer",
                               "Data Analyst", "Data Scientist", "DevOps Engineer", "Cybersecurity Analyst"],
                    "update_state": {"step": "ask_role", "roadmap_choice": "know_profile"}
                }
            else:
                self.state["roadmap_choice"] = "not_clear"
                self.state["current_step"] = "ask_interests"
                self.state["question_count"] = 1
                return {
                    "response": "No problem! Let me help you discover suitable careers.\n\n**Question 1/7: What are your main interests?** (e.g., Web Development, Data Analysis, AI/ML)",
                    "action": "ask",
                    "options": ["Web Development", "Data Analysis", "AI/ML", "Cybersecurity", "Cloud Computing"],
                    "update_state": {"step": "ask_interests", "roadmap_choice": "not_clear", "question_count": 1}
                }
        
        # Step 3: If knows role, get it and generate roadmap
        elif self.state["current_step"] == "ask_role":
            self.state["target_role"] = user_input
            self.state["current_step"] = "generate_roadmap"
            return {
                "response": f"Excellent! Generating roadmap for **{user_input}**...",
                "action": "generate_roadmap",
                "options": [],
                "update_state": {"target_role": user_input, "step": "generate_roadmap"}
            }
        
        # Step 4-10: If not clear, ask all 7 questions
        elif self.state["current_step"] == "ask_interests":
            self.state["interests"] = user_input
            self.state["current_step"] = "ask_subjects"
            self.state["question_count"] = 2
            return {
                "response": f"Thanks! Interests: {user_input}\n\n**Question 2/7: What are your strong subjects?** (e.g., Mathematics, Science, Computer Science)",
                "action": "ask",
                "options": ["Mathematics", "Science", "Computer Science", "Statistics", "Business"],
                "update_state": {"interests": user_input, "step": "ask_subjects", "question_count": 2}
            }
        
        elif self.state["current_step"] == "ask_subjects":
            self.state["strong_subjects"] = user_input
            self.state["current_step"] = "ask_leisure"
            self.state["question_count"] = 3
            return {
                "response": f"Got it! Strong subjects: {user_input}\n\n**Question 3/7: What do you enjoy doing in your leisure time?** (e.g., Coding, Reading, Gaming, Sports)",
                "action": "ask",
                "update_state": {"strong_subjects": user_input, "step": "ask_leisure", "question_count": 3}
            }
        
        elif self.state["current_step"] == "ask_leisure":
            self.state["leisure_activities"] = user_input
            self.state["current_step"] = "ask_work_env"
            self.state["question_count"] = 4
            return {
                "response": f"Nice! Leisure: {user_input}\n\n**Question 4/7: What is your preferred work environment?**",
                "action": "ask",
                "options": ["Remote", "Office", "Hybrid"],
                "update_state": {"leisure_activities": user_input, "step": "ask_work_env", "question_count": 4}
            }
        
        elif self.state["current_step"] == "ask_work_env":
            self.state["work_environment"] = user_input
            self.state["current_step"] = "ask_salary"
            self.state["question_count"] = 5
            return {
                "response": f"Understood! Work environment: {user_input}\n\n**Question 5/7: What are your salary expectations?** (e.g., Entry level, Mid level, Senior level)",
                "action": "ask",
                "options": ["Entry level ($40k-$60k)", "Mid level ($60k-$100k)", "Senior level ($100k+)"],
                "update_state": {"work_environment": user_input, "step": "ask_salary", "question_count": 5}
            }
        
        elif self.state["current_step"] == "ask_salary":
            self.state["salary_expectations"] = user_input
            self.state["current_step"] = "ask_industry"
            self.state["question_count"] = 6
            return {
                "response": f"Noted! Salary: {user_input}\n\n**Question 6/7: Do you have any specific industry preference?** (e.g., Tech, Finance, Healthcare, None)",
                "action": "ask",
                "options": ["Tech", "Finance", "Healthcare", "E-commerce", "None"],
                "update_state": {"salary_expectations": user_input, "step": "ask_industry", "question_count": 6}
            }
        
        elif self.state["current_step"] == "ask_industry":
            self.state["industry_preference"] = user_input
            self.state["current_step"] = "ask_considered"
            self.state["question_count"] = 7
            return {
                "response": f"Got it! Industry: {user_input}\n\n**Question 7/7: Have you considered any specific careers before?** (Type 'None' if not)",
                "action": "ask",
                "update_state": {"industry_preference": user_input, "step": "ask_considered", "question_count": 7}
            }
        
        elif self.state["current_step"] == "ask_considered":
            self.state["considered_careers"] = user_input
            self.state["current_step"] = "suggest_careers"
            return {
                "response": "Perfect! Analyzing your responses to suggest the best career options for you...",
                "action": "suggest_careers",
                "options": [],
                "update_state": {"considered_careers": user_input, "step": "suggest_careers"}
            }
        
        elif self.state["current_step"] == "generate_roadmap":
            return {
                "response": f"✅ **Roadmap for {self.state['target_role']} generated!**",
                "action": "show_roadmap",
                "options": []
            }
        
        elif self.state["current_step"] == "suggest_careers":
            # Use LLM to get career suggestions
            from utils.grokai_helper import recommend_careers
            
            careers_data = recommend_careers(
                subjects=self.state.get("strong_subjects"),
                interests=self.state.get("interests"),
                leisure_activities=self.state.get("leisure_activities"),
                work_environment=self.state.get("work_environment"),
                salary_expectations=self.state.get("salary_expectations"),
                industry_preference=self.state.get("industry_preference"),
                considered_careers=self.state.get("considered_careers")
            )
            
            if careers_data and "careers" in careers_data:
                # Store suggested careers for selection
                career_options = [c["role"] for c in careers_data["careers"]]
                career_text = "🎯 **Suggested Career Options:**\n\n"
                for i, career in enumerate(careers_data["careers"], 1):
                    career_text += f"{i}. **{career['role']}**\n"
                    career_text += f"   - {career['reason']}\n\n"
                career_text += "\n**Choose one to view the roadmap!**"
                
                # Update state and return response
                self.state["suggested_careers"] = career_options
                self.state["current_step"] = "select_career"
                return {
                    "response": career_text,
                    "action": "suggest_careers",
                    "options": career_options,
                    "update_state": {"step": "select_career", "suggested_careers": career_options}
                }
            else:
                # Fallback
                career_options = ["Frontend Developer", "Data Analyst", "Cybersecurity Analyst"]
                self.state["suggested_careers"] = career_options
                self.state["current_step"] = "select_career"
                return {
                    "response": "🎯 **Suggested Career Options:**\n\n1. **Frontend Developer**\n2. **Data Analyst**\n3. **Cybersecurity Analyst**\n\n**Choose one to view the roadmap!**",
                    "action": "suggest_careers",
                    "options": career_options,
                    "update_state": {"step": "select_career", "suggested_careers": career_options}
                }

        elif self.state["current_step"] == "select_career":
            # User selected a career
            if user_input in self.state.get("suggested_careers", []):
                self.state["target_role"] = user_input
                self.state["current_step"] = "generate_roadmap"
                return {
                    "response": f"✅ Selected: **{user_input}**\n\nGenerating roadmap...",
                    "action": "generate_roadmap",
                    "options": [],
                    "update_state": {"target_role": user_input, "step": "generate_roadmap"}
                }
            else:
                # User typed something else
                return {
                    "response": "Please select one of the suggested careers to continue.",
                    "action": "ask",
                    "options": self.state.get("suggested_careers", []),
                    "update_state": {"step": "select_career"}
                }
        
        # Fallback: if step is not recognized, start from beginning
        self.state["current_step"] = "roadmap_choice"
        return {
            "response": "Great! Let's create your career roadmap.\n\n**Do you know exactly what job profile you want to become?**",
            "action": "ask",
            "options": ["Yes, I know my target job", "No, I'm not clear about career options"],
            "update_state": {"step": "roadmap_choice"}
        }
    
    def _skillbridge_response(self, user_input):
        """Handle skillbridge flow according to architecture"""
        
        # Step 1: Ask for target role
        if self.state["current_step"] == "skillbridge_start":
            self.state["current_step"] = "ask_target_role"
            return {
                "response": "Great! Let's bridge your skill gap.\n\n**What job profile do you want to target?**",
                "action": "ask",
                "options": ["Frontend Developer", "Backend Developer", "Full Stack Developer",
                           "Data Analyst", "Data Scientist", "DevOps Engineer", "Cybersecurity Analyst"],
                "update_state": {"step": "ask_target_role"}
            }
        
        # Step 2: Ask if has resume
        elif self.state["current_step"] == "ask_target_role":
            self.state["target_role"] = user_input
            self.state["current_step"] = "ask_resume"
            return {
                "response": f"Target role set: **{user_input}**\n\n**Do you have a resume?**",
                "action": "ask",
                "options": ["Yes, I have a resume", "No, I don't have a resume"],
                "update_state": {"target_role": user_input, "step": "ask_resume"}
            }
        
        # Step 3: Handle resume choice
        elif self.state["current_step"] == "ask_resume":
            if "yes" in user_input.lower():
                self.state["has_resume"] = True
                self.state["current_step"] = "upload_resume"
                return {
                    "response": "Perfect! Please upload your resume using the uploader above.",
                    "action": "upload_resume",
                    "options": [],
                    "update_state": {"has_resume": True, "step": "upload_resume"}
                }
            else:
                self.state["has_resume"] = False
                self.state["current_step"] = "manual_skills"
                return {
                    "response": "No problem! Let's manually input your skills.\n\n**Enter your first skill:** (e.g., Python, React, SQL)",
                    "action": "ask_skill",
                    "options": [],
                    "update_state": {"has_resume": False, "step": "manual_skills"}
                }
        
        # Step 4: After resume upload, confirm skills (handled in app.py)
        elif self.state["current_step"] == "confirm_skills":
            # This will be handled in app.py after proficiency confirmation
            self.state["current_step"] = "calculate_readiness"
            return {
                "response": "Calculating your readiness for the target role...",
                "action": "calculate_readiness",
                "options": []
            }
        
        # Other steps...
        return {
            "response": "Processing your SkillBridge request...",
            "action": "continue",
            "options": []
        }
    
    def reset(self):
        """Reset agent state"""
        self.state = {
            "mode": None,
            "roadmap_choice": None,
            "has_resume": None,
            "target_role": None,
            "interests": None,
            "strong_subjects": None,
            "leisure_activities": None,
            "work_environment": None,
            "salary_expectations": None,
            "industry_preference": None,
            "considered_careers": None,
            "current_step": "start",
            "question_count": 0
        }

# Create global instance
agent = SkillBridgeAgent()

def get_agent_response(user_input, session_state=None):
    """Wrapper function for compatibility"""
    return agent.get_response(user_input, session_state)
