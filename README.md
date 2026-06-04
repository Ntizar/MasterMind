<p align="center">
  <img src="assets/banner.svg" alt="Ntizar Mastermind" width="800"/>
</p>

<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>Framework de orquestación multi-agente con skills especializados por dominio.<br>Ejecutándose en Hermes Agent sobre NaN.builders con GitHub como repositorio.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#inicio-rápido">Inicio Rápido</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0-blue?style=flat-square" alt="Version 4.0"/>
  <img src="https://img.shields.io/badge/orquestador-1-purple?style=flat-square" alt="1 Orquestador"/>
  <img src="https://img.shields.io/badge/skills-143-orange?style=flat-square" alt="143 Skills"/>
  <img src="https://img.shields.io/badge/plataformas-Hermes+GitHub-green?style=flat-square" alt="Hermes + GitHub"/>
  <img src="https://img.shields.io/badge/licencia-MIT-lightgrey?style=flat-square" alt="MIT License"/>
</p>

---

## Tu IA que realmente recuerda

Usas IA todos los días. Copias y pegas contexto. Re-explicas tu proyecto. Pierdes aprendizajes entre sesiones. Tus prompts son largos, caros y frágiles.

**¿Y si tu IA tuviera cerebro?**

No un chatbot. No un solo prompt. Un sistema estructurado, con un orquestador inteligente, 143 skills especializados y memoria persistente.

**Diseñado para la comunidad nan.builders** — ejecutándose en Hermes Agent sobre NaN.builders con GitHub como repositorio.

---

## ¿Qué es Ntizar Mastermind?

Ntizar Mastermind es un **framework de orquestación multi-agente** que usa **Hermes Agent** como motor de ejecución y **GitHub** como fuente de verdad.

```
Tu das una tarea
    │
    ▼
Koldo (orquestador) la clasifica (dominio + complejidad)
    │
    ▼
Carga los skills especializados del dominio relevante
    │
    ▼
Cada skill ejecuta con conocimiento profundo de su dominio
    │
    ▼
Koldo integra, verifica y presenta el resultado
    │
    ▼
La siguiente sesión empieza más inteligente, no desde cero
```

### Comparativa rápida

| Característica | v3.1 (Legacy) | **v4.0 (Actual)** |
|---|---|---|
| Plataforma | OpenCode + Obsidian | **Hermes Agent + GitHub** |
| Agentes | 11 agentes genéricos | **1 orquestador + 143 skills especializados** |
| Modelos | Multi-modelo manual | **Modelo único (qwen3.6)** |
| Memoria | Ebbinghaus decay manual | **`memory` + `session_search` nativo** |
| Skills | 15 skills propios | **143 skills Hermes (carga bajo demanda)** |
| Archivos | 221 (2 capas) | **136 (1 capa, Markdown plano)** |
| Deploy | GitHub Pages | **NaN.builders + GitHub Pages** |
| Portabilidad | Obsidian vault | **VM permanente** |

---

## ¿Cómo funciona?

### 1. Un orquestador, muchos especialistas

**Antes (v3.1):** 11 agentes genéricos que hacían todo y mal.

**Ahora (v4.0):** 1 orquestador (Koldo) que clasifica y delega a 143 skills especializados.

| Dominio | Skills | Especialización |
|---------|--------|----------------|
| 🔥 **Software** | 17 | TDD, debug, code review, refactor |
| 📦 **GitHub** | 7 | PR workflow, issues, repo mgmt |
| 📦 **Frontend** | 3 | Aurora Design System, dashboards |
| 📦 **Backend** | 6 | APIs REST, ESM, fetch paralelo |
| 📦 **Infra** | 6 | Docker, seguridad, cache, HTTP |
| 📦 **DevOps** | 10 | Deploy NaN, cron jobs, pipelines |
| 📦 **Data Science** | 8 | Simuladores, Monte Carlo |
| 📦 **Creative** | 22 | Diagramas, ASCII, diseño |

### 2. Niveles de ejecución

| Nivel | Cuándo | Patrón |
|-------|--------|--------|
| **1 — Directo** | Tareas simples (1-3 tool calls) | Koldo solo |
| **2 — Simple** | 3-5 archivos, 1 módulo | Koldo → 1 delegate_task |
| **3 — Paralelo** | 5+ archivos, múltiples módulos | Koldo → 2-3 delegate_tasks |
| **4 — Orquestación** | Proyectos completos | Planner → Implementers → Reviewer |

### 3. Human Loop

En cambios críticos (>5 archivos, decisiones de arquitectura, deploy), Koldo presenta diffs y espera ✅ antes de ejecutar.

**Nunca silenciar. Siempre aprobar.**

---

## Inicio Rápido

### Requisitos

- **Hermes Agent** — Framework de agentes
- **NaN.builders** — Infraestructura (MicroVM 1vCPU/2GB)
- **GitHub** — Repositorio de código

### Uso

No necesitas instalar nada. Koldo carga los skills necesarios automáticamente:

```
Tarea: "Refactoriza el frontend del dashboard"
  → Koldo clasifica → dominio: frontend-dashboard-patterns
  → Carga: aurora-design-system, frontend-dashboard-patterns
  → Delega: delegate_task con esos skills
  → Integra y verifica
```

### Niveles de carga de skills

1. **🔥 Core (HIGH)** → Se cargan automáticamente en cada sesión
2. **📦 Dominio (MEDIUM)** → Se cargan con `skill_view()` cuando toca
3. **🗄️ Archivo (LOW)** → Solo si el usuario los pide

---

## Estructura del Proyecto

```
NtizarBrainMasterMind/
├── SOUL.md              ← Orquestador (Koldo) + principios + reglas
├── AGENTS.md            ← Referencia rápida de arquitectura y niveles
├── CHANGELOG.md         ← Historial de cambios
├── CONTRIBUTING.md      ← Guía para contribuir
├── LICENSE              ← Licencia MIT
├── README.md            ← Este archivo
├── README_EN.md         ← Versión en inglés
├── legacy/              ← v3.1 (Obsidian+OpenCode) — referencia
│   ├── agents/          ← 11 agentes documentales legacy
│   ├── .opencode/       ← 11 agentes ejecutables legacy
│   └── skills/          ← 15 skills propios legacy
├── docs/                ← Documentación técnica
├── design-system/       ← Aurora Design System
├── learning-platform/   ← Brain Academy
└── assets/              ← Recursos estáticos (banners, imágenes)
```

**Nota:** Los 143 skills especializados viven en `/hermes-home/skills/` (sistema nativo de Hermes Agent), no en el repositorio de GitHub.

---

## Roadmap

- [ ] Migrar aprendizajes valiosos de `legacy/` a `memory` + `docs/`
- [ ] Crear skill `deployment-gate` para validación antes de deploy
- [ ] Eliminar branch `master` (quedar solo `main`)
- [ ] Implementar tracking de tokens y costes por sesión
- [ ] Explorar CDN Aurora Design System con tag de versión en lugar de `@master`

---

## Licencia

MIT License — David Antizar

---

**Hecho con (L) por David Antizar**  
**v4.0.0 — 2026-06-04**
