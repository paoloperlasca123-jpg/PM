"""Orquesta el pipeline completo: ingest -> transcribe -> analyze -> subtitles -> render.

Si el motor de transcripción no puede descargar su modelo (por ejemplo,
sin acceso de red al proveedor del modelo), el pipeline no se detiene:
degrada a un modo sin subtítulos, usando detección de silencios por
audio en vez de por transcripción, y lo deja explícito en el EDL.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from video_engine import analyze, ingest, render, subtitles, transcribe


def run(video_path: Path, work_dir: Path, model_size: str = "small") -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)

    info = ingest.probe(video_path)

    audio_path = work_dir / "audio.wav"
    ingest.extract_audio(video_path, audio_path)

    transcripcion_disponible = True
    error_transcripcion = None
    words = []

    try:
        words = transcribe.transcribe(audio_path, model_size=model_size)
    except Exception as exc:  # noqa: BLE001 - degradar sin romper el pipeline
        transcripcion_disponible = False
        error_transcripcion = str(exc).splitlines()[-1] if str(exc) else type(exc).__name__

    if transcripcion_disponible:
        silences = analyze.detect_silences(words)
        muletillas = analyze.detect_muletillas(words)
        ass_path = work_dir / "subtitulos.ass"
        subtitles.build_ass(words, render.TARGET_WIDTH, render.TARGET_HEIGHT, ass_path)
    else:
        silences = analyze.detect_silences_audio(audio_path)
        muletillas = []
        ass_path = None

    final_path = work_dir / "final_vertical.mp4"
    render.render_vertical(video_path, ass_path, final_path)

    edl = {
        "video_original": str(video_path),
        "info_original": info,
        "procesado": datetime.now(timezone.utc).isoformat(),
        "transcripcion_disponible": transcripcion_disponible,
        "error_transcripcion": error_transcripcion,
        "transcripcion": " ".join(w["word"] for w in words) if words else None,
        "palabras": words,
        "silencios_detectados": silences,
        "metodo_deteccion_silencios": "transcripcion" if transcripcion_disponible else "nivel_de_audio",
        "muletillas_detectadas": muletillas,
        "subtitulos_generados": ass_path is not None,
        "salida_final": str(final_path),
    }
    (work_dir / "edl.json").write_text(
        json.dumps(edl, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return edl
