"""
Suno AI Custom Soundtrack & Score Generation Engine.
Generates full instrumental background audio matching the niche mood.
"""

import os
import requests
import subprocess
from pathlib import Path
from src.config import ProConfig

class SunoAIEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ProConfig.SUNO_API_KEY
        self.base_url = "https://api.suno.ai/v1"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def generate_soundtrack(self, prompt: str, output_path: str, duration_sec: float = 60.0, genre: str = "cinematic_ambient") -> str:
        """Generates tailored background music via Suno AI API or procedural synth."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_available():
            print(f"⚠️ Suno AI credentials not detected. Generating procedural background audio for {genre}...")
            return self._fallback_procedural_audio(output_path, duration_sec)

        url = f"{self.base_url}/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": f"{genre}, instrumental, atmospheric, high-production background score for documentary: {prompt}",
            "make_instrumental": True,
            "wait_audio": True
        }

        try:
            print(f"🎵 [Suno AI] Composing custom soundtrack ({genre})...")
            response = requests.post(url, json=payload, headers=headers, timeout=90)
            if response.status_code in (200, 201):
                data = response.json()
                audio_url = data.get("audio_url") or data.get("tracks", [{}])[0].get("audio_url")
                if audio_url:
                    self._download_file(audio_url, output_path)
                    print(f"🎧 [Suno AI] Soundtrack saved: {output_path}")
                    return output_path
        except Exception as e:
            print(f"⚠️ Suno AI error: {e}")

        return self._fallback_procedural_audio(output_path, duration_sec)

    def _fallback_procedural_audio(self, output_path: str, duration: float) -> str:
        """Generates a pleasant, subtle ambient chord tone using FFmpeg synth."""
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=220:duration={duration}",
            "-af", "volume=0.08,afade=t=in:ss=0:d=2,afade=t=out:st={}:d=2".format(max(0, duration - 2)),
            "-c:a", "libmp3lame",
            output_path
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🎵 [Procedural Audio] Ambient soundtrack saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"⚠️ Audio synth error: {e}")
            return ""

    def _download_file(self, url: str, path: str):
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        with open(path, "wb") as f:
            f.write(res.content)
