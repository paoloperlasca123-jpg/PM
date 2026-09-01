"""Carga de video y extracción de audio."""

import subprocess
from pathlib import Path


def extract_audio(video_path: Path, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def probe(video_path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-show_entries", "format=duration",
        "-of", "csv=p=0:s=,",
        str(video_path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    lines = [line for line in result.stdout.strip().splitlines() if line]
    width, height = lines[0].split(",")
    duration = lines[1]
    return {"width": int(width), "height": int(height), "duration": float(duration)}
