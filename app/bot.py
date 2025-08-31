import telebot
import os
from dotenv import load_dotenv

from app.handlers.textHandler import register_text_handler
from app.handlers.voiceHandler import register_voice_handler
from app.handlers.imageHandler import register_image_handler
from app.services.database import MessageLog, save_message
from app.services.database import SessionLocal, MessageLog
from app.handlers.urlHandler import register_url_handler 
from app.services.shortenerService import shorten_url

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# handlers
register_text_handler(bot)
register_voice_handler(bot)
register_image_handler(bot)
register_url_handler(bot)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am Nalayak but I am very layak :)")

@bot.message_handler(commands=['image'])
def image(message):
    bot.reply_to(message, "Please send me an image.")

@bot.message_handler(commands=['help'])
def help_cmd(message):
        bot.reply_to(message,
            "📌 Available Commands:\n"
            "/start - Welcome message\n"
            "/help - Show this help menu\n"
            "/history - Show your last 5 chats"
        )

@bot.message_handler(commands=["shorten"])
def handle_shorten(message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Usage: /shorten <URL>")
            return

        original_url = parts[1]
        short_url = shorten_url(user_id=str(message.from_user.id), original_url=original_url)
        if short_url:
            bot.reply_to(message, f"✅ Your short link: {short_url}")
        else:
            bot.reply_to(message, "❌ Failed to create short URL. Try again.")
    except Exception as e:
        print(f"[BOT ERROR] {e}")
        bot.reply_to(message, "❌ Error occurred while shortening.")

@bot.message_handler(commands=['history'])
def history_cmd(message):
        db = SessionLocal()
        logs = db.query(MessageLog).filter_by(user_id=str(message.from_user.id)).order_by(MessageLog.created_at.desc()).limit(5).all()
        db.close()

        if not logs:
            bot.reply_to(message, "⚠️ No history found.")
            return

        history_text = "🕘 Your last 5 chats:\n\n"
        for log in reversed(logs):
            history_text += f"👉 {log.message_type.upper()}: {log.content}\n🤖 {log.reply}\n\n"

        bot.reply_to(message, history_text.strip())

def save_message(user_id: int, message_type: str, content: str):
    try:
        db = SessionLocal()
        log = MessageLog(user_id=str(user_id), message_type=message_type, content=content)
        db.add(log)
        db.commit()
        db.refresh(log)
        db.close()

        print(f"[DB] Saved message -> {message_type} from {user_id}")
    except Exception as e:
        print(f"[DB ERROR] {e}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()