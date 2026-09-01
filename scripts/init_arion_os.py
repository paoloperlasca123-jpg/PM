#!/usr/bin/env python3
"""Inicializa la estructura raíz de ARION_OS en la carpeta de CONTENIDO.

Uso:
    python3 scripts/init_arion_os.py
    python3 scripts/init_arion_os.py --root ~/ArionOS
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arion_os.paths import get_content_root  # noqa: E402

TOP_LEVEL_FOLDERS = [
    "00_INBOX",
    "01_ARION_EMPRESA",
    "02_MARCA_PERSONAL",
    "03_CLIENTES",
    "04_RECURSOS_COMPARTIDOS",
    "05_AUTOMATIZACIONES",
    "06_PROYECTOS_ACTIVOS",
    "07_ARCHIVO",
    "08_SISTEMA_Y_DOCUMENTACION",
]

AUTOMATIZACIONES_README = """Esta carpeta es solo un puntero.

El código de ARION_OS (scripts, plantillas, conectores) vive en el
repositorio de git "PM", no aquí. Clónalo en tu Mac y ejecuta los
scripts desde ahí, apuntando a esta carpeta de contenido con --root
o con la variable de entorno ARION_OS_ROOT.
"""


def init_structure(root: Path) -> None:
    for folder in TOP_LEVEL_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    (root / "05_AUTOMATIZACIONES" / "LEEME.txt").write_text(
        AUTOMATIZACIONES_README, encoding="utf-8"
    )

    index_path = root / "06_PROYECTOS_ACTIVOS" / "index.json"
    if not index_path.exists():
        index_path.write_text("[]\n", encoding="utf-8")

    for sub in ("01_ESTRATEGIA", "02_RECURSOS", "PROYECTOS"):
        (root / "02_MARCA_PERSONAL" / sub).mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inicializa ARION_OS")
    parser.add_argument("--root", default=None, help="Ruta raíz de contenido (opcional)")
    args = parser.parse_args()

    root = get_content_root(args.root)
    init_structure(root)
    print(f"ARION_OS inicializado en: {root}")


if __name__ == "__main__":
    main()
