#!/usr/bin/env python3
"""
Test the improved professional blog generation without asterisks and emojis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.blog_generator import LinkedInBlogGenerator

def test_professional_blog():
    print("🧪 Testing Professional Blog Generation")
    print("=" * 60)
    
    try:
        generator = LinkedInBlogGenerator()
        
        # Generate a sample blog
        blog_post = generator.generate_blog_post(
            topic="The Future of Artificial Intelligence in Business",
            tone="professional",
            length="medium",
            target_audience="business professionals"
        )
        
        print("✅ Blog Generated Successfully!")
        print("=" * 60)
        print(f"📝 TITLE: {blog_post.get('title', 'No title')}")
        print("=" * 60)
        print(f"📄 CONTENT:\n{blog_post.get('content', 'No content')}")
        print("=" * 60)
        print(f"🏷️ HASHTAGS: {blog_post.get('hashtags', 'No hashtags')}")
        print("=" * 60)
        print(f"📢 CALL TO ACTION: {blog_post.get('call_to_action', 'No CTA')}")
        print("=" * 60)
        
        # Check for unwanted formatting
        content_check = blog_post.get('content', '')
        asterisk_count = content_check.count('*')
        emoji_pattern = r'[🎯📝💡🚀✨🔥💪🌟📈⭐️]'
        
        import re
        emoji_matches = len(re.findall(emoji_pattern, content_check))
        
        print(f"📊 QUALITY CHECK:")
        print(f"   Asterisks found: {asterisk_count}")
        print(f"   Emojis found: {emoji_matches}")
        print(f"   Content length: {len(content_check)} characters")
        
        if asterisk_count == 0 and emoji_matches == 0:
            print("✅ PROFESSIONAL FORMATTING: PASSED")
        else:
            print("⚠️ PROFESSIONAL FORMATTING: NEEDS IMPROVEMENT")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_professional_blog()