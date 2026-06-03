# Session State

## Estado actual
tarea_activa: ninguna
fase_actual: ninguna
ultimo_checkpoint: migración a v3 — multi-agente real
subagente_en_curso: ninguno
reintentos_restantes: 2
bloqueado_por: ninguno
version_sistema: 3.1

## Historial de sesiones anteriores
> 13 ciclos completados en sesiones previas (2026-03-19 a 2026-03-25).
> Sesión 2026-03-26: migración del sistema a v3 (multi-agente real con OpenCode subagents).
> Detalles en los learnings individuales del [[_index|learnings/_index]].

## Tareas pendientes de archivar
- Ninguna — todas las tareas previas archivadas en ciclo v3

## Notas de contexto activo
- **Skills activos:** 4 → [[software-dev]], [[dashboard-dev]], [[pwa-android]], [[web-deploy]]
- **Learnings registrados:** 32 → indexados en [[_index|learnings/_index]] (con decay Ebbinghaus)
- **Clusters activos:** 7 → #sistema, #github, #web, #arquitectura-software, #datos, #finanzas-tech, #mobile
- **Proyectos con hub:** 5 → [[montecarlo]], [[nap-dashboard]], [[caedelcielo]], [[medvisit]], [[learning-platform]]
- **Agentes ejecutables:** 11 → en `.opencode/agents/` (2 primary + 9 subagents)
- **Comandos disponibles:** 4 → `/ntizar-start`, `/ntizar-status`, `/ntizar-models`, `/ntizar-archive`

## Reglas permanentes del sistema
> Consolidadas de 13 ciclos de aprendizaje + migración v3. Cada regla está vinculada a su learning de origen.

|| # | Regla | Origen |
||---|-------|--------|
|| R1 | Flujo completo obligatorio — ningún agente se salta, aunque emita "PASS SIN HALLAZGOS" | ciclo-4 |
|| R2 | Sincronización multi-archivo — propagar datos críticos a todos los archivos antes de copiar a deploy | [[2026-03-19-caedelcielo-multifile-sync]] |
|| R3 | Iconos PWA: PNG binarios reales — verificar magic bytes `89504e47` antes de desplegar | [[pwa-android]] |
|| R4 | GitHub Pages no sirve desde /public — usar GitHub Actions con peaceiris/actions-gh-pages | [[2026-03-20-montecarlo-github-pages-subdirectory]] |
|| R5 | README actualizado con cada versión — incluir número y Changelog detallado | ciclo-11 |
|| R6 | [[00-orchestrator]] pregunta al humano antes de decidir diseño/arquitectura — nunca decide en silencio | regla global #8 |
|| R7 | Clusters dinámicos — se crean con nuevos dominios, no se definen cerrados | regla global #9 |
|| R8 | Learnings individuales bajo demanda — según señal y decay R(t) > 0.3 del [[_index\|learnings/_index]], nunca todos | [[2026-03-24-sistema-v2-index-inteligente]] |
|| R9 | Capacidad mínima por agente documentada — ver tabla en [[_system-config]] | [[2026-03-24-sistema-v2-index-inteligente]] |
|| R10 | Critic: omitir antes que degradar — notificar al humano si se omite | [[2026-03-24-sistema-v2-index-inteligente]] |
|| R11 | Verificar site live antes de entregar en cualquier deploy | [[2026-03-20-montecarlo-deploy-sin-verificar]] |
|| R12 | El orchestrator PROPONE modelos por subagente — nunca decide en silencio. El humano confirma o modifica. | migración v3 |
|| R13 | Critic activación objetiva — se activa automáticamente si ≥1 criterio se cumple (complejidad≥4, ≥3 reintentos, ≥3 archivos, impacto alto, reviewer WARNINGs) | v3.1 |

## Notas técnicas
- MonteCarloInversion live: https://ntizar.github.io/MonteCarloInversion/
- Pendiente: test con API key real en producción (Vercel deploy) — nap-dashboard
- v3: classifier integrado en orchestrator (ntizar-build). 01-classifier.md conservado como doc.
- v3: `agents/` = docs completas (Obsidian). `.opencode/agents/` = config ejecutable. Verificar con `verify-system.bat`
