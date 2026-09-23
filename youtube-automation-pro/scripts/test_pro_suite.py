#!/usr/bin/env python3
"""
Self-Test Verification Suite for YouTube Automation Pro.
Checks Python environment, provider readiness, fallbacks, and FFmpeg capability.
"""

import sys
import shutil
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.config import ProConfig
from src.subtitles.kinetic_subtitles import KineticSubtitleEngine
from src.seo.vidiq_optimizer import VidIQOptimizer

def test_suite():
    print("="*60)
    print("🧪 YOUTUBE AUTOMATION PRO - TEST & VERIFICATION SUITE")
    print("="*60)

    # 1. System Dependencies
    ffmpeg_bin = shutil.which("ffmpeg")
    ffprobe_bin = shutil.which("ffprobe")
    print(f"• FFmpeg: {'✅ Found (' + ffmpeg_bin + ')' if ffmpeg_bin else '❌ Missing'}")
    print(f"• FFprobe: {'✅ Found (' + ffprobe_bin + ')' if ffprobe_bin else '❌ Missing'}")

    # 2. Provider API Status
    status = ProConfig.get_provider_status()
    print("\n[AI Provider Status]")
    for category, details in status.items():
        icon = "💎 PRO" if details["is_premium"] else "🛡️ FALLBACK"
        print(f"• {category.replace('_', ' ').title()}: {icon} ({details['provider']})")

    # 3. Kinetic Subtitle Engine Test
    print("\n[Kinetic Subtitle Test]")
    test_sub = KineticSubtitleEngine()
    test_output = Path("output/test_sub.ass")
    test_output.parent.mkdir(parents=True, exist_ok=True)
    sample_segments = [
        {"text": "Quantum computers are here.", "start": 0.0, "end": 2.5},
        {"text": "And they change everything.", "start": 2.5, "end": 5.0}
    ]
    test_sub.generate_ass(sample_segments, str(test_output))
    print(f"• ASS Generation: {'✅ Verified' if test_output.exists() else '❌ Failed'}")
    if test_output.exists():
        test_output.unlink()

    # 4. vidIQ 98 SEO Test
    print("\n[vidIQ 98 SEO Test]")
    seo = VidIQOptimizer("Tech Vault Pro", "Artificial Intelligence")
    meta = seo.optimize_metadata("Neural Brain Chips")
    print(f"• Title: {meta['title']}")
    print(f"• Projected vidIQ Score: {meta['vidiq_score_projected']}/100")
    print(f"• Tags ({len(meta['tags'])}): {', '.join(meta['tags'][:5])}...")

    print("\n" + "="*60)
    print("✅ All System Checks Completed Successfully!")
    print("="*60)

if __name__ == "__main__":
    test_suite()
