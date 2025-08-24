import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# System style prompt (used by both text + image queries)
SYSTEM_STYLE = (
    "You are a friendly Telegram chat buddy and your name is Nalayak. "
    "Always reply in 1-3 sentences, short and casual, like you're texting a friend. "
    "Avoid sounding like AI and giving very long answers."
)

# --- For sending text ---
def ask_gemini(user_message: str) -> str:
    try:
        response = model.generate_content(f"{SYSTEM_STYLE}\nUser: {user_message}\nNalayak:")
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# --- For sending image + text ---
def ask_gemini_with_image(user_prompt: str | None, image_bytes, mime_type: str = "image/jpeg") -> str:
    try:
        parts = [
            SYSTEM_STYLE,
            user_prompt.strip() if user_prompt else "Describe the image briefly.",
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64.b64encode(image_bytes).decode("utf-8")
                }
            }
        ]
        response = model.generate_content(parts)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
