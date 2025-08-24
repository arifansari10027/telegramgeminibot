import telebot
import os
from dotenv import load_dotenv

from app.handlers.textHandler import register_text_handler
from app.handlers.voiceHandler import register_voice_handler
from app.handlers.imageHandler import register_image_handler
from app.services.database import save_message

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# handlers
register_text_handler(bot)
register_voice_handler(bot)
register_image_handler(bot)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    bot.infinity_polling()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am Nalayak but I am very layak :)")

@bot.message_handler(commands=['image'])
def image(message):
    bot.reply_to(message, "Please send me an image.")

print("Bot is running...")
bot.polling()