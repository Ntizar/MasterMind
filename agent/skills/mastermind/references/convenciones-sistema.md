# Convenciones de Sistema — Mastermind 2026-06-03

## Memoria (MEMORY.md / USER.md)

Formato: cada entrada empieza con `[categoria]` seguido del texto, separadas por `§`.

Categorías vigentes:
- `[infra]` — Configuración del stack, NaN, SOUL.md
- `[aurora]` — Aurora design system, nightly jobs
- `[esios]` — ESIOS API, indicadores, pitfalls técnicos
- `[skills]` — Skills del sistema, scripts de búsqueda
- `[pdf]` — Pipeline PDF→artifacts
- `[lang]` — Idioma (castellano)
- `[identidad]` — Nombre, alias, atribución
- `[prefs]` — Preferencias de comunicación, CSS, TTS, workflow

Companion: `INDEX.yaml` en `repo raíz/memories/` — versión estructurada con árbol jerárquico.

## Notas (notes/)

Toda nota nueva DEBE tener frontmatter YAML:

```yaml
---
title: Título descriptivo
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
category: sistema|infraestructura|esios|github|multi-agent|vision|other
author: David Antizar
---
```

Usar `notes/_template.md` como plantilla.

## Índice de notas

`notes/INDEX.md` se genera con:

```bash
python3 /root/workspace/Mastermind/scripts/generate-notes-index.py
```

El script parsea frontmatter de todas las notas y las agrupa por categoría en formato tabla. Las notas sin frontmatter aparecen como "other" y sin badge ✅.

## Prioridad de skills

`config/skill-priority.json` categoriza los 144 skills en 3 niveles:

- **HIGH (42):** Core. ESIOS, Aurora, infraestructura, HTTP, debugging, GitHub, etc.
- **MEDIUM (55):** Dominio. Visión, testing, multi-agente, solar, voz, vídeo, etc.
- **LOW (45):** Archivo. MLops, red-teaming, gaming, Apple, experimentos.

Regla: cargar MEDIUM bajo demanda por dominio. No cargar todos.

## Configuraciones clave

| Parámetro | Valor | Dónde |
|---|---|---|
| auto_prune | true | config.yaml → sessions |
| retention_days | 60 | config.yaml → sessions |
| voice (TTS) | es-ES-AlvaroNeural | config.yaml → tts → edge |
| language | es | config.yaml → display |
| memory_char_limit | 2200 | config.yaml → memory |
| user_char_limit | 1375 | config.yaml → memory |

## Scripts de mantenimiento

| Script | Función | Cuándo ejecutar |
|---|---|---|
| `scripts/generate-notes-index.py` | Regenera INDEX.md | Tras crear/modificar notas |
| `scripts/mastermind-autoconfig.sh` | Sync bidireccional repo↔Hermes | Diario (cron 09:00 UTC) |
| `scripts/restore-soul.sh` | Restaurar SOUL.md truncado | Cuando SOUL.md <1000 bytes |
| `scripts/backup-hermes-memory.sh` | Backup memoria a repo | Manual cuando memoria cambie |

## Historial de cambios

- **2026-06-03:** Auto-auditoría completa. MEMORY.md reestructurada con `[tags]`. INDEX.yaml companion. auto_prune activado. Frontmatter YAML en 14 notas. generate-notes-index.py creado. skill-priority.json con HIGH/MEDIUM/LOW. SOUL.md actualizado.