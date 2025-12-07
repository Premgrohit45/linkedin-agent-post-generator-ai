"""
🤖 LinkedIn Blog Agent - Advanced AI Assistant
Next-generation AI agent interface for professional content creation and distribution.
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json
import time
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import re

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our custom modules
try:
    from src.linkedin_blog_agent import LinkedInBlogAgent
    from src.blog_generator import LinkedInBlogGenerator  
    from src.email_sender import EmailSender
except ImportError as e:
    st.error(f"🚨 Agent Module Error: {e}")
    st.stop()

# Advanced Page Configuration
st.set_page_config(
    page_title="🤖 AI Blog Agent | Professional Content Creator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Agent-like Design
def load_agent_css():
    st.markdown("""
    <style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 25%, #16213e 50%, #1a1a2e 75%, #0a0a0f 100%);
        font-family: 'Rajdhani', sans-serif;
        color: #ffffff;
    }
    
    /* Enhanced Text Rendering for All Elements */
    * {
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        font-feature-settings: "kern" 1, "liga" 1 !important;
    }
    
    /* Improved Typography Base */
    body, div, p, span {
        word-spacing: 1px !important;
        letter-spacing: 0.3px !important;
        line-height: 1.7 !important;
    }
    
    /* Header Container */
    .agent-header {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 150, 255, 0.1) 100%);
        border: 2px solid #00ffff;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        animation: pulse-border 3s ease-in-out infinite;
    }
    
    @keyframes pulse-border {
        0%, 100% { border-color: #00ffff; box-shadow: 0 0 30px rgba(0, 255, 255, 0.3); }
        50% { border-color: #0096ff; box-shadow: 0 0 40px rgba(0, 150, 255, 0.5); }
    }
    
    .agent-title {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        color: #00ffff;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
        margin: 0;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    .agent-subtitle {
        font-size: 1.5rem;
        color: #a0a0ff;
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .agent-status {
        font-size: 1rem;
        color: #00ff88;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Status Dashboard */
    .status-dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .status-card {
        background: linear-gradient(145deg, rgba(0, 255, 255, 0.05) 0%, rgba(0, 150, 255, 0.05) 100%);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        border-color: #00ffff;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .status-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .status-title {
        color: #00ffff;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-value {
        color: #ffffff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Control Panels */
    .control-panel {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.03) 0%, rgba(0, 255, 255, 0.03) 100%);
        border: 2px solid rgba(0, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(15px);
    }
    
    .panel-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        color: #00ffff;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* Agent Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00ffff 0%, #0096ff 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.3);
        font-family: 'Orbitron', monospace;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.5);
        background: linear-gradient(135deg, #0096ff 0%, #00ffff 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 15px;
        color: #ffffff;
        font-size: 1.1rem;
        padding: 1rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ffff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #00ffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(10, 10, 15, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
        border-right: 2px solid rgba(0, 255, 255, 0.3);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%);
        border: 2px solid #00ff88;
        border-radius: 15px;
        color: #00ff88;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 0, 100, 0.1) 0%, rgba(200, 0, 50, 0.1) 100%);
        border: 2px solid #ff0064;
        border-radius: 15px;
        color: #ff0064;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 200, 0, 0.1) 0%, rgba(255, 150, 0, 0.1) 100%);
        border: 2px solid #ffc800;
        border-radius: 15px;
        color: #ffc800;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 150, 255, 0.1) 0%, rgba(0, 100, 200, 0.1) 100%);
        border: 2px solid #0096ff;
        border-radius: 15px;
        color: #0096ff;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffff 0%, #0096ff 100%);
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.05) 0%, rgba(0, 150, 255, 0.05) 100%);
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Code Blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Loading Animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid rgba(0, 255, 255, 0.1);
        border-top: 4px solid #00ffff;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Terminal-like output */
    .terminal-output {
        background: #000000;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #00ff00;
        margin: 1rem 0;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Enhanced Text Rendering */
    .blog-content-text {
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 400 !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        text-align: justify !important;
        padding: 1.5rem !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 10px !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* Blog Title Styling */
    .blog-title {
        color: #00ffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 0 !important;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5) !important;
    }
    
    /* Content Container */
    .content-container {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 2px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Section Headers */
    .section-header {
        color: #00ffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    /* Hashtag and CTA Styling */
    .meta-content {
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        overflow-y: auto !important;
        max-height: 120px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(0, 150, 255, 0.1) 100%) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #00ffff !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1.5rem !important;
    }
    
    /* Markdown text improvements */
    .stMarkdown {
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    .stMarkdown p {
        color: #ffffff !important;
        line-height: 1.6 !important;
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown strong {
        color: #00ffff !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'agent_initialized' not in st.session_state:
        st.session_state.agent_initialized = False
    if 'blog_history' not in st.session_state:
        st.session_state.blog_history = []
    if 'total_generated' not in st.session_state:
        st.session_state.total_generated = 0
    if 'total_emails_sent' not in st.session_state:
        st.session_state.total_emails_sent = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'generated_blog' not in st.session_state:
        st.session_state.generated_blog = None
    if 'generation_topic' not in st.session_state:
        st.session_state.generation_topic = ''

# Agent Header Component
def render_agent_header():
    st.markdown("""
    <div class="agent-header">
        <div class="agent-title">🤖 AI BLOG AGENT</div>
        <div class="agent-subtitle">Professional Content Creator & Distribution System</div>
        <div class="agent-status">● ONLINE | READY FOR DEPLOYMENT</div>
    </div>
    """, unsafe_allow_html=True)

# Status Dashboard Component
def render_status_dashboard():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🚀</div>
            <div class="status-title">System Status</div>
            <div class="status-value">OPERATIONAL</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">📝</div>
            <div class="status-title">Blogs Generated</div>
            <div class="status-value">{st.session_state.total_generated}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">📧</div>
            <div class="status-title">Emails Sent</div>
            <div class="status-value">{st.session_state.total_emails_sent}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🤖</div>
            <div class="status-title">AI Model</div>
            <div class="status-value">GEMINI 2.5</div>
        </div>
        """, unsafe_allow_html=True)

# Initialize Agent
@st.cache_resource
def initialize_agent():
    try:
        agent = LinkedInBlogAgent()
        return agent, True, "Agent successfully initialized"
    except Exception as e:
        return None, False, f"Agent initialization failed: {str(e)}"

# Email validation function
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Blog Generation Interface
def render_blog_generator():
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">🚀 BLOG GENERATION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("🎯 BLOG TOPIC", placeholder="Enter your blog topic here...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            tone = st.selectbox("🎨 TONE", ["professional", "casual", "inspirational", "technical"])
        with col_b:
            length = st.selectbox("📏 LENGTH", ["short", "medium", "long"])
        
        audience = st.text_input("👥 TARGET AUDIENCE", value="professionals", placeholder="Target audience...")
    
    with col2:
        st.markdown("### 🎛️ GENERATION CONTROLS")
        
        if st.button("🚀 GENERATE BLOG"):
            if topic:
                # Store the parameters and navigate to generation page
                st.session_state.generation_topic = topic
                st.session_state.generation_tone = tone
                st.session_state.generation_length = length
                st.session_state.generation_audience = audience
                st.session_state.current_page = 'generating'
                st.rerun()
            else:
                st.error("⚠️ Please enter a blog topic")
        
        if st.button("💡 GET AI SUGGESTIONS"):
            get_topic_suggestions()

def generate_single_blog():
    """Generate blog with stored parameters and navigate to results"""
    try:
        # Get parameters from session state
        topic = st.session_state.generation_topic
        tone = st.session_state.generation_tone
        length = st.session_state.generation_length
        audience = st.session_state.generation_audience
        
        agent, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Initialize
        progress_bar.progress(20)
        status_text.text("🔧 Initializing AI systems...")
        time.sleep(0.5)
        
        # Step 2: Generate
        progress_bar.progress(40)
        status_text.text("🧠 Generating content with Gemini AI...")
        
        blog_post = agent.blog_generator.generate_blog_post(
            topic=topic,
            tone=tone,
            length=length,
            target_audience=audience
        )
        
        # Step 3: Processing
        progress_bar.progress(80)
        status_text.text("⚙️ Processing and formatting...")
        time.sleep(0.3)
        
        # Step 4: Complete
        progress_bar.progress(100)
        status_text.text("✅ Blog generation complete!")
        time.sleep(0.5)
        
        # Update session state
        st.session_state.total_generated += 1
        st.session_state.blog_history.append({
            'title': blog_post.get('title'),
            'topic': topic,
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Store the generated blog and navigate to results
        st.session_state.generated_blog = blog_post
        st.session_state.current_page = 'results'
        st.rerun()
        
    except Exception as e:
        st.error(f"🚨 Generation failed: {str(e)}")
        time.sleep(2)
        st.session_state.current_page = 'home'
        st.rerun()

def render_blog_display(blog_post):
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">📖 GENERATED CONTENT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact title styling
    title = blog_post.get('title', 'Untitled')
    st.markdown(f"""
    <div style="
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        text-align: center;
    ">
        <h4 style="color: #00ffff; margin: 0; font-family: 'Orbitron', monospace; font-weight: 600; font-size: 1.1rem;">
            🎯 {title}
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Content with compact formatting
    st.markdown("""
    <div style="
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    ">
        <h4 style="color: #00ffff; font-family: 'Orbitron', monospace; margin-bottom: 0.5rem; font-size: 1rem;">
            📝 GENERATED CONTENT
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Use compact content display
    content = blog_post.get('content', 'No content')
    
    # Create a compact styled container for the content
    st.markdown(f"""
    <div style="
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        max-height: 300px;
        overflow-y: auto;
    ">
        <div style="
            color: #ffffff;
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.95rem;
            font-weight: 400;
            line-height: 1.5;
            text-align: justify;
            word-spacing: 1px;
            letter-spacing: 0.3px;
        ">
        {content.replace(chr(10), '<br><br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact hashtags and CTA sections
    col1, col2 = st.columns(2)
    
    with col1:
        hashtags = blog_post.get('hashtags', 'No hashtags')
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.3rem;
            max-height: 120px;
            overflow-y: auto;
        ">
            <h5 style="
                color: #00ff88; 
                font-family: 'Orbitron', monospace; 
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                text-align: center;
            ">
                🏷️ HASHTAGS
            </h5>
            <div style="
                color: #ffffff;
                font-family: 'Rajdhani', sans-serif;
                font-size: 0.85rem;
                font-weight: 400;
                line-height: 1.3;
                word-spacing: 1px;
                letter-spacing: 0.2px;
            ">
            {hashtags.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cta = blog_post.get('call_to_action', 'No CTA')
        st.markdown(f"""
        <div style="
            background: rgba(255, 150, 0, 0.1);
            border: 1px solid rgba(255, 150, 0, 0.3);
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.3rem;
            max-height: 120px;
            overflow-y: auto;
        ">
            <h5 style="
                color: #ff9600; 
                font-family: 'Orbitron', monospace; 
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                text-align: center;
            ">
                📢 CALL TO ACTION
            </h5>
            <div style="
                color: #ffffff;
                font-family: 'Rajdhani', sans-serif;
                font-size: 0.85rem;
                font-weight: 400;
                line-height: 1.3;
                word-spacing: 1px;
                letter-spacing: 0.2px;
            ">
            {cta.replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Compact download options
    st.markdown("""
    <div style="
        background: rgba(128, 0, 255, 0.1);
        border: 1px solid rgba(128, 0, 255, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 1rem 0;
    ">
        <h5 style="color: #8000ff; font-family: 'Orbitron', monospace; margin-bottom: 0.5rem; text-align: center; font-size: 0.9rem;">
            💾 DOWNLOAD OPTIONS
        </h5>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 DOWNLOAD JSON",
            data=json.dumps(blog_post, indent=2),
            file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="download_json"
        )
    
    with col2:
        text_content = f"""TITLE: {blog_post.get('title', 'Untitled')}

CONTENT:
{blog_post.get('content', 'No content')}

HASHTAGS: {blog_post.get('hashtags', 'No hashtags')}

CALL TO ACTION: {blog_post.get('call_to_action', 'No CTA')}

---
Generated: {blog_post.get('generated_at', datetime.now().isoformat())}"""
        
        st.download_button(
            label="� DOWNLOAD TXT",
            data=text_content,
            file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_txt"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_email_section(blog_post):
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">📧 EMAIL DISTRIBUTION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 SINGLE RECIPIENT", "📮 MULTIPLE RECIPIENTS"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            single_email = st.text_input("📧 RECIPIENT EMAIL", placeholder="recipient@example.com")
            subject_prefix = st.text_input("📝 SUBJECT PREFIX", value="Generated LinkedIn Blog Post")
        
        with col2:
            st.markdown("### 🎛️ SEND CONTROLS")
            if st.button("📤 SEND EMAIL"):
                if single_email and validate_email(single_email):
                    send_single_email(blog_post, single_email, subject_prefix)
                else:
                    st.error("⚠️ Please enter a valid email address")
    
    with tab2:
        render_multiple_recipients_section(blog_post)

def render_multiple_recipients_section(blog_post):
    st.markdown("### 📮 MULTIPLE RECIPIENTS SYSTEM")
    
    # Recipients input area
    recipients_text = st.text_area(
        "📧 RECIPIENT EMAILS (one per line)",
        height=150,
        placeholder="recipient1@example.com\nrecipient2@example.com\nrecipient3@example.com"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject_prefix_multi = st.text_input("📝 SUBJECT PREFIX (MULTI)", value="Generated LinkedIn Blog Post")
        validate_emails_check = st.checkbox("✅ VALIDATE EMAILS", value=True)
    
    with col2:
        st.markdown("### 🎛️ BATCH CONTROLS")
        if st.button("📮 SEND TO ALL"):
            if recipients_text.strip():
                recipients = [email.strip() for email in recipients_text.split('\n') if email.strip()]
                send_multiple_emails(blog_post, recipients, subject_prefix_multi, validate_emails_check)
            else:
                st.error("⚠️ Please enter at least one email address")

def send_single_email(blog_post, email, subject_prefix):
    try:
        agent, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        with st.spinner("📤 Sending email..."):
            success = agent.email_sender.send_blog_post(
                blog_post=blog_post,
                recipient=email,
                subject_prefix=subject_prefix
            )
        
        if success:
            st.success(f"✅ Email sent successfully to {email}")
            st.session_state.total_emails_sent += 1
        else:
            st.error("❌ Failed to send email")
            
    except Exception as e:
        st.error(f"🚨 Email sending failed: {str(e)}")

def send_multiple_emails(blog_post, recipients, subject_prefix, validate_emails):
    try:
        agent, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        with st.spinner("📮 Processing multiple recipients..."):
            results = agent.generate_and_send_to_multiple_recipients(
                topic=blog_post.get('topic', 'Generated Blog'),
                recipients=recipients,
                validate_emails=validate_emails,
                save_to_file=False
            )
        
        # Display results
        if results['success']:
            email_results = results.get('email_results', {})
            if 'summary' in email_results:
                summary = email_results['summary']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📧 Total Recipients", summary['total_recipients'])
                with col2:
                    st.metric("✅ Valid Emails", summary['valid_emails'])
                with col3:
                    st.metric("📤 Successfully Sent", summary['emails_sent'])
                with col4:
                    st.metric("❌ Failed", summary['emails_failed'])
                
                st.session_state.total_emails_sent += summary['emails_sent']
                
                # Show detailed results
                if summary['invalid_emails'] > 0:
                    validation = results.get('validation_results', {})
                    invalid_emails = [email for email, valid in validation.items() if not valid]
                    st.warning(f"⚠️ Invalid emails found: {', '.join(invalid_emails)}")
                
                if summary['emails_sent'] > 0:
                    st.success(f"🎉 Successfully sent {summary['emails_sent']} emails!")
                    
        else:
            st.error("❌ Failed to send emails")
            for error in results.get('errors', []):
                st.error(f"Error: {error}")
                
    except Exception as e:
        st.error(f"🚨 Batch email sending failed: {str(e)}")

def get_topic_suggestions():
    with st.form("topic_suggestions_form"):
        st.markdown("### 💡 AI TOPIC SUGGESTIONS")
        
        col1, col2 = st.columns(2)
        with col1:
            industry = st.text_input("🏢 INDUSTRY", placeholder="e.g., Technology, Marketing, Finance")
        with col2:
            keywords = st.text_input("🔍 KEYWORDS", placeholder="AI, automation, trends (comma-separated)")
        
        if st.form_submit_button("🧠 GET AI SUGGESTIONS"):
            if industry:
                try:
                    agent, success, message = initialize_agent()
                    if not success:
                        st.error(f"🚨 {message}")
                        return
                    
                    with st.spinner("🤖 AI is generating topic suggestions..."):
                        keyword_list = [kw.strip() for kw in keywords.split(',')] if keywords else None
                        topics = agent.get_topic_suggestions(industry, keyword_list)
                    
                    if topics:
                        st.success("💡 AI-Generated Topic Suggestions:")
                        for i, topic in enumerate(topics, 1):
                            if st.button(f"📝 {i}. {topic}", key=f"topic_{i}"):
                                st.session_state['selected_topic'] = topic
                                st.rerun()
                    else:
                        st.warning("No suggestions generated. Try different keywords.")
                        
                except Exception as e:
                    st.error(f"🚨 Suggestion generation failed: {str(e)}")
            else:
                st.error("⚠️ Please enter an industry")

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="agent-header" style="margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 900;">🤖 AGENT CONTROL</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Controls
        st.markdown("### 🗺️ NAVIGATION")
        
        current_page = st.session_state.current_page
        if current_page != 'home':
            if st.button("🏠 HOME"):
                st.session_state.current_page = 'home'
                st.session_state.generated_blog = None
                st.rerun()
        
        if current_page == 'results':
            if st.button("🚀 NEW BLOG"):
                st.session_state.current_page = 'home'
                st.session_state.generated_blog = None
                st.rerun()
        
        st.markdown("---")
        
        # Agent Status
        agent, success, message = initialize_agent()
        
        if success:
            st.success("🟢 AGENT ONLINE")
            st.info("📡 Connected to Google AI")
            st.info("📧 Email System Ready")
        else:
            st.error("🔴 AGENT OFFLINE")
            st.error(f"⚠️ {message}")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 MISSION STATS")
        st.metric("🎯 Blogs Generated", st.session_state.total_generated)
        st.metric("📧 Emails Deployed", st.session_state.total_emails_sent)
        
        st.markdown("---")
        
        # Recent Activity
        if st.session_state.blog_history:
            st.markdown("### 🕒 RECENT OPERATIONS")
            for i, blog in enumerate(st.session_state.blog_history[-3:], 1):
                st.text(f"🔸 {blog['title'][:30]}...")
                st.text(f"   📅 {blog['generated_at']}")
        
        st.markdown("---")
        
        # System Controls
        st.markdown("### ⚙️ SYSTEM CONTROLS")
        
        if st.button("🔄 RESET STATS"):
            st.session_state.total_generated = 0
            st.session_state.total_emails_sent = 0
            st.session_state.blog_history = []
            st.success("✅ Stats reset")
            st.rerun()
        
        if st.button("🧪 RUN DIAGNOSTICS"):
            run_system_diagnostics()

def run_system_diagnostics():
    st.markdown("### 🔍 SYSTEM DIAGNOSTICS")
    
    with st.spinner("🔧 Running system diagnostics..."):
        # Test agent initialization
        agent, success, message = initialize_agent()
        
        if success:
            st.success("✅ Agent initialization: PASS")
            
            # Test email connection
            try:
                email_test = agent.email_sender.test_connection()
                if email_test:
                    st.success("✅ Email system: PASS")
                else:
                    st.error("❌ Email system: FAIL")
            except:
                st.error("❌ Email system: FAIL")
        else:
            st.error(f"❌ Agent initialization: FAIL - {message}")

# Generation Page
def render_generation_page():
    render_agent_header()
    
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">🤖 GENERATING YOUR BLOG POST</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show generation parameters
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h4 style="color: #00ffff; margin-bottom: 1rem;">📋 GENERATION PARAMETERS</h4>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Topic:</strong> {st.session_state.generation_topic}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Tone:</strong> {st.session_state.generation_tone}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Length:</strong> {st.session_state.generation_length}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Audience:</strong> {st.session_state.generation_audience}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔙 BACK TO HOME"):
            st.session_state.current_page = 'home'
            st.rerun()
    
    # Generate the blog
    generate_single_blog()

# Results Page
def render_results_page():
    render_agent_header()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔙 BACK TO HOME"):
            st.session_state.current_page = 'home'
            st.session_state.generated_blog = None
            st.rerun()
    
    with col3:
        if st.button("🚀 GENERATE NEW"):
            st.session_state.current_page = 'home'
            st.session_state.generated_blog = None
            st.rerun()
    
    # Display the generated blog
    if st.session_state.generated_blog:
        st.success("🎉 Blog generated successfully!")
        render_blog_display(st.session_state.generated_blog)
        render_email_section(st.session_state.generated_blog)
    else:
        st.error("No blog data found. Please generate a new blog.")

# Main Application
def main():
    load_agent_css()
    initialize_session_state()
    
    # Page routing based on current_page
    if st.session_state.current_page == 'home':
        # Render home page
        render_agent_header()
        render_status_dashboard()
        render_blog_generator()
        render_sidebar()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 2rem;">
            <p>🤖 AI Blog Agent | Powered by Google Gemini 2.5-Flash | Built with ❤️ using Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state.current_page == 'generating':
        # Render generation page
        render_generation_page()
        
    elif st.session_state.current_page == 'results':
        # Render results page
        render_results_page()

if __name__ == "__main__":
    main()