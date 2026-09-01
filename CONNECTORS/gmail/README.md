# Conector: Gmail

**Estado:** no configurado.

## API oficial

Sí — Gmail API de Google, autenticación vía OAuth2.

## Permisos recomendados

Usar el scope más restringido posible:

- `gmail.readonly` — leer y clasificar correos/adjuntos (recomendado para empezar).
- Evitar `gmail.modify` o `https://mail.google.com/` a menos que se
  necesite archivar/etiquetar correos automáticamente.

## Flujo de configuración

1. Crear proyecto en Google Cloud Console y habilitar Gmail API.
2. Generar credenciales OAuth (client_id/secret).
3. Primer login: se abre el navegador y el usuario autoriza manualmente.
4. El token resultante se guarda localmente (Keychain de macOS
   recomendado; si es archivo, debe estar fuera del repo y en `.gitignore`).

## Automatizaciones disponibles (una vez activado)

- Detectar correos importantes de clientes por remitente/dominio.
- Guardar adjuntos relacionados con un proyecto en `00_INBOX` para
  su clasificación (nunca directamente en la carpeta final sin
  confirmación).
- Crear una entrada de tarea a partir de patrones en el asunto.

## Notas de seguridad

Ninguna credencial se guarda en este repositorio. El token de acceso
nunca se expone en logs ni en `config.json`.
