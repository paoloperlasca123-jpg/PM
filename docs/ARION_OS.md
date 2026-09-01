# ARION_OS — Sistema Operativo de Contenido

## Principio central

**SISTEMA** (código, reglas, plantillas, conectores) vive en este
repositorio de git. **CONTENIDO** (videos, recursos, manifiestos
reales de clientes — archivos pesados) vive fuera de git, en el
filesystem local, por defecto en `~/ArionOS` (configurable con
`ARION_OS_ROOT` o `--root`).

Esto es intencional: git no debe cargar video pesado, y los datos de
clientes no deben depender de estar sincronizados con GitHub.

## Estructura de CONTENIDO (creada por `scripts/init_arion_os.py`)

```
~/ArionOS/
├── 00_INBOX                     → todo lo nuevo entra aquí primero
├── 01_ARION_EMPRESA             → marca/redes/estrategia de la agencia
├── 02_MARCA_PERSONAL            → tu marca personal (misma forma que un cliente)
│   ├── 01_ESTRATEGIA
│   ├── 02_RECURSOS
│   └── PROYECTOS/VIDEO_XXX/...
├── 03_CLIENTES
│   └── <CLIENTE>/
│       ├── manifest.json
│       ├── 01_ESTRATEGIA
│       ├── 02_RECURSOS
│       └── PROYECTOS/VIDEO_XXX/...
├── 04_RECURSOS_COMPARTIDOS      → assets reutilizables entre proyectos
├── 05_AUTOMATIZACIONES          → puntero: el código real vive en este repo (PM)
├── 06_PROYECTOS_ACTIVOS         → index.json, NO copia física (ver más abajo)
├── 07_ARCHIVO                   → contenido cerrado/histórico
└── 08_SISTEMA_Y_DOCUMENTACION
    └── logs/automation.log      → registro JSON Lines de acciones
```

## Estructura de un proyecto de video

```
VIDEO_XXX/
├── manifest.json      → etapa_actual, cliente, plataformas, métricas
├── 01_RAW              → video crudo (cámara / iPhone)
├── 02_AUDIO             → audio grabado aparte, si aplica
├── 03_BROLL_RECURSOS
├── 04_EDICION            → proyecto de edición, subtítulos generados
└── 05_FINAL              → exports por plataforma
```

Nota: `media/` en la raíz de este repo es el entorno de pruebas del
**motor de edición automática** (transcripción, subtítulos, cortes —
desarrollado en la fase anterior del proyecto). No es donde vive el
contenido real de clientes; cuando el motor esté integrado, leerá y
escribirá directamente sobre `VIDEO_XXX/01_RAW` y `VIDEO_XXX/05_FINAL`.

## Por qué NO hay una carpeta por etapa

El flujo idea → investigación → guion → ... → archivo tiene 13 etapas,
pero la mayoría no producen un tipo de archivo distinto — son
*estados administrativos*, no *tipos de contenido*. Modelarlas como
carpetas físicas obligaría a mover archivos constantemente y a
duplicarlos.

En su lugar, cada proyecto tiene un `manifest.json` con el campo
`etapa_actual` (uno de los 13 valores). Las carpetas físicas
(`01_RAW`...`05_FINAL`) solo existen para tipos de archivo reales.

Esto también resuelve `06_PROYECTOS_ACTIVOS`: en vez de copiar
carpetas de proyectos activos (lo que generaría duplicados y
desincronización), es un `index.json` que lista los proyectos con
`etapa_actual` distinta de `publicado`/`archivo`, apuntando a su
ubicación real. Se recalcula, no se sincroniza a mano.

## Automatizaciones — qué es seguro y qué no

| Acción | ¿Automática? |
|---|---|
| Crear cliente / proyecto (`new_client.py`, `new_project.py`) | Sí, bajo tu ejecución explícita |
| Escribir `manifest.json`, crear carpetas nuevas | Sí |
| Registrar en `automation.log` | Sí, siempre |
| Mover archivos desde `00_INBOX` a su destino | Solo con confirmación tuya |
| Eliminar o sobrescribir archivos | Nunca automático |

Los watchers (vigilar `00_INBOX` en background) y las integraciones
con Gmail/CapCut/etc. se activan en fases posteriores (V2/V3) — ver
plan de implementación.

## Seguridad

1. Nunca se elimina nada automáticamente.
2. Nunca se sobrescribe un archivo original (nombres con ID único).
3. El backup del CONTENIDO (fuera de git) es responsabilidad de Time
   Machine o un espejo local/cloud — el sistema no lo reemplaza.
4. Todo movimiento/creación relevante se registra en
   `automation.log` (JSON Lines: timestamp, accion, origen, destino,
   resultado, error).
5. Acciones ambiguas o fuera de INBOX piden confirmación.
6. Credenciales nunca en el repo — variables de entorno o Keychain.
7. `.gitignore` cubre `.env`, `venv/`, `__pycache__/`, `models/`.

## Conectores

Ver `CONNECTORS/README.md`. Cada conector es independiente,
desactivado por defecto (`enabled: false`), con su propia
documentación de API oficial, scopes recomendados y automatizaciones
disponibles.

## Plan de implementación

- **MVP (este commit):** estructura completa, scripts de creación de
  cliente/proyecto, logging, esqueleto de conectores.
- **V2:** watcher de `00_INBOX` con clasificación por reglas (con
  confirmación), vía `launchd` + Python.
- **V3:** activar conectores con API oficial clara (Gmail primero).
- **V4:** capa de IA para lenguaje natural y clasificación de casos
  ambiguos, reutilizando la misma capa LLM diseñada para el motor de
  edición de video.

## Cómo usarlo

```bash
# Clona este repo en tu Mac, luego:
python3 scripts/init_arion_os.py                 # crea ~/ArionOS
python3 scripts/new_client.py "Juan Perez"        # nuevo cliente
python3 scripts/new_project.py "Titulo del video" --cliente JUAN_PEREZ
python3 scripts/new_project.py "Titulo"           # proyecto de marca personal (sin --cliente)

# Ruta de contenido personalizada:
export ARION_OS_ROOT=~/Documents/ArionOS
# o usar --root en cualquier script
```
