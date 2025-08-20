import telebot
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)  

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am Nalayak but I am very layak :)")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    question = message.text
    print(f"[USER] {message.from_user.username or message.chat.id}: {question}")

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )
        answer = response.text.strip()
        print(f"[GEMINI] {answer}\n")
        bot.reply_to(message, answer)

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[ERROR] {error_msg}")
        bot.reply_to(message, error_msg)

print("Bot started.........")
bot.polling()
