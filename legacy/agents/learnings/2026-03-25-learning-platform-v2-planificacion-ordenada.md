---
fecha: 2026-03-25
tarea: learning-platform-v2-planificacion-ordenada
tipo: operaciones
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: iterative-development-with-context-limits
---

# Learning Platform v2 — Planificación Ordenada con Límites de Contexto

## Decisión clave
Para proyectos complejos como la v2 de la learning platform, trabajar por partes pequeñas y archivando cada learning intermedio evita exceder límites de contexto y permite retomar eficientemente.

## Patrón reutilizable
**Nombre:** iterative-development-with-context-limits
**Descripción:** Dividir proyectos grandes en micro-tareas de <15min cada una, archivar learning después de cada subtarea completada, y usar el índice para recuperar contexto al retomar. Esto mantiene el contexto fresco y permite pausar/reanudar sin pérdida.

## Qué funcionó
- Crear roadmap completo primero (visión global)
- Dividir en fases de 1 semana cada una
- El humano recordó la regla: "nunca pases el límite de contexto, si no llegues es mejor planificar y volver a empezar"
- Archivar la lección como learning para reaplicar

## Qué evitar
- No intentar implementar todo el roadmap en una sesión
- No saltar fases sin completar la anterior
- No olvidar archivar learnings intermedios

## Skills usados
- software-dev.md (estructura de proyectos web)
- web-deploy.md (consideraciones de deploy)

## Criterios que validaron el éxito
- Roadmap completo creado y archivado
- Lección de "trabajar ordenado por partes" explícitamente documentada
- Fase 1 lista para empezar de manera acotada

## Contexto de la tarea
- Flujo ejecutado: orchestrator → planner → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: corto

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-24-sistema-v2-index-inteligente]] · [[2026-03-25-learning-platform-vercel-deploy]]
