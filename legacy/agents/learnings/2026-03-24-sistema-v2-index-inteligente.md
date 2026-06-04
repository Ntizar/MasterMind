---
fecha: 2026-03-24
tarea: sistema-v2-index-inteligente
tipo: conocimiento
complejidad: alta
clusters: [#sistema]
proyecto: ninguno
patron: on-demand-context-loading
---

# Sistema v2 — Índice inteligente y gestión de tokens por agente

## Decisión clave
El sistema carga contexto bajo demanda usando señales de relevancia declaradas en `_index.md`, y cada agente documenta su capacidad mínima para que el humano pueda degradar al modelo más económico en fases mecánicas sin comprometer las fases críticas.

## Patrón reutilizable
**Nombre:** on-demand-context-loading
**Descripción:** Definir en el índice central una columna `señal_de_relevancia` (qué situación activa este learning) y una columna `cuando_cargar` (siempre / condicional). El orchestrator lee solo el índice al arrancar y carga el learning completo únicamente si la señal coincide con la tarea activa. Reduce el contexto de entrada ~40-60% en sesiones típicas.

## Qué funcionó
- Separar la tabla de índice del contenido de los learnings permite tomar la decisión de carga con coste casi cero
- Documentar la capacidad mínima requerida directamente en cada archivo de agente hace que la información esté donde se necesita, no en un doc separado que se puede olvidar
- La tabla de degradabilidad en `00-orchestrator.md` (degradable / no degradable / omitir antes de degradar) es suficientemente clara para que el humano tome la decisión sin tener que pensar
- Añadir `⚡ MODO AHORRO` como protocolo activable explícitamente evita que el orchestrator ahorre tokens sin avisar — el humano siempre sabe el coste de cada decisión

## Qué evitar
- No añadir señales de relevancia demasiado amplias ("cualquier tarea de software") — pierden su función de filtro. Deben ser precisas y situacionales
- No degradar el Critic — un critic con modelo débil tiende a aprobar todo sin detectar problemas reales; es peor que no tenerlo. Siempre notificar al humano si se omite

## Skills usados
- ninguno

## Criterios que validaron el éxito
- Los 11 archivos de agente (00-10) tienen `## Capacidad mínima requerida` verificado con grep (11/11 matches)
- `_index.md` tiene columnas `señal_de_relevancia` y `cuando_cargar` para cada learning
- `00-orchestrator.md` tiene `## Protocolo de gestión de tokens y modelo` con tabla de degradabilidad y protocolo ⚡ MODO AHORRO

## Contexto de la tarea
- Flujo ejecutado: orchestrator → spec-writer → implementer → reviewer → critic → synthesizer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: largo

## Conexiones
**Clusters:** #sistema
**Aprendizajes relacionados:** [[2026-03-19-system-gaps-fix]] · [[2026-03-24-sistema-v2-obsidian-graph]]
