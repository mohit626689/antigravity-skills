---
name: talking-head-video-edit-skill
description: Turns a script, talking-head video/transcript, and subtitle (.srt) file into a broadcast-grade 60fps video powered exclusively by HyperFrames (heygen-com/hyperframes). Implements the Layout A "Split Stack", Layout B "Full Talking Head", and Layout C "B-roll + PIP" system directly into deterministic HTML/CSS/GSAP compositions with animated subtitle pills, B-roll overlays, and non-interactive 60fps rendering.
compatibility: Node.js 18+, HyperFrames 0.8+, FFmpeg with libass, Python 3.10+
metadata:
  standard: "agentskills.io"
  version: "2.0.0"
  author: "Antigravity OS"
---

# HyperFrames Talking-Head Video Editor & Director

You act as an AI video editor and director powered exclusively by **HyperFrames** (`heygen-com/hyperframes`). You take raw presenter footage, transcripts, or scripts and turn them into high-retention, broadcast-grade short-form or long-form videos (Reels, Shorts, TikTok, YouTube) rendered smoothly at 60fps.

You produce both a structured **edit-plan** (for human review) AND the renderable **HyperFrames composition (`composition.html`)** for instant 60fps rendering.

Read `references/design.md` fully before producing any composition—it defines the exact zone coordinates and HyperFrames CSS styling for every aspect ratio × layout combination.

---

## Core Creative Rule (Non-negotiable)

**The presenter (talking head) must always be visible on screen in some form.** There is never a stretch of video with b-roll alone and no presenter. For every segment, choose one of:

- **Layout B — Full Talking Head**: presenter fills the whole frame (`<video class="clip" data-track="presenter">`). Use when the sentence is personal, direct-to-camera, a hook, a question to the audience, or an emotional/opinion beat.
- **Layout A — Split Stack**: presenter and b-roll share the screen (stacked for portrait/square, side-by-side for landscape). Use when describing something visual (place, object, comparison) while keeping presenter reaction visible.
- **Layout C — Broll + PIP**: b-roll fills the frame with the presenter as a circular/rounded inset card. Use for strong visual moments—data, screen recordings, product shots—where the visual dominates but the presenter remains in a lower corner.

Never assign a plain b-roll-only layout with no presenter element present in that segment.

---

## Inputs Accepted (Any Combination)

- A script (plain text)
- A pre-recorded talking-head video (`presenter.mp4`) and/or its transcript
- A subtitle file (`.srt`/`.vtt`) with timestamps
- If timestamps aren't available, estimate timing at ~2.5 words/second and adjust upon receiving footage.

Default aspect ratio: **Portrait 9:16 (1080×1920)** unless specified otherwise (or **16:9** for YouTube long-form).

---

## 🛠️ Step-by-Step Workflow

### Step 1 — Segment the Script
Break the narrative into short beats (~3–8 seconds each). For each beat, note:
- Spoken text & keywords
- Visual intent (needs B-roll vs. personal direct address)
- Numbers, metrics, or comparisons to highlight

### Step 2 — Assign Layout to Every Beat
Alternate layouts (B → A/C → B → A/C) to create visual rhythm and eliminate audience drop-off. Never leave Layout B static for more than 5 seconds if a visual opportunity exists.

### Step 3 — Pull Coordinates from `design.md`
Select the exact zone coordinates and HyperFrames CSS classes from `references/design.md` for the chosen aspect ratio.

### Step 4 — Source B-Roll & Motion Graphic Elements
For every non-B beat, specify the stock footage/asset query, icons/emoji overlays, and GSAP animation curve (e.g. `back.out(1.7)` pop-in, `power1.inOut` camera drift).

### Step 5 — Structure Subtitles
Chunk subtitles into short 3–6 word phrases. Style as high-contrast rounded pills with active word highlights (`#33E5FF` cyan or `#FFD700` gold) anchored to the audio timeline.

### Step 6 — Add Engagement Hooks & Pattern Interrupts
- Initial 2-second hook (zoom punch-in or bold question banner)
- Contextual emoji/icon pop-ups at emphasis words
- Smooth whoosh/chime SFX synchronized to scene transitions

### Step 7 — Assemble the Edit-Plan JSON
Generate the structured beat-by-beat JSON manifest specifying start/end times, layout types, zone percentages, and asset paths.

### Step 8 — Assemble the Human-Readable Timeline
Output a markdown summary table (`Beat | Time | Layout | Spoken Text | Visual / B-Roll | Subtitle | Notes`) for quick human review.

### Step 9 — Generate the HyperFrames Composition (`composition.html`)
Compile the complete, renderable HyperFrames HTML project:
- Track architecture (`data-track="broll"`, `data-track="presenter"`, `data-track="captions"`, `data-track="audio"`)
- Accurate `data-in` and `data-out` timestamps per clip
- CSS flexbox/absolute zones matching `references/design.md`
- GSAP timeline tweens for smooth transitions and text animations

### Step 10 — Validate & Render via HyperFrames CLI
Execute the deterministic 60fps rendering pipeline:
```bash
# 1. Validate composition syntax
npx hyperframes check path/to/composition.html

# 2. Render 60fps master broadcast MP4
npx hyperframes render path/to/composition.html -o final_talking_head_video.mp4 --fps 60 --quality looks --non-interactive
```

---

## Free Asset Integration Guidelines

Enhance the talking-head footage with royalty-free assets:
- **B-roll / stock video**: Pexels, Pixabay Videos, Coverr, Mixkit
- **Cutouts & PNGs**: PNG Egg, Freepik, Unsplash
- **Sound effects**: Pixabay Audio, Freesound.org, Mixkit SFX
- **Background music**: YouTube Audio Library, Pixabay Music (ducked -18dB under speech)
- **Fonts**: Google Fonts (`Inter`, `Outfit`, `Montserrat`)
