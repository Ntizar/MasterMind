---
name: archify-diagram-compiler
version: "1.0.0"
description: "Use al querer diagramas de sistema verificables con diffs."
tags: [diagrams, architecture-as-code, json-ir, verification, nodejs, agent-skills]
---

# Archify — diagramas de arquitectura verificables (tt-a1i/archify)

Repo: https://github.com/tt-a1i/archify (MIT, ~49K⭐ verificado 2026-09-05, versión dev v2.17.0-dev.1). Sistema Node.js de renderizado+validación para agentes (Cursor, Claude Code, Codex CLI, OpenCode): el agente produce **JSON IR tipado**, Archify lo compila **determinísticamente** a HTML/SVG.

## Idea central (patrón reutilizable)
- **Diagram-as-code con IR tipado**: en vez de que el LLM escriba SVG directamente (alucina topología), genera un JSON IR validado y un compilador determinista lo renderiza. Interacciones 100% grounded: sin topología inventada.
- **Diff de snapshots**: compara dos IR validados como Before / Delta / After con hechos exactos de nodos añadidos/eliminados/cambiados/movidos/re-enrutados. Útil para revisar cambios de arquitectura antes de merge.
- 5 tipos de diagrama (arquitectura, workflow, secuencia, data-flow, lifecycle), 4 presets, temas claro/oscuro, marcas de marca, movimiento finito.
- Export: HTML autocontenido + PNG, SVG, WebM y share cards 1200×630.

## Workflow
1. Instalar desde el repo (npm) o el zip del skill; se integra como skill nativo en Claude Code / Codex / OpenCode.
2. El agente escribe JSON IR (tipos de nodos, aristas, agrupaciones, rutas) conforme al schema de Archify.
3. Compilar: Node produce HTML validado; cualquier violación de schema falla antes de renderizar.
4. Para revisión de cambios: guardar IR por versión y pedir el diff de snapshots.
5. Export: PNG/SVG/WebM/1200×630 desde el HTML interactivo.

## Cuándo elegirlo sobre escribir SVG a mano
- Necesitas **verificabilidad** (IR validado, cero topología inventada) o **diffs entre versiones** de arquitectura.
- Pipeline automatizado: muchos diagramas regenerables desde descripciones estructuradas.
- Para un diagrama editorial one-off, usar `creative/editorial-diagrams` (estética) o `creative/architecture-diagram` (infra dark).

## Pitfalls
- Requiere Node.js (no funciona solo en navegador).
- El JSON IR debe seguir el schema exacto del repo — leer CHANGELOG/docs de la versión en uso (v2.16-dev en 2026-08, API en evolución).
- Interactividad (búsqueda, tracing, stories) vive en el HTML generado; el SVG estático pierde esas funciones.

## Verificación
- Compilación sin errores de validación de IR.
- Abrir el HTML: búsqueda de nodos, trace upstream/downstream y diff Before/After funcionan.
- Export PNG/SVG correcto a tamaño solicitado.
