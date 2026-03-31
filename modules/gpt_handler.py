# modules/gpt_handler.py
import streamlit as st
from openai import OpenAI

# 🔐 Pull the GitHub API token securely from Streamlit Secrets
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    # Initialize the client pointing to GitHub's free endpoint
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=GITHUB_TOKEN,
    )
except Exception:
    client = None
    print("⚠️ WARNING: GITHUB_TOKEN not found in Streamlit Secrets.")

def gpt_summary(text):
    if not client:
        return "⚠️ GPT API key not found. Please add GITHUB_TOKEN to Streamlit secrets."

    try:
        # Using gpt-4o-mini as the fast, high-context replacement for gpt-3.5-turbo
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this content:\n{text}"}
            ],
            max_tokens=500 # Slightly increased for better summaries
        )
        # Updated syntax for OpenAI v1.0+
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ GPT Error: {str(e)}"
