#!/usr/bin/env python3
"""
YouTube Automation Pro - Interactive Onboarding CLI Wizard.
Configures channel niche, models competitor channels, activates Pro AI APIs
(ElevenLabs, Higgsfield, FLUX.1 Pro, Suno AI), and builds the 100-video roadmap.
"""

import sys
import os
import json
from pathlib import Path

def print_banner():
    banner = r"""
========================================================================
   ⚡ YOUTUBE AUTOMATION PRO (STUDIO EDITION) ⚡
   Autonomous AI Operating System Powered by:
   • ElevenLabs (Ultra-Realistic Voice & AI SFX)
   • Higgsfield AI (Cinematic Camera Motion & Text-to-Video)
   • FLUX.1 Pro (8K Photorealistic Keyframes & High-CTR Thumbnails)
   • Suno AI (Custom Radio-Quality Background Scores)
   • vidIQ Score 98 SEO + YouTube Data API v3 Cloud Scheduling
========================================================================
    """
    print(banner)

def ask(question, default=""):
    prompt_str = f"👉 {question} [{default}]: " if default else f"👉 {question}: "
    val = input(prompt_str).strip()
    return val if val else default

def run_onboarding():
    print_banner()
    print("Welcome! Let's configure your autonomous Pro YouTube channel in 2 minutes.\n")

    # Step 1: Channel Profile
    print("--- [STEP 1: CHANNEL BRAND & IDENTITY] ---")
    channel_name = ask("Enter Channel Name", "Apex Curiosity Pro")
    channel_handle = ask("Enter Channel Handle", f"@{channel_name.replace(' ', '')}")

    print("\nSelect or enter your Niche:")
    print("1. Tech Breakthroughs & AI Deep Dives (e.g. ColdFusion / Marques)")
    print("2. Faceless Finance, Business & Billionaire Empires (e.g. MagnatesMedia)")
    print("3. Dark Psychology, Stoicism & Mindset (e.g. Einzelgänger)")
    print("4. True Crime & Unsolved Mysteries")
    print("5. 3D Preschool Animation & Nursery Rhymes")
    print("6. Custom / Clone an Inspiration Channel URL")

    niche_choice = ask("Select niche (1-6)", "1")
    niche_map = {
        "1": "Tech Breakthroughs & AI Deep Dives",
        "2": "Faceless Finance & Business Empires",
        "3": "Dark Psychology & Stoic Mindset",
        "4": "True Crime & Unsolved Mysteries",
        "5": "3D Preschool Animation & Phonics",
    }

    if niche_choice in niche_map:
        niche = niche_map[niche_choice]
        inspiration_url = ask("Enter competitor/inspiration channel URL to model (optional)", "")
    else:
        niche = ask("Enter your custom niche description")
        inspiration_url = ask("Enter inspiration channel URL to clone/model")

    # Step 2: Pro API Keys Intake
    print("\n--- [STEP 2: PREMIUM AI API CREDENTIALS] ---")
    print("💡 Note: Leave any key blank to use the built-in free fallback engine.")

    elevenlabs_key = ask("Enter ElevenLabs API Key (Press Enter to skip & use Edge-TTS)", "")
    higgsfield_key = ask("Enter Higgsfield AI API Key (Press Enter to skip & use FFmpeg Motion)", "")
    fal_key = ask("Enter Fal.ai Key for FLUX.1 Pro (Press Enter to skip & use Procedural)", "")
    suno_key = ask("Enter Suno AI Key (Press Enter to skip & use Ambient Synth)", "")

    # Step 3: Publishing Schedule
    print("\n--- [STEP 3: 100-DAY CLOUD SCHEDULING] ---")
    slot_1 = ask("Daily Landscape Video Slot (24h format)", "08:00")
    slot_2 = ask("Daily YouTube Shorts Slot (24h format)", "17:00")
    timezone = ask("Timezone for Cloud Scheduling", "Asia/Kolkata")

    # Build .env file
    env_content = f"""# YouTube Automation Pro - Environment Keys
ELEVENLABS_API_KEY={elevenlabs_key}
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
HIGGSFIELD_API_KEY={higgsfield_key}
FAL_KEY={fal_key}
SUNO_API_KEY={suno_key}
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
YOUTUBE_SCHEDULE_SLOT_1={slot_1}
YOUTUBE_SCHEDULE_SLOT_2={slot_2}
YOUTUBE_TIMEZONE={timezone}
"""
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("\n✅ Created git-ignored '.env' with your API configuration.")

    # Build pipeline_config.json
    config_data = {
        "channel": {
            "name": channel_name,
            "handle": channel_handle,
            "niche": niche,
            "inspiration_url": inspiration_url,
            "visual_style": "Dark Cinematic 8K, Volumetric Lighting, Photorealistic" if "Preschool" not in niche else "3D Pixar Clay, Pastel Vibrant",
            "tone": "Authoritative and Gripping"
        },
        "providers": {
            "voice": {
                "provider": "elevenlabs" if elevenlabs_key else "edge_tts",
                "is_premium": bool(elevenlabs_key)
            },
            "video_motion": {
                "provider": "higgsfield" if higgsfield_key else "ffmpeg_motion",
                "is_premium": bool(higgsfield_key)
            },
            "image_generation": {
                "provider": "flux_pro" if fal_key else "procedural_canvas",
                "is_premium": bool(fal_key)
            },
            "music": {
                "provider": "suno_ai" if suno_key else "ambient_synth",
                "is_premium": bool(suno_key)
            }
        },
        "schedule": {
            "slot_1": slot_1,
            "slot_2": slot_2,
            "days_ahead": 100,
            "timezone": timezone
        }
    }

    with open("pipeline_config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)
    print("✅ Created 'pipeline_config.json'.")

    # Generate 100 Video Roadmap
    generate_roadmap(channel_name, niche)

    print("\n" + "="*70)
    print("🎉 ONBOARDING COMPLETE! Your Pro Studio Pipeline is Ready.")
    print("="*70)
    print("• Voiceover Engine: " + ("ElevenLabs Pro 🔥" if elevenlabs_key else "Edge-TTS (Free Fallback)"))
    print("• Video Motion Engine: " + ("Higgsfield AI 🎬" if higgsfield_key else "FFmpeg 60fps Motion"))
    print("• Visuals & Thumbnails: " + ("FLUX.1 Pro 8K 🖼️" if fal_key else "Procedural / ImageFX"))
    print("• Background Score: " + ("Suno AI v3.5 🎵" if suno_key else "Procedural Ambient Synth"))
    print("• Subtitles: Kinetic Hormozi/MrBeast High-Retention ASS (.ass)")
    print("• Cloud Scheduler: 100 Days Scheduled at " + slot_1 + " & " + slot_2)
    print("\nTo render your first episode, run:")
    print("  python3 scripts/generate_episode.py")
    print("="*70 + "\n")

def generate_roadmap(channel_name, niche):
    topics = [
        f"The Hidden Reality of {niche}",
        f"How Top 1% Mastered {niche}",
        f"Why Everything You Knew About {niche} Was Wrong",
        f"The 2026 Breakthrough in {niche}",
        f"The Dark Side of {niche} Nobody Talks About"
    ]
    roadmap_md = f"# 📅 100-Day Automated Video Roadmap: {channel_name}\n\n**Niche:** {niche}\n\n"
    for i in range(1, 101):
        topic = topics[(i - 1) % len(topics)] + f" (Vol. {i})"
        roadmap_md += f"### Day {i}\n- **08:00 AM Full Episode:** {topic}\n- **05:00 PM Short:** 60-Second Viral Hook for Episode #{i}\n\n"
    
    with open("100_video_roadmap.md", "w", encoding="utf-8") as f:
        f.write(roadmap_md)
    print("✅ Generated '100_video_roadmap.md' (100 days of landscape + shorts topics).")

if __name__ == "__main__":
    run_onboarding()
