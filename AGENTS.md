# Ntizar Mastermind v4.0 — Referencia Rápida de Arquitectura

> **Un orquestador (Koldo) + 143 skills especializados.**
> Para reglas completas y principios del sistema, consultar **SOUL.md**.

---

## Diagrama de Flujo

```
Tarea del usuario
       │
       ▼
Koldo (orquestador)
  ├── Clasifica → dominio + complejidad (1-4)
  ├── Carga skills del dominio vía skill_view()
  └── Decide nivel de ejecución
        │
        ▼
  delegate_task → Subagente especializado
        │
        ▼
  Koldo integra, verifica y presenta resultado
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
| **Software** | 17 | Código, refactor, debug, testing |
| **GitHub** | 7 | PRs, issues, repo management |
| **Frontend** | 3 | Dashboards, Aurora CSS |
| **Backend** | 6 | APIs, ESM, fetch paralelo |
| **Infra** | 6 | Docker, seguridad, cache, HTTP |
| **DevOps** | 10 | Deploy NaN, cron jobs, pipelines |
| **Data Science** | 8 | Simuladores, Monte Carlo |
| **Creative** | 22 | Diagramas, ASCII, diseño |

### 🗄️ Archivo (LOW) — Solo si el usuario los pide

Skills nicho que solo se cargan explícitamente (70 skills en categorías como visión, MLops, STEM, media, etc.).

## Human Loop — Cuándo activar

| Criterio | Acción |
|----------|--------|
| >5 archivos modificados | Human loop obligatorio |
| Decisiones de arquitectura | Human loop obligatorio |
| Deploy a producción | Human loop obligatorio |
| Migraciones | Human loop obligatorio |
| Usuario lo solicita | Human loop obligatorio |

**Patrón:** Planificar → Esperar ✅ → Implementar → Esperar ✅ → Sintetizar → Esperar ✅

---

> Para reglas completas, principios del sistema y configuración del orquestador, consultar **[SOUL.md](SOUL.md)**.

**Hecho con ❤️ por David Antizar**  
**v4.0.0 — 2026-06-04**
