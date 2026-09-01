#!/usr/bin/env python3
"""Convierte el edl.json del motor de edición (video_engine) al formato
Caption[] que espera el proyecto Remotion (remotion/), para renderizar
subtítulos animados.

Esto desacopla la transcripción (bloqueada por red en este entorno,
pero funciona en tu Mac) del renderizado (funciona aquí, vía npm).

Uso:
    python3 scripts/edl_to_remotion_captions.py \
        media/output/processed/rawclip/edl.json \
        remotion/public/rawclip.json

    # Copia también el video de origen a remotion/public/ con el
    # mismo nombre base para que el componente CaptionedVideo lo cargue.
"""

import argparse
import json
import sys
from pathlib import Path


def convert(edl_path: Path) -> list:
    edl = json.loads(edl_path.read_text(encoding="utf-8"))

    if not edl.get("transcripcion_disponible"):
        raise ValueError(
            "Este edl.json no tiene transcripción disponible "
            f"(error: {edl.get('error_transcripcion')}). "
            "Corre scripts/edit_video.py en un entorno con acceso a "
            "internet sin restricciones para generar la transcripción."
        )

    captions = []
    for w in edl["palabras"]:
        captions.append({
            "text": w["word"],
            "startMs": round(w["start"] * 1000),
            "endMs": round(w["end"] * 1000),
            "timestampMs": round(w["start"] * 1000),
            "confidence": None,
        })
    return captions


def main() -> None:
    parser = argparse.ArgumentParser(description="EDL -> Remotion Caption[]")
    parser.add_argument("edl", help="Ruta a edl.json generado por video_engine")
    parser.add_argument("out", help="Ruta de salida .json para remotion/public/")
    args = parser.parse_args()

    try:
        captions = convert(Path(args.edl))
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(captions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Captions escritos en: {out_path} ({len(captions)} palabras)")


if __name__ == "__main__":
    main()
