# Ntizar Mastermind v4.0 — Sistema Hermes-Native

> **Framework de orquestación multi-agente con skills especializados por dominio.**
> Ejecutándose en Hermes Agent sobre NaN.builders con GitHub como repositorio.

---

## Qué es esto

Sistema de inteligencia operativa que usa **Hermes Agent** como motor de ejecución y **GitHub** como fuente de verdad. Reemplaza el antiguo sistema v3.1 (Obsidian+OpenCode) con una arquitectura 100% Hermes-native.

## Principios

1. **Un orquestador, muchos especialistas** — Koldo clasifica y delega. Los skills especializados ejecutan.
2. **GitHub como fuente de verdad** — Markdown plano, sin wikilinks, sin dependencias externas.
3. **Skills sobre agentes** — Cada rol se especializa en un dominio, no en un proceso genérico.
4. **Simpleza sobre complejidad** — `delegate_task` nativo > 11 agentes con specs y checkpoints.
5. **Human loop obligatorio** — En cambios críticos, Koldo presenta diffs y espera ✅.

## Arquitectura

```
Ntizar Mastermind v4.0
│
├── SOUL.md ← Orquestador (Koldo)
│   ├── Clasifica tarea → dominio + complejidad
│   ├── Carga skills del dominio relevante
│   └── Decide: directo o delegate_task
│
├── skills/ ← Especialistas por dominio
│   ├── software-development/  → 17 skills (dev, testing, debug, code review)
│   ├── github/                → 7 skills (PR, issues, repo management)
│   ├── frontend-dashboard/    → 3 skills (Aurora, patrones dashboard)
│   ├── backend/               → 6 skills (APIs, ESM, fetch paralelo)
│   ├── infraestructura/       → 6 skills (HTTP, Docker, seguridad, cache)
│   ├── devops/                → 10 skills (deploy NaN, Aurora Nightly)
│   ├── data-science/          → 8 skills (simuladores, Monte Carlo)
│   ├── creative/              → 22 skills (diagramas, diseño, ASCII)
│   └── ... (33 categorías, 143 skills)
│
├── legacy/ ← v3.1 (Obsidian+OpenCode) — referencia, no ejecución
│   ├── agents/        → 11 agentes documentales (marcados como legacy)
│   ├── .opencode/     → 11 agentes ejecutables (marcados como legacy)
│   └── skills/        → 15 skills propios (marcados como legacy)
│
├── projects/ ← Proyectos activos
│   ├── montecarlo/
│   ├── nap-dashboard/
│   ├── caedelcielo/
│   ├── learning-platform/
│   └── medvisit/
│
└── notes/ ← Notas de sesión (reemplaza agents/state/)
```

## Modelo de Especialización

### Antes (v3.1) — Agentes genéricos

```
Orchestrator → Explorer → Planner → Spec-Writer → Implementer → Reviewer → Critic → Synthesizer
```

Cada agente era un **rol genérico** sin especialización. El Implementer no sabía de frontend, backend, ni infra. Hacía todo y mal.

### Después (v4.0) — Skills especializados

```
Koldo (clasifica) → Carga skills del dominio → delegate_task con contexto especializado
```

Cada skill es un **especialista en un dominio**:

| Dominio | Skills | Especialización |
|---------|--------|----------------|
| **Software** | 17 skills | TDD, debug, code review, refactor, TDD, iteración |
| **GitHub** | 7 skills | PR workflow, code review, issues, repo management |
| **Frontend** | 3 skills | Aurora Design System, patrones dashboard vanilla JS |
| **Backend** | 6 skills | APIs REST, ESM interop, fetch paralelo, resúmenes |
| **Infra** | 6 skills | HTTP robusto, Docker, seguridad, cache, validación |
| **DevOps** | 10 skills | Deploy NaN, Aurora Nightly, MCP, Nango |
| **Data Science** | 8 skills | Simuladores eléctricos, Monte Carlo, análisis |
| **Creative** | 22 skills | Diagramas, ASCII, diseño, video, música |

**Resultado:** Mejor calidad porque cada skill tiene conocimiento profundo de su dominio, no genérico.

## Niveles de Ejecución

### Nivel 1 — Directo (Koldo solo)
- 1-3 tool calls
- 1-2 archivos
- Lectura, búsqueda, commit simple
- **Ejemplo:** "Busca errores en el deploy"

### Nivel 2 — Delegación simple
- 4-8 tool calls
- 3-5 archivos
- Koldo carga skills del dominio → 1 delegate_task
- **Ejemplo:** "Refactoriza el módulo de API"

### Nivel 3 — Paralelo
- 8+ tool calls
- Múltiples módulos independientes
- Koldo → 2-3 delegate_tasks en paralelo
- **Ejemplo:** "Optimiza frontend + backend + tests"

### Nivel 4 — Orquestación completa
- Proyectos grandes, múltiples PRs
- Planner → Implementers → Reviewer → Koldo integra
- **Ejemplo:** "Feature completa con backend, frontend, docs, tests"

## Human Loop

Cuando la tarea es crítica (>5 archivos, decisiones de arquitectura, deploy), Koldo ejecuta:

```
1. PLANIFICAR → presentas plan/diffs al humano
2. ESPERAR → ✅ o feedback
3. IMPLEMENTAR → ejecutas con diffs visibles
4. ESPERAR → ✅ o feedback
5. SINTEZAR → presentas resultado
6. ESPERAR → ✅ para archivar
```

**Reglas:**
- Nunca silenciar — terminar fase, presentar resultado, continuar
- Máximo 2 reintentos por fase
- Cambios >5 archivos → mostrar diffs antes de commit
- Decisión de diseño → siempre preguntar

## Memoria y Aprendizaje

| v3.1 (Legacy) | v4.0 (Actual) |
|---|---|
| Ebbinghaus decay manual en archivos | `memory` tool nativa de Hermes |
| 32 learnings en `agents/learnings/` | `session_search` + `memory` |
| Librarian mantenía índices | `skill_manage` + `skill_view` |
| `_index.md` con tabla de relevancia | Skills se cargan bajo demanda |

## Reglas Globales

1. Flujo completo obligatorio — ningún skill se salta
2. GitHub como fuente de verdad — Markdown plano
3. Nunca borrar del repo — solo crear o modificar
4. Notas significativas → `notes/YYYY-MM-DD-titulo.md`
5. Skills nuevos → `/hermes-home/skills/`
6. Cada aprendizaje importante → commit al repo
7. No crear secrets en notes/commits/chat
8. TODO en castellano — NUNCA inglés en repos, scripts, cron, informes
9. Atribución correcta: "Hecho con (L) por David Antizar"
10. Human loop en cambios críticos — nunca silenciar

## Migración de v3.1 → v4.0

| v3.1 | v4.0 | Estado |
|------|------|--------|
| 11 agentes OpenCode | 1 orquestador + 143 skills | ✅ Completado |
| Obsidian vault | GitHub repo | ✅ Completado |
| OpenCode Task tool | `delegate_task` nativo | ✅ Completado |
| Ebbinghaus decay | `memory` + `session_search` | ✅ Completado |
| 15 skills propios | 143 skills Hermes | ✅ Completado |
| 2 capas (docs+exec) | 1 capa (GitHub) | ✅ Completado |
| 4 comandos slash | 0 comandos (lenguaje natural) | ✅ Completado |
| Portabilidad Obsidian | VM permanente | ✅ Completado |

---

**Autor:** David Antizar  
**Versión:** 4.0.0  
**Fecha:** 2026-06-03  
**Stack:** Hermes Agent + NaN.builders + GitHub
