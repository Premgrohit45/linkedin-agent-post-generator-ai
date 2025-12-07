#!/usr/bin/env python3
"""
Quick test to generate a sample blog and show the improved formatting
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.blog_generator import LinkedInBlogGenerator

def test_blog_generation():
    print("🤖 Testing Blog Generation with Improved Formatting")
    print("=" * 60)
    
    generator = LinkedInBlogGenerator()
    
    # Generate a sample blog
    blog_post = generator.generate_blog_post(
        topic="The Future of Artificial Intelligence in Business",
        tone="professional",
        length="medium",
        target_audience="business professionals"
    )
    
    print("✅ Blog Generated Successfully!")
    print(f"📝 Title: {blog_post.get('title', 'No title')}")
    print(f"📄 Content Length: {len(blog_post.get('content', ''))} characters")
    print(f"🏷️ Hashtags: {blog_post.get('hashtags', 'No hashtags')[:50]}...")
    print(f"📢 CTA: {blog_post.get('call_to_action', 'No CTA')[:50]}...")
    
    print("\n🌐 Open your browser and go to: http://localhost:8502")
    print("🚀 Try generating a blog to see the improved formatting!")
    print("=" * 60)

if __name__ == "__main__":
    test_blog_generation()