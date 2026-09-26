# Video Layout Design System

Reference spec for AI video-editing agents (e.g. Antigravity). Defines 3 reusable layout templates, expressed for every standard aspect ratio. Each layout uses named zones so an agent can map source assets (broll clip, talking-head clip, subtitle track) onto the correct region without ambiguity.

---

## Layout Types (apply to every ratio below)

### Layout A — "Split Stack" (broll + talking head)
Two full-width video zones stacked (portrait/square) or placed side-by-side (landscape/wide), with a subtitle pill anchored near the boundary/bottom.
- **Zone 1 — broll**: primary b-roll footage, top or left
- **Zone 2 — talking_head**: presenter cam footage, bottom or right
- **Zone 3 — subtitle**: pill-shaped caption, overlaid at the seam between the two zones or at the bottom-center

### Layout B — "Full Talking Head"
Single full-canvas zone of the presenter, subtitle pinned near the bottom edge.
- **Zone 1 — talking_head**: fills 100% of canvas
- **Zone 2 — subtitle**: pill caption, bottom-center, ~5–8% margin from bottom edge

### Layout C — "Broll with PIP"
Full-canvas broll with a circular picture-in-picture talking-head insert, subtitle pinned at the bottom.
- **Zone 1 — broll**: fills 100% of canvas
- **Zone 2 — talking_head_pip**: circular mask, positioned in a lower corner/third, diameter ~55–65% of canvas short-side
- **Zone 3 — subtitle**: pill caption, bottom-center

---

## 1. Portrait 9:16 (1080×1920) — Reels / Shorts / TikTok

### Layout A — Split Stack (vertical)
| Zone | Position (x, y, w, h) | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 52% | top half |
| talking_head | 0%, 52%, 100%, 48% | bottom half |
| subtitle | centered, y ≈ 92% | pill overlaps bottom of talking_head zone |

### Layout B — Full Talking Head
| Zone | Position | Notes |
|---|---|---|
| talking_head | 0%, 0%, 100%, 100% | full bleed |
| subtitle | centered, y ≈ 90% | pill, bottom-safe margin |

### Layout C — Broll + PIP
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 100% | full bleed |
| talking_head_pip | circle, center at (68%, 65%), diameter 60% of width | lower-right circular cutout |
| subtitle | centered, y ≈ 92% | pill, below/clear of PIP circle |

---

## 2. Landscape 16:9 (1920×1080) — YouTube / TV

### Layout A — Split Stack (horizontal)
| Zone | Position (x, y, w, h) | Notes |
|---|---|---|
| broll | 0%, 0%, 60%, 100% | left ~60% of canvas |
| talking_head | 60%, 0%, 40%, 100% | right ~40% of canvas |
| subtitle | centered, y ≈ 90%, spans full width | pill crosses the seam at bottom |

*Alternative split for landscape:* top/bottom 70/30 works if the agent needs a broll-dominant cut — broll 0,0,100%,70% / talking_head 0,70%,100%,30%.

### Layout B — Full Talking Head
| Zone | Position | Notes |
|---|---|---|
| talking_head | 0%, 0%, 100%, 100% | full bleed |
| subtitle | centered, y ≈ 88% | pill, bottom-safe margin |

### Layout C — Broll + PIP
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 100% | full bleed |
| talking_head_pip | circle, center at (82%, 72%), diameter 32% of height | lower-right circular cutout, smaller relative size than portrait since canvas is wider |
| subtitle | centered, y ≈ 90% | pill, clear of PIP circle |

---

## 3. Square 1:1 (1080×1080) — Feed posts

### Layout A — Split Stack
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 55% | top |
| talking_head | 0%, 55%, 100%, 45% | bottom |
| subtitle | centered, y ≈ 92% | pill at seam/bottom |

### Layout B — Full Talking Head
| Zone | Position | Notes |
|---|---|---|
| talking_head | 0%, 0%, 100%, 100% | full bleed |
| subtitle | centered, y ≈ 90% | pill, bottom-safe margin |

### Layout C — Broll + PIP
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 100% | full bleed |
| talking_head_pip | circle, center at (70%, 68%), diameter 55% of width | lower-right circular cutout |
| subtitle | centered, y ≈ 92% | pill, clear of PIP circle |

---

## 4. Portrait 4:5 (1080×1350) — Instagram feed portrait

### Layout A — Split Stack
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 53% | top |
| talking_head | 0%, 53%, 100%, 47% | bottom |
| subtitle | centered, y ≈ 92% | pill at seam/bottom |

### Layout B — Full Talking Head
| Zone | Position | Notes |
|---|---|---|
| talking_head | 0%, 0%, 100%, 100% | full bleed |
| subtitle | centered, y ≈ 90% | pill, bottom-safe margin |

