
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

audio = open("Recording.mp3","rb")

output = client.audio.translations.create(
        model="whisper-1",
        file=audio
    )
print(output)
print(output.text)