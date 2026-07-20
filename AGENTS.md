# NtizarBrainMasterMind v4.1 — Referencia Rápida

> **Agente Mastermind + 303 skills indexados semánticamente vía ChromaDB.**
> Reglas completas → **[SOUL.md](mastermind/SOUL.md)**

---

## Flujo real

```
Tarea del usuario
       │
       ▼
Mastermind (agente IA en NaN.builders)
  ├── 1. ChromaDB → consultar-skills.py "palabras clave" --json
  ├── 2. Filtra score > 0.25, carga con skill_view()
  ├── 3. Decide nivel de ejecución
  │     ├── 🟢 Directo   (1-3 tool calls)
  │     ├── 🟡 Simple    (4-8 tool calls)
  │     ├── 🟠 Paralelo  (delegate_task)
  │     └── 🔴 Complejo  (orquestación multi-subagente)
  ├── 4. Ejecuta y verifica
  └── 5. Aprendizaje continuo
        ├── ¿Skill nuevo? → skill_manage(create)
        ├── ¿Nota? → notes/YYYY-MM-DD-titulo.md
        └── ¿Memoria? → memory(add)
```

## ChromaDB — Búsqueda semántica

**303 skills indexados por significado, no por nombre.**

```bash
# Consultar skills relevantes
cd /hermes-home/scripts && NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python consultar-skills.py "tu consulta" --json

# Re-indexar todos los skills
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python indexar-skills.py [--reset]
```

- **URL:** localhost:8000
- **Colección:** mastermind-skills
- **Modelo:** qwen3-embedding (NaN API, 4096 dimensiones)
- **Distancia:** coseno
- **Threshold:** > 0.25
- **Re-indexación:** domingo 04:00 UTC (cron `chromadb-reindex-semanal`)

## Niveles de Ejecución

| Nivel | Tool Calls | Cuándo |
|-------|-----------|--------|
| **🟢 1 — Directo** | 1-3 | Buscar, leer, commit |
| **🟡 2 — Simple** | 4-8 | Refactor de módulo |
| **🟠 3 — Paralelo** | 8+ | Frontend + Backend + Tests |
| **🔴 4 — Complejo** | Proyecto completo | Feature completa, multi-subagente |

## Cron Jobs Activos (8 jobs Hermes)

| Job | Schedule | Estado |
|-----|----------|--------|
| `BiciMad Tetuán` | L-Mi 06:30, 13:00 | ✅ ok |
| `inventario-apis-procesar` | cada 30m | ✅ ok |
| `inventario-apis-resumen-diario` | 22:00 UTC | ✅ ok |
| `skill-maintenance` | día 1 cada mes | ✅ ok |
| `chromadb-reindex-semanal` | domingo 04:00 UTC | ✅ ok |
| `skills-sync-to-github` | 05:00 UTC diario | ✅ ok |
| `stars-explorer-nocturno` | 03:00 UTC diario | ✅ ok |
| `deep-learning-diario` | 03:30 UTC diario | ✅ ok |

## Human Loop

| Criterio | Acción |
|----------|--------|
| >5 archivos modificados | Activar human loop |
| Decisiones de arquitectura | Activar human loop |
| Deploy a producción | Activar human loop |
| Migraciones | Activar human loop |
| Usuario lo solicita | Activar human loop |

**Patrón:** Planificar → ✅ → Implementar → ✅ → Sintetizar → ✅

→ Detalle completo en **[mastermind/SOUL.md](mastermind/SOUL.md)**

---

**Hecho con ❤️ por David Antizar** · **v4.1 — 2026-07-20**