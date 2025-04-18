import requests
import json
import os
import base64
from config import ELEVENLABS_API_KEY

class ElevenLabsClient:
    BASE_URL = "https://api.elevenlabs.io/v1"
    
    def __init__(self, api_key=ELEVENLABS_API_KEY):
        self.api_key = api_key
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def list_voices(self):
        """List all available voices in your ElevenLabs account"""
        response = requests.get(
            f"{self.BASE_URL}/voices",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list voices: {response.text}")
    
    def get_premade_voices(self):
        """Get list of premade voices available on ElevenLabs"""
        voices = self.list_voices()
        return [v for v in voices.get('voices', []) if not v.get('category') == 'cloned']
        
    def text_to_speech(self, text, voice_id, model_id="eleven_multilingual_v2"):
        """Convert text to speech"""
        url = f"{self.BASE_URL}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.content  
        else:
            raise Exception(f"Text-to-speech failed: {response.text}")
    
    def speech_to_text(self, audio_data):
        """Convert speech to text using ElevenLabs API"""
        url = f"{self.BASE_URL}/speech-recognition"
        
        files = {
            'audio': ('audio.mp3', audio_data, 'audio/mpeg')
        }
        
        headers = {"xi-api-key": self.api_key}
        
        response = requests.post(
            url,
            headers=headers,
            files=files
        )
        
        if response.status_code == 200:
            return response.json().get('text', '')
        else:
            raise Exception(f"Speech-to-text failed: {response.text}")
