#!/usr/bin/env python3
"""Crea la estructura de un nuevo proyecto de video en ARION_OS.

Si no se pasa --cliente, el proyecto se crea bajo 02_MARCA_PERSONAL.

Uso:
    python3 scripts/new_project.py "Como escalar tu marca personal"
    python3 scripts/new_project.py "Caso de exito" --cliente JUAN_PEREZ
    python3 scripts/new_project.py "Titulo" --plataformas tiktok reels
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arion_os.eventlog import log_event  # noqa: E402
from arion_os.paths import get_content_root  # noqa: E402

TEMPLATE_PATH = (
    Path(__file__).resolve().parent.parent
    / "arion_os"
    / "templates"
    / "project_manifest.template.json"
)

SUBFOLDERS = ["01_RAW", "02_AUDIO", "03_BROLL_RECURSOS", "04_EDICION", "05_FINAL"]


def next_project_id(proyectos_dir: Path) -> str:
    existing = [p.name for p in proyectos_dir.glob("VIDEO_*") if p.is_dir()]
    numbers = []
    for name in existing:
        try:
            numbers.append(int(name.split("_")[1]))
        except (IndexError, ValueError):
            continue
    n = max(numbers, default=0) + 1
    return f"VIDEO_{n:03d}"


def create_project(
    root: Path, cliente: Optional[str], titulo: str, plataformas: List[str]
) -> Path:
    if cliente:
        cliente_dir = root / "03_CLIENTES" / cliente
        if not cliente_dir.exists():
            raise FileNotFoundError(
                f"El cliente '{cliente}' no existe. Créalo primero con new_client.py"
            )
        base = cliente_dir / "PROYECTOS"
    else:
        base = root / "02_MARCA_PERSONAL" / "PROYECTOS"

    base.mkdir(parents=True, exist_ok=True)
    project_id = next_project_id(base)
    project_dir = base / project_id

    for sub in SUBFOLDERS:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    template.update(
        {
            "id": project_id,
            "titulo": titulo,
            "cliente": cliente or "MARCA_PERSONAL",
            "plataformas_destino": plataformas,
            "etapa_actual": "idea",
            "creado": datetime.now(timezone.utc).isoformat(),
        }
    )
    (project_dir / "manifest.json").write_text(
        json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log_event(root, "nuevo_proyecto", destino=str(project_dir))
    return project_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea un nuevo proyecto de video en ARION_OS")
    parser.add_argument("titulo", help="Título o tema del video")
    parser.add_argument(
        "--cliente", default=None, help="Slug del cliente (si se omite, es de MARCA_PERSONAL)"
    )
    parser.add_argument(
        "--plataformas", nargs="*", default=["tiktok", "reels", "shorts"]
    )
    parser.add_argument("--root", default=None, help="Ruta raíz de contenido (opcional)")
    args = parser.parse_args()

    root = get_content_root(args.root)
    try:
        project_dir = create_project(root, args.cliente, args.titulo, args.plataformas)
    except FileNotFoundError as exc:
        log_event(root, "nuevo_proyecto", resultado="error", error=str(exc))
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Proyecto creado: {project_dir}")


if __name__ == "__main__":
    main()
