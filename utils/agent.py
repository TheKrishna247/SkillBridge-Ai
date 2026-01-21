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
            "interests": [],
            "current_step": "start"
        }
        self.questions_asked = 0
        self.max_questions = 5
        
    def get_response(self, user_input):
        """Main function to get agent response"""
        
        # Clean user input
        user_input = user_input.lower().strip()
        
        # === START: Determine mode ===
        if self.state["mode"] is None:
            if "roadmap" in user_input:
                self.state["mode"] = "roadmap"
                self.state["current_step"] = "roadmap_start"
                return self._roadmap_response(user_input)
            elif "skillbridge" in user_input or "skill" in user_input:
                self.state["mode"] = "skillbridge"
                self.state["current_step"] = "skillbridge_start"
                return self._skillbridge_response(user_input)
            else:
                return {
                    "response": "Welcome! Please choose:\n1. **Roadmap** - Get career path\n2. **SkillBridge** - Analyze your skills\n\nType 'Roadmap' or 'SkillBridge' to begin.",
                    "action": "ask",
                    "options": ["Roadmap", "SkillBridge"]
                }
        
        # === Route based on mode ===
        if self.state["mode"] == "roadmap":
            return self._roadmap_response(user_input)
        else:
            return self._skillbridge_response(user_input)
    
    def _roadmap_response(self, user_input):
        """Handle roadmap flow"""
        
        # Step 1: Ask if user knows their job profile
        if self.state["current_step"] == "roadmap_start":
            self.state["current_step"] = "roadmap_choice"
            return {
                "response": "Great! Let's create your career roadmap.\n\n**Do you know exactly what job profile you want to become?**",
                "action": "ask",
                "options": ["Yes, I know my target job", "No, I'm not clear about career options"]
            }
        
        # Step 2: Handle choice
        elif self.state["current_step"] == "roadmap_choice":
            if "yes" in user_input.lower() or "know" in user_input.lower():
                self.state["roadmap_choice"] = "know_profile"
                self.state["current_step"] = "ask_role"
                return {
                    "response": "Perfect! **What is your target job role?**",
                    "action": "ask",
                    "options": ["Frontend Developer", "Backend Developer", "Data Analyst", 
                               "Data Scientist", "DevOps Engineer", "Cybersecurity Analyst"]
                }
            else:
                self.state["roadmap_choice"] = "not_clear"
                self.state["current_step"] = "ask_interests"
                return {
                    "response": "No problem! Let me help you discover suitable careers.\n\n**What are your main interests?** (You can type multiple)",
                    "action": "ask",
                    "options": ["Web Development", "Data Analysis", "AI/ML", 
                               "Cybersecurity", "Cloud Computing", "Mobile App Development"]
                }
        
        # Step 3: If knows role, get it
        elif self.state["current_step"] == "ask_role":
            self.state["target_role"] = user_input
            self.state["current_step"] = "generate_roadmap"
            return {
                "response": f"Excellent! Generating roadmap for **{user_input}**...",
                "action": "generate_roadmap",
                "options": []
            }
        
        # Step 4: If not clear, ask more questions
        elif self.state["current_step"] == "ask_interests":
            self.state["interests"] = user_input
            self.state["current_step"] = "ask_subjects"
            return {
                "response": f"Thanks! Interests: {user_input}\n\n**What are your strong subjects?**",
                "action": "ask",
                "options": ["Mathematics", "Science", "Computer Science", "Statistics", 
                           "Business", "Arts/Design", "Languages"]
            }
        
        elif self.state["current_step"] == "ask_subjects":
            self.state["current_step"] = "suggest_careers"
            return {
                "response": f"Based on your interests and subjects, I'll suggest suitable careers...",
                "action": "suggest_careers",
                "options": []
            }
        
        elif self.state["current_step"] == "generate_roadmap":
            return {
                "response": f"✅ **Roadmap for {self.state['target_role']} generated!**",
                "action": "show_roadmap",
                "options": []
            }
        
        elif self.state["current_step"] == "suggest_careers":
            return {
                "response": "🎯 **Suggested Career Options:**\n1. Frontend Developer\n2. Full Stack Developer\n3. Web Developer\n\nChoose one to view roadmap!",
                "action": "show_career_options",
                "options": ["Frontend Developer", "Full Stack Developer", "Web Developer"]
            }
    
    def _skillbridge_response(self, user_input):
        """Handle skillbridge flow"""
        
        # Step 1: Ask for target role
        if self.state["current_step"] == "skillbridge_start":
            self.state["current_step"] = "ask_target_role"
            return {
                "response": "Great! Let's bridge your skill gap.\n\n**What job profile do you want to target?**",
                "action": "ask",
                "options": ["Frontend Developer", "Backend Developer", "Data Analyst", 
                           "Data Scientist", "DevOps Engineer", "Cybersecurity Analyst"]
            }
        
        # Step 2: Ask if has resume
        elif self.state["current_step"] == "ask_target_role":
            self.state["target_role"] = user_input
            self.state["current_step"] = "ask_resume"
            return {
                "response": f"Target role set: **{user_input}**\n\n**Do you have a resume?**",
                "action": "ask",
                "options": ["Yes, I have a resume", "No, I don't have a resume"]
            }
        
        # Step 3: Handle resume choice
        elif self.state["current_step"] == "ask_resume":
            if "yes" in user_input.lower():
                self.state["has_resume"] = True
                self.state["current_step"] = "upload_resume"
                return {
                    "response": "Please upload your resume.",
                    "action": "upload_resume",
                    "options": []
                }
            else:
                self.state["has_resume"] = False
                self.state["current_step"] = "manual_skills"
                return {
                    "response": "No problem! Let's manually input your skills.",
                    "action": "ask_skill",
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
            "interests": [],
            "current_step": "start"
        }

# Create global instance
agent = SkillBridgeAgent()

def get_agent_response(user_input):
    """Wrapper function for compatibility"""
    return agent.get_response(user_input)