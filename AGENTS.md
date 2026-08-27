# NtizarBrainMasterMind v4.1 — Referencia Rápida

> **Agente Mastermind + 265 skills indexados semánticamente.**
> Reglas completas → **[SOUL.md](SOUL.md)**

---

## Flujo real

```
Tarea del usuario
       │
       ▼
Mastermind (agente qwen3.6)
  ├── 1. Consulta ChromaDB → consultar-skills.py
  ├── 2. Filtra score > 0.25
  ├── 3. Carga skills con skill_view()
  ├── 4. Decide nivel de ejecución (1-4)
  │     ├── 🟢 Directo (1-3 tool calls)
  │     ├── 🟡 Simple (4-8 tool calls)
  │     ├── 🟠 Paralelo (delegate_task)
  │     └── 🔴 Orquestación (multi-subagente)
  ├── 5. Ejecuta y verifica
  └── 6. Aprendizaje continuo
        ├── ¿Skill nuevo? → skill_manage(create)
        ├── ¿Nota? → notes/YYYY-MM-DD-titulo.md
        └── ¿Memoria? → memory(add)
```

## ChromaDB — Búsqueda semántica

**265 skills indexados por significado, no por nombre.**

```bash
# Consultar skills relevantes
cd scripts && python3 consultar-skills.py "tu consulta" --json

# Re-indexar todos los skills
python3 indexar-skills.py [--reset]
```

- **URL:** localhost:8000
- **Colección:** mastermind-skills
- **Modelo:** qwen3-embedding (NaN API)
- **Distancia:** coseno
- **Threshold:** > 0.25
- **Re-indexación:** domingo 04:00 UTC (cron)

## Niveles de Ejecución

| Nivel | Tool Calls | Cuándo |
|-------|-----------|--------|
| **🟢 1 — Directo** | 1-3 | Buscar, leer, commit |
| **🟡 2 — Simple** | 4-8 | Refactor de módulo |
| **🟠 3 — Paralelo** | 8+ | Frontend + Backend + Tests |
| **🔴 4 — Orquestación** | Completo | Feature completa, multi-subagente |

## Skills por Dominio

| Dominio | Skills | Cuándo |
|---------|--------|--------|
| 🔥 **Core** | ~17 | TDD, debug, code review, refactor |
| 📦 **GitHub** | ~7 | PR workflow, issues, repo mgmt |
| 📦 **Frontend** | ~3 | Aurora CSS, dashboards |
| 📦 **Backend** | ~6 | APIs REST, ESM, fetch paralelo |
| 📦 **Infra** | ~6 | Docker, seguridad, cache, HTTP |
| 📦 **DevOps** | ~10 | Deploy NaN, cron jobs, pipelines |
| 📦 **Data Science** | ~8 | Simuladores, Monte Carlo |
| 📦 **Creative** | ~22 | Diagramas, ASCII, diseño |
| 🧠 **Mastermind** | ~10 | Orquestación, ChromaDB, deploy, backup |
| 📚 **STEM** | ~40 | Matemáticas, física, dibujo técnico, química, biología |
| 🔬 **Visión/ML** | ~15 | Object detection, segmentación, video |
| Otros | ~100 | MCP, salud, crypto, finanzas, media, geoespacial |

**Total: 265 skills** — cargados bajo demanda vía ChromaDB.

## Cron Jobs Activos (10 jobs Hermes)

| Job | Schedule | Estado |
|-----|----------|--------|
| `esios-daily-telegram` | 09:00 UTC | ✅ |
| `BiciMad Tetuán` | L-Mi 06:30, 13:00 | ✅ |
| `inventario-apis-procesar` | cada 30m | ✅ |
| `inventario-apis-resumen-diario` | 22:00 UTC | ✅ |
| `skill-maintenance` | día 1 cada mes | ✅ |
| `deep-learning` | 03:00 UTC | ✅ |
| `chromadb-reindex-semanal` | domingo 04:00 UTC | ✅ |
| `skills-sync-to-github` | cada 6h | ✅ |
| `stars-explorer-nocturno` | 03:00 UTC | ✅ |
| `gtfsspain-update` | domingo 06:00 UTC | ⏸️ pausado |

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

**Hecho con ❤️ por David Antizar** · **v4.1 — 2026-07-01**