import os
import tempfile
import requests
import base64
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from server import conversation, speech_to_text, text_to_speech  
import config

app = Flask(__name__)

# Replace with personal whatsapp number to test
TO_NUMBER = os.getenv("WHATSAPP_VERIFY_NUMBER")  

client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

conversation_history = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    if media_url and media_type.startswith("audio"):
        # Step 1: Download the audio
        audio_response = requests.get(media_url)
        if audio_response.status_code != 200:
            return respond("Failed to download audio")

        audio_data = audio_response.content
        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        stt_result = speech_to_text(audio_b64)
        if stt_result["status"] != "success":
            return respond(f"Speech-to-text failed: {stt_result['message']}")

        transcribed = stt_result["text"]

        history = conversation_history.get(from_number, "")
        conversation_history[from_number] = history + f"\nUser: {transcribed}\n"

        reply = conversation(history=conversation_history[from_number], user_input=transcribed)

        conversation_history[from_number] += f"Claude: {reply}\n"

        response_text = reply

        tts_result = text_to_speech(response_text, config.ELEVENLABS_VOICE_ID)
        if tts_result["status"] != "success":
            return respond(f"Text-To-Speech failed: {tts_result['message']}")

        audio_b64 = tts_result["audio_base64"]
        audio_bin = base64.b64decode(audio_b64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_bin)
            tmp_path = tmp.name

        message = client.messages.create(
            from_= config.TWILIO_WHATSAPP_NUMBER,
            to=from_number,
            media_url=[upload_temp_file_to_twilio(tmp_path)]
        )

        return respond("Sent back voice message!")

    else:
        return respond("Please send a voice message.")

def upload_temp_file_to_twilio(path):
    with open(path, "rb") as f:
        r = requests.post("https://file.io", files={"file": f})
        if r.status_code == 200:
            return r.json()["link"]
        else:
            raise Exception("Failed to upload audio file")

def respond(msg):
    resp = MessagingResponse()
    resp.message(msg)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5003)

