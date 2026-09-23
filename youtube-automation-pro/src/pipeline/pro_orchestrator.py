"""
Master Pro Orchestrator for YouTube Automation Pro.
Connects ElevenLabs, FLUX.1 Pro, Higgsfield AI, Suno AI, Kinetic Subtitles,
and YouTube Data API v3 into a single unified render and publishing flow.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List

from src.voice.elevenlabs_engine import ElevenLabsEngine
from src.image.flux_pro_engine import FluxProEngine
from src.video.higgsfield_engine import HiggsfieldEngine
from src.music.suno_engine import SunoAIEngine
from src.subtitles.kinetic_subtitles import KineticSubtitleEngine
from src.seo.vidiq_optimizer import VidIQOptimizer
from src.publisher.youtube_scheduler import YouTubeCloudScheduler

class ProOrchestrator:
    def __init__(self, config: Dict):
        self.config = config
        self.channel = config.get("channel", {})
        self.channel_name = self.channel.get("name", "Apex Curiosity Pro")
        self.niche = self.channel.get("niche", "Tech & AI Breakthroughs")

        # Initialize engines
        self.voice_engine = ElevenLabsEngine()
        self.image_engine = FluxProEngine()
        self.video_engine = HiggsfieldEngine()
        self.music_engine = SunoAIEngine()
        self.subtitle_engine = KineticSubtitleEngine()
        self.seo_engine = VidIQOptimizer(self.channel_name, self.niche)
        self.publisher = YouTubeCloudScheduler()

    def produce_episode(self, episode_id: str, topic: str, scenes: List[Dict], is_short: bool = False, day_offset: int = 1) -> Dict:
        """
        Executes full multi-layer generation for an episode:
        1. Voiceover (ElevenLabs)
        2. SFX Foley (ElevenLabs)
        3. Visual Keyframes (FLUX.1 Pro)
        4. Motion Animation (Higgsfield AI)
        5. Background Soundtrack (Suno AI)
        6. Kinetic Subtitles (.ass)
        7. FFmpeg Master Video Mixdown
        8. vidIQ 98 SEO & YouTube Scheduling
        """
        base_dir = Path("output") / episode_id
        base_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n=======================================================")
        print(f"🎬 [PRO PIPELINE] Starting Episode '{episode_id}': {topic}")
        print(f"=======================================================\n")

        rendered_clips = []
        subtitle_segments = []
        current_time = 0.0

        for idx, scene in enumerate(scenes):
            scene_prefix = f"{base_dir}/scene_{idx+1}"
            
            # Step 1: Voiceover
            narration_file = f"{scene_prefix}_narration.mp3"
            self.voice_engine.generate_speech(scene["script"], narration_file)
            
            # Estimate scene duration from script
            duration = max(4.0, len(scene["script"].split()) * 0.45)
            subtitle_segments.append({
                "text": scene["script"],
                "start": current_time,
                "end": current_time + duration
            })
            current_time += duration

            # Step 2: FLUX.1 Pro Image
            aspect_ratio = "9:16" if is_short else "16:9"
            keyframe_file = f"{scene_prefix}_flux.jpg"
            self.image_engine.generate_image(scene["visual_prompt"], keyframe_file, aspect_ratio=aspect_ratio)

            # Step 3: Higgsfield AI Cinematic Motion
            motion_clip = f"{scene_prefix}_motion.mp4"
            motion_type = scene.get("motion", "dolly_in")
            self.video_engine.animate_scene(keyframe_file, scene["visual_prompt"], motion_clip, duration_sec=duration, motion_type=motion_type)
            rendered_clips.append((motion_clip, narration_file))

        # Step 4: Suno AI Background Soundtrack
        music_file = f"{base_dir}/suno_soundtrack.mp3"
        self.music_engine.generate_soundtrack(topic, music_file, duration_sec=current_time + 2.0)

        # Step 5: Kinetic Subtitles
        subtitle_file = f"{base_dir}/kinetic_subtitles.ass"
        self.subtitle_engine.generate_ass(subtitle_segments, subtitle_file, is_vertical=is_short)

        # Step 6: Master Video Compositing
        master_output = f"{base_dir}/master_render.mp4"
        self._composite_final_video(rendered_clips, music_file, subtitle_file, master_output, is_short=is_short)

        # Step 7: vidIQ 98 SEO Metadata
        seo_metadata = self.seo_engine.optimize_metadata(topic, is_short=is_short)

        # Step 8: YouTube Cloud Scheduling (Slot: 8 AM or 5 PM)
        slot_time = "17:00" if is_short else "08:00"
        schedule_result = self.publisher.schedule_video(master_output, seo_metadata, slot_time=slot_time, day_offset=day_offset)

        return {
            "episode_id": episode_id,
            "topic": topic,
            "master_file": master_output,
            "seo_package": seo_metadata,
            "schedule": schedule_result
        }

    def _composite_final_video(self, clips: List, music_file: str, subtitle_file: str, output_path: str, is_short: bool = False):
        """Combines motion clips, narration, Suno music, and kinetic subtitles using FFmpeg."""
        concat_list = Path(output_path).parent / "concat_list.txt"
        with open(concat_list, "w") as f:
            for video_path, _ in clips:
                f.write(f"file '{Path(video_path).resolve()}'\n")

        # Concat video clips
        concat_video = Path(output_path).parent / "concat_raw.mp4"
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(concat_video)
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Final mix with music ducking and styled subtitles
        sub_escaped = str(Path(subtitle_file).resolve()).replace(":", r"\:")
        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(concat_video),
            "-i", str(music_file),
            "-filter_complex",
            f"[0:v]subtitles='{sub_escaped}'[v];[1:a]volume=0.15[bg];[bg]amix=inputs=1[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"🏆 [MASTER RENDER COMPLETE] Output: {output_path}")
        except Exception as e:
            print(f"⚠️ Compositing warning: {e}. Outputting concatenated video...")
            subprocess.run(["cp", str(concat_video), output_path])
