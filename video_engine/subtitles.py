"""Generador de subtítulos dinámicos (.ass) con resaltado por palabra.

Usa las etiquetas \\k (karaoke) de ASS/libass para que cada palabra se
resalte exactamente cuando se pronuncia, sin necesidad de re-renderizar
frame a frame — ffmpeg quema el .ass en un solo pase.
"""

from pathlib import Path
from typing import List

from video_engine.transcribe import Word

MAX_CHUNK_WORDS = 5
MAX_CHUNK_SECONDS = 2.8
PAUSE_BREAK_SECONDS = 0.6

HEADER_TEMPLATE = """[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,{fontsize},&H00FFFFFF,&H0000D7FF,&H00101010,&H96000000,1,0,0,0,100,100,1,0,1,4,0,2,60,60,{marginv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _fmt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def _chunk_words(words: List[Word]) -> List[List[Word]]:
    chunks: List[List[Word]] = []
    current: List[Word] = []

    for w in words:
        if current:
            gap = w["start"] - current[-1]["end"]
            duration = w["end"] - current[0]["start"]
            if gap >= PAUSE_BREAK_SECONDS or len(current) >= MAX_CHUNK_WORDS or duration >= MAX_CHUNK_SECONDS:
                chunks.append(current)
                current = []
        current.append(w)

    if current:
        chunks.append(current)
    return chunks


def _dialogue_line(chunk: List[Word]) -> str:
    start = _fmt_time(chunk[0]["start"])
    end = _fmt_time(chunk[-1]["end"])

    parts = []
    for i, w in enumerate(chunk):
        word_dur = w["end"] - w["start"]
        if i + 1 < len(chunk):
            word_dur += chunk[i + 1]["start"] - w["end"]
        k = max(1, round(word_dur * 100))
        parts.append(f"{{\\k{k}}}{w['word']}")

    text = " ".join(parts)
    return f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}"


def build_ass(words: List[Word], video_width: int, video_height: int, out_path: Path) -> Path:
    fontsize = max(28, video_width // 16)
    marginv = int(video_height * 0.12)

    header = HEADER_TEMPLATE.format(
        width=video_width, height=video_height, fontsize=fontsize, marginv=marginv
    )

    chunks = _chunk_words(words)
    lines = [_dialogue_line(c) for c in chunks if c]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return out_path
