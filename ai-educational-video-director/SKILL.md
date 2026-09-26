---
name: ai-educational-video-director
description: Direct, design, and produce broadcast-grade educational, explainer, course, presentation, finance, tech, and knowledge-based videos powered exclusively by HyperFrames (heygen-com/hyperframes) for 60fps butter-smooth animations, dynamic presenter framing (Split Stack, PIP card, Full Screen), SVG/GSAP animated charts, kinetic typography, and multi-track audio synchronization.
compatibility: Node.js 18+, HyperFrames 0.8+, FFmpeg with libass, Python 3.10+
metadata:
  standard: "agentskills.io"
  version: "2.0.0"
  author: "Antigravity OS"
---

# AI Educational Video Director (HyperFrames Edition)

This skill establishes a production-grade framework to turn scripts, voice-overs, narration, talking-head footage, or raw topics into visually compelling, professional educational explainer videos—rendered and edited exclusively with **HyperFrames** (`heygen-com/hyperframes`) at 60fps.

The core principle: **Do not simply add random B-roll to a presenter's recording.** Instead:
1. **Understand what is being said.**
2. **Determine what the viewer needs to see to comprehend the concept.**
3. **Design the visual explanation.**
4. **Synchronize it with the narration/timing.**
5. **Integrate the presenter dynamically.**
6. **Produce and render the final 60fps composition via HyperFrames.**

---

## 1. Input Adaptation & Workflow Strategy

The director adapts dynamically based on the inputs provided:

*   **Script Only**: Draft a scene-by-scene visual plan, generate programmatic visual assets (SVG/HTML charts, diagrams), author the HyperFrames composition (`composition.html`), and render the master video.
*   **Voice-over / Audio Narration Only**: Analyze the audio timing (transcribe/detect pauses), construct an audio-driven timeline in HyperFrames with `data-in` and `data-out`, and synchronize GSAP animations to voice triggers.
*   **Talking-Head Video Only**: Cut out pauses and dead air, place the presenter on `data-track="presenter"`, and layer animated cards, charts, and annotations on `data-track="visual_stage"`.
*   **Talking-Head + Script**: Map script beats to the footage timeline, dynamically alternating presenter layouts (Full talking head, Split Stack, or Circular PIP).
*   **Topic Only**: First research and draft an educational script, then generate assets, construct the HyperFrames composition, and compile the final video.

---

## 2. Scene Mapping & Narration Analysis

Before authoring code or rendering, construct a detailed **Narration Analysis & Storyboard Timeline**. For each segment/scene, specify:
*   **Timecode / Timing Range**: (Start/End in seconds).
*   **Spoken Text**: The exact line or narrative beat.
*   **Main Idea & Keywords**: The core takeaway and visual trigger words.
*   **Visual Treatment & Composition**: What the screen looks like (e.g., presenter PIP on left, diagram on right).
*   **Presenter Layout**: (Layout A "Split Stack", Layout B "Full Talking Head", Layout C "Broll + PIP", or Removed).
*   **Programmatic Graphics / Charts**: Code-based SVG, Canvas, HTML/CSS, or charting tools.
*   **Animation / Transition**: (Slide-in, draw-in, fade, count-up with GSAP easing).
*   **Asset Requirements**: (Screenshots, icon names, B-roll clips, illustrations).

### Example Mapping Structure
```markdown
### Scene [01] - [00:00 - 00:15]
*   **Narration**: "Understanding compound interest starts with how your principal generates earnings over time..."
*   **Keywords**: "compound interest", "principal", "earnings over time"
*   **Visual**: Presenter in a sleek rounded glass card on the left; an animated SVG line chart on the right showing exponential growth.
*   **Presenter Layout**: Left Card (35% width, safe padding).
*   **HyperFrames Track**: `data-track="presenter"` (left card) + `data-track="visual_stage"` (right chart).
*   **Graphics**: SVG Line chart with progressive GSAP stroke-dashoffset draw animation.
*   **Reason**: Visually show the exponential curve matching the word "compounds".
```

---

## 3. Visual Decision Engine

Select the visual treatment that makes the concept easiest to understand:

| Visual Category | Sub-type / Layout | Primary Use Case |
| :--- | :--- | :--- |
| **Presenter Integration** | Full-Screen Talking Head (Layout B) | Personal introductions, transitions, direct quotes, conclusions. |
| | Left/Right Split Stack (Layout A) | Presenter on one side, clean bullet points or small graphics on the other. |
| | B-roll + Circular PIP (Layout C) | Presenter inside a floating circular card while showing full-screen UI, chart, or media. |
| | Floating Presenter Card | Rounded cutout with glassmorphism border hovering over background schematic. |
| **Data & Charts** | Bar Chart / Column Chart | Comparative growth, rankings, discrete quantities. |
| | Line Chart / Area Chart | Trends, values compounding over time, trajectory. |
| | Donut / Pie Chart | Proportions, compositions, market share. |
| | Number Animation | Key statistics, counts, financial metrics counting up via GSAP. |
| **Diagrams & Layouts** | Workflow / Process Diagram | Timelines, multi-step systems, cause-and-effect pathways. |
| | Information Grid | Categories, company portfolios, examples, product variations. |
| | High-Contrast Maps | Geographic location context, regional metrics. |
| **Media & Motion** | High-Quality B-Roll | Real-world metaphors, conceptual illustrations. |
| | Kinetic Typography | Title hooks, definitions, critical warnings, bold statements. |
| | Product/Screen Demo | Software guides, web app walkthroughs, interface explanations. |

