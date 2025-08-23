import os
from services.geminiService import ask_gemini
from services.speechService import speech_to_text, text_to_speech
from telebot import TeleBot

def register_voice_handler(bot: TeleBot):
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_path = "user_voice.ogg"
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)

        try:
            #voice to text
            user_text = speech_to_text(file_path)
            print(f"[USER VOICE] {user_text}")

            #Asking gemini
            answer = ask_gemini(user_text)
            print(f"[GEMINI] {answer}")

            # Text to voice
            response_path = text_to_speech(answer, "bot_response.ogg")
            with open(response_path, 'rb') as f:
                bot.send_voice(message.chat.id, f)

        except Exception as e:
            bot.reply_to(message, f"Error: {str(e)}")