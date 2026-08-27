# Mejorar app existente vs crear nueva (2026-06-10)

## Contexto

El usuario pidió "mejorar dieta-ntizar.apps.nan.builders" — añadir una pestaña IA, chatbot, macros vs objetivo.

## Error cometido

Creé un proyecto nuevo dieta-nan/ con package.json, server.js, index.html nuevos.

## Corrección

El usuario queria evolución del proyecto existente, no un proyecto nuevo.

### Patrón correcto

1. Clonar repo existente (/root/workspace/dieta/)
2. Modificar dashboard.html con patch — añadir nueva sección/tab
3. Extender server.js con nuevos endpoints
4. Actualizar Dockerfile si es necesario (ej: añadir USER appuser)
5. Commit + push — NaN redeploya automáticamente

### Lección

Cuando el usuario dice "mejorar X", "añadir a X", "actualizar X" — trabajar sobre X existente, no crear X-nuevo.
