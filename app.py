import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq
import base64
from typing import Dict, List, Optional
import re

# Page Configuration
st.set_page_config(
    page_title="AroMi AI - Health & Wellness Coach",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #50C878;
        --accent-color: #FF6B6B;
        --background-dark: #1E1E2E;
        --text-light: #E0E0E0;
    }
    
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #E0E0E0;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Chat Messages */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #50C878 0%, #3CB371 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1E1E2E 0%, #2D2D44 100%);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Progress Indicator */
    .progress-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        text-align: center;
        color: #666;
        line-height: 1.6;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Success/Info/Warning Messages */
    .success-box {
        background: linear-gradient(135deg, #50C878 0%, #3CB371 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq Client
def initialize_groq_client(api_key: str) -> Optional[Groq]:
    """Initialize Groq client with API key"""
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {str(e)}")
        return None

# Session State Initialization
def init_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'age': 0,
            'weight': 0,
            'height': 0,
            'fitness_level': 'Beginner',
            'goals': [],
            'health_conditions': [],
            'dietary_preferences': []
        }
    
    if 'workout_plan' not in st.session_state:
        st.session_state.workout_plan = None
    
    if 'nutrition_plan' not in st.session_state:
        st.session_state.nutrition_plan = None
    
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = {
            'workouts_completed': 0,
            'calories_tracked': 0,
            'weight_progress': [],
            'streak_days': 0
        }

# AI Chat Function
def chat_with_ai(client: Groq, message: str, context: str = "") -> str:
    """Generate AI response using Groq LLM"""
    try:
        system_prompt = f"""You are AroMi, an expert AI Health & Wellness Coach. You provide:
        - Personalized fitness and workout guidance
        - Nutrition and meal planning advice
        - Motivational support and progress tracking
        - Health condition-aware recommendations
        
        User Context: {context}
        
        Be empathetic, professional, and adaptive to user needs. Provide actionable advice."""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Language Translation Function
def translate_text(client: Groq, text: str, target_language: str) -> str:
    """Translate text to target language using Groq LLM"""
    try:
        prompt = f"""Translate the following text to {target_language}. 
        Provide ONLY the translation, no explanations:
        
        {text}"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Translation error: {str(e)}"

# Image Analysis Function
def analyze_image(client: Groq, image_data: str, analysis_type: str) -> str:
    """Analyze image using Groq Vision capabilities"""
    try:
        if analysis_type == "Food Recognition":
            prompt = """Analyze this food image and provide:
            1. Food items identified
            2. Estimated calories
            3. Macronutrient breakdown (protein, carbs, fats)
            4. Nutritional assessment
            5. Healthier alternatives if applicable"""
        
        elif analysis_type == "Workout Form":
            prompt = """Analyze this workout/exercise image and provide:
            1. Exercise identified
            2. Form assessment
            3. Common mistakes to avoid
            4. Suggestions for improvement
            5. Safety tips"""
        
        else:  # General Health
            prompt = """Analyze this health-related image and provide relevant insights."""
        
        # Note: Groq's llama-3.3-70b-versatile doesn't support vision
        # This is a placeholder for when vision models are available
        return """Image analysis feature requires a vision-capable model. 
        Currently, llama-3.3-70b-versatile doesn't support image inputs.
        
        To analyze images, you would need to:
        1. Use a vision-capable model like GPT-4 Vision or similar
        2. Or describe the image content, and I can provide guidance based on your description.
        
        Please describe what you see in the image, and I'll help you with the analysis!"""
    
    except Exception as e:
        return f"Image analysis error: {str(e)}"

# Generate Workout Plan
def generate_workout_plan(client: Groq, user_profile: Dict) -> str:
    """Generate personalized workout plan"""
    try:
        prompt = f"""Create a personalized weekly workout plan for:
        - Age: {user_profile['age']}
        - Fitness Level: {user_profile['fitness_level']}
        - Goals: {', '.join(user_profile['goals']) if user_profile['goals'] else 'General Fitness'}
        - Health Conditions: {', '.join(user_profile['health_conditions']) if user_profile['health_conditions'] else 'None'}
        
        Provide a detailed 7-day workout plan with:
        - Daily exercises
        - Sets and reps
        - Duration
        - Rest periods
        - Progression tips"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"

# Generate Nutrition Plan
def generate_nutrition_plan(client: Groq, user_profile: Dict) -> str:
    """Generate personalized nutrition plan"""
    try:
        prompt = f"""Create a personalized nutrition plan for:
        - Age: {user_profile['age']}
        - Weight: {user_profile['weight']} kg
        - Height: {user_profile['height']} cm
        - Goals: {', '.join(user_profile['goals']) if user_profile['goals'] else 'General Health'}
        - Dietary Preferences: {', '.join(user_profile['dietary_preferences']) if user_profile['dietary_preferences'] else 'None'}
        
        Provide:
        - Daily calorie target
        - Macronutrient breakdown
        - Meal timing suggestions
        - Sample meal plan for a day
        - Hydration guidelines"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating nutrition plan: {str(e)}"

# Main Application
def main():
    """Main application function"""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏃‍♂️ AroMi AI Agent</h1>
        <p>Your Adaptive Health & Wellness Coach</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key Input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key to enable AI features"
        )
        
        if api_key:
            st.success("✅ API Key configured!")
            client = initialize_groq_client(api_key)
        else:
            st.warning("⚠️ Please enter your Groq API key")
            client = None
        
        st.markdown("---")
        
        # User Profile
        st.markdown("### 👤 User Profile")
        
        with st.expander("Edit Profile", expanded=False):
            st.session_state.user_profile['name'] = st.text_input(
                "Name", 
                value=st.session_state.user_profile['name']
            )
            
            st.session_state.user_profile['age'] = st.number_input(
                "Age", 
                min_value=0, 
                max_value=120, 
                value=st.session_state.user_profile['age'] if st.session_state.user_profile['age'] > 0 else 25
            )
            
            st.session_state.user_profile['weight'] = st.number_input(
                "Weight (kg)", 
                min_value=0.0, 
                max_value=300.0, 
                value=float(st.session_state.user_profile['weight']) if st.session_state.user_profile['weight'] > 0 else 70.0
            )
            
            st.session_state.user_profile['height'] = st.number_input(
                "Height (cm)", 
                min_value=0.0, 
                max_value=250.0, 
                value=float(st.session_state.user_profile['height']) if st.session_state.user_profile['height'] > 0 else 170.0
            )
            
            st.session_state.user_profile['fitness_level'] = st.selectbox(
                "Fitness Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.user_profile['fitness_level'])
            )
            
            goals_options = ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "General Fitness"]
            st.session_state.user_profile['goals'] = st.multiselect(
                "Fitness Goals",
                goals_options,
                default=st.session_state.user_profile['goals']
            )
            
            dietary_options = ["Vegetarian", "Vegan", "Keto", "Paleo", "No Restrictions"]
            st.session_state.user_profile['dietary_preferences'] = st.multiselect(
                "Dietary Preferences",
                dietary_options,
                default=st.session_state.user_profile['dietary_preferences']
            )
            
            health_conditions = st.text_area(
                "Health Conditions (optional)",
                placeholder="e.g., diabetes, hypertension"
            )
            if health_conditions:
                st.session_state.user_profile['health_conditions'] = [
                    cond.strip() for cond in health_conditions.split(',')
                ]
        
        # Display current BMI
        if st.session_state.user_profile['weight'] > 0 and st.session_state.user_profile['height'] > 0:
            height_m = st.session_state.user_profile['height'] / 100
            bmi = st.session_state.user_profile['weight'] / (height_m ** 2)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Current BMI</div>
                <div class="metric-value">{bmi:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Progress Stats
        st.markdown("### 📊 Progress Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Workouts",
                st.session_state.progress_data['workouts_completed']
            )
        
        with col2:
            st.metric(
                "Streak",
                f"{st.session_state.progress_data['streak_days']} days"
            )
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 AI Chat",
        "🏋️ Workout Plans",
        "🥗 Nutrition",
        "🌍 Translation",
        "📸 Image Analysis"
    ])
    
    # Tab 1: AI Chat
    with tab1:
        st.markdown("### 💬 Chat with AroMi")
        
        if not client:
            st.warning("⚠️ Please configure your Groq API key in the sidebar to use the chat feature.")
        else:
            # Chat container
            chat_container = st.container()
            
            with chat_container:
                # Display chat history
                for message in st.session_state.chat_history:
                    if message['role'] == 'user':
                        st.markdown(f"""
                        <div class="user-message">
                            <strong>You:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="assistant-message">
                            <strong>AroMi:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Chat input
            user_input = st.text_input(
                "Type your message...",
                key="chat_input",
                placeholder="Ask me about workouts, nutrition, or your health goals..."
            )
            
            col1, col2 = st.columns([6, 1])
            
            with col1:
                if st.button("Send Message", use_container_width=True):
                    if user_input:
                        # Add user message to history
                        st.session_state.chat_history.append({
                            'role': 'user',
                            'content': user_input
                        })
                        
                        # Generate context from user profile
                        context = f"""User Profile:
                        - Name: {st.session_state.user_profile['name']}
                        - Age: {st.session_state.user_profile['age']}
                        - Fitness Level: {st.session_state.user_profile['fitness_level']}
                        - Goals: {', '.join(st.session_state.user_profile['goals'])}
                        """
                        
                        # Get AI response
                        with st.spinner("AroMi is thinking..."):
                            response = chat_with_ai(client, user_input, context)
                        
                        # Add assistant response to history
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': response
                        })
                        
                        st.rerun()
            
            with col2:
                if st.button("Clear", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
    
    # Tab 2: Workout Plans
    with tab2:
        st.markdown("### 🏋️ Personalized Workout Plans")
        
        if not client:
            st.warning("⚠️ Please configure your Groq API key in the sidebar.")
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("""
                <div class="info-box">
                    <strong>🎯 Generate Your Custom Workout Plan</strong><br>
                    Based on your profile, fitness level, and goals, AroMi will create a personalized workout routine.
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Generate Plan", use_container_width=True):
                    if st.session_state.user_profile['age'] == 0:
                        st.error("⚠️ Please complete your profile in the sidebar first!")
                    else:
                        with st.spinner("Creating your personalized workout plan..."):
                            plan = generate_workout_plan(client, st.session_state.user_profile)
                            st.session_state.workout_plan = plan
            
            # Display workout plan
            if st.session_state.workout_plan:
                st.markdown("---")
                st.markdown("#### 📋 Your Workout Plan")
                st.markdown(st.session_state.workout_plan)
                
                # Log workout button
                if st.button("✅ Mark Today's Workout Complete"):
                    st.session_state.progress_data['workouts_completed'] += 1
                    st.session_state.progress_data['streak_days'] += 1
                    st.success("🎉 Great job! Workout logged successfully!")
                    st.rerun()
    
    # Tab 3: Nutrition
    with tab3:
        st.markdown("### 🥗 Personalized Nutrition Guidance")
        
        if not client:
            st.warning("⚠️ Please configure your Groq API key in the sidebar.")
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("""
                <div class="info-box">
                    <strong>🍎 Generate Your Nutrition Plan</strong><br>
                    Get a customized meal plan based on your goals, preferences, and dietary restrictions.
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Generate Nutrition Plan", use_container_width=True):
                    if st.session_state.user_profile['age'] == 0:
                        st.error("⚠️ Please complete your profile in the sidebar first!")
                    else:
                        with st.spinner("Creating your personalized nutrition plan..."):
                            plan = generate_nutrition_plan(client, st.session_state.user_profile)
                            st.session_state.nutrition_plan = plan
            
            # Display nutrition plan
            if st.session_state.nutrition_plan:
                st.markdown("---")
                st.markdown("#### 📋 Your Nutrition Plan")
                st.markdown(st.session_state.nutrition_plan)
                
                # Calorie tracker
                st.markdown("---")
                st.markdown("#### 📊 Daily Calorie Tracker")
                
                calories = st.number_input(
                    "Log calories consumed today:",
                    min_value=0,
                    max_value=5000,
                    step=50
                )
                
                if st.button("Log Calories"):
                    st.session_state.progress_data['calories_tracked'] += calories
                    st.success(f"✅ Logged {calories} calories!")
    
    # Tab 4: Translation
    with tab4:
        st.markdown("### 🌍 Language Translation")
        
        if not client:
            st.warning("⚠️ Please configure your Groq API key in the sidebar.")
        else:
            st.markdown("""
            <div class="info-box">
                <strong>🗣️ Translate Health & Fitness Content</strong><br>
                Translate workout instructions, nutrition advice, or health information to your preferred language.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                text_to_translate = st.text_area(
                    "Enter text to translate:",
                    height=200,
                    placeholder="Paste your text here..."
                )
            
            with col2:
                target_language = st.selectbox(
                    "Select target language:",
                    [
                        "Spanish", "French", "German", "Italian", "Portuguese",
                        "Chinese", "Japanese", "Korean", "Hindi", "Arabic",
                        "Russian", "Dutch", "Swedish", "Polish", "Turkish"
                    ]
                )
                
                if st.button("Translate", use_container_width=True):
                    if text_to_translate:
                        with st.spinner(f"Translating to {target_language}..."):
                            translation = translate_text(client, text_to_translate, target_language)
                        
                        st.markdown("#### Translation Result:")
                        st.markdown(f"""
                        <div class="success-box">
                            {translation}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Please enter text to translate!")
    
    # Tab 5: Image Analysis
    with tab5:
        st.markdown("### 📸 Image Analysis")
        
        if not client:
            st.warning("⚠️ Please configure your Groq API key in the sidebar.")
        else:
            st.markdown("""
            <div class="info-box">
                <strong>📷 Analyze Health & Fitness Images</strong><br>
                Upload images for food recognition, workout form analysis, or general health insights.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                uploaded_file = st.file_uploader(
                    "Upload an image:",
                    type=['png', 'jpg', 'jpeg'],
                    help="Supported formats: PNG, JPG, JPEG"
                )
            
            with col2:
                analysis_type = st.selectbox(
                    "Analysis Type:",
                    ["Food Recognition", "Workout Form", "General Health"]
                )
            
            if uploaded_file:
                # Display uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                
                if st.button("Analyze Image", use_container_width=True):
                    # Convert image to base64
                    image_bytes = uploaded_file.read()
                    image_base64 = base64.b64encode(image_bytes).decode()
                    
                    with st.spinner("Analyzing image..."):
                        analysis = analyze_image(client, image_base64, analysis_type)
                    
                    st.markdown("#### Analysis Result:")
                    st.markdown(f"""
                    <div class="success-box">
                        {analysis}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: white; padding: 2rem;">
        <p><strong>AroMi AI Agent</strong> - Your Adaptive Health & Wellness Coach</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Powered by Groq LLM (Llama 3.3 70B Versatile) | Built with Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
