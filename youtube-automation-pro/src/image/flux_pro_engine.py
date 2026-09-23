"""
FLUX.1 Pro High-Fidelity Visuals & High-CTR Thumbnail Engine.
Supports Fal.ai and Replicate API endpoints with procedural fallbacks.
"""

import os
import requests
from pathlib import Path
from src.config import ProConfig

class FluxProEngine:
    def __init__(self, fal_key: str = None, replicate_token: str = None):
        self.fal_key = fal_key or ProConfig.FAL_KEY
        self.replicate_token = replicate_token or ProConfig.REPLICATE_API_TOKEN

    def is_available(self) -> bool:
        return bool((self.fal_key and len(self.fal_key.strip()) > 5) or 
                    (self.replicate_token and len(self.replicate_token.strip()) > 5))

    def generate_image(self, prompt: str, output_path: str, aspect_ratio: str = "16:9", is_thumbnail: bool = False) -> str:
        """Generates visual keyframe or thumbnail using FLUX.1 Pro."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        enhanced_prompt = self._enhance_prompt(prompt, is_thumbnail=is_thumbnail)

        if not self.is_available():
            print("⚠️ FLUX.1 Pro credentials not detected. Generating procedural placeholder...")
            return self._generate_procedural_placeholder(enhanced_prompt, output_path, aspect_ratio)

        # 1. Try Fal.ai API
        if self.fal_key:
            try:
                import fal_client
                os.environ["FAL_KEY"] = self.fal_key
                print(f"🎨 [FLUX.1 Pro / Fal.ai] Submitting prompt: {enhanced_prompt[:80]}...")
                result = fal_client.subscribe(
                    "fal-ai/flux-pro/v1.1",
                    arguments={
                        "prompt": enhanced_prompt,
                        "image_size": "landscape_16_9" if aspect_ratio == "16:9" else "portrait_16_9",
                        "num_inference_steps": 30,
                        "guidance_scale": 3.5,
                        "enable_safety_checker": True
                    }
                )
                image_url = result["images"][0]["url"]
                self._download_file(image_url, output_path)
                print(f"🖼️ [FLUX.1 Pro] Image saved: {output_path}")
                return output_path
            except Exception as e:
                print(f"⚠️ Fal.ai generation error: {e}. Trying Replicate...")

        # 2. Try Replicate API
        if self.replicate_token:
            try:
                import replicate
                os.environ["REPLICATE_API_TOKEN"] = self.replicate_token
                print(f"🎨 [FLUX.1 Pro / Replicate] Submitting prompt...")
                output = replicate.run(
                    "black-forest-labs/flux-1.1-pro",
                    input={
                        "prompt": enhanced_prompt,
                        "aspect_ratio": aspect_ratio,
                        "output_format": "jpg",
                        "output_quality": 95
                    }
                )
                image_url = str(output)
                self._download_file(image_url, output_path)
                print(f"🖼️ [FLUX.1 Pro] Image saved: {output_path}")
                return output_path
            except Exception as e:
                print(f"⚠️ Replicate generation error: {e}")

        return self._generate_procedural_placeholder(enhanced_prompt, output_path, aspect_ratio)

    def _enhance_prompt(self, base_prompt: str, is_thumbnail: bool = False) -> str:
        """Injects cinematic lighting, composition, and high-CTR visual anchors."""
        style_anchors = "8k resolution, photorealistic masterpiece, cinematic volumetric lighting, raytracing, award-winning cinematography, ultra-detailed textures"
        if is_thumbnail:
            return f"Extreme high-CTR YouTube thumbnail style, high contrast, vivid expressive focal subject, clean composition, {base_prompt}, {style_anchors}"
        return f"{base_prompt}, {style_anchors}"

    def _download_file(self, url: str, path: str):
        res = requests.get(url, timeout=60)
        res.raise_for_status()
        with open(path, "wb") as f:
            f.write(res.content)

    def _generate_procedural_placeholder(self, prompt: str, output_path: str, aspect_ratio: str) -> str:
        """Generates a high-resolution gradient canvas with prompt overlay as a safe offline fallback."""
        from PIL import Image, ImageDraw, ImageFont
        w, h = (1920, 1080) if aspect_ratio == "16:9" else (1080, 1920)
        img = Image.new("RGB", (w, h), color=(18, 22, 34))
        draw = ImageDraw.Draw(img)
        
        # Draw tech grid / gradient accent
        for i in range(0, w, 80):
            draw.line([(i, 0), (i, h)], fill=(28, 36, 52), width=1)
        for j in range(0, h, 80):
            draw.line([(0, j), (w, j)], fill=(28, 36, 52), width=1)
            
        text = f"[FLUX.1 PRO SCENE]\n{prompt[:120]}..."
        draw.text((w // 8, h // 2 - 40), text, fill=(255, 215, 0))
        img.save(output_path, "JPEG")
        print(f"🎨 [Procedural Canvas] Placeholder saved to {output_path}")
        return output_path
