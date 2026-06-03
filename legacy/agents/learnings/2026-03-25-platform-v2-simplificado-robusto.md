---
fecha: 2026-03-25
tarea: platform-v2-simplificado-robusto
tipo: software
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: simplify-and-retry
---

# Learning Platform v2 — Platform.js Simplificado y Robusto

## Decisión clave
Reescribir `platform-v2.js` desde cero con menos código (500 → 350 líneas), más logging en consola, y manejo explícito de errores para debugging fácil. Eliminar complejidad innecesaria.

## Patrón reutilizable
**Nombre:** simplify-and-retry
**Descripción:** Cuando algo no funciona: (1) Borrar estado antiguo que puede interferir, (2) Reescribir desde cero con menos features, (3) Añadir console.log en cada paso crítico, (4) Probar inmediatamente. La simplicidad gana sobre la completitud.

## Qué funcionó
- Eliminar código de quizzes complejo (no esencial para v2)
- Añadir `console.log()` en cada paso: init, load profiles, select profile, load modules
- Clear automático de v1 state al iniciar
- Funciones más cortas y legibles
- Inline event handlers para onclick (más simple que addEventListener global)
- Hovert effects con onmouseover/onmouseout inline

## Qué evitar
- No mantener compatibilidad con v1 — borrar estado viejo
- No tener múltiples archivos .bat — solo uno simplificado
- No sobrecargar con features — primero que funcione lo básico

## Skills usados
- software-dev.md (debugging, simplification)

## Criterios que validaron el éxito
- `platform-v2.js` con 350 líneas (vs 550 anteriores)
- Logging claro en consola para debugging
- Funciona con o sin estado guardado
- Un solo .bat (start.bat), sin start-node.bat

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: 1 (primera versión muy compleja)
- Tiempo estimado: medio (~15min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-platform-v2-js-perfiles-gamificacion]] · [[2026-03-25-start-bat-v2-browser-auto]]