---

## 4. HyperFrames 60fps Video Editing & Composition Engine

All video composition, assembly, and rendering is handled exclusively by **HyperFrames** (`heygen-com/hyperframes`).

### Composition Contract:
1. **Resolution & Canvas**: Defined in the `<meta name="hyperframes:dimension">` tag (e.g. `1080x1920` for Shorts/Reels, `1920x1080` for YouTube).
2. **Tracks (`data-track`)**: Separate visual elements onto dedicated tracks to avoid z-index collisions:
   - `data-track="bg"`: Ambient blurred backdrop or solid background.
   - `data-track="visual_stage"`: Charts, diagrams, B-roll footage, and card graphics.
   - `data-track="presenter"`: Talking-head presenter video (`<video class="clip">`).
   - `data-track="captions"`: Kinetic subtitles and text callouts.
   - `data-track="soundtrack"`: Voiceover, background music ducking, and sound effects.
3. **Clips & Timing**: Every clip declares `data-in` and `data-out` in seconds (e.g., `<div class="clip" data-in="0" data-out="5.2">`).
4. **GSAP 60fps Motion**: Use GreenSock (GSAP 3) for easing curves, camera moves, and progress bars:
   - Entrance: `gsap.fromTo(".card", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, ease: "back.out(1.7)" })`
   - Data Chart Reveal: `gsap.fromTo(".chart-path", { strokeDashoffset: 1000 }, { strokeDashoffset: 0, ease: "power2.out" })`

### Core CLI Commands:
```bash
# 1. Validate composition syntax and deterministic rendering rules
npx hyperframes check path/to/composition.html

# 2. Render 60fps master broadcast MP4 (non-interactive)
npx hyperframes render path/to/composition.html -o final_educational_video.mp4 --fps 60 --quality looks --non-interactive
```

---

## 5. Aspect Ratio & Composition Design System

Adapt the layout structure dynamically based on the target video aspect ratio:

### Vertical Video Production (9:16 - 1080x1920)
*   **Upper-Half Spacing**: Place titles, body content, and diagram grids in the upper half of the canvas (`top: 180px` to `900px`).
*   **Presenter Placement**:
    *   *Layout A (Split Stack)*: Top 52% visual diagram / Bottom 48% presenter.
    *   *Layout C (B-roll + PIP)*: Bottom-right circular cutout (`420x420` size centered at `x: 620, y: 1360`).
*   **Captions**: Positioned at `y ≈ 92%` in a high-contrast rounded pill.

### Landscape Video Production (16:9 - 1920x1080)
*   **Left-Aligned Content**: Align all text columns, lists, and graphic blocks to the left half (`x: 80px` to `1100px`).
*   **Presenter Placement**:
    *   *Layout A (Split Stack)*: Left 60% graphics & B-roll / Right 40% presenter.
    *   *Layout C (B-roll + PIP)*: Presenter circular cutout (`380x380`) at lower right (`x: 1480, y: 640`).
*   **Horizontal Layout Flow**: Process diagrams and timelines flow horizontally (`node1 → node2 → node3`).

---

## 6. Subtitles & Kinetic Typography

*   **Subtitle Chunking**: Limit subtitles to a maximum of **3 to 5 words per line** for high reading speed.
*   **Word Pop & Typewriter**: Highlight active spoken words with bright accent colors (`#33E5FF` cyan or `#FFD700` gold).
*   **Layout Collision Protection**: Subtitles automatically adjust vertical/horizontal alignment so they never overlap the presenter cutout or on-screen diagram labels.

---

## 7. Quality Control Checklist

Before completing production or video rendering, verify:
*   [ ] **HyperFrames Check**: Does `npx hyperframes check` pass with zero timing or track errors?
*   [ ] **Sync Check**: Are chart animations and text callouts aligned with the spoken voiceover timestamps?
*   [ ] **Text Readability**: Is contrast ratio ≥ 4.5:1 with clear drop shadows against moving footage?
*   [ ] **Presenter Visibility**: Is the presenter present in every segment (Full screen, Split Stack, or Circular PIP)?
*   [ ] **Smooth 60fps Motion**: Are all transitions smoothed with GSAP `power1.inOut` or `back.out` curves?
*   [ ] **Audio Continuity**: Is background music ducked automatically during narration?
