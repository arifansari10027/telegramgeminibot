import io
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from app.services.geminiService import ask_gemini
from app.services.database import SessionLocal, MessageLog  # ✅ import DB session + model


def register_voice_handler(bot):
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        db = SessionLocal()
        try:
            # Download the voice file from Telegram
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Convert OGG to WAV in-memory using pydub
            audio_ogg = io.BytesIO(downloaded_file)
            audio = AudioSegment.from_file(audio_ogg, format="ogg")

            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)

            # Recognize speech using SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            print(f"[VOICE->TEXT] {text}")

            # Ask Gemini for a reply
            reply = ask_gemini(f"User said: {text}. Reply shortly like a chat buddy.")

            # Save to DB (user input + bot reply)
            log = MessageLog(
                user_id=str(message.from_user.id),
                message_type="voice",
                content=f"User: {text}\nBot: {reply}"
            )
            db.add(log)
            db.commit()

            # Convert Gemini reply to speech (TTS)
            tts = gTTS(reply, lang="en")
            voice_io = io.BytesIO()
            tts.write_to_fp(voice_io)
            voice_io.seek(0)

            # Send voice reply back
            bot.send_voice(message.chat.id, voice_io)

            # Also send text reply for clarity
            bot.reply_to(message, reply)

        except Exception as e:
            error_msg = f"Voice processing error: {str(e)}"
            print(f"[ERROR] {error_msg}")
            bot.reply_to(message, error_msg)

        finally:
            db.close()