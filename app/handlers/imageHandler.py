from app.services.geminiService import ask_gemini_with_image
from app.services.database import SessionLocal, MessageLog

def register_image_handler(bot):
    @bot.message_handler(content_types=['photo', 'document'])
    def handle_image(message):
        db = SessionLocal()
        try:
            user_prompt = (message.caption or "").strip()

            image_bytes = None
            mime_type = "image/jpeg"

            if message.content_type == 'photo':
                # Pick largest resolution photo
                largest = max(message.photo, key=lambda p: (p.file_size or 0))
                file_info = bot.get_file(largest.file_id)
                image_bytes = bot.download_file(file_info.file_path)
                mime_type = "image/jpeg"

            elif message.content_type == 'document':
                doc = message.document
                if not doc.mime_type or not doc.mime_type.startswith("image/"):
                    bot.reply_to(message, "Please send a valid image file.")
                    return
                file_info = bot.get_file(doc.file_id)
                image_bytes = bot.download_file(file_info.file_path)
                mime_type = doc.mime_type

            if not image_bytes:
                bot.reply_to(message, "Couldn't read the image.")
                return

            # Ask Gemini
            answer = ask_gemini_with_image(user_prompt, image_bytes, mime_type)
            bot.reply_to(message, answer)

            # ✅ Save to DB
            log = MessageLog(
                user_id=str(message.from_user.id),
                message_type="image",
                content=f"Prompt: {user_prompt or '[No prompt]'}\nBot: {answer}"
            )
            db.add(log)
            db.commit()

        except Exception as e:
            bot.reply_to(message, "An error occurred while processing the image.")
            print(f"[ERROR] {e}")

        finally:
            db.close()