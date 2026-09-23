# ⚡ YouTube Automation Pro (Studio Edition)

> **Universal Autonomous YouTube Operating System powered by ElevenLabs, Higgsfield AI, FLUX.1 Pro, Suno AI, and vidIQ 98 SEO.**  
> Built for creators, founders, and automated studio networks running 100-day automated publishing pipelines.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs_Pro-orange.svg)](https://elevenlabs.io/)
[![Higgsfield AI](https://img.shields.io/badge/Motion-Higgsfield_AI-purple.svg)](https://higgsfield.ai/)
[![FLUX.1 Pro](https://img.shields.io/badge/Visuals-FLUX.1_Pro_8K-cyan.svg)](https://blackforestlabs.ai/)
[![Suno AI](https://img.shields.io/badge/Soundtrack-Suno_AI_v3.5-red.svg)](https://suno.com/)
[![vidIQ Score](https://img.shields.io/badge/vidIQ_Score-98%2F100-green.svg)](https://vidiq.com/)

---

## 🌟 What is YouTube Automation Pro?

While standard automation systems produce generic slideshows with robotic voices, **YouTube Automation Pro** connects Hollywood-grade and broadcast AI tools into a unified production pipeline:

```
                          ┌───────────────────────────┐
                          │  Interactive Onboarding   │
                          │        (setup.py)         │
                          └─────────────┬─────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
│    🎙️ ElevenLabs    │      │   🖼️ FLUX.1 Pro     │      │    🎵 Suno AI       │
│  Hyper-Realistic    │      │  8K Photorealistic  │      │  Custom Instrumental│
│  Voice & Native SFX │      │  Visual Keyframes   │      │  Documentary Score  │
└──────────┬──────────┘      └──────────┬──────────┘      └──────────┬──────────┘
           │                            │                            │
           │                            ▼                            │
           │                 ┌─────────────────────┐                 │
           │                 │  🎬 Higgsfield AI   │                 │
           │                 │  Cinematic Camera   │                 │
           │                 │  Pan / Dolly Motion │                 │
           │                 └──────────┬──────────┘                 │
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │   Kinetic Hormozi Subtitles   │
                        │    + FFmpeg Master Mixdown    │
                        └───────────────┬───────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │  vidIQ 98 SEO + Cloud Publish │
                        │  (8:00 AM & 5:00 PM Daily)    │
                        └───────────────────────────────┘
```

---

## 💎 The Pro Multi-Layer AI Stack

### 1. 🎙️ Voice & Sound Effects: **ElevenLabs**
- **Hyper-Realistic Emotional Delivery**: Articulates nuanced pacing, suspenseful pauses, and dramatic vocal emphasis.
- **Voice Cloning Ready**: Drop in any cloned voice ID in `.env` to speak in your own personal voice.
- **Native AI Foley SFX**: Automatically generates contextual audio foley (cinematic bass drops, whooshes, chimes).
- *Fallback: Microsoft Edge-TTS (`ChristopherNeural` / `AnaNeural`).*

### 2. 🎬 Video Motion & Camera Dynamics: **Higgsfield AI**
- **Physical Camera Trajectories**: Generates dynamic cinematic moves (dolly in, dolly zoom, orbit, pan left/right).
- **Temporal Consistency**: Eliminates warped artifacts and unstable frames.
- *Fallback: Procedural 60fps FFmpeg Ken Burns zoom/pan engine.*

### 3. 🖼️ Visual Keyframes & 8K Thumbnails: **FLUX.1 Pro**
- **Photorealistic Realism**: State-of-the-art prompt fidelity via Fal.ai or Replicate.
- **High-CTR Composition**: Automatically applies thumbnail enhancement rules with high-contrast focal points.
- *Fallback: High-resolution procedural canvas / ImageFX.*

### 4. 🎵 Background Soundtrack: **Suno AI (v3.5)**
- **Radio-Quality Custom Music**: Composes original instrumental scores matching the exact mood, tempo, and genre of your niche.
- *Fallback: Procedural harmonic ambient synth with auto-ducking.*

### 5. 📝 High-Retention Typography: **Hormozi / MrBeast Style**
- **SubStation Alpha (`.ass`) Precision**: Word-level active pop highlighting, heavy drop shadows, and high-visibility contrast.
- **Zero-Overlap Guarantee**: Built-in sequential clearance buffers to eliminate subtitle collisions.

### 6. 📊 vidIQ Score 98/100 SEO & Cloud Scheduler
- **High-CTR Title Formulas**: Question-based curiosity hooks engineered for viral click-through rates.
- **Automatic Playlist Routing**: Directs landscape masterclasses and vertical Shorts into dedicated channel playlists.
- **Autonomous Cloud Publishing**: Uses YouTube Data API v3's native `publishAt` parameter. Videos publish automatically at **8:00 AM & 5:00 PM** without needing your computer running!

---

## 🚀 Quick Start (Under 3 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/mohit626689/youtube-automation-pro.git
cd youtube-automation-pro
```

### 2. Run Interactive Onboarding
```bash
python3 setup.py
```
The onboarding wizard will guide you through:
1. Channel Name, Handle, and Target Niche (or model any inspiration channel URL).
2. Entering your API Keys (ElevenLabs, Higgsfield, Fal.ai/FLUX, Suno).
3. Choosing your daily publication schedule (e.g. 8:00 AM & 5:00 PM).
4. Auto-generating your `.env`, `pipeline_config.json`, and `100_video_roadmap.md`.

### 3. Verify Your Environment
```bash
python3 scripts/test_pro_suite.py
```

### 4. Render an Episode
```bash
python3 scripts/generate_episode.py
```

---

## 🛡️ Built-in Zero-Failure Fallback System

You don't need all API keys active on Day 1. **YouTube Automation Pro** features smart fallbacks for every single layer:

| Layer | Pro Engine (Active with API Key) | Fallback Engine (Free / Offline) |
| :--- | :--- | :--- |
| **Voice** | ElevenLabs Multilingual v2 | Microsoft Edge-TTS (400+ voices) |
| **Motion** | Higgsfield AI Text/Image-to-Video | FFmpeg 60fps Smooth Camera Motion |
| **Visuals** | FLUX.1 Pro 8K (Fal.ai / Replicate) | Procedural 1080p Canvas Engine |
| **Music** | Suno AI Custom Instrumental | Ambient Harmonic Synthesizer |
| **Uploads** | YouTube Data API v3 (Cloud Schedule) | Local Staging & Dry-Run Simulator |

---

## 🔒 Security & Privacy

This repository strictly excludes sensitive credentials via `.gitignore`:
- API keys are read solely from your local `.env`.
- Google OAuth tokens (`client_secrets.json`, `token.json`) are never committed.
- Clean templates (`.env.example`, `client_secrets.example.json`) are provided for easy setup.

---

## 🤝 Community & Support

- **Skool Community**: Join discussions and get automation workflows in the [AI Workshop Community](https://skool.com/aiworkshop).
- **Skills Suite**: Explore our full [Antigravity AI Agent Skills Collection](https://github.com/mohit626689/antigravity-skills).

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
