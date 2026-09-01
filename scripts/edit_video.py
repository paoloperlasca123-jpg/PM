#!/usr/bin/env python3
"""CLI del motor de edición automática de video.

Uso:
    python3 scripts/edit_video.py media/input/rawclip.mp4
    python3 scripts/edit_video.py media/input/rawclip.mp4 --model small
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from video_engine.pipeline import run  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Edita automáticamente un video corto")
    parser.add_argument("video", help="Ruta al video original")
    parser.add_argument("--out", default="media/output/processed", help="Carpeta de trabajo/salida")
    parser.add_argument("--model", default="small", help="Tamaño del modelo Whisper (tiny/base/small/medium)")
    args = parser.parse_args()

    video_path = Path(args.video)
    work_dir = Path(args.out) / video_path.stem

    edl = run(video_path, work_dir, model_size=args.model)

    if edl["transcripcion_disponible"]:
        print(f"Transcripción: {edl['transcripcion'][:200]}...")
        print(f"Subtítulos generados: sí")
    else:
        print(f"Transcripción NO disponible: {edl['error_transcripcion']}")
        print("Subtítulos generados: no (silencios detectados por nivel de audio)")
    print(f"Silencios detectados: {len(edl['silencios_detectados'])}")
    print(f"Muletillas detectadas: {len(edl['muletillas_detectadas'])}")
    print(f"Video final: {edl['salida_final']}")


if __name__ == "__main__":
    main()
