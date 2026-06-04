<p align="center">
  <img src="assets/banner.svg" alt="Ntizar Mastermind" width="800"/>
</p>

<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>Multi-agent orchestration framework with specialized skills.<br>Running on Hermes Agent over NaN.builders with GitHub as repository.</strong>
</p>

<p align="center">
  <a href="README.md">🇪🇸 Español</a> · <a href="tokens/">📊 Token Dashboard</a> · <a href="https://github.com/Ntizar/NtizarBrainMasterMind">GitHub</a>
</p>

---

## What is Ntizar Mastermind?

Ntizar Mastermind is an **open-source multi-agent orchestration framework** built on top of [Hermes Agent](https://github.com/NousResearch/hermes-agent). It provides a single orchestrator (Koldo) that routes tasks to **143 specialized skills** across 8 domains, with persistent memory that survives between sessions.

### Key Features

- **🧠 Intelligent Orchestration** — Koldo classifies tasks by domain and complexity, then decides whether to handle directly or delegate to specialized sub-agents
- **⚡ 143 Specialized Skills** — Software, GitHub, Frontend, Backend, Infra, DevOps, Data Science, Creative — each with deep domain knowledge
- **💾 Persistent Memory** — 3-layer memory system: preferences (`memory`), procedures (skills), history (`session_search`)
- **☁️ Cloud Deploy** — MicroVM on NaN.builders (1vCPU/2GB), accessible via Telegram and WebUI

### Architecture

```
User Task → Koldo (Orchestrator) → Domain Skills → Execution → Memory
                   ↓
          8 domains: Software, GitHub, Frontend, Backend,
          Infra, DevOps, Data Science, Creative
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Ntizar/NtizarBrainMasterMind.git

# Open with your agent editor
cd NtizarBrainMasterMind
hermes .     # or your preferred IDE

# Activate the system
/ntizar-start
```

## Project Structure

```
├── SOUL.md              # Agent identity — single source of truth
├── index.html           # Landing page (GitHub Pages)
├── CONTRIBUTING.md      # Contribution guidelines
├── CHANGELOG.md         # Version history
├── AGENTS.md            # AI agent behavior rules
├── tokens/              # Token tracking dashboard
├── notes/               # Session learnings and notes
├── skills/              # System skills
├── legacy/              # Archived v3.1 code
├── design-system/       # Local Aurora CSS
├── assets/              # Images and SVGs
├── profiles.json        # User profiles
├── pages.yml            # GitHub Pages config
├── verify-system.sh     # System health check script
├── .github/workflows/   # CI/CD pipelines
└── .gitignore
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | Hermes Agent (NousResearch) |
| Model | qwen3.6 via NaN.builders |
| Infrastructure | NaN.builders MicroVM (1vCPU/2GB/20GB) |
| Design System | Aurora (Ntizar) |
| Hosting | GitHub Pages |
| Version Control | GitHub |

## 12 Rules (Derived from 13 Real-World Cycles)

1. One orchestrator, many specialists
2. Skills on-demand by domain
3. Persistent memory between sessions
4. GitHub as single source of truth
5. Never delete from the Koldo repo — only create or modify
6. Significant notes → `notes/YYYY-MM-DD-titulo.md`
7. New skills → `/hermes-home/skills/`
8. Every important learning → commit to the repo
9. No secrets in notes/commits/chat
10. SOUL.md is the single source of truth for system identity
11. Everything in Spanish — never English in repos, scripts, reports
12. Human loop on critical changes — present diffs and wait for approval

## Evolution: v3 → v4

| Aspect | v3 (Legacy) | v4 (Current) |
|--------|-------------|---------------|
| Architecture | Monolithic SOUL.md (900+ lines) | Orchestral SOUL.md + 143 modular skills |
| Memory | Ebbinghaus decay (5 levels) | memory + skills + session_search (3 layers) |
| Routing | Model-based (flash/preferred) | Domain and complexity-based |
| Deploy | Local / host-dependent | NaN.builders MicroVM + GitHub Pages |

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Made with ❤️ by David Antizar**

*v4.0.1 — 2026-06-04*
