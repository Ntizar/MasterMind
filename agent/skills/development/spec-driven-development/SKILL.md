---
name: spec-driven-development
description: "Usa al diseñar software con spec-kit (specify)."
version: "2.0.0"
tags: [specs, spec-kit, specify, desarrollo, golang, ia, especificaciones]
related_skills: [spec-driven-development, project-spec-workflow, plan, test-driven-development]
---

# Spec-Driven Development — flujo con spec-kit (specify)

> ⚠️ Corrección 2026-09-05 (auditoría): el CLI se instala con `uv tool install specify-cli` (no `pip install`), y el flujo actual es `specify init` + comandos slash `/speckit-*`, no `specify new spec/plan/tasks`.

**Repo:** `https://github.com/github/spec-kit` (Python, ~134K⭐).

## When to Use

- Cuando pidas construir software **especificando antes que codificando** (spec → plan → tasks) con el flujo que GitHub usa internamente.

## Uso (CLI actual)

```bash
uv tool install specify-cli                # NO pip install
# inicializar el repo
specify init
# el flujo usa comandos slash: /speckit-specify, /speckit-plan, /speckit-tasks,
# /speckit-implement, /speckit-converge, /speckit-constitution
# subcomandos: specify extension / preset / bundle / self / integration
```

## Estructura generada

- `specs/` (especificaciones) · `constitution.md` (vía `/speckit-constitution`) · `.specify/`
- *(CONTRACT.md, PLANNING.md, tasks/, `.specify/cache/` son de versiones viejas.)*

## Pitfalls

- Instalación: **`uv tool install specify-cli`**, no `pip install specify`.
- **No** existe `specify new spec/plan/tasks` ni `specify status` — el flujo es `specify init` + slash commands.

## Verificación

- `uv tool install specify-cli` → `specify init` en un repo vacío → usar `/speckit-specify` y ver `specs/` + `constitution.md`.
