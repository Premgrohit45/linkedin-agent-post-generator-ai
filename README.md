# 💼 LinkedGenius - AI LinkedIn Content Creator

Generate professional LinkedIn blog posts with AI and send them via email.

## ✨ Features
- 🤖 AI-Powered (Google Gemini 2.5-Flash)
- 🎨 Modern Dark UI
- 📧 Email Distribution
- ⚙️ Customizable tone, length, audience
- 📊 Analytics Dashboard

## 🚀 Deploy to Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. New app → Select your fork
4. Main file: `streamlit_app_modern.py`
5. Add secrets (Advanced settings):
```toml
GOOGLE_API_KEY = "your_key"
EMAIL_SENDER = "your@gmail.com"
EMAIL_PASSWORD = "app_password"
EMAIL_RECIPIENT = "recipient@gmail.com"
```
6. Deploy!

## 🔑 Get API Keys

**Google AI:** [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
**Gmail App Password:** [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

## 💻 Local Setup

```bash
git clone https://github.com/yourusername/linkedin-agent.git
cd linkedin-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
streamlit run streamlit_app_modern.py
```

## 📖 Usage

1. Enter topic
2. Choose settings
3. Generate
4. Send email

Made with ❤️ and AI
