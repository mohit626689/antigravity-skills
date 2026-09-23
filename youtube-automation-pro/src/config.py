"""
Configuration Loader & Environment Manager for YouTube Automation Pro.
Handles API credentials, fallback routing, and channel parameters.
Zero-dependency native .env loader with python-dotenv support.
"""

import os
import json
from pathlib import Path

# Base Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "pipeline_config.json"
EXAMPLE_CONFIG_PATH = BASE_DIR / "pipeline_config.example.json"
ENV_PATH = BASE_DIR / ".env"

def _load_env_native(filepath: Path):
    """Parses .env file natively without requiring third-party libraries."""
    if not filepath.exists():
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = val

try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=ENV_PATH)
except ImportError:
    _load_env_native(ENV_PATH)

class ProConfig:
    """Manages API keys, provider configurations, and fallbacks."""
    
    # API Keys
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY", "")
    
    FAL_KEY = os.getenv("FAL_KEY", "")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
    
    SUNO_API_KEY = os.getenv("SUNO_API_KEY", "")
    
    YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    
    @classmethod
    def load_pipeline_config(cls) -> dict:
        """Loads user pipeline_config.json or falls back to example."""
        target_path = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_CONFIG_PATH
        if not target_path.exists():
            return {}
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    @classmethod
    def get_provider_status(cls) -> dict:
        """Audits which premium providers are unlocked and active."""
        return {
            "voice": {
                "provider": "ElevenLabs" if cls.ELEVENLABS_API_KEY else "Edge-TTS (Fallback)",
                "is_premium": bool(cls.ELEVENLABS_API_KEY),
            },
            "video_motion": {
                "provider": "Higgsfield AI" if cls.HIGGSFIELD_API_KEY else "FFmpeg Motion (Fallback)",
                "is_premium": bool(cls.HIGGSFIELD_API_KEY),
            },
            "image_generation": {
                "provider": "FLUX.1 Pro" if (cls.FAL_KEY or cls.REPLICATE_API_TOKEN) else "Procedural / ImageFX (Fallback)",
                "is_premium": bool(cls.FAL_KEY or cls.REPLICATE_API_TOKEN),
            },
            "music": {
                "provider": "Suno AI" if cls.SUNO_API_KEY else "Royalty-Free Procedural (Fallback)",
                "is_premium": bool(cls.SUNO_API_KEY),
            }
        }
