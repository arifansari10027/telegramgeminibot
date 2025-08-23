import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# For sending text to gemini and getting response
def ask_gemini(user_message: str) -> str:

    system_prompt = (
        "You are a friendly Telegram chat buddy and your name is Nalayak."
        "Always reply in 1-3 sentences, short and casual."
        "like you're texting a friend. Avoid sounding like AI and giving very long answers."
    )

    response = model.generate_content(f"{system_prompt}\nUser: {user_message}\nNalayak:")
    return response.text.strip()