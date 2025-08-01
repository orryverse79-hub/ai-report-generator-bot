# modules/gpt_handler.py
import openai

# 🔐 Replace the placeholder string below with your own OpenAI API key
OPENAI_API_KEY = "REPLACE_ME_WITH_YOUR_API_KEY"

if OPENAI_API_KEY == "REPLACE_ME_WITH_YOUR_API_KEY":
    print("⚠️ WARNING: Please replace the placeholder API key in gpt_handler.py before using GPT features.")

openai.api_key = OPENAI_API_KEY

def gpt_summary(text):
    if OPENAI_API_KEY == "REPLACE_ME_WITH_YOUR_API_KEY":
        return "⚠️ GPT API key not found. Please open `gpt_handler.py` and paste your OpenAI key."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Summarize this content:\n{text}"}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ GPT Error: {str(e)}"
