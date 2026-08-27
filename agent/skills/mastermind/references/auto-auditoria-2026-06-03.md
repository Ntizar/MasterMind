# Auto-auditoría 2026-06-03 — Mastermind al Desnudo

## Contexto

David pidió una autoauditoría honesta de cómo procesa información, usa brain/memory/skills, y dónde se almacena todo.

## Pipeline real de procesamiento (4 capas)

### ① System Prompt (~4KB / ~1K tokens)
- **Dónde:** `repo raíz/SOUL.md` → inyectado en system prompt de cada sesión
- **Qué:** Identidad, reglas, stack, pitfalls, preferencias
- **Frecuencia:** Cada sesión nueva + cada turno

### ② Memoria Activa (~3KB / ~800 tokens)
- **Dónde:** `MEMORY.md` + `USER.md` → inyectados en system prompt
- **Qué:** 15 facts técnicos + perfil usuario, categorizados con tags `[infra]` `[aurora]` `[esios]`
- **Frecuencia:** Cada turno

### ③ Skills Snapshot (~80KB / ~20K tokens)
- **Dónde:** `agent/skills/` + `index.json` → snapshot comprimido inyectado cada turno
- **Qué:** 144 skills (42 HIGH, 55 MEDIUM, 45 LOW)
- **Problema identificado:** 80KB por turno es desproporcionado
- **Mejora:** `config/skill-priority.json` prioriza HIGH sobre MEDIUM/LOW

### ④ Contexto de Sesión (variable)
- **Dónde:** `state.db` (SQLite) + sesiones JSONL
- **Qué:** Conversación actual + resultados de herramientas
- **Compresión:** threshold 50% → ratio 20%, protege primeros 3 + últimos 20 mensajes

## Métricas del sistema (2026-06-03)

| Métrica | Valor |
|---|---|
| Modelo | qwen3.6 vía NaN (128K tokens) |
| Skills | 144 totales (42 HIGH, 55 MEDIUM, 45 LOW) |
| Sesiones | 828 |
| Mensajes | 36.534 |
| Notas | 55 (17 con frontmatter YAML) |
| Commits | 67 |
| Cron jobs | 6 activos |
| DB size | 450MB SQLite |

## Mejoras implementadas en esta sesión

1. **Memory con tags** — MEMORY.md/USER.md categorizados, INDEX.yaml companion
2. **Auto-prune** — `auto_prune: true`, `retention_days: 60`
3. **Frontmatter YAML** — 14 notas con metadatos estructurados
4. **Índice auto-generado** — `generate-notes-index.py` → `notes/INDEX.md`
5. **Prioridad de skills** — `config/skill-priority.json` con 3 niveles
