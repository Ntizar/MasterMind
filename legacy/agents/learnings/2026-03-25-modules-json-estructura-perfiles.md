---
fecha: 2026-03-25
tarea: modules-json-estructura-perfiles
tipo: software
complejidad: baja
clusters: [sistema, web]
proyecto: learning-platform
patron: single-source-personalization
---

# Learning Platform v2 — Estructura de Módulos con Personalización Dinámica

## Decisión clave
Mantener un único `modules.json` como fuente de verdad para el contenido base (M0-M5) y usar `profiles.json` + lógica en `platform.js` para inyectar ejemplos, vocabulario y casos de uso dinámicamente según el perfil seleccionado.

## Patrón reutilizable
**Nombre:** single-source-personalization
**Descripción:** Para plataformas multi-perfil sin duplicar contenido: (1) Contenido base en un solo archivo, (2) Configuración de perfiles separada con vocabulario/ejemplos, (3) Inyección dinámica en runtime reemplazando placeholders. Reduce mantenimiento y evita inconsistencias.

## Qué funcionó
- Separar configuración (`profiles.json`) de contenido (`modules.json`)
- Usar placeholders en el contenido: `{{EJEMPLO_DOMINIO}}`, `{{CASO_USO_1}}`, `{{DURACION_ESTIMADA}}`
- La personalización ocurre en `platform.js` al cargar el módulo
- El mismo contenido base sirve para 5 perfiles distintos

## Qué evitar
- No duplicar `modules.json` × 5 perfiles — imposible de mantener
- No hardcodear ejemplos específicos en el contenido base
- No asumir que el usuario ya seleccionó perfil antes de cargar M0-M2

## Skills usados
- software-dev.md (estructura JSON)

## Criterios que validaron el éxito
- Decisión documentada: Opción B (personalización dinámica)
- `modules.json` se mantiene como única fuente de contenido
- `profiles.json` tiene datos para personalización
- `platform.js` se modificará para inyectar contenido por perfil

## Contexto de la tarea
- Flujo ejecutado: orchestrator → planner → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: corto (~5min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-profiles-json-5-perfiles]] · [[2026-03-25-learning-platform-v2-planificacion-ordenada]]
