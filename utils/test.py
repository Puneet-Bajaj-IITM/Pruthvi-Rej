import os
from openai import OpenAI


os.environ['OPENAI_API_KEY'] = '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'
client = OpenAI()

audio_file_path = 'uploads/audio/ni-i-001.mp3'
os.remove(audio_file_path)
"""
MAX_FILE_SIZE = 1024 * 1024 * 10

with open(audio_file_path, "rb") as audio_file:
    audio_data = audio_file.read(MAX_FILE_SIZE)

partial_file_path = f'uploads/1.mp3'
with open(partial_file_path, "wb") as partial_audio_file:
    partial_audio_file.write(audio_data)

audio_data = open(partial_file_path, "rb")

translation = client.audio.translations.create(
    model="whisper-1",
    file=audio_data
)
print(translation)"""