---
name: youtube-kids-automation
description: Autonomous broadcast-grade YouTube channel automation operating system for kids and preschool animation channels. Generates 3D Pixar-clay characters, high-retention toddler scripts, authentic neural child voiceovers, dynamic animated Ken Burns scenes with synchronized cartoon SFX, zero-overlap ASS subtitles, vidIQ 96-score SEO metadata, and 100-day automated scheduled publishing via YouTube Data API v3.
compatibility: Python 3.10+, FFmpeg with libass, Node.js 18+, YouTube Data API v3
metadata:
  standard: "agentskills.io"
  version: "1.0.0"
  author: "Antigravity & ABC Zoo TV"
---

# YouTube Kids Channel Automation Engine

An end-to-end autonomous operating system designed for running a high-retention, broadcast-grade preschool and toddler YouTube channel (Letters A–Z, daily habit songs, early learning concepts, and mega compilation binge loops).

---

## ⚡ Triggers & Activation

Activate this skill when:
- The user wants to automate, produce, or scale a YouTube Kids / Preschool / Animation channel.
- The user requests scripts, 3D character IP, or scene prompts for nursery rhymes and alphabet songs.
- The user asks to compose, render, or animate preschool videos in 1080p Landscape (16:9) or Shorts (9:16).
- The user wants authentic neural child voiceovers (`en-US-AnaNeural`) with dynamic sequential audio chaining.
- The user asks to auto-upload or schedule videos on YouTube with vidIQ 96+ SEO metadata and automatic playlist organization.

---

## 🏛️ System Architecture

```
youtube-kids-automation/
├── SKILL.md                          # Master skill instructions and reference
├── pipeline_config.json              # 26-Character mascot IP database, colors, phonics & objects
├── channel_brand_bible.md            # IP guidelines, 3D Pixar-Clay visual tokens, sonic standards
├── 100_video_roadmap.md              # 4-Phase sequential 100-video content calendar
├── kids_script_template.md           # 5-Scene high-retention toddler script formula
└── scripts/
    ├── generate_neural_child_voice.js # Microsoft Edge neural child voice synthesizer (en-US-AnaNeural)
    ├── generate_animated_episode.py   # Multi-layer video compositor (Ken Burns + SFX + zero-overlap ASS)
    ├── upload_to_youtube.py          # Zero-dependency YouTube Data API v3 uploader & playlist router
    └── autonomous_100_days_scheduler.py # 100-Day 2x daily (8 AM & 5 PM) cloud scheduler
```

---

## 🚀 Core Workflows

### 1. 3D Clay-Pixar Visual Asset Generation
All scenes adhere to the channel's fixed aesthetic prompt tokens:
> *"3D Pixar and claymation style, adorable stylized cute baby animal, huge expressive sparkling glass eyes, friendly warm smile, soft rounded geometry, smooth tactile silicone clay texture, bright pastel studio lighting, rim lighting, 8k resolution, cinematic depth of field, vibrant colorful background"*

For each episode, generate:
- `thumbnail_hero.jpg`: Ultra-high CTR thumbnail with golden yellow/cyan contrast borders.
- `scene_01_hook.jpg`: Mascot introduction & letter reveal.
- `scene_02_dancing.jpg`: Action, rhyming dance & interactive "Find the Object" game scene.
- `scene_03_celebration.jpg`: High-five celebration & farewell outro.

### 2. Studio Neural Child Voiceover (`en-US-AnaNeural`)
Authentic child voice synthesis without robotic pitch-shifting:
```bash
node scripts/generate_neural_child_voice.js "episodes/Ep_001_Letter_A" "en-US-AnaNeural"
```
Produces verbatim audio clips (`ana_seg_0.mp3` to `ana_seg_7.mp3`) with verified speech cadence.

### 3. Dynamic Sequential Audio & Video Composition
Renders 1080p Full HD video with **Dynamic Sequential Chaining** to guarantee zero vocal collisions and zero subtitle overlaps:
```bash
python3 scripts/generate_animated_episode.py --episode_dir "episodes/Ep_001_Letter_A" --format both --theme 0
```
- **Sequential Voice Chaining:** Uses `ffprobe` to probe exact segment durations; starts lines sequentially with breathing pauses (`0.60s` for rhymes, `1.35s` for interactive games).
- **Zero-Overlap Subtitles:** Clamps subtitle end time to `min(seg[i]['end'] + 0.3s, seg[i+1]['start'] - 0.15s)` so dialogues never collide on screen.
- **Synchronized Cartoon SFX:** Procedural pop on mascot entrance, chime on letter reveal, boing on dancing verse, and fanfare on celebration.
- **Rotating Subtitle Typography:** Rotates across 10 custom typography designs (`Arial Rounded MT Bold`, `Chalkboard SE`, `Marker Felt`, `Comic Sans MS`, `Arial Black`).

### 4. vidIQ Score 96+ Upload & Automatic Playlist Organization
Uploads video using YouTube Data API v3 with pre-configured OAuth 2.0:
```bash
python3 scripts/upload_to_youtube.py \
  --episode_dir "episodes/Ep_001_Letter_A" \
  --format landscape \
  --privacy unlisted \
  --playlist_id "PLK8H9ffAc9HcY7cafr91S1k3bsZnRB3Xc"
```
- **Title Formula:** `Can You Find the {Object}? | Letter {Letter} Phonics Lesson for Kids | ABC Zoo TV`
- **Shorts Formula:** `Can You Find the {Object}? 🎈 Letter {Letter} Phonics Song #Shorts`
- **SEO Description:** 3 keyword-rich paragraphs targeting `preschool learning`, `kids animation`, and `phonics song`, followed by lyrics, timestamps, and COPPA certification (`madeForKids: true`).
- **Playlist Routing:** Automatically adds Landscape videos to the core learning playlist and Shorts to the shorts playlist.

### 5. 100-Day Autonomous Scheduled Publishing
```bash
python3 scripts/autonomous_100_days_scheduler.py --schedule_next 2
```
Schedules two videos daily on YouTube using native cloud scheduling (`publishAt`):
- **Slot 1 (08:00 AM IST / 02:30 UTC):** Core Long-Form Episode (16:9)
- **Slot 2 (05:00 PM IST / 11:30 UTC):** High-Energy Vertical Short (9:16)
YouTube flips the videos to **Public** automatically at the designated minute without requiring your computer to stay on!
