"""Render final: recorte a 9:16 y quemado de subtítulos con ffmpeg."""

import subprocess
from pathlib import Path
from typing import Optional

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920


def render_vertical(video_path: Path, ass_path: Optional[Path], out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    vf = f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:force_original_aspect_ratio=increase,crop={TARGET_WIDTH}:{TARGET_HEIGHT}"
    if ass_path is not None:
        ass_escaped = str(ass_path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        vf += f",subtitles='{ass_escaped}'"

    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
