# ARION_OS

Sistema de organización y automatización de contenido para **Arion**
(agencia, marca personal y marcas personales de clientes), más el
motor de edición automática de video para TikTok/Reels/Shorts.

- Arquitectura completa y guía de uso: [`docs/ARION_OS.md`](docs/ARION_OS.md)
- Conectores (Gmail, Drive, CapCut, etc.): [`CONNECTORS/README.md`](CONNECTORS/README.md)
- Scripts de gestión: `scripts/init_arion_os.py`, `scripts/new_client.py`, `scripts/new_project.py`
- Entorno de pruebas del motor de edición de video: [`media/`](media/)

## Quickstart

```bash
python3 scripts/init_arion_os.py            # crea la carpeta de contenido (~/ArionOS por defecto)
python3 scripts/new_client.py "Nombre Cliente"
python3 scripts/new_project.py "Titulo del video" --cliente NOMBRE_CLIENTE
```

El contenido real (videos, recursos) vive fuera de este repo, en el
filesystem local — ver `docs/ARION_OS.md` para el porqué.
