# Company Storybook Art Style Anchors

Select ONE style anchor and append it to EVERY illustration prompt (cover + chapter artwork) to ensure the entire company book remains visually cohesive, cinematic, and executive-grade. Always end every prompt with: `no text, no words, no lettering, no borders`.

---

### 1. Editorial Graphic Novel & Silicon Valley Noir (Default — Dynamic, Tech-Modern, Inspiring)
`High-end editorial graphic novel illustration, refined ink line art with rich gouache textures, cinematic warm lighting, subtle glowing highlights, sophisticated color palette of deep navy, amber gold, and warm paper cream, stylized founder and tech atmosphere, polished New Yorker and Bloomberg Businessweek cover aesthetic, no text, no words, no lettering, no borders.`

---

### 2. Architectural Gouache & Modernist Storybook (Structured, Elegant, Strategic)
`Editorial picture-book illustration in modernist gouache and matte acrylic, clean geometric perspective, bold architectural lines, mid-century executive design feel, warm golden hour ambient lighting, elegant muted tones with electric accent colors, premium business storybook art, no text, no words, no lettering, no borders.`

---

### 3. Cinematic 3D Stylized / Animated Film (Broad Appeal, Emotion, Visionary)
`Stylized 3D cinematic illustration, Pixar and Spider-Verse inspired executive storytelling aesthetic, rich subsurface scattering, warm volumetric light beams, soft depth of field, expressive heroic framing, polished tech-futurism and human ambition, no text, no words, no lettering, no borders.`

---

### 4. Classic Heritage Pencil & Watercolor Wash (Heirloom, Historical, Deep Gravitas)
`Classic editorial watercolor and delicate pencil illustration, subtle wash textures, muted earth tones and rich indigo accents, timeless journalistic biography feel, elegant and thoughtful pacing, heirloom storybook art, no text, no words, no lettering, no borders.`

---

## 🎨 Antigravity Image Generation Guidelines

- **Tool**: Native Antigravity `generate_image`.
- **AspectRatio**: `'3:4'` (Vertical portrait format matching 8×10 book pages).
- **Cover Image Composition**: Include `"leave open, uncluttered negative space at the TOP third of the image for book title overlay"`.
- **Consistency across Chapters**:
  - Keep the exact same style anchor string across all 6 prompts (`cover` + 5 chapters).
  - For recurring founder characters, describe key physical attributes identically (e.g. hair style, glasses, clothing style).
  - Pass the approved cover or chapter 1 image path into `ImagePaths` in subsequent `generate_image` calls.
- **Negative Constraints**: Always include `"no text, no words, no lettering, no watermarks, no borders"`.