### Layout C — Broll + PIP
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 100% | full bleed |
| talking_head_pip | circle, center at (68%, 66%), diameter 58% of width | lower-right circular cutout |
| subtitle | centered, y ≈ 92% | pill, clear of PIP circle |

---

## 5. Landscape 4:3 (1440×1080) — Classic / presentation style

### Layout A — Split Stack (horizontal)
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 62%, 100% | left |
| talking_head | 62%, 0%, 38%, 100% | right |
| subtitle | centered, y ≈ 90%, full width | pill at bottom |

### Layout B — Full Talking Head
| Zone | Position | Notes |
|---|---|---|
| talking_head | 0%, 0%, 100%, 100% | full bleed |
| subtitle | centered, y ≈ 88% | pill, bottom-safe margin |

### Layout C — Broll + PIP
| Zone | Position | Notes |
|---|---|---|
| broll | 0%, 0%, 100%, 100% | full bleed |
| talking_head_pip | circle, center at (80%, 72%), diameter 34% of height | lower-right circular cutout |
| subtitle | centered, y ≈ 90% | pill, clear of PIP circle |

---

## Shared Style Rules (all ratios)

- **Subtitle pill**: rounded-rectangle background, high-contrast fill vs. its background zone, centered horizontally, single or double line max, safe margin ≥ 4% from nearest edge.
- **Safe zones**: keep all text 5% inset from every canvas edge to survive platform crop/UI overlays.
- **PIP circle border**: optional 2–4px stroke in accent color for separation from broll.
- **Zone naming convention** (use exactly these keys so the agent maps assets correctly):
  - `broll` — b-roll / background footage
  - `talking_head` — full-frame presenter footage
  - `talking_head_pip` — circular presenter insert
  - `subtitle` — caption pill/track

## How an agent should use this file
1. Read the target `aspect_ratio` for the requested video.
2. Pick one of Layout A / B / C based on the content brief (has broll? presenter-only? broll-led with narrator inset?).
3. Look up the matching table above for that ratio + layout.
4. Place/crop/scale each source asset into its zone's (x, y, w, h) or circle spec.
5. Render the subtitle pill last, on top, respecting the safe-zone margins.

---

## 6. HyperFrames HTML/CSS Layout Implementation

### Layout A — Split Stack (Portrait 9:16)
```html
<div class="clip layout-split-stack" data-in="0" data-out="4.5" style="display: flex; flex-direction: column; width: 1080px; height: 1920px; position: absolute; top: 0; left: 0;">
  <!-- Top: B-roll / Visual Graphic (52%) -->
  <div style="width: 100%; height: 52%; position: relative; overflow: hidden;">
    <video src="assets/broll_01.mp4" style="width: 100%; height: 100%; object-fit: cover;"></video>
  </div>
  <!-- Bottom: Presenter Footage (48%) -->
  <div style="width: 100%; height: 48%; position: relative; overflow: hidden; border-top: 4px solid #FFFFFF;">
    <video src="assets/presenter.mp4" style="width: 100%; height: 100%; object-fit: cover;"></video>
  </div>
</div>
```

### Layout B — Full Talking Head (Portrait 9:16)
```html
<div class="clip layout-full-talking-head" data-in="4.5" data-out="8.0" style="width: 1080px; height: 1920px; position: absolute; top: 0; left: 0; overflow: hidden;">
  <video src="assets/presenter.mp4" style="width: 100%; height: 100%; object-fit: cover;"></video>
</div>
```

### Layout C — B-roll + Circular PIP (Portrait 9:16)
```html
<div class="clip layout-broll-pip" data-in="8.0" data-out="12.5" style="width: 1080px; height: 1920px; position: absolute; top: 0; left: 0; overflow: hidden;">
  <!-- Full Bleed B-roll -->
  <video src="assets/broll_02.mp4" style="width: 100%; height: 100%; object-fit: cover;"></video>
  <!-- Circular Presenter PIP (Lower Right) -->
  <div style="position: absolute; right: 40px; bottom: 220px; width: 440px; height: 440px; border-radius: 50%; overflow: hidden; border: 6px solid #FFFFFF; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
    <video src="assets/presenter.mp4" style="width: 100%; height: 100%; object-fit: cover;"></video>
  </div>
</div>
```

### Subtitle Pill Track (Global Overlay)
```html
<div class="clip caption-pill" data-in="0" data-out="3.2" style="position: absolute; bottom: 120px; left: 50%; transform: translateX(-50%); background: rgba(10, 15, 29, 0.85); backdrop-filter: blur(12px); border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 36px; padding: 18px 36px; color: #FFFFFF; font-family: 'Inter', sans-serif; font-size: 44px; font-weight: 800; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
  Stop scrolling! <span style="color: #33E5FF;">Watch this carefully.</span>
</div>
```

