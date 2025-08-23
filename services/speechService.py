import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import os

recognizer = sr.Recognizer()

#This will convert voice to text using google stt
def speech_to_text(file_path: str) -> str:
    wav_path = file_path.replace(".ogg", ".wav")
    AudioSegment.from_file(file_path).export(wav_path, format="wav")
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

#This will convert text to speech and return .ogg file path
def text_to_speech(text: str, output_path: str = "response.ogg") -> str:
    tts = gTTS(text = text, lang='en')
    mp3_path = output_path.replace(".ogg", ".mp3")
    tts.save(mp3_path)
    
    #Convertion to ogg
    AudioSegment.from_file(mp3_path).export(output_path, format="ogg")
    return output_path