"""Resolución de la carpeta raíz de CONTENIDO de ARION_OS.

El contenido real (videos, recursos, manifiestos de cliente) vive
fuera de este repositorio de git, normalmente en el Mac del usuario.
Este módulo decide dónde está esa carpeta.
"""

import os
from pathlib import Path
from typing import Optional


def get_content_root(override: Optional[str] = None) -> Path:
    """Devuelve la carpeta raíz de contenido de ARION_OS, creándola si no existe.

    Orden de prioridad:
    1. `override` (por ejemplo, el flag --root de un script).
    2. Variable de entorno ARION_OS_ROOT.
    3. Valor por defecto: ~/ArionOS
    """
    if override:
        root = Path(override).expanduser()
    elif os.environ.get("ARION_OS_ROOT"):
        root = Path(os.environ["ARION_OS_ROOT"]).expanduser()
    else:
        root = Path.home() / "ArionOS"

    root.mkdir(parents=True, exist_ok=True)
    return root
