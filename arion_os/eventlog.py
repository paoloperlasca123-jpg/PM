"""Registro de acciones de ARION_OS en formato JSON Lines.

El log vive dentro de la carpeta de CONTENIDO (08_SISTEMA_Y_DOCUMENTACION/logs),
no en el repositorio de git, porque puede contener nombres de archivos y
clientes reales.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def log_event(
    root: Path,
    accion: str,
    origen: Optional[str] = None,
    destino: Optional[str] = None,
    resultado: str = "ok",
    error: Optional[str] = None,
) -> None:
    log_dir = root / "08_SISTEMA_Y_DOCUMENTACION" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "accion": accion,
        "origen": origen,
        "destino": destino,
        "resultado": resultado,
        "error": error,
    }

    with (log_dir / "automation.log").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
