#!/usr/bin/env python3
"""
Generate a complete episode with YouTube Automation Pro.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.config import ProConfig
from src.pipeline.pro_orchestrator import ProOrchestrator

def main():
    config = ProConfig.load_pipeline_config()
    orchestrator = ProOrchestrator(config)

    # Example sample script for generation
    sample_topic = "Quantum Artificial Intelligence Breakthrough 2026"
    sample_scenes = [
        {
            "script": "What happens when quantum computing meets artificial general intelligence? It is not science fiction anymore.",
            "visual_prompt": "Hyper-realistic glowing quantum computer processor suspended in cryogenic mist, blue and golden quantum circuits, 8k cinematic shot",
            "motion": "dolly_in"
        },
        {
            "script": "Traditional supercomputers take thousands of years to decrypt complex mathematical equations. Quantum algorithms do it in three seconds.",
            "visual_prompt": "Futuristic server room with streaming data streams, holographic equations dissolving in air, dramatic lighting",
            "motion": "pan_left"
        },
        {
            "script": "The implications for science, medicine, and cryptography are staggering. And the race for total dominance has officially begun.",
            "visual_prompt": "Futuristic skyline with towering data spires, dramatic overcast clouds, volumetric neon lighting, 8k resolution",
            "motion": "dolly_in"
        }
    ]

    print("🚀 Running Pro Video Pipeline...")
    result = orchestrator.produce_episode(
        episode_id="ep_001_quantum_ai",
        topic=sample_topic,
        scenes=sample_scenes,
        is_short=False,
        day_offset=1
    )
    print("\n✅ Execution Finished Successfully!")
    print(f"Master Video File: {result['master_file']}")
    print(f"vidIQ Projected Score: {result['seo_package']['vidiq_score_projected']}/100")
    print(f"Title: {result['seo_package']['title']}")

if __name__ == "__main__":
    main()
