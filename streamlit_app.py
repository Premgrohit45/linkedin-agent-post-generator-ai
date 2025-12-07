"""
🚀 LinkedIn Blog Agent - Modern Streamlit Frontend
Beautiful, modern UI for AI-powered LinkedIn blog generation and email distribution.
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import time
import plotly.graph_objects as go
import plotly.express as px

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.linkedin_blog_agent import LinkedInBlogAgent
from src.blog_generator import LinkedInBlogGenerator
from src.email_sender import EmailSender

# Page configuration
st.set_page_config(
    page_title="LinkedIn Blog Agent 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 0;
        opacity: 0.9;
    }
    
    /* Card styles */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #e1e8ed;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-error {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Blog preview styles */
    .blog-preview {
        background: #f8f9fa;
        border-left: 4px solid #0073b1;
        padding: 1.5rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    .blog-title {
        color: #0073b1;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .blog-content {
        line-height: 1.6;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .blog-hashtags {
        color: #0073b1;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    .blog-cta {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        font-style: italic;
        color: #2c3e50;
        margin-top: 1rem;
    }
    
    /* Sidebar styles */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #0073b1, #005885);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,115,177,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #005885, #004066);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,115,177,0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
    }
    
    /* Email recipient chips */
    .email-chip {
        background: #e8f4f8;
        color: #0073b1;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
        border: 1px solid #b3d9eb;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

def main_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 LinkedIn Blog Agent</h1>
        <p>AI-Powered Content Creation & Email Distribution Platform</p>
    </div>
    """, unsafe_allow_html=True)

