"""
Test Script for LinkedIn Blog Agent
Run this to verify your setup is working correctly.
"""

import os
import sys
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_environment():
    """Test environment setup and dependencies."""
    print("🔧 Testing Environment Setup...")
    
    # Test imports
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Google Generative AI: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    # Test .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
        load_dotenv()
        
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key and google_key != 'your_google_api_key_here':
            print("✅ Google API key configured")
        else:
            print("⚠️ Google API key not configured in .env file")
        
        email_sender = os.getenv('EMAIL_SENDER')
        if email_sender and '@' in email_sender:
            print("✅ Email sender configured")
        else:
            print("⚠️ Email sender not configured in .env file")
            
    else:
        print("❌ .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    return True

def test_google_ai():
    """Test Google AI SDK connection."""
    print("\n🤖 Testing Google AI SDK Connection...")
    
    try:
        from src.blog_generator import LinkedInBlogGenerator
        
        generator = LinkedInBlogGenerator()
        print("✅ LinkedInBlogGenerator initialized successfully")
        
        # Test a simple generation (this will use your API quota)
        print("🔄 Testing blog generation (this may take a few seconds)...")
        
        blog_post = generator.generate_blog_post(
            topic="Test Topic",
            length="short"
        )
        
        if blog_post and blog_post.get('title'):
            print("✅ Blog generation test successful!")
            print(f"   Generated title: {blog_post.get('title')[:50]}...")
            return True
        else:
            print("❌ Blog generation failed - no content returned")
            return False
            
    except Exception as e:
        print(f"❌ Google AI SDK test failed: {str(e)}")
        if "API_KEY" in str(e):
            print("   → Make sure your Google API key is correctly set in .env file")
        elif "quota" in str(e).lower():
            print("   → You may have exceeded your API quota. Try again later.")
        return False

def test_email():
    """Test email configuration."""
    print("\n📧 Testing Email Configuration...")
    
    try:
        from src.email_sender import EmailSender
        
        email_sender = EmailSender()
        print("✅ EmailSender initialized successfully")
        
        # Test connection (without sending email)
        if email_sender.test_connection():
            print("✅ Email connection test successful!")
            return True
        else:
            print("❌ Email connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        if "EMAIL_SENDER" in str(e) or "EMAIL_PASSWORD" in str(e):
            print("   → Make sure your email credentials are correctly set in .env file")
            print("   → Use a Gmail App Password, not your regular password")
        return False

def test_full_agent():
    """Test the complete agent functionality."""
    print("\n🚀 Testing Complete Agent Functionality...")
    
    try:
        from src.linkedin_blog_agent import LinkedInBlogAgent
        
        agent = LinkedInBlogAgent()
        print("✅ LinkedInBlogAgent initialized successfully")
        
        print("🔄 Testing topic suggestions...")
        topics = agent.get_topic_suggestions("Technology", ["AI", "automation"])
        
        if topics:
            print(f"✅ Topic suggestions generated successfully! ({len(topics)} topics)")
            print(f"   Example topic: {topics[0] if topics else 'None'}")
            return True
        else:
            print("⚠️ No topic suggestions generated (may be an API issue)")
            return False
            
    except Exception as e:
        print(f"❌ Full agent test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧪 LinkedIn Blog Agent - Setup Verification\n")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Run tests
    if test_environment():
        tests_passed += 1
    
    if test_google_ai():
        tests_passed += 1
    
    if test_email():
        tests_passed += 1
        
    if test_full_agent():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your LinkedIn Blog Agent is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Run: python main.py --interactive")
        print("   2. Or run: python main.py --topic 'Your Topic Here'")
    elif tests_passed >= 2:
        print("⚠️ Some tests failed, but basic functionality should work.")
        print("   Check the error messages above for specific issues.")
    else:
        print("❌ Multiple tests failed. Please check your setup.")
        print("   Review the README.md file for detailed setup instructions.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()