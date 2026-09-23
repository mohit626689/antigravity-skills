---
name: youtube-automation-pro
description: Studio-grade autonomous YouTube automation operating system powered by ElevenLabs (hyper-realistic voice & SFX), Higgsfield AI (cinematic camera motion & video), FLUX.1 Pro (8K photorealistic keyframes & high-CTR thumbnails), Suno AI (custom radio-quality background scores), kinetic Hormozi subtitles, vidIQ 98 SEO metadata, and 100-day autonomous cloud scheduling (8 AM & 5 PM daily) via YouTube Data API v3.
---

# YouTube Automation Pro (Studio Edition)

Autonomous AI studio engine for producing broadcast-grade YouTube videos for any niche using premium AI tools (with intelligent free fallbacks).

## When to Use This Skill
- Directing, scripting, rendering, and auto-publishing premium YouTube videos.
- Setting up a channel clone modeled after any inspiration YouTube URL.
- Generating hyper-realistic voiceovers with ElevenLabs and context-aware SFX.
- Generating cinematic camera motion with Higgsfield AI.
- Generating 8K photorealistic visuals and high-CTR thumbnails with FLUX.1 Pro.
- Composing custom instrumental soundtracks with Suno AI v3.5.
- Applying kinetic Hormozi/MrBeast word-pop typography via SubStation Alpha (`.ass`).
- Optimizing metadata for vidIQ score 98/100 and routing to playlists.
- Scheduling 100 days of automated uploads (8 AM Landscape & 5 PM Shorts).

---

## 🛠️ CLI Commands & Workflows

### 1. Interactive Pro Onboarding
Run the onboarding wizard to configure the channel brand bible, API credentials, and 100-video roadmap:
```bash
python3 setup.py
```

### 2. Verify AI Provider Status & System Suite
Test FFmpeg, API credentials readiness, subtitle renderers, and vidIQ scorers:
```bash
python3 scripts/test_pro_suite.py
```

### 3. Generate a Single Pro Episode
Renders multi-layer scenes, composites audio ducking, burns kinetic subtitles, and outputs the master video:
```bash
python3 scripts/generate_episode.py
```

---

## 🏗️ Architecture & Engines

### 1. Voice & SFX Engine (`src/voice/elevenlabs_engine.py`)
- Uses ElevenLabs `eleven_multilingual_v2` for emotional delivery.
- Uses ElevenLabs `/v1/sound-effects` for procedural foley audio.
- Fallback: High-fidelity Microsoft Edge-TTS (`ChristopherNeural`, `AnaNeural`).

### 2. Video Motion Engine (`src/video/higgsfield_engine.py`)
- Directs camera trajectories: `dolly_in`, `dolly_zoom`, `pan_left`, `orbit`, `tilt_up`.
- Fallback: Procedural 60fps FFmpeg Ken Burns zoom/pan engine.

### 3. Visuals & Thumbnail Engine (`src/image/flux_pro_engine.py`)
- Dispatches prompts to FLUX.1 Pro via Fal.ai or Replicate.
- Automatically formats aspect ratios (`16:9` landscape, `9:16` Shorts).
- Enforces high-contrast focal rules for YouTube thumbnails.
- Fallback: Procedural gradient canvas / ImageFX.

### 4. Custom Music Engine (`src/music/suno_engine.py`)
- Composes radio-grade instrumental scores matching niche mood and pacing.
- Fallback: Procedural harmonic ambient synth with auto-ducking.

### 5. Kinetic Subtitles (`src/subtitles/kinetic_subtitles.py`)
- MrBeast / Alex Hormozi active word pop typography.
- High-visibility styling with drop shadows and black outlines.
- Sequential clearance buffers to eliminate subtitle collisions.

### 6. vidIQ 98 SEO & Auto-Playlists (`src/seo/vidiq_optimizer.py`)
- Curiosity question hooks for high CTR.
- 3-paragraph search-first descriptions with timestamps.
- Auto-routes to dedicated landscape and Shorts playlists.

### 7. 100-Day Cloud Scheduler (`src/publisher/youtube_scheduler.py`)
- YouTube Data API v3 native `publishAt` automation.
- Slot 1: 08:00 AM (Core landscape deep-dive).
- Slot 2: 17:00 PM (Viral vertical Short).
