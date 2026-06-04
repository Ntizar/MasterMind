---
fecha: 2026-03-19
tarea: system-gaps-fix
tipo: operaciones
complejidad: media
clusters: [sistema]
proyecto: ninguno
patron: gap-fix-short-flow
---

# Corrección de gaps estructurales del sistema (ciclo 3)

## Decisión clave
Los gaps estructurales de un sistema nuevo se detectan mejor ejecutando ciclos reales que haciendo auditoría teórica — el uso revela lo que el diseño no anticipó.

## Patrón reutilizable
sí → `gap-fix-short-flow`
Cuando el diagnóstico ya está hecho (gaps identificados durante ciclos previos), usar flujo corto sin explorer ni planner: CLASSIFY → SPEC → IMPLEMENT → REVIEW → ARCHIVE. El reviewer verifica que no se rompió nada existente.

## Qué funcionó
- Diagnosticar gaps en conversación antes de ejecutar evita especulación en la spec
- 4 entregables ejecutados en paralelo en la fase implement (session-prompt.md, template-skill.md, AGENTS.md, 10-librarian.md)
- PASS limpio del reviewer sin reintentos (8/8 criterios, 0 findings)
- Usar `## Ciclo de reaprendizaje` como señal de detección para el librarian — sin listas hardcodeadas

## Qué evitar
- Dejar ciclos a medias — el session-state queda inconsistente si el archive no se ejecuta
- No asumir que el diseño inicial de un sistema cubre todos los casos de uso reales

## Skills usados
- ninguno

## Tests/criterios que validaron esto
Reviewer verificó 8 criterios: session-prompt.md autosuficiente, template-skill.md con 2 secciones nuevas, AGENTS.md con sección "Cómo dar tareas", 10-librarian.md con detección por `## Ciclo de reaprendizaje`, sin archivos rotos, sin reglas contradictorias, todo en español, todo en kebab-case.

## Conexiones
**Cluster:** #sistema
**Aprendizajes relacionados:** [[2026-03-19-software-skill-md]] · [[2026-03-19-dashboard-skill-md]]
