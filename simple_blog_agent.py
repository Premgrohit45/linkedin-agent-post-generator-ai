"""
Simple LinkedIn Blog Generator - No Email Required
Run this to generate blogs without email setup.
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append('src')
from blog_generator import LinkedInBlogGenerator

def main():
    print("🚀 LinkedIn Blog Agent - Simple Mode")
    print("=" * 40)
    print("Generate professional LinkedIn blog posts using AI!")
    print("No email setup required - posts will be saved to files.")
    print()
    
    try:
        generator = LinkedInBlogGenerator()
        print("✅ Blog generator initialized successfully!")
        print()
        
        # Create output directory
        os.makedirs('output', exist_ok=True)
        
        while True:
            print("Options:")
            print("1. Generate blog post")
            print("2. Get topic suggestions") 
            print("3. Exit")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                generate_blog(generator)
            elif choice == '2':
                get_suggestions(generator)
            elif choice == '3':
                print("👋 Thanks for using LinkedIn Blog Agent!")
                break
            else:
                print("Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"❌ Error initializing generator: {str(e)}")
        print("Make sure your GOOGLE_API_KEY is set in the .env file")

def generate_blog(generator):
    """Generate a single blog post."""
    topic = input("\nEnter blog topic: ").strip()
    if not topic:
        print("Topic cannot be empty!")
        return
    
    # Get optional settings
    tone = input("Enter tone (professional/casual/inspirational) [professional]: ").strip() or "professional"
    length = input("Enter length (short/medium/long) [medium]: ").strip() or "medium"
    
    print(f"\n🤖 Generating blog post about: {topic}")
    print(f"   Tone: {tone}, Length: {length}")
    print("   This may take a few seconds...")
    
    try:
        blog = generator.generate_blog_post(
            topic=topic,
            tone=tone, 
            length=length
        )
        
        print("\n📖 Generated Blog Post:")
        print("=" * 50)
        print(f"TITLE: {blog.get('title', 'No title')}")
        print()
        print("CONTENT:")
        print(blog.get('content', 'No content'))
        print()
        print(f"HASHTAGS: {blog.get('hashtags', 'No hashtags')}")
        print()
        print(f"CALL TO ACTION: {blog.get('call_to_action', 'No CTA')}")
        print("=" * 50)
        
        # Save to file
        save_blog_to_file(blog, topic)
        
    except Exception as e:
        print(f"❌ Error generating blog: {str(e)}")

def get_suggestions(generator):
    """Get topic suggestions."""
    industry = input("\nEnter industry/field: ").strip()
    if not industry:
        print("Industry cannot be empty!")
        return
    
    keywords_input = input("Enter keywords (comma-separated, optional): ").strip()
    keywords = [kw.strip() for kw in keywords_input.split(',')] if keywords_input else None
    
    print(f"\n🤖 Getting topic suggestions for {industry}...")
    
    try:
        topics = generator.get_topic_suggestions(industry, keywords)
        
        if topics:
            print(f"\n💡 Suggested Topics for {industry}:")
            print("-" * 40)
            for i, topic in enumerate(topics, 1):
                print(f"{i}. {topic}")
        else:
            print("❌ No topic suggestions generated")
            
    except Exception as e:
        print(f"❌ Error getting suggestions: {str(e)}")

def save_blog_to_file(blog, topic):
    """Save blog post to files."""
    try:
        # Create filename
        safe_topic = topic.replace(' ', '_').replace('/', '_').replace('\\', '_')[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_filename = f"output/blog_{safe_topic}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(blog, f, indent=2, ensure_ascii=False)
        
        # Save readable text
        txt_filename = f"output/blog_{safe_topic}_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {blog.get('title', 'No title')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(blog.get('content', 'No content'))
            f.write(f"\n\nHashtags: {blog.get('hashtags', '')}")
            f.write(f"\n\nCall to Action: {blog.get('call_to_action', '')}")
            f.write(f"\n\n---\nGenerated: {blog.get('generated_at', '')}")
        
        print(f"\n💾 Blog saved successfully!")
        print(f"   📄 JSON: {json_filename}")
        print(f"   📄 Text: {txt_filename}")
        
    except Exception as e:
        print(f"❌ Error saving blog: {str(e)}")

if __name__ == "__main__":
    main()