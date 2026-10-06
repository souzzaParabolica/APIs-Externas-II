from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

texto = input("Digite o texto: ")

audio = client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    text=texto,
    model_id="eleven_multilingual_v2",
    output_format="mp3_22050_32"
)

with open("voz.mp3", "wb") as arquivo:
    for chunk in audio:
        arquivo.write(chunk)

print("Áudio criado com sucesso!")
print("Arquivo: voz.mp3")