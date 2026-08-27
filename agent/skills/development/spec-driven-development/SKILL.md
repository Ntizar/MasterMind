---
name: spec-driven-development
version: "1.0.0"
description: "Spec-Driven Development — metodología para construir software basado en specs (PRD, planes, constituciones) en vez de 'vibe coding'. Basado en el toolkit de GitHub spec-kit (113K⭐)."
tags: [development, methodology, spec, prd, planning, github, copilot]
---

# Spec-Driven Development (SDD)

## Resumen

SDD invierte el orden tradicional de desarrollo: **spec primero → código después**. En vez de comenzar codificando, empiezas con un documento de especificación que define:

- **Qué** construir (product scenario)
- **Por qué** (business value / user need)
- **Cómo medir** (success criteria)
- **Restricciones** (non-goals, constraints)

## Toolkit: `specify-cli`

El paquete `github/spec-kit` provee:

```bash
# Inicializar un proyecto SDD
specify init

# Crear una spec
specify new spec

# Crear un plan de trabajo
specify new plan

# Crear tareas desde la spec
specify new tasks

# Ver estado
specify status
```

## Estructura de un proyecto SDD

```
project/
├── CONTRACT.md          # Acuerdo entre stakeholders
├── PLANNING.md          # Plan de trabajo
├── tasks/               # Tareas desglosadas
│   ├── spec-001.md
│   └── spec-002.md
├── specs/               # Especificaciones
│   ├── SPEC-001.md     # Feature spec
│   └── SPEC-002.md     # API spec
├── constitution.md      # Reglas del equipo
├── .specify/
│   └── cache/
└── README.md
```

## Ventajas

| Aspecto | Vibe Coding | SDD |
|---------|-------------|-----|
| **Predictibilidad** | Baja | Alta |
| **Revisión** | Post-hoc | Pre-commit |
| **Calidad** | Variable | Consistente |
| **Documentación** | Escasa | Obligatoria |
| **IA-ready** | No | Sí (prompts estructurados) |
| **Despliegue** | Caótico | Orquestado |

## Integración con IA

Spec Kit soporta:

- **GitHub Copilot** — specs como contexto
- **Claude Code** — plans como prompt
- **Cursor, Codex, Windsurf** — SDD como workflow
- **Any LLM**: Las specs son prompts perfectos

## Flujo típico con Mastermind

1. **Spec primero** → `specify new spec`
2. **Plan** → `specify new plan`
3. **Tasks** → `specify new tasks`
4. **Implementar** → usar skills de Mastermind
5. **Review** → `specify status` (checklist)

## Pitfalls

- No sobre-documentar — las specs deben ser **ejecutables**, no ensayos
- SDD funciona mejor con **proyectos > 1 semana** (para proyectos de 1 día, plan en README)
- La `constitution.md` del repo define reglas de IA (no override)

## Referencia

- Repo: `github/spec-kit`
- CLI: `specify` (Python, pip install)
- Docs: https://github.github.io/spec-kit/