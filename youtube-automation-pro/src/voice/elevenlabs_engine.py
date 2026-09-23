"""
ElevenLabs Hyper-Realistic Voice & Sound Effects Engine.
Includes automatic fallback to Microsoft Edge TTS if API key is not present.
"""

import os
import requests
import asyncio
from pathlib import Path
from src.config import ProConfig

class ElevenLabsEngine:
    def __init__(self, api_key: str = None, voice_id: str = None):
        self.api_key = api_key or ProConfig.ELEVENLABS_API_KEY
        self.voice_id = voice_id or ProConfig.ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM" # Default: Rachel
        self.base_url = "https://api.elevenlabs.io/v1"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate_speech(self, text: str, output_path: str, model_id: str = "eleven_multilingual_v2") -> str:
        """Generates voiceover using ElevenLabs API or falls back to Edge-TTS."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_available():
            print("⚠️ ElevenLabs API key not detected. Falling back to Edge-TTS...")
            return self._fallback_edge_tts(text, output_path)

        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.35,
                "use_speaker_boost": True
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"🎙️ [ElevenLabs] Speech saved: {output_path}")
                return output_path
            else:
                print(f"⚠️ ElevenLabs API returned {response.status_code}: {response.text}")
                print("Falling back to Edge-TTS...")
                return self._fallback_edge_tts(text, output_path)
        except Exception as e:
            print(f"⚠️ ElevenLabs generation error: {e}. Falling back to Edge-TTS...")
            return self._fallback_edge_tts(text, output_path)

    def generate_sfx(self, prompt: str, output_path: str, duration_seconds: float = 2.5) -> str:
        """Generates contextual AI sound effect using ElevenLabs SFX API."""
        if not self.is_available():
            print(f"ℹ️ ElevenLabs SFX skipped (No key). Using silent stub for {prompt}")
            return ""

        url = f"{self.base_url}/sound-effects"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": prompt,
            "duration_seconds": duration_seconds,
            "prompt_influence": 0.3
        }

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                print(f"🔊 [ElevenLabs SFX] Sound effect saved: {output_path}")
                return output_path
        except Exception as e:
            print(f"⚠️ SFX generation failed: {e}")
        return ""

    def _fallback_edge_tts(self, text: str, output_path: str, voice: str = "en-US-ChristopherNeural") -> str:
        """Free high-quality fallback using edge-tts."""
        import edge_tts
        
        async def _run():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            
        asyncio.run(_run())
        print(f"🎙️ [Edge-TTS Fallback] Speech saved: {output_path}")
        return output_path
