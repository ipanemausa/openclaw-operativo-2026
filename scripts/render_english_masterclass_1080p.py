"""
==============================================================================
OPENCLAW 2026 — MASTERCLASS ENGLISH 1080P FASTSTART
==============================================================================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import whisper
from build_complete_bilingual_masterclass_2026 import render_masterclass_for_language

if __name__ == "__main__":
    whisper_model = whisper.load_model("base")
    output = render_masterclass_for_language("en", whisper_model)
    print(f"\n[FINAL OK] English Masterclass generated at: {output}")
