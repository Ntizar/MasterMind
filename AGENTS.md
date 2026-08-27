# Ntizar MasterMind v4.2 — Referencia Rápida

> **Agente Mastermind + skills indexados semánticamente.**
> Reglas completas → **[SOUL.md](SOUL.md)**

---

## Flujo real

```
Tarea del usuario
       │
       ▼
Mastermind (agente Hermes — qwen3.8 / glm5.3 vía NaN API)
  ├── 1. Consulta ChromaDB → scripts/consultar-skills.py
  ├── 2. Filtra score > 0.25
  ├── 3. Carga skills con skill_view()
  ├── 4. Decide nivel de ejecución (1-4)
  │     ├── 🟢 Directo (1-3 tool calls)
  │     ├── 🟡 Simple (4-8 tool calls)
  │     ├── 🟠 Paralelo (delegate_task)
  │     └── 🔴 Orquestación (multi-subagente)
  ├── 5. Ejecuta y verifica
  └── 6. Aprendizaje continuo
        ├── ¿Skill nuevo? → skill_manage(create) + indexar-skills.py
        ├── ¿Nota? → notes/YYYY-MM-DD-titulo.md
        └── ¿Memoria? → memory(add)
```

## ChromaDB — Búsqueda semántica

**Skills indexados por significado, no por nombre.** La cifra crece con cada ciclo — no es fija.

```bash
# Consultar skills relevantes (desde la raíz del repo)
python scripts/consultar-skills.py "tu consulta" --json

# Re-indexar (nuevos skills) o todo (--reset)
python scripts/indexar-skills.py [--reset]
```

- **BBDD:** `~/.mastermind/chromadb` (persistente, embebida — no necesita servidor)
- **Colección:** mastermind-skills
- **Modelo:** qwen3-embedding (NaN API) — dim 4096
- **Distancia:** coseno · **Threshold:** score > 0.25
- **Python:** usar el Python del sistema (`C:\Users\d_ant\AppData\Local\Programs\Python\Python312\python.exe`), no el venv de Hermes

## Niveles de Ejecución

| Nivel | Tool Calls | Cuándo |
|-------|-----------|--------|
| **🟢 1 — Directo** | 1-3 | Buscar, leer, commit |
| **🟡 2 — Simple** | 4-8 | Refactor de módulo |
| **🟠 3 — Paralelo** | 8+ | Frontend + Backend + Tests |
| **🔴 4 — Orquestación** | Completo | Feature completa, multi-subagente |

## Estructura del repo

| Ruta | Qué es |
|------|--------|
| `agent/skills/` | Skills por dominio (fuente de verdad) |
| `agent/MEMORY.md` + `agent/USER.md` | Memoria persistente |
| `agent/SOUL.md` | Identidad del agente |
| `scripts/` | Motor: ChromaDB, stars, backup, lifecycle |
| `notes/` | Notas de aprendizaje |
| `data/` | stars-registry.json |
| `mastermind/` | Docs del sistema |

## Cron Jobs Activos

| Job | Schedule | Estado |
|-----|----------|--------|
| `mastermind-scout` | cada 6h | ✅ (explora stars → crea skills → push) |
| `mastermind-weekly-digest` | lunes 09:00 | ✅ (resumen semanal) |

Otros crons del sistema antiguo (ESIOS, BiciMad, inventario APIs...) se pueden reactivar bajo demanda.

## Dominios de Skills

Core · GitHub · Frontend · Backend · Infra · DevOps · Data Science · Creative · Mastermind · STEM · Visión/ML · GIS/Transporte · Salud · Crypto · Media · Investigación — y creciendo.

**Total: consulta con `python scripts/indexar-skills.py` — el número no es fijo.**

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

**Hecho con ❤️ por David Antizar** · **v4.2 — 2026-08-27**
