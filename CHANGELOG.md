# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] — 2026-06-03

### 🎯 Breaking Changes
- **Migrated from OpenCode+Obsidian to Hermes Agent+GitHub** — the entire system now runs on Hermes native tools
- **11 generic agents → 1 orchestrator + 143 specialized skills** — domain-based specialization replaces role-playing agents
- **All OpenCode configs moved to `legacy/`** — `.opencode/`, `agents/`, `skills/` now under `legacy/` (reference only, not executed)

### ✨ Added
- **`SOUL.md`** — Single orchestrator definition with principles, architecture, and rules
- **`AGENTS.md`** — System overview with execution levels and specialization model
- **`skills/SKILLS-INDEX.md`** — Complete index of 143 Hermes skills organized by domain with priority levels
- **`human-loop-control` skill** — Approval gate system for critical changes (>5 files, architecture decisions, production deploy)
- **Domain-based specialization model** — 8 skill domains (software, github, frontend, backend, infra, devops, data-science, creative) with HIGH/MEDIUM/LOW priority loading
- **`legacy/README.md`** — Documentation explaining the legacy v3.1 system

### 🔄 Changed
- **221 files → 136 files** — 108 legacy + 28 new
- **2 layers (docs+exec) → 1 layer (GitHub Markdown)** — no more Obsidian wikilinks or OpenCode YAML
- **Ebbinghaus decay manual → Hermes `memory` + `session_search`** — native persistence
- **15 skills propios → 143 skills Hermes** — loaded on-demand by domain
- **4 slash commands → language natural** — Koldo understands natural language
- **Multi-model per agent → single model (qwen3.6)** — simplified model management
- **README.md** — updated for v4.0 with comparison tables
- **`docs/ARCHITECTURE.md`** — complete rewrite with specialization model, human loop, memory system

### 🗑️ Removed
- **OpenCode dependency** — no more `.opencode/agents/` or `.opencode/commands/` in active code
- **Obsidian dependency** — no more `agents/` with wikilinks in active code
- **Ebbinghaus decay system** — replaced by Hermes native memory
- **Classifier subagent** — classification integrated in Koldo (already was in v3)
- **Spec-Writer subagent** — specs integrated into `delegate_task` goal
- **Planner subagent** — planning integrated in Koldo's decision process

### 📊 Migration Summary

| Aspect | v3.1 | v4.0 |
|--------|------|------|
| Platform | OpenCode + Obsidian | Hermes Agent + GitHub |
| Agents | 11 generic | 1 orchestrator + 143 specialized |
| Skills | 15 propios | 143 Hermes (carga bajo demanda) |
| Memoria | Ebbinghaus manual | `memory` + `session_search` |
| Archivos | 221 (2 capas) | 136 (1 capa) |
| Comandos | 4 slash | 0 (lenguaje natural) |
| Modelos | Multi-modelo manual | qwen3.6 único |

---

## [3.0.0] — 2026-03-26

### Added
- **Multi-agent real architecture** — 11 agents with OpenCode Task tool delegation
- **Two-layer architecture** — `agents/` (Obsidian docs) + `.opencode/agents/` (executable configs)
- **Ebbinghaus decay memory** — `R(t) = a/(log(t+1))^b + c` with 4 decay types
- **Multi-model routing** — each agent can use a different model
- **Classifier integrated** into orchestrator (needs full conversation context)
- **Brain Academy v3.0** — learning platform with 2 profiles, 6 modules, gamification
- **Design System** — Liquid Glass CSS (1,379 lines)
- **GitHub Pages** — automated deploy via Actions
- **Landing page** — Aurora Design System with mesh gradients and glassmorphism
- **32 learnings** — indexed with decay, relevance signals, on-demand loading
- **4 domain skills** — software-dev, dashboard-dev, web-deploy, pwa-android
- **7 knowledge clusters** — dynamic, growing organically
- **5 project hubs** — montecarlo, nap-dashboard, caedelcielo, medvisit, learning-platform
- **12 system rules** — consolidated from 13 cycles of real use
- **README.md** — professional with badges, comparison table, agent list
- **README_EN.md** — English version
- **CONTRIBUTING.md** — contribution guide
- **verify-system.bat** — Windows verification script

### Changed
- Migrated from v2 (role-playing) to v3 (real OpenCode subagents)
- 42% reduction in executable layer tokens via two-layer architecture
- Classifier merged into orchestrator (needs full conversation context)

### Fixed
- Multiple structural gaps from v1/v2 identified and documented in learnings
