"""
Configuration helper to support both local .env and Streamlit Cloud secrets
"""
import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

def get_secret(key: str, default=None):
    """
    Get secret from Streamlit secrets or environment variables.
    Prioritizes Streamlit secrets for cloud deployment.
    """
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    
    # Fall back to environment variables (for local development)
    return os.getenv(key, default)
