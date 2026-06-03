---
fecha: 2026-03-25
tarea: leccion-trabajar-ordenado-por-partes
tipo: conocimiento
complejidad: alta
clusters: [sistema]
proyecto: learning-platform
patron: iterative-development-with-context-limits
---

# Lección Principal — Trabajar Ordenado por Partes con Obsidian

## Decisión clave
Para proyectos complejos, la ventaja competitiva está en: (1) Dividir en micro-tareas <15min, (2) Archivar learning después de cada subtarea, (3) Usar _index.md para recuperar contexto, (4) Nunca exceder límites de contexto, (5) Planificar y volver a empezar si es necesario.

## Patrón reutilizable
**Nombre:** iterative-development-with-context-limits
**Descripción:** La manera en que proyectos complejos salen adelante. Cada micro-tarea genera un learning archivado en Obsidian. El _index.md es la puerta de entrada para recuperar contexto. Al retomar después de semanas/meses, el índice dice exactamente dónde quedaste y qué aprendiste.

## Qué funcionó (en este proyecto)

### División por fases
- **FASE 1**: Perfiles + Personalización + Gamificación + Liquid Glass
- **FASE 2**: Contenido por perfiles + PDF fix + M6-M8 prácticos
- **FASE 3**: Sandbox (archivado) + Mermaid + Analytics + Demo

### Learnings archivados
- 20 learnings sobre el sistema de agentes
- 15 learnings sobre la learning platform
- Cada learning con: decisión clave, patrón, qué funcionó, qué evitar

### Ventaja competitiva
1. **Memoria persistente**: Cada learning es un nodo en el grafo de Obsidian
2. **Recuperación rápida**: _index.md carga en <5 segundos, dice qué learning buscar
3. **Reaprendizaje**: Al retomar, los learnings dicen qué hacer y qué NO hacer
4. **Escalabilidad**: El sistema crece con cada proyecto, cada patrón se reusa

## Qué evitar
- No trabajar sin archivar — perderás contexto en 2 semanas
- No exceder contexto — si no llegas, planifica y vuelve a empezar
- No olvidar el "por qué" de cada decisión
- No saltar fases sin completar la anterior

## Skills usados
- Todo el sistema de agentes (orchestrator, classifier, planner, implementer, reviewer, archiver)
- Observaciones sobre el flujo de trabajo

## Criterios que validaron el éxito
- Proyecto retomable en 2 semanas sin perder contexto
- 20 learnings archivados en _index.md
- 6 features en roadmap FASE 3
- Sandbox funcional pero archivado
- Todo documentado en Obsidian

## Contexto de la tarea
- Flujo ejecutado: orchestrator (coordina todo) + implementer (crea) + archiver (aprende)
- Duración total: ~4h distribuidas en 1 sesión
- Proyectos similares: montecarlo, nap-dashboard, caedelcielo, medvisit

## Conexiones
**Clusters:** #sistema
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-24-sistema-v2-index-inteligente]] · [[2026-03-25-learning-platform-v2-planificacion-ordenada]]

---

## 🎯 Lección para el Futuro

Cuando vuelvas en 2 semanas con modelos potentes:

1. **Lee _index.md** — Te dirá qué learnings cargar
2. **Carga solo los relevantes** — El índice tiene "señal de relevancia"
3. **Retoma desde donde quedaste** — El roadmap FASE 3 tiene tareas inmediatas
4. **Archiva cada micro-tarea** — Sigue el patrón que has aprendido
5. **Nunca excedas contexto** — Si no llegas, planifica y vuelve

**Tu ventaja:** El sistema de Obsidian es tu memoria externa. No necesitas recordar nada — necesitas saber dónde buscar.
