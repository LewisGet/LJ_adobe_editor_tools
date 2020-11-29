import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.oauth2 import service_account

# api keys
api_keys = service_account.Credentials.from_service_account_file('project-keys.json')

# Instantiates a client
client = speech.SpeechClient(credentials=api_keys)

# The name of the audio file to transcribe
file_name = os.path.join("resource", "pre_vc2_org", "1598700665.729779-1598700013.6414268.wav")

with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="zh-TW",
)

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
