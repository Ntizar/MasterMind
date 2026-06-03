---
fecha: 2026-03-25
tarea: platform-v2-js-perfiles-gamificacion
tipo: software
complejidad: alta
clusters: [sistema, web]
proyecto: learning-platform
patron: stateful-personalization-engine
---

# Learning Platform v2 — Platform.js con Perfiles y Gamificación

## Decisión clave
Reescribir `platform.js` a `platform-v2.js` para soportar: (1) selección de perfil en onboarding, (2) personalización dinámica de contenido con placeholders, (3) sistema básico de XP y niveles, (4) estado persistente en localStorage v2.

## Patrón reutilizable
**Nombre:** stateful-personalization-engine
**Descripción:** Para plataformas educativas personalizables: motor JS que carga perfiles, reemplaza placeholders en runtime, guarda estado completo (perfil, progreso, XP) en localStorage, y restaura sesión al volver. Todo sin backend.

## Qué funcionó
- Onboarding en 2 pasos: nombre → selección de perfil (5 cards clickeables)
- `personalize()` function reemplaza 15+ placeholders según perfil
- XP system: +50 por módulo, +25 quiz perfecto, +200 completar todo
- Niveles cada 200 XP (5 niveles: Iniciado, Aprendiz, Operador, Arquitecto, Maestro)
- Estado persistente en `brainacademy_state_v2` con perfil, progreso, XP, badges
- Export JSON incluye perfil y gamificación

## Qué evitar
- No mezclar estado v1 y v2 — usar localStorage keys distintas
- No olvidar restaurar `userProfile` al cargar estado guardado
- No hardcodear nombres de nivel — usar array `levelNames`
- No award XP múltiples veces por mismo módulo (falta validación)

## Skills usados
- software-dev.md (JavaScript vanilla, fetch, localStorage)
- dashboard-dev.md (UX de gamificación)

## Criterios que validaron el éxito
- `platform-v2.js` creado con 550+ líneas
- Función `showProfileSelection()` carga 5 perfiles desde JSON
- Función `personalize()` reemplaza todos los placeholders
- Función `awardXP()` con level-up y modal
- Estado guarda: userName, userProfile, xp, level, badges, progress
- Export JSON incluye perfil y stats de gamificación

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: medio (~25min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-profiles-json-5-perfiles]] · [[2026-03-25-modules-v2-placeholders-personalizacion]]
