import os
import base64
import tempfile
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP, Context, Image

from elevenlabs_utils import ElevenLabsClient
from config import ELEVENLABS_VOICE_ID

mcp = FastMCP("Personal VoiceBot")

eleven_client = ElevenLabsClient()

@mcp.tool()
def text_to_speech(text: str, voice_id: str) -> Dict[str, Any]:
    """
    Convert text to speech using ElevenLabs API
    
    Args:
        text: The text to convert to speech
        voice_id: Voice ID to use (defaults to configured voice)
        
    Returns:
        Dictionary containing status, audio data as base64, and format
    """
    voice_id = ELEVENLABS_VOICE_ID
    
    if not voice_id:
        return {
            "status": "error",
            "message": "No voice ID configured."          
        }
    try:
        audio_data = eleven_client.text_to_speech(text, voice_id)
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "status": "success",
            "audio_base64": audio_base64,
            "format": "mp3"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def speech_to_text(audio_base64: str) -> Dict[str, Any]:
    """
    Convert speech to text using ElevenLabs API
    
    Args:
        audio_base64: Base64-encoded audio data
        
    Returns:
        Dictionary containing status and transcribed text
    """
    try:
        audio_data = base64.b64decode(audio_base64)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name        
        
        with open(temp_file_path, 'rb') as f:
            transcription = eleven_client.speech_to_text(f.read())
        
        os.unlink(temp_file_path)
        
        return {
            "status": "success",
            "text": transcription
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def list_elevenlabs_voices() -> Dict[str, Any]:
    """
    List all available voices from ElevenLabs
    
    Returns:
        Dictionary containing status and list of voices
    """
    try:
        voices = eleven_client.list_voices()
        return {
            "status": "success",
            "voices": voices
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.prompt()
def conversation(context: Context, history: str, user_input: str) -> str:
    """
    Continues a natural conversation based on chat history and user input.
    """
    return f"""
    Conversation so far:
    {history}

    User just said:
    {user_input}

    Your reply:
    """

if __name__ == "__main__":
    mcp.run()

