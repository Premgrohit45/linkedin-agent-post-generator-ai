# LinkedIn Blog Agent Setup Guide

## 📋 Complete Step-by-Step Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Internet connection
- Gmail account (for email sending)

### Step 1: Get Google AI API Key (FREE)

1. **Go to Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the API key** - you'll need this for the `.env` file
5. **No credit card required** - Free tier includes:
   - 15 requests per minute
   - 1,500 requests per day
   - Perfect for blog generation

### Step 2: Set Up Gmail App Password (for email sending)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Go to**: https://myaccount.google.com/apppasswords
3. **Generate an App Password** for "Mail"
4. **Copy the 16-character password** (no spaces)
5. This is what you'll use as EMAIL_PASSWORD in .env

### Step 3: Configure Environment Variables

1. **Copy `.env.example` to `.env`**:
   ```bash
   copy .env.example .env
   ```

2. **Edit the `.env` file** with your credentials:
   ```
   # Google AI API Configuration
   GOOGLE_API_KEY=your_actual_google_ai_api_key_here
   
   # Email Configuration (Gmail SMTP)
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password
   EMAIL_RECIPIENT=recipient@gmail.com
   
   # Agent Configuration
   AGENT_NAME=LinkedIn Blog Agent
   BLOG_TONE=professional
   BLOG_LENGTH=medium
   ```

### Step 4: Install Dependencies

The virtual environment and packages are already set up! If you need to reinstall:

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install packages
pip install google-generativeai python-dotenv
```

### Step 5: Run the Agent

#### Option A: Interactive Mode (Recommended for beginners)
```bash
python main.py --interactive
```

#### Option B: Command Line Mode
```bash
# Generate a single blog post
python main.py --topic "The Future of AI in Business" --tone professional --length medium

# With custom email recipient
python main.py --topic "Remote Work Tips" --email "recipient@example.com"
```

#### Option C: Run individual components for testing
```bash
# Test blog generator only
python src/blog_generator.py

# Test email sender only
python src/email_sender.py

# Run full agent
python src/linkedin_blog_agent.py
```

## 🚀 Usage Examples

### Example 1: Generate Single Blog Post
```python
from src.linkedin_blog_agent import LinkedInBlogAgent

agent = LinkedInBlogAgent()
results = agent.generate_and_send_blog(
    topic="5 Tips for Remote Team Management",
    tone="professional",
    length="medium",
    target_audience="managers and team leaders"
)
```

### Example 2: Generate Multiple Posts
```python
topics = [
    "The Future of AI in Marketing",
    "Building Strong Remote Teams",
    "Personal Branding on LinkedIn"
]

results = agent.generate_multiple_blogs(
    topics=topics,
    tone="inspirational",
    send_separately=True
)
```

### Example 3: Get Topic Suggestions
```python
suggestions = agent.get_topic_suggestions(
    industry="Digital Marketing",
    keywords=["SEO", "content", "social media"]
)
```

## 📁 Project Structure

```
Agent 1/
├── main.py                 # Main entry point
├── .env                    # Environment variables (your secrets)
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
├── src/
│   ├── blog_generator.py  # Google AI SDK blog generation
│   ├── email_sender.py    # Email sending functionality
│   └── linkedin_blog_agent.py  # Main agent orchestrator
├── config/                # Configuration files
├── output/                # Generated blog posts saved here
└── docs/                  # Documentation
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "Google API Key not found"
- Make sure you copied your API key correctly to the `.env` file
- Ensure there are no extra spaces in the `.env` file
- Check that the file is named exactly `.env` (not `.env.txt`)

#### 2. "Email authentication failed"
- Ensure you're using an App Password, not your regular Gmail password
- Enable 2-Factor Authentication on your Gmail account first
- Double-check the 16-character app password has no spaces

#### 3. "Module not found" errors
- Make sure you're running from the correct directory
- Activate the virtual environment: `.venv\Scripts\activate`
- Reinstall packages: `pip install -r requirements.txt`

#### 4. "API quota exceeded"
- You've hit the free tier limits (15/minute, 1500/day)
- Wait a few minutes or try again tomorrow
- Consider upgrading to paid tier for higher limits

#### 5. "Email delivery failed"
- Check your internet connection
- Verify Gmail SMTP settings
- Make sure recipient email is valid

### Testing Your Setup

1. **Test Google AI connection**:
   ```bash
   python -c "from src.blog_generator import LinkedInBlogGenerator; g = LinkedInBlogGenerator(); print('Google AI connection: OK')"
   ```

2. **Test email connection**:
   ```bash
   python -c "from src.email_sender import EmailSender; e = EmailSender(); print('Email connection:', 'OK' if e.test_connection() else 'Failed')"
   ```

## 📊 Cost Information

### Google AI SDK - FREE TIER
- **Cost**: $0 (completely free)
- **Limits**: 15 requests/minute, 1,500 requests/day
- **Perfect for**: Personal projects, learning, small-scale automation

### Paid Tier (if needed later)
- **Cost**: $0.000125 per 1K characters (input) + $0.000375 per 1K characters (output)
- **Example**: A 500-word blog post costs approximately $0.002-0.005
- **Very affordable** for professional use

### Email Sending
- **Cost**: Free (uses your existing Gmail account)
- **Limits**: Gmail's standard sending limits apply

## 🔧 Advanced Configuration

### Custom Prompts
Edit `src/blog_generator.py` to customize the blog generation prompts:
```python
# Modify the _create_blog_prompt method for custom templates
```

### Email Templates
Edit `src/email_sender.py` to customize email formatting:
```python
# Modify _create_email_body or _create_html_body methods
```

### Scheduling (Optional)
Add a scheduler to run the agent automatically:
```python
import schedule
import time

def run_daily_blog():
    agent = LinkedInBlogAgent()
    agent.generate_and_send_blog("Daily Industry Insights")

schedule.every().day.at("09:00").do(run_daily_blog)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🎯 Next Steps

1. **Start with the interactive mode** to get familiar with the agent
2. **Generate a few test blog posts** to see how it works
3. **Customize the prompts** for your specific needs
4. **Set up automated scheduling** if desired
5. **Explore the Google AI SDK documentation** for advanced features

## 📚 Additional Resources

- **Google AI Documentation**: https://ai.google.dev/
- **Gmail App Passwords**: https://support.google.com/accounts/answer/185833
- **Python SMTP Guide**: https://docs.python.org/3/library/smtplib.html