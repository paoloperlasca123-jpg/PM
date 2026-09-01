"""Transcripción con timestamps por palabra usando faster-whisper."""

from pathlib import Path
from typing import List, TypedDict


class Word(TypedDict):
    word: str
    start: float
    end: float


def transcribe(audio_path: Path, model_size: str = "small", language: str = "es") -> List[Word]:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        vad_filter=True,
    )

    words: List[Word] = []
    for segment in segments:
        for w in segment.words:
            words.append({"word": w.word.strip(), "start": w.start, "end": w.end})
    return words
