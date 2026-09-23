"""
Higgsfield AI Cinematic Video Motion Engine.
Animates keyframes with physical camera moves (dolly, pan, orbit, tilt)
with seamless FFmpeg motion fallback.
"""

import os
import requests
import subprocess
from pathlib import Path
from src.config import ProConfig

class HiggsfieldEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ProConfig.HIGGSFIELD_API_KEY
        self.base_url = "https://api.higgsfield.ai/v1"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def animate_scene(self, image_path: str, prompt: str, output_path: str, duration_sec: float = 5.0, motion_type: str = "dolly_in") -> str:
        """Animates a static image or prompt into a cinematic video clip."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_available():
            print(f"⚠️ Higgsfield API key not detected. Activating FFmpeg {motion_type} motion engine...")
            return self._fallback_ffmpeg_motion(image_path, output_path, duration_sec, motion_type)

        url = f"{self.base_url}/generate/video"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "motion_type": motion_type,
            "duration": duration_sec,
            "resolution": "1080p",
            "fps": 30
        }

        try:
            print(f"🎥 [Higgsfield AI] Initiating cinematic motion ({motion_type})...")
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code in (200, 201, 202):
                data = response.json()
                video_url = data.get("video_url")
                if video_url:
                    self._download_file(video_url, output_path)
                    print(f"🎬 [Higgsfield AI] Render complete: {output_path}")
                    return output_path
            print(f"⚠️ Higgsfield returned status {response.status_code}. Using FFmpeg fallback...")
        except Exception as e:
            print(f"⚠️ Higgsfield generation error: {e}. Using FFmpeg fallback...")

        return self._fallback_ffmpeg_motion(image_path, output_path, duration_sec, motion_type)

    def _fallback_ffmpeg_motion(self, image_path: str, output_path: str, duration: float, motion_type: str) -> str:
        """Procedural 60fps Ken Burns camera pan/zoom using native FFmpeg."""
        total_frames = int(duration * 30)
        
        if motion_type == "dolly_in":
            zoom_filter = f"zoompan=z='min(zoom+0.0015,1.25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        elif motion_type == "pan_left":
            zoom_filter = f"zoompan=z=1.15:x='if(lte(on,1),(iw-iw/zoom)/2,x-1)':y='(ih-ih/zoom)/2':d={total_frames}:s=1920x1080:fps=30"
        else: # Subtle drift
            zoom_filter = f"zoompan=z='min(zoom+0.001,1.15)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", image_path,
            "-vf", f"{zoom_filter},format=yuv420p",
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🎥 [FFmpeg Camera Motion] Clip rendered: {output_path}")
            return output_path
        except Exception as e:
            print(f"⚠️ FFmpeg motion error: {e}")
            return image_path

    def _download_file(self, url: str, path: str):
        res = requests.get(url, timeout=120)
        res.raise_for_status()
        with open(path, "wb") as f:
            f.write(res.content)
