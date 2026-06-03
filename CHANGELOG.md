# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `verify-system.sh` — cross-platform verification script (Linux/macOS/WSL)
- `.gitignore` — ignore Obsidian cache, IDE files, OS artifacts, env files
- `CHANGELOG.md` — this file

### Changed
- Branch renamed from `master` to `main`
- GitHub Pages workflow updated to use `main` branch

### Fixed
- `_system-config.md`: removed hardcoded Windows path (`C:\Users\d_ant\...`), now portable
- `_session-state.md`: removed stale pending tasks from pre-v3 migration
- `pages.yml`: updated branch from `master` to `main`

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
