# Ntizar Mastermind v4.0 — Referencia Rápida

> **Un orquestador (Koldo) + 143 skills especializados.**
> Reglas completas y principios → **[SOUL.md](SOUL.md)**

---

## Flujo

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

| Nivel | Tool Calls | Archivos | Cuándo usar |
|-------|-----------|----------|-------------|
| **🟢 1 — Directo** | 1-3 | 1-2 | Buscar, leer, commit |
| **🟡 2 — Simple** | 4-8 | 3-5 | Refactor de módulo |
| **🟠 3 — Paralelo** | 8+ | 5+ | Frontend + Backend + Tests |
| **🔴 4 — Orquestación** | Completo | Multi-PR | Feature completa |

## Skills por Dominio

| Dominio | Skills | Cuándo |
|---------|--------|--------|
| 🔥 **Core** | 17 | TDD, debug, code review, refactor |
| 📦 **GitHub** | 7 | PR workflow, issues, repo mgmt |
| 📦 **Frontend** | 3 | Aurora CSS, dashboards |
| 📦 **Backend** | 6 | APIs REST, ESM, fetch paralelo |
| 📦 **Infra** | 6 | Docker, seguridad, cache, HTTP |
| 📦 **DevOps** | 10 | Deploy NaN, cron jobs, pipelines |
| 📦 **Data Science** | 8 | Simuladores, Monte Carlo |
| 📦 **Creative** | 22 | Diagramas, ASCII, diseño |

> Skills nicho (LOW): 70 en categorías como visión, MLops, STEM, media. Solo si el usuario los pide.

## Human Loop

| Criterio | Acción |
|----------|--------|
| >5 archivos modificados | Activar human loop |
| Decisiones de arquitectura | Activar human loop |
| Deploy a producción | Activar human loop |
| Migraciones | Activar human loop |
| Usuario lo solicita | Activar human loop |

**Patrón:** Planificar → ✅ → Implementar → ✅ → Sintetizar → ✅

→ Detalle completo en **[SOUL.md](SOUL.md#human-loop--sistema-de-control)**

---

**Hecho con ❤️ por David Antizar** · **v4.0.2 — 2026-06-04**
