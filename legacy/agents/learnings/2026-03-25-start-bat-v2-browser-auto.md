---
fecha: 2026-03-25
tarea: start-bat-v2-browser-auto
tipo: operaciones
complejidad: baja
clusters: [sistema, web]
proyecto: learning-platform
patron: local-dev-with-auto-open
---

# Learning Platform v2 — Start.bat con Apertura Automática de Navegador

## Decisión clave
Actualizar `start.bat` para verificar archivos v2 requeridos y abrir el navegador automáticamente al iniciar el servidor local, facilitando testing rápido.

## Patrón reutilizable
**Nombre:** local-dev-with-auto-open
**Descripción:** Para desarrollo frontend local: script que (1) verifica archivos críticos antes de iniciar, (2) intenta múltiples servidores (Python, Node, PHP), (3) abre navegador automáticamente con `start http://localhost:PUERTO`, (4) muestra mensajes claros de error si falta algo.

## Qué funcionó
- Check inicial de 4 archivos: index.html, modules-v2.json, platform-v2.js, profiles.json
- Apertura automática con `start http://localhost:8000` (Python) o `:8080` (Node/PHP)
- Mensajes de error específicos si falta algún archivo v2
- Mensajes mejorados con emojis para mejor UX

## Qué evitar
- No abrir el navegador antes de que el servidor esté listo — `start` va después del echo del puerto
- No verificar solo index.html — los archivos JSON/JS críticos también deben existir
- No usar puertos distintos para cada opción — mantener 8000 (Python) y 8080 (Node/PHP)

## Skills usados
- web-deploy.md (testing local)

## Criterios que validaron el éxito
- `start.bat` actualizado con check de archivos v2
- Navegador se abre automáticamente en todos los casos (Python, Node, PHP)
- Error específico si falta modules-v2.json, platform-v2.js o profiles.json
- `index.html` actualizado para usar `platform-v2.js`

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: corto (~5min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-platform-v2-js-perfiles-gamificacion]] · [[2026-03-25-modules-v2-placeholders-personalizacion]]
