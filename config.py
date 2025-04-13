import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")  # We'll set this after creating a voice
