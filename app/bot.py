import telebot
import os
from dotenv import load_dotenv

from app.handlers.textHandler import register_text_handler
from app.handlers.voiceHandler import register_voice_handler
from app.handlers.imageHandler import register_image_handler
from app.services.database import MessageLog, save_message
from app.services.database import SessionLocal, MessageLog

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# handlers
register_text_handler(bot)
register_voice_handler(bot)
register_image_handler(bot)

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