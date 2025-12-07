"""
Test Dynamic Email Recipients Functionality
Demonstrates the new dynamic email recipient features.
"""

import sys
import os
sys.path.append('src')

from linkedin_blog_agent import LinkedInBlogAgent

def test_dynamic_recipients():
    """Test the dynamic email recipients functionality."""
    
    print("🧪 Testing Dynamic Email Recipients")
    print("=" * 40)
    
    try:
        # Initialize agent
        agent = LinkedInBlogAgent()
        print("✅ Agent initialized successfully")
        
        # Test email validation
        print("\n📧 Testing Email Validation:")
        
        test_emails = [
            "valid@gmail.com",
            "another.valid@company.com", 
            "invalid-email",
            "missing@domain",
            "user@valid-domain.co.uk"
        ]
        
        validation_results = agent.email_sender.validate_recipients(test_emails)
        
        for email, is_valid in validation_results.items():
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"   {email}: {status}")
        
        # Test blog generation with multiple recipients
        print(f"\n🤖 Testing Blog Generation with Multiple Recipients:")
        
        # Use only valid emails for the test
        valid_emails = [email for email, is_valid in validation_results.items() if is_valid]
        print(f"   Using {len(valid_emails)} valid email addresses")
        
        # Generate blog post and send to multiple recipients
        results = agent.generate_and_send_to_multiple_recipients(
            topic="Testing Dynamic Email System",
            recipients=valid_emails,
            tone="professional",
            length="short",
            subject_prefix="Test Blog Post",
            validate_emails=True,
            save_to_file=True
        )
        
        # Display results
        if results['success']:
            print("✅ Blog generation and sending completed!")
            
            # Blog details
            blog_post = results['blog_post']
            print(f"\n📖 Generated Blog:")
            print(f"   Title: {blog_post.get('title')}")
            print(f"   Content length: {len(blog_post.get('content', '').split())} words")
            
            # File saving
            if results.get('file_saved'):
                print(f"   Saved to: {results.get('file_path')}")
            
            # Email results
            email_results = results.get('email_results', {})
            if 'summary' in email_results:
                summary = email_results['summary']
                print(f"\n📧 Email Summary:")
                print(f"   Total recipients: {summary['total_recipients']}")
                print(f"   Valid emails: {summary['valid_emails']}")
                print(f"   Successfully sent: {summary['emails_sent']}")
                print(f"   Failed: {summary['emails_failed']}")
            
        else:
            print("❌ Test failed")
            for error in results.get('errors', []):
                print(f"   Error: {error}")
        
        print(f"\n🎉 Dynamic recipients test completed!")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        print("Make sure your .env file is configured with valid credentials")

def demo_interactive_mode():
    """Demonstrate the interactive mode with dynamic recipients."""
    
    print("\n🎯 Interactive Mode Demo")
    print("=" * 25)
    print("To test the full interactive experience:")
    print("1. Run: python main.py --interactive")
    print("2. Select option 3: 'Generate blog with dynamic recipients'")
    print("3. Follow the prompts to:")
    print("   - Enter blog topic")
    print("   - Choose tone and length") 
    print("   - Add multiple email recipients")
    print("   - See validation results")
    print("   - Confirm and send")

if __name__ == "__main__":
    print("🚀 LinkedIn Blog Agent - Dynamic Email Recipients Test")
    print("=" * 60)
    
    try:
        # Run validation and generation test
        test_dynamic_recipients()
        
        # Show interactive demo instructions
        demo_interactive_mode()
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Make sure your environment is properly configured.")