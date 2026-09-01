# Conectores de ARION_OS

Cada carpeta es un conector independiente. Ninguno se activa por
defecto: `config.json` trae `"enabled": false` hasta que se configure
explícitamente.

Estructura de cada conector:

```
<conector>/
  README.md      → qué automatiza, requisitos, límites conocidos
  config.json     → enabled, estado, permisos/scopes necesarios
```

Reglas:

- Ninguna credencial se guarda en estos archivos ni en el repo. Usa
  variables de entorno (`.env`, ignorado por git) o el Keychain de
  macOS para tokens locales.
- Un conector con `enabled: false` no debe ser invocado por ninguna
  automatización.
- CapCut no tiene API oficial de automatización: su carpeta documenta
  qué se puede preparar alrededor de la app, no una integración directa.

| Conector | Estado | API oficial |
|---|---|---|
| gmail | no_configurado | Sí (Gmail API, OAuth2) |
| google_drive | no_configurado | Sí |
| google_calendar | no_configurado | Sí |
| notion | no_configurado | Sí |
| slack | no_configurado | Sí |
| whatsapp_business | no_configurado | Sí (Cloud API, requiere cuenta business) |
| instagram | no_configurado | Sí (Graph API, cuentas business/creator) |
| tiktok | no_configurado | Sí (limitada, revisión de app requerida) |
| youtube | no_configurado | Sí (YouTube Data API) |
| dropbox | no_configurado | Sí |
| capcut | sin_api_oficial | No — ver README propio |
