---
name: agent-skills-standard
version: "1.0.0"
description: >
  Standard open Agent Skills — formato y patrón para skills reutilizables 
  de agentes IA. Inspirado en K-Dense-AI/scientific-agent-skills (26k⭐) 
  con 142 skills científicas. Incluye estructura SKILL.md, metadata, 
  y patrones de organización.
license: MIT
tags: [software-development, skills, standard, format]

---

# Standard Open Agent Skills

## Visión General

El estándar [Agent Skills](https://agentskills.io/) define un formato para skills reutilizables de agentes IA, compatible con Claude Code, Cursor, Codex, OpenCode, Hermes Agent y otros.

## Estructura SKILL.md

```yaml
---
name: skill-name
description: >
  Descripción clara de cuándo y para qué usar esta skill.
  Incluir palabras clave para matching automático.
allowed-tools: Read, Write, Edit, Bash, Browser
license: MIT license
metadata:
  version: "1.0"
  skill-author: Author Name
---

# Skill Title

## Overview

Descripción general de la skill y su propósito.

## When to Use

Lista de condiciones para activar la skill:
- Cuando el usuario pide X
- Cuando el contexto indica Y
- Para tareas de tipo Z

## When NOT to Use

Cuándo NO usar esta skill (evitar activación incorrecta).

## Quick Reference

| Concepto | Comando/Valor | Descripción |
|----------|--------------|-------------|
| X | `cmd` | Descripción |

## Numbered Steps

1. **Paso 1** — Descripción
2. **Paso 2** — Descripción
3. **Paso 3** — Descripción

## Pitfalls

- Error común 1 y cómo evitarlo
- Error común 2 y cómo evitarlo

## Verification

Cómo verificar que la skill se ejecutó correctamente.

## References
- [Repositorio](https://github.com/...)
- [Documentación](https://...)
```

## Estructura de Directorio

```
skill-name/
├── SKILL.md              # Definición principal
├── references/           # Documentación de referencia
│   ├── api.md
│   └── schemas.md
├── templates/            # Templates reutilizables
│   ├── config.yaml
│   └── report.md
└── scripts/              # Scripts de apoyo
    ├── validate.py
    └── generate.sh
```

## Patrones del Ecosistema

### K-Dense Scientific Skills (142 skills)
- Organización por dominio científico
- Scripts de validación (`scan_skills.py`)
- Assets de referencia

### Nango Agent Builder
- Skills para crear/mejorar subagentes
- Templates de agent files
- Ejemplos prácticos

### Orca Skills
- Skills para orquestación multi-agente
- Skills para CLI y computer use
- Patrón de mensajería inter-agentes

## Metadatos Importantes

| Campo | Descripción | Obligatorio |
|-------|-------------|-------------|
| `name` | Identificador único | Sí |
| `description` | Cuándo activar | Sí |
| `allowed-tools` | Herramientas permitidas | Sí |
| `license` | Licencia | Recomendado |
| `metadata.version` | Versión de la skill | Recomendado |
| `tags` | Tags para categorización | Opcional |
| `globs` | Glob patterns para activación | Opcional |
| `alwaysApply` | Aplicar siempre | Opcional |

## Referencias
- [Agent Skills Standard](https://agentskills.io/)
- [K-Dense Scientific Skills](https://github.com/K-Dense-AI/scientific-agent-skills) (26k⭐)
- [Nango Agent Builder](https://github.com/NangoHQ/nango) (9.4k⭐)
