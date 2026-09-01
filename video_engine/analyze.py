"""Análisis determinístico del ritmo: silencios y muletillas.

No corta ni modifica el video — solo detecta y reporta, para que el
corte real requiera una decisión explícita (ver principio de no
eliminar/modificar automáticamente).
"""

import re
import subprocess
from pathlib import Path
from typing import List

from video_engine.transcribe import Word

MULETILLAS_ES = {
    "eh", "este", "esto", "o sea", "tipo", "bueno", "entonces",
    "digamos", "osea", "ehh", "mmm", "eeh",
}


def detect_silences(words: List[Word], min_gap: float = 0.4) -> List[dict]:
    silences = []
    for prev, nxt in zip(words, words[1:]):
        gap = nxt["start"] - prev["end"]
        if gap >= min_gap:
            silences.append({
                "start": round(prev["end"], 2),
                "end": round(nxt["start"], 2),
                "duracion": round(gap, 2),
            })
    return silences


def detect_silences_audio(audio_path: Path, noise_db: float = -30.0, min_duration: float = 0.4) -> List[dict]:
    """Detecta silencios directamente del nivel de audio, sin transcripción.

    Fallback usado cuando el motor de transcripción no está disponible
    (por ejemplo, sin acceso de red al modelo de IA).
    """
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration}",
        "-f", "null", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    starts = [float(m) for m in re.findall(r"silence_start:\s*([\d.]+)", result.stderr)]
    ends = [float(m) for m in re.findall(r"silence_end:\s*([\d.]+)", result.stderr)]

    silences = []
    for start, end in zip(starts, ends):
        silences.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "duracion": round(end - start, 2),
        })
    return silences


def detect_muletillas(words: List[Word]) -> List[dict]:
    hits = []
    for w in words:
        token = w["word"].strip().lower().strip(".,!?¿¡")
        if token in MULETILLAS_ES:
            hits.append({
                "palabra": w["word"],
                "start": round(w["start"], 2),
                "end": round(w["end"], 2),
            })
    return hits
