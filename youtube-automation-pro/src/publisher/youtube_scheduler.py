"""
Autonomous 100-Day YouTube Cloud Scheduler (Data API v3).
Uploads videos with publishAt timestamp for automatic cloud publishing (8 AM & 5 PM).
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

class YouTubeCloudScheduler:
    def __init__(self, client_secrets_file: str = "client_secrets.json", token_file: str = "token.json"):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file

    def is_configured(self) -> bool:
        return Path(self.client_secrets_file).exists()

    def schedule_video(self, video_path: str, metadata: Dict, slot_time: str = "08:00", day_offset: int = 1) -> Dict:
        """
        Uploads and schedules video for automatic publication at specified time in YouTube cloud.
        """
        target_date = datetime.now() + timedelta(days=day_offset)
        hour, minute = map(int, slot_time.split(":"))
        publish_time = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        publish_at_iso = publish_time.isoformat() + "Z"

        if not self.is_configured():
            print(f"ℹ️ [Dry Run] YouTube OAuth secrets ({self.client_secrets_file}) not found.")
            print(f"📅 Simulated Schedule: '{metadata['title']}' for {publish_at_iso} in playlist '{metadata['playlist']}'")
            return {
                "status": "simulated",
                "video_id": f"sim_{day_offset}_{slot_time.replace(':', '')}",
                "publish_at": publish_at_iso,
                "title": metadata["title"]
            }

        # Google API execution
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials

        creds = Credentials.from_authorized_user_file(self.token_file, ["https://www.googleapis.com/auth/youtube.upload"])
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": metadata["title"],
                "description": metadata["description"],
                "tags": metadata.get("tags", []),
                "categoryId": metadata.get("category_id", "28")
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_at_iso,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"✅ Video scheduled in YouTube Cloud! ID: {video_id} (Publishes at: {publish_at_iso})")
        return response
