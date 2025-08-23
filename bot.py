import telebot
import os
from dotenv import load_dotenv

from handlers.textHandler import register_text_handler
from handlers.voiceHandler import register_voice_handler

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# handlers
register_text_handler(bot)
register_voice_handler(bot)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am Nalayak but I am very layak :)")

print("Bot is running...")
bot.polling()