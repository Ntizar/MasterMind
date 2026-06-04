---
fecha: 2026-03-25
tarea: fase-3-semana-1-sandbox-completo
tipo: operaciones
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: interactive-simulation-pattern
---

# FASE 3 Semana 1 — Sandbox Integrado Completado (Archivo)

## Decisión clave
Sandbox creado pero archivado (no visible en navbar) porque consume muchos tokens. La feature existe pero no se usa activamente. Prioridad cambiada a Mermaid.js, Analytics, Demo, Comparador, Misiones.

## Patrón reutilizable
**Nombre:** feature-archived-but-ready
**Descripción:** Cuando una feature funciona pero no se quiere activar: (1) Ocultar de UI (quitar navbar link), (2) Mantener archivos (sandbox.html, sandbox.js), (3) Documentar en learning por qué se archivó, (4) Mantener en start.bat check para que no se pierda. Permite reactivar fácilmente.

## Qué funcionó
- Sandbox: 6 tipos de respuesta + 1 default, typing indicator, agent-flow animation
- Ocultar: solo quitar navbar link, archivos intactos
- Archiving: este learning documenta el "por qué" de archivar

## Qué evitar
- No eliminar archivos — mantener para reactivar
- No olvidar documentar por qué se archivó
- No borrar el check en start.bat

## Skills usados
- software-dev.md (feature flagging, archiving)

## Criterios que validaron el éxito
- Sandbox funciona pero no está visible en navbar
- Archivos intactos en learning-platform/
- Documentado en learning por qué se archivó

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Decisión humana: "Sandbox consume muchos tokens, ocultarlo"
- Siguiente fase: Mermaid.js + Analytics + Demo

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-sandbox-integrado-semana-1]] · [[2026-03-25-fase-3-roadmap-creado]]

---

## 🔧 Para Reactivar Sandbox
1. En `index.html`, busca la sección navbar
2. Añade: `<a href="sandbox.html" ...>🧪 Sandbox</a>`
3. Start.bat ya tiene el check de sandbox.html y sandbox.js
