---
fecha: 2026-03-25
tarea: modules-v2-placeholders-personalizacion
tipo: software
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: placeholder-injection-pattern
---

# Learning Platform v2 — Modules.json con Placeholders para Personalización

## Decisión clave
Crear `modules-v2.json` con placeholders (`{{NAME}}`, `{{DURACION_TOTAL}}`, `{{EJEMPLO_RELEVANTE_1}}`, `{{CASOS_USO_LIST}}`, etc.) que se reemplazan dinámicamente en `platform.js` según el perfil del usuario.

## Patrón reutilizable
**Nombre:** placeholder-injection-pattern
**Descripción:** Para contenido multi-perfil: usar placeholders en el formato `{{VARIABLE}}` dentro del contenido base, y reemplazarlos en runtime con datos del perfil. Permite un solo archivo de contenido para múltiples audiencias.

## Qué funcionó
- Placeholders para: nombre, duración, ejemplos de dominio, casos de uso, vocabulario
- Cada módulo (M0-M5) tiene placeholders específicos
- M0: `{{DURACION_TOTAL}}`, `{{EJEMPLOS_DOMINIO}}`, `{{PERFIL_NOMBRE}}`, `{{PERFIL_DESCRIPCION}}`, `{{CASOS_USO}}`
- M1: `{{EJEMPLO_RELEVANTE_1/2/3}}`, `{{CASOS_USO_LIST}}`
- M5: `{{EJEMPLO_TAREA_PERFIL}}`
- Quizzes mantenidos en el mismo JSON

## Qué evitar
- No usar placeholders ambiguos — siempre descriptivos (`{{EJEMPLO_RELEVANTE_1}}` no `{{E1}}`)
- No olvidar ningún placeholder — si falta, se verá `{{VARIABLE}}` en el UI
- No poner placeholders en los quizzes (las preguntas son iguales para todos)

## Skills usados
- software-dev.md (estructura JSON)

## Criterios que validaron el éxito
- `modules-v2.json` creado con 6 módulos (M0-M5)
- Todos los placeholders documentados y consistentes
- Quizzes incluidos en M1, M2, M3, M4, M5
- Botones de navegación con `data-next` y `data-prev`

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: medio (~20min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-profiles-json-5-perfiles]] · [[2026-03-25-modules-json-estructura-perfiles]]
