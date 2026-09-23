"""
Kinetic Typography & Subtitle Engine (Hormozi / MrBeast Style).
Generates SubStation Alpha (.ass) with dynamic active-word pop and zero-overlap clearance.
"""

from pathlib import Path
from typing import List, Dict

class KineticSubtitleEngine:
    def __init__(self, font_name: str = "Arial Black", font_size: int = 32):
        self.font_name = font_name
        self.font_size = font_size

    def generate_ass(self, segments: List[Dict], output_path: str, is_vertical: bool = False) -> str:
        """
        Takes segments [{'text': str, 'start': float, 'end': float}]
        and creates high-retention animated subtitles.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        res_x, res_y = (1080, 1920) if is_vertical else (1920, 1080)
        margin_v = 450 if is_vertical else 120
        font_size = 54 if is_vertical else 42

        # ASS Script Header
        header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {res_x}
PlayResY: {res_y}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{self.font_name},{font_size},&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4,2,2,40,40,{margin_v},1
Style: Highlight,{self.font_name},{font_size + 4},&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,105,105,1,0,1,5,3,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

        events = []
        for seg in segments:
            start_str = self._format_timestamp(seg["start"])
            end_str = self._format_timestamp(seg["end"])
            raw_text = seg["text"].strip().upper()
            
            # Active word pop effect
            words = raw_text.split()
            if len(words) <= 4:
                formatted_text = r"{\t(0,100,\fscx110\fscy110)\t(100,200,\fscx100\fscy100)}" + raw_text
                events.append(f"Dialogue: 0,{start_str},{end_str},Highlight,,0,0,0,,{formatted_text}")
            else:
                # Split longer sentence to avoid screen crowding
                mid = len(words) // 2
                p1 = " ".join(words[:mid])
                p2 = " ".join(words[mid:])
                mid_time = seg["start"] + (seg["end"] - seg["start"]) / 2
                
                events.append(f"Dialogue: 0,{start_str},{self._format_timestamp(mid_time)},Default,,0,0,0,,{p1}")
                events.append(f"Dialogue: 0,{self._format_timestamp(mid_time)},{end_str},Highlight,,0,0,0,,{p2}")

        full_content = header + "\n".join(events) + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        print(f"📝 [Kinetic Subtitles] Styled ASS saved to {output_path}")
        return output_path

    def _format_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:05.2f}"
