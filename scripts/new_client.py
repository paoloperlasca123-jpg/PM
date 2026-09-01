#!/usr/bin/env python3
"""Crea la estructura de un nuevo cliente dentro de ARION_OS.

Uso:
    python3 scripts/new_client.py "Juan Perez"
    python3 scripts/new_client.py "Juan Perez" --root ~/ArionOS
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arion_os.eventlog import log_event  # noqa: E402
from arion_os.paths import get_content_root  # noqa: E402

TEMPLATE_PATH = (
    Path(__file__).resolve().parent.parent
    / "arion_os"
    / "templates"
    / "client_manifest.template.json"
)


def slugify(name: str) -> str:
    return "_".join(name.strip().upper().split())


def create_client(name: str, root: Path) -> Path:
    slug = slugify(name)
    if not slug:
        raise ValueError("El nombre del cliente no puede estar vacío")

    client_dir = root / "03_CLIENTES" / slug
    if client_dir.exists():
        raise FileExistsError(f"El cliente '{slug}' ya existe en {client_dir}")

    for sub in ("01_ESTRATEGIA", "02_RECURSOS", "PROYECTOS"):
        (client_dir / sub).mkdir(parents=True, exist_ok=True)

    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    template.update(
        {
            "nombre": name,
            "slug": slug,
            "creado": datetime.now(timezone.utc).isoformat(),
        }
    )
    (client_dir / "manifest.json").write_text(
        json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    log_event(root, "nuevo_cliente", destino=str(client_dir))
    return client_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea un nuevo cliente en ARION_OS")
    parser.add_argument("nombre", help="Nombre del cliente, ej: 'Juan Perez'")
    parser.add_argument("--root", default=None, help="Ruta raíz de contenido (opcional)")
    args = parser.parse_args()

    root = get_content_root(args.root)
    try:
        client_dir = create_client(args.nombre, root)
    except (ValueError, FileExistsError) as exc:
        log_event(root, "nuevo_cliente", resultado="error", error=str(exc))
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Cliente creado: {client_dir}")


if __name__ == "__main__":
    main()