def sidebar_navigation():
    """Sidebar navigation"""
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        
        page = st.selectbox(
            "Choose your action:",
            [
                "🏠 Dashboard",
                "✍️ Generate Single Blog",
                "📧 Dynamic Recipients",
                "📝 Multiple Blogs", 
                "💡 Topic Suggestions",
                "⚙️ Settings & Test"
            ]
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("## 📊 Quick Stats")
        
        # Count generated blogs
        output_dir = "output"
        if os.path.exists(output_dir):
            json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
            st.metric("Generated Blogs", len(json_files))
        else:
            st.metric("Generated Blogs", 0)
        
        # AI Model info
        st.info("🤖 **AI Model**: Gemini 2.5 Flash")
        st.success("🔑 **Status**: Ready")
        
        return page

def dashboard_page():
    """Dashboard overview page"""
    st.markdown("## 🏠 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>✍️</h3>
            <h2>Blog Generator</h2>
            <p>AI-powered content creation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #2ecc71, #27ae60);">
            <h3>📧</h3>
            <h2>Email System</h2>
            <p>Dynamic recipient management</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f39c12, #e67e22);">
            <h3>💡</h3>
            <h2>Topic Ideas</h2>
            <p>AI-suggested content topics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #9b59b6, #8e44ad);">
            <h3>📊</h3>
            <h2>Analytics</h2>
            <p>Performance tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent blogs
    st.markdown("## 📚 Recent Blog Posts")
    
    output_dir = "output"
    if os.path.exists(output_dir):
        json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
        json_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
        
        if json_files:
            for i, file in enumerate(json_files[:5]):  # Show last 5
                try:
                    with open(os.path.join(output_dir, file), 'r', encoding='utf-8') as f:
                        blog_data = json.load(f)
                    
                    with st.expander(f"📖 {blog_data.get('title', 'Untitled')}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Topic:** {blog_data.get('topic', 'Unknown')}")
                            st.markdown(f"**Generated:** {blog_data.get('generated_at', 'Unknown')}")
                            st.markdown(f"**Length:** {len(blog_data.get('content', '').split())} words")
                        
                        with col2:
                            if st.button(f"📥 Download", key=f"download_{i}"):
                                st.download_button(
                                    label="Download JSON",
                                    data=json.dumps(blog_data, indent=2),
                                    file_name=file,
                                    mime="application/json"
                                )
                
                except Exception as e:
                    st.error(f"Error reading {file}: {str(e)}")
        else:
            st.info("No blog posts generated yet. Create your first one! 🚀")
    else:
        st.info("No blog posts generated yet. Create your first one! 🚀")

def generate_single_blog_page():
    """Single blog generation page"""
    st.markdown("## ✍️ Generate Single Blog Post")
    
    with st.form("single_blog_form"):
        st.markdown("### 📝 Blog Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "🎯 Blog Topic",
                placeholder="e.g., The Future of AI in Business",
                help="What should your blog post be about?"
            )
            
            tone = st.selectbox(
                "🎨 Writing Tone",
                ["professional", "casual", "inspirational"],
                help="Choose the tone for your blog post"
            )
        
        with col2:
            length = st.selectbox(
                "📏 Content Length",
                ["short", "medium", "long"],
                index=1,
                help="How long should the blog post be?"
            )
            
            audience = st.text_input(
                "👥 Target Audience",
                value="professionals",
                help="Who is your target audience?"
            )
        
        st.markdown("### 📧 Email Settings")
        
        send_email = st.checkbox("📨 Send via email", value=True)
        
        if send_email:
            recipient = st.text_input(
                "📮 Recipient Email",
                placeholder="recipient@example.com",
                help="Email address to send the blog post to"
            )
        
        submitted = st.form_submit_button("🚀 Generate Blog Post", use_container_width=True)
        
        if submitted:
            if not topic:
                st.error("❌ Please enter a blog topic!")
                return
            
            if send_email and not recipient:
                st.error("❌ Please enter recipient email!")
                return
            
            generate_single_blog(topic, tone, length, audience, send_email, recipient)

def generate_single_blog(topic, tone, length, audience, send_email, recipient):
    """Generate a single blog post"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize agent
        status_text.text("🔧 Initializing AI agent...")
        progress_bar.progress(20)
        
        agent = LinkedInBlogAgent()
        
        # Generate blog
        status_text.text("🤖 Generating blog post with AI...")
        progress_bar.progress(60)
        
        if send_email and recipient:
            results = agent.generate_and_send_blog(
                topic=topic,
                tone=tone,
                length=length,
                target_audience=audience,
                recipient_email=recipient,
                save_to_file=True
            )
        else:
            # Generate without email
            blog_post = agent.blog_generator.generate_blog_post(
                topic=topic,
                tone=tone,
                length=length,
                target_audience=audience
            )
            
            # Save to file
            file_path = agent._save_blog_to_file(blog_post)
            
            results = {
                'success': True,
                'blog_post': blog_post,
                'file_saved': True,
                'file_path': str(file_path),
                'email_sent': False
            }
        
        progress_bar.progress(100)
        status_text.text("✅ Blog post generated successfully!")
        
        # Display results
        if results['success']:
            blog_post = results['blog_post']
            
            st.success("🎉 Blog post generated successfully!")
            
            # Blog preview
            display_blog_preview(blog_post)
            
            # Results summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📝 Word Count", len(blog_post.get('content', '').split()))
            
            with col2:
                if results.get('file_saved'):
                    st.metric("💾 File Saved", "✅ Yes")
                else:
                    st.metric("💾 File Saved", "❌ No")
            
            with col3:
                if results.get('email_sent'):
                    st.metric("📧 Email Sent", "✅ Yes")
                else:
                    st.metric("📧 Email Sent", "❌ No")
            
            # Download options
            st.markdown("### 📥 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # JSON download
                json_data = json.dumps(blog_post, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_data,
                    file_name=f"blog_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                # Text download
                text_data = f"""TITLE: {blog_post.get('title', 'Untitled')}

CONTENT:
{blog_post.get('content', 'No content')}

HASHTAGS: {blog_post.get('hashtags', '')}

CALL TO ACTION: {blog_post.get('call_to_action', '')}

---
Generated: {blog_post.get('generated_at', '')}
Topic: {topic}
Tone: {tone}
"""
                st.download_button(
                    label="📝 Download Text",
                    data=text_data,
                    file_name=f"blog_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        else:
            st.error("❌ Failed to generate blog post")
            for error in results.get('errors', []):
                st.error(f"Error: {error}")
    
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Error occurred")
        st.error(f"❌ Error: {str(e)}")

def dynamic_recipients_page():
    """Dynamic recipients blog generation page"""
    st.markdown("## 📧 Generate Blog with Dynamic Recipients")
    
    with st.form("dynamic_recipients_form"):
        st.markdown("### 📝 Blog Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input(
                "🎯 Blog Topic",
                placeholder="e.g., Remote Work Best Practices"
            )
            
            tone = st.selectbox(
                "🎨 Writing Tone",
                ["professional", "casual", "inspirational"]
            )
        
        with col2:
            length = st.selectbox(
                "📏 Content Length", 
                ["short", "medium", "long"],
                index=1
            )
            
            audience = st.text_input(
                "👥 Target Audience",
                value="professionals"
            )
        
        st.markdown("### 📧 Email Recipients")
        
        # Email input methods
        input_method = st.radio(
            "Choose input method:",
            ["✍️ Manual Entry", "📋 Paste List", "📁 Upload File"],
            horizontal=True
        )
        
        recipients = []
        
        if input_method == "✍️ Manual Entry":
            st.markdown("**Add recipients one by one:**")
            
            # Dynamic email input
            if 'recipients_list' not in st.session_state:
                st.session_state.recipients_list = []
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                new_email = st.text_input("📮 Email Address", placeholder="user@example.com")
            
            with col2:
                if st.form_submit_button("➕ Add", use_container_width=True):
                    if new_email and new_email not in st.session_state.recipients_list:
                        st.session_state.recipients_list.append(new_email)
            
            # Display current recipients
            if st.session_state.recipients_list:
                st.markdown("**Current Recipients:**")
                for i, email in enumerate(st.session_state.recipients_list):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"📧 {email}")
                    with col2:
                        if st.form_submit_button(f"🗑️", key=f"remove_{i}"):
                            st.session_state.recipients_list.remove(email)
                            st.experimental_rerun()
            
            recipients = st.session_state.recipients_list
        
        elif input_method == "📋 Paste List":
            email_text = st.text_area(
                "Paste email addresses (one per line):",
                placeholder="user1@example.com\nuser2@example.com\nuser3@example.com",
                height=150
            )
            
            if email_text:
                recipients = [email.strip() for email in email_text.split('\n') if email.strip()]
        
        elif input_method == "📁 Upload File":
            uploaded_file = st.file_uploader(
                "Upload CSV or TXT file with email addresses",
                type=['csv', 'txt']
            )
            
            if uploaded_file:
                content = uploaded_file.read().decode('utf-8')
                recipients = [email.strip() for email in content.replace(',', '\n').split('\n') if email.strip()]
        
        # Email settings
        col1, col2 = st.columns(2)
        
        with col1:
            subject_prefix = st.text_input(
                "📝 Email Subject Prefix",
                value="Generated LinkedIn Blog Post"
            )
        
        with col2:
            validate_emails = st.checkbox("✅ Validate emails before sending", value=True)
        
        # Show recipient summary
        if recipients:
            st.markdown(f"### 📊 Recipients Summary ({len(recipients)} emails)")
            
            # Display recipients in a nice format
            recipient_display = ""
            for i, email in enumerate(recipients, 1):
                recipient_display += f"<span class='email-chip'>{i}. {email}</span> "
            
            st.markdown(recipient_display, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 Generate & Send to All", use_container_width=True)
        
        if submitted:
            if not topic:
                st.error("❌ Please enter a blog topic!")
                return
            
            if not recipients:
                st.error("❌ Please add at least one email recipient!")
                return
            
            generate_dynamic_recipients_blog(
                topic, tone, length, audience, recipients, 
                subject_prefix, validate_emails
            )

def generate_dynamic_recipients_blog(topic, tone, length, audience, recipients, subject_prefix, validate_emails):
    """Generate blog and send to multiple recipients"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize agent
        status_text.text("🔧 Initializing AI agent...")
        progress_bar.progress(10)
        
        agent = LinkedInBlogAgent()
        
        # Validate emails first if requested
        if validate_emails:
            status_text.text("✅ Validating email addresses...")
            progress_bar.progress(30)
            
            validation_results = agent.email_sender.validate_recipients(recipients)
            valid_emails = [email for email, is_valid in validation_results.items() if is_valid]
            invalid_emails = [email for email, is_valid in validation_results.items() if not is_valid]
            
            if invalid_emails:
                st.warning(f"⚠️ Found {len(invalid_emails)} invalid email addresses:")
                for email in invalid_emails:
                    st.markdown(f"<span class='status-error'>❌ {email}</span>", unsafe_allow_html=True)
                
                st.info(f"✅ Proceeding with {len(valid_emails)} valid emails")
                recipients = valid_emails
        
        # Generate blog
        status_text.text("🤖 Generating blog post with AI...")
        progress_bar.progress(60)
        
        results = agent.generate_and_send_to_multiple_recipients(
            topic=topic,
            recipients=recipients,
            tone=tone,
            length=length,
            target_audience=audience,
            subject_prefix=subject_prefix,
            validate_emails=validate_emails,
            save_to_file=True
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Blog post generated and emails sent!")
        
        # Display results
        if results['success']:
            blog_post = results['blog_post']
            
            st.success("🎉 Blog post generated and sent successfully!")
            
            # Blog preview
            display_blog_preview(blog_post)
            
            # Email results
            st.markdown("### 📧 Email Sending Results")
            
            email_results = results.get('email_results', {})
            
            if 'summary' in email_results:
                summary = email_results['summary']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📧 Total Recipients", summary['total_recipients'])
                
                with col2:
                    st.metric("✅ Valid Emails", summary['valid_emails'])
                
                with col3:
                    st.metric("📩 Successfully Sent", summary['emails_sent'])
                
                with col4:
                    st.metric("❌ Failed", summary['emails_failed'])
                
                # Detailed results
                if 'sending' in email_results:
                    sending_results = email_results['sending']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        successful = [email for email, success in sending_results.items() if success]
                        if successful:
                            st.markdown("#### ✅ Successfully Sent To:")
                            for email in successful:
                                st.markdown(f"<span class='status-success'>📧 {email}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        failed = [email for email, success in sending_results.items() if not success]
                        if failed:
                            st.markdown("#### ❌ Failed To Send To:")
                            for email in failed:
                                st.markdown(f"<span class='status-error'>📧 {email}</span>", unsafe_allow_html=True)
            
            # Download options
            st.markdown("### 📥 Download Blog Post")
            
            col1, col2 = st.columns(2)
            
            with col1:
                json_data = json.dumps(blog_post, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_data,
                    file_name=f"blog_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                text_data = f"""TITLE: {blog_post.get('title', 'Untitled')}

CONTENT:
{blog_post.get('content', 'No content')}

HASHTAGS: {blog_post.get('hashtags', '')}

CALL TO ACTION: {blog_post.get('call_to_action', '')}"""
                
                st.download_button(
                    label="📝 Download Text",
                    data=text_data,
                    file_name=f"blog_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        else:
            st.error("❌ Failed to generate blog post or send emails")
            for error in results.get('errors', []):
                st.error(f"Error: {error}")
    
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Error occurred")
        st.error(f"❌ Error: {str(e)}")

def display_blog_preview(blog_post):
    """Display a beautiful blog post preview"""
    st.markdown("### 📖 Generated Blog Post Preview")
    
    title = blog_post.get('title', 'Untitled')
    content = blog_post.get('content', 'No content')
    hashtags = blog_post.get('hashtags', '')
    cta = blog_post.get('call_to_action', '')
    
    preview_html = f"""
    <div class="blog-preview">
        <div class="blog-title">{title}</div>
        <div class="blog-content">{content}</div>
        <div class="blog-hashtags">{hashtags}</div>
        <div class="blog-cta"><strong>Call to Action:</strong> {cta}</div>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)

def topic_suggestions_page():
    """Topic suggestions page"""
    st.markdown("## 💡 AI-Powered Topic Suggestions")
    
    with st.form("topic_suggestions_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.text_input(
                "🏢 Industry/Field",
                placeholder="e.g., Technology, Marketing, Healthcare"
            )
        
        with col2:
            keywords_input = st.text_input(
                "🔍 Keywords (optional)",
                placeholder="e.g., AI, automation, productivity"
            )
        
        submitted = st.form_submit_button("💡 Get Topic Suggestions", use_container_width=True)
        
        if submitted:
            if not industry:
                st.error("❌ Please enter an industry or field!")
                return
            
            get_topic_suggestions(industry, keywords_input)

def get_topic_suggestions(industry, keywords_input):
    """Get AI-powered topic suggestions"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🤖 Getting AI-powered topic suggestions...")
        progress_bar.progress(50)
        
        agent = LinkedInBlogAgent()
        
        keywords = [kw.strip() for kw in keywords_input.split(',')] if keywords_input else None
        
        topics = agent.get_topic_suggestions(industry, keywords)
        
        progress_bar.progress(100)
        status_text.text("✅ Topic suggestions generated!")
        
        if topics:
            st.success(f"🎉 Generated {len(topics)} topic suggestions for {industry}!")
            
            st.markdown("### 📋 Suggested Topics")
            
            for i, topic in enumerate(topics, 1):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{i}.** {topic}")
                
                with col2:
                    if st.button("✍️ Use", key=f"use_topic_{i}"):
                        st.session_state.selected_topic = topic
                        st.success(f"Selected: {topic}")
                        st.info("Go to 'Generate Single Blog' or 'Dynamic Recipients' to create a post with this topic!")
            
            # Download topics
            st.markdown("### 📥 Download Topics")
            
            topics_text = f"Topic Suggestions for {industry}\n" + "="*50 + "\n\n"
            for i, topic in enumerate(topics, 1):
                topics_text += f"{i}. {topic}\n"
            
            st.download_button(
                label="📄 Download Topic List",
                data=topics_text,
                file_name=f"topics_{industry.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        else:
            st.warning("⚠️ No topic suggestions generated. Please try again with different keywords.")
    
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Error occurred")
        st.error(f"❌ Error: {str(e)}")

def settings_page():
    """Settings and testing page"""
    st.markdown("## ⚙️ Settings & System Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 System Configuration")
        
        # AI Model info
        st.info("🤖 **AI Model**: Gemini 2.5 Flash")
        st.info("🔑 **API Provider**: Google Generative AI")
        
        # Test connections
        if st.button("🧪 Test AI Connection", use_container_width=True):
            test_ai_connection()
        
        if st.button("📧 Test Email Connection", use_container_width=True):
            test_email_connection()
    
    with col2:
        st.markdown("### 📊 System Statistics")
        
        # File statistics
        output_dir = "output"
        if os.path.exists(output_dir):
            json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
            txt_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            
            st.metric("📄 JSON Files", len(json_files))
            st.metric("📝 Text Files", len(txt_files))
            
            # Calculate total words
            total_words = 0
            for file in json_files:
                try:
                    with open(os.path.join(output_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        content = data.get('content', '')
                        total_words += len(content.split())
                except:
                    continue
            
            st.metric("📝 Total Words Generated", total_words)
        
        else:
            st.metric("📄 Generated Files", 0)

def test_ai_connection():
    """Test AI connection"""
    with st.spinner("Testing AI connection..."):
        try:
            generator = LinkedInBlogGenerator()
            st.success("✅ AI connection successful!")
            st.info("🤖 Google Gemini 2.5 Flash is ready")
        except Exception as e:
            st.error(f"❌ AI connection failed: {str(e)}")

def test_email_connection():
    """Test email connection"""
    with st.spinner("Testing email connection..."):
        try:
            sender = EmailSender()
            if sender.test_connection():
                st.success("✅ Email connection successful!")
                st.info("📧 Gmail SMTP is ready")
            else:
                st.error("❌ Email connection failed")
        except Exception as e:
            st.error(f"❌ Email connection error: {str(e)}")

def multiple_blogs_page():
    """Multiple blogs generation page"""
    st.markdown("## 📝 Generate Multiple Blog Posts")
    
    with st.form("multiple_blogs_form"):
        st.markdown("### 📋 Topics Configuration")
        
        topics_input = st.text_area(
            "🎯 Blog Topics (one per line)",
            placeholder="The Future of AI in Business\nRemote Work Best Practices\nPersonal Branding Tips\nDigital Marketing Trends",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            tone = st.selectbox("🎨 Writing Tone", ["professional", "casual", "inspirational"])
            length = st.selectbox("📏 Content Length", ["short", "medium", "long"], index=1)
        
        with col2:
            audience = st.text_input("👥 Target Audience", value="professionals")
            send_emails = st.checkbox("📧 Send via email", value=True)
        
        if send_emails:
            recipient = st.text_input("📮 Recipient Email", placeholder="recipient@example.com")
        
        submitted = st.form_submit_button("🚀 Generate All Blog Posts", use_container_width=True)
        
        if submitted:
            if not topics_input:
                st.error("❌ Please enter at least one blog topic!")
                return
            
            topics = [topic.strip() for topic in topics_input.split('\n') if topic.strip()]
            
            if send_emails and not recipient:
                st.error("❌ Please enter recipient email!")
                return
            
            generate_multiple_blogs(topics, tone, length, audience, send_emails, recipient)

def generate_multiple_blogs(topics, tone, length, audience, send_emails, recipient):
    """Generate multiple blog posts"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔧 Initializing AI agent...")
        progress_bar.progress(10)
        
        agent = LinkedInBlogAgent()
        
        status_text.text(f"🤖 Generating {len(topics)} blog posts...")
        progress_bar.progress(30)
        
        results = agent.generate_multiple_blogs(
            topics=topics,
            tone=tone,
            length=length,
            target_audience=audience,
            recipient_email=recipient if send_emails else None,
            send_separately=True,
            save_to_files=True
        )
        
        progress_bar.progress(100)
        status_text.text("✅ All blog posts generated!")
        
        if results['success']:
            blog_posts = results['blog_posts']
            
            st.success(f"🎉 Successfully generated {len(blog_posts)} blog posts!")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📝 Posts Generated", len(blog_posts))
            
            with col2:
                total_words = sum(len(post.get('content', '').split()) for post in blog_posts)
                st.metric("📊 Total Words", total_words)
            
            with col3:
                if send_emails:
                    email_results = results.get('email_results', {})
                    successful_emails = sum(1 for success in email_results.values() if success)
                    st.metric("📧 Emails Sent", f"{successful_emails}/{len(email_results)}")
                else:
                    st.metric("📧 Emails Sent", "0 (disabled)")
            
            # Display each blog post
            st.markdown("### 📚 Generated Blog Posts")
            
            for i, post in enumerate(blog_posts, 1):
                with st.expander(f"📖 {i}. {post.get('title', 'Untitled')}"):
                    display_blog_preview(post)
                    
                    # Individual download
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        json_data = json.dumps(post, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="📄 Download JSON",
                            data=json_data,
                            file_name=f"blog_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            key=f"json_download_{i}"
                        )
                    
                    with col2:
                        text_data = f"""TITLE: {post.get('title', 'Untitled')}

CONTENT:
{post.get('content', 'No content')}

HASHTAGS: {post.get('hashtags', '')}

CALL TO ACTION: {post.get('call_to_action', '')}"""
                        
                        st.download_button(
                            label="📝 Download Text",
                            data=text_data,
                            file_name=f"blog_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key=f"text_download_{i}"
                        )
        
        else:
            st.error("❌ Failed to generate blog posts")
            for error in results.get('errors', []):
                st.error(f"Error: {error}")
    
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Error occurred")
        st.error(f"❌ Error: {str(e)}")

def main():
    """Main application"""
    # Load custom CSS
    load_css()
    
    # Main header
    main_header()
    
    # Sidebar navigation
    selected_page = sidebar_navigation()
    
    # Page routing
    if selected_page == "🏠 Dashboard":
        dashboard_page()
    elif selected_page == "✍️ Generate Single Blog":
        generate_single_blog_page()
    elif selected_page == "📧 Dynamic Recipients":
        dynamic_recipients_page()
    elif selected_page == "📝 Multiple Blogs":
        multiple_blogs_page()
    elif selected_page == "💡 Topic Suggestions":
        topic_suggestions_page()
    elif selected_page == "⚙️ Settings & Test":
        settings_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 LinkedIn Blog Agent | Powered by Google Gemini 2.5 Flash | Built with Streamlit</p>
        <p>Made with ❤️ for professional content creators</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()