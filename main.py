"""
LinkedIn Blog Agent - Main Entry Point
Run this file to start the LinkedIn Blog Agent.
"""

import sys
import os

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main agent
from src.linkedin_blog_agent import main

if __name__ == "__main__":
    main()