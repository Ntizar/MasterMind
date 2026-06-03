# Ntizar Mastermind v4.0 — Sistema de Agentes

> **Un orquestador, muchos especialistas.** Koldo clasifica, carga skills del dominio, y delega con `delegate_task`.

---

## Arquitectura

```
Koldo (SOUL.md)
  │
  ├── Clasifica tarea → dominio + complejidad
  ├── Carga skills del dominio relevante
  └── Decide: directo o delegate_task
        │
        ▼
  delegate_task → Subagente especializado
        │
        ▼
  Koldo integra y verifica
```

## Niveles de Ejecución

| Nivel | Tool Calls | Archivos | Patrón | Ejemplo |
|-------|-----------|----------|--------|---------|
| **1 — Directo** | 1-3 | 1-2 | Koldo solo | Buscar, leer, commit |
| **2 — Simple** | 4-8 | 3-5 | 1 delegate_task | Refactor de módulo |
| **3 — Paralelo** | 8+ | 5+ | 2-3 delegate_tasks | Frontend + Backend + Tests |
| **4 — Orquestación** | Proyecto completo | Multi-PR | Planner → Implementers → Reviewer | Feature completa |

## Especialización por Dominio

### 🔥 Core (HIGH) — Se cargan automáticamente

| Skill | Especialización |
|-------|----------------|
| `subagent-driven-development` | Planificar → delegar → 2-stage review |
| `delegar-no-comprimir` | Paralelizar vs comprimir contexto |
| `koldo-orchestration` | Patrón de delegación y niveles |
| `github-workflow` | Git, PR lifecycle, deploy |
| `systematic-debugging` | 4-phase root cause debugging |

### 📦 Dominio (MEDIUM) — Se cargan con `skill_view()`

| Dominio | Skills | Cuándo usar |
|---------|--------|-------------|
| **Software** | 17 skills | Código, refactor, debug, testing |
| **GitHub** | 7 skills | PRs, issues, repo management |
| **Frontend** | 3 skills | Dashboards, Aurora CSS |
| **Backend** | 6 skills | APIs, ESM, fetch paralelo |
| **Infra** | 6 skills | Docker, seguridad, cache, HTTP |
| **DevOps** | 10 skills | Deploy NaN, cron jobs, pipelines |
| **Data Science** | 8 skills | Simuladores, Monte Carlo |
| **Creative** | 22 skills | Diagramas, ASCII, diseño |

### 🗄️ Archivo (LOW) — Solo si el usuario los pide

Skills nicho que solo se cargan explícitamente.

## Human Loop

### Cuándo activar

| Criterio | Acción |
|----------|--------|
| >5 archivos modificados | Human loop obligatorio |
| Decisiones de arquitectura | Human loop obligatorio |
| Deploy a producción | Human loop obligatorio |
| Migraciones | Human loop obligatorio |

### Patrón

```
1. PLANIFICAR → presentar diffs/plan
2. ESPERAR → ✅ o feedback
3. IMPLEMENTAR → ejecutar con diffs visibles
4. ESPERAR → ✅ o feedback
5. SINTEZAR → presentar resultado
6. ESPERAR → ✅ para archivar
```

## Migración desde v3.1

| v3.1 Legacy | v4.0 Actual |
|---|---|
| 11 agentes OpenCode | 1 orquestador + 143 skills especializados |
| Obsidian vault | GitHub repo (Markdown plano) |
| OpenCode Task tool | `delegate_task` nativo |
| Ebbinghaus decay manual | `memory` + `session_search` |
| 15 skills propios | 143 skills Hermes |
| 2 capas (docs+exec) | 1 capa (GitHub) |
| 4 comandos slash | 0 comandos (lenguaje natural) |

## Legacy

El sistema v3.1 (Obsidian+OpenCode) se ha movido a `legacy/`. No se ejecuta, solo se mantiene como referencia.

---

**Autor:** David Antizar  
**Versión:** 4.0.0  
**Fecha:** 2026-06-03
