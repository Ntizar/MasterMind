<div align="center">

<img src="assets/banner.svg" alt="MasterMind" width="720"/>

# 🧠 MasterMind

**An AI agent that learns on its own, remembers everything, and while you sleep
studies the repos you starred.**

[![Platform](https://img.shields.io/badge/platform-Windows_11-0078D4?style=flat-square&logo=windows11&logoColor=white)](https://github.com/Ntizar/MasterMind)
[![Engine](https://img.shields.io/badge/engine-Hermes_Agent-blue?style=flat-square)](https://github.com/NousResearch/hermes-agent)
[![Models](https://img.shields.io/badge/models-NaN.builders-FF6B35?style=flat-square)](https://nan.builders)
[![Search](https://img.shields.io/badge/skills-ChromaDB_semantic-8A2BE2?style=flat-square)](https://www.trychroma.com)
[![Language](https://img.shields.io/badge/language-Spanish_%2B_English-FFD700?style=flat-square)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

[🌐 Website](https://ntizar.github.io/MasterMind/) · [How it works](#-how-it-works) · [The autonomous loop](#-the-autonomous-loop) · [Español](README.md)

</div>

---

> [!IMPORTANT]
> **This is not an open-source framework.** You cannot clone it and run it as-is — it is David Antizar's personal AI agent system. What it *is*: a **real, battle-tested reference architecture** for how an agent can learn from every task, index its knowledge by meaning, and learn from GitHub while you sleep.

---

## 💡 The idea in 30 seconds

Most AI assistants suffer amnesia: every session starts from zero, they don't know who you are or what they did yesterday, and their useful knowledge evaporates.

**MasterMind is the opposite.** It lives on my PC (Windows 11), runs on [Hermes Agent](https://github.com/NousResearch/hermes-agent) with models from [NaN.builders](https://nan.builders), and has three superpowers:

| Superpower | How |
|---|---|
| 🧠 **It remembers** | Persistent memory injected into every session: who I am, my projects, my preferences and the lessons learned |
| 📚 **It knows how to search** | Its skills are not loaded by name but **by meaning**, with semantic search in ChromaDB and embeddings |
| 🌙 **It learns on its own** | Every 6 hours it explores the repos I star on GitHub, extracts their patterns and turns what it learns into new skills |

And all of this is backed up in this repository, which is its source of truth.

---

## 🔄 How it works

```
                        David's task
                              │
                              ▼
     ┌─────────────────────────────────────────────┐
     │   MASTERMIND (Hermes Agent + NaN.builders)  │
     └─────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  1️⃣ SEARCH             2️⃣ EXECUTE            3️⃣ LEARN
  Semantic search       The agent's tools:    Does it deserve
  in ChromaDB:          terminal, browser,    a skill? A note?
  "what do I know       files, delegation     Memory? → it
  about X?" → skills    to sub-agents         saves it and
  ranked by relevance                         commits
                              │
                              ▼
                  The next session knows more
```

### 1️⃣ Semantic search (the heart of the system)

MasterMind does **not** have a list of skills it loads all at once. It has a vector database:

```bash
python scripts/consultar-skills.py "transport isochrone map" --json
```

```json
[
  { "name": "routing-isochrones",     "score": 0.72 },
  { "name": "accessibility-map",      "score": 0.68 },
  { "name": "valhalla-routing",       "score": 0.61 }
]
```

Every skill is indexed with `qwen3-embedding` (4096 dimensions, cosine distance). If a task needs 3 skills, it loads 3. If it needs 50, it loads 50. **No artificial limits — only relevance.**

### 2️⃣ Execution levels

Before acting, MasterMind decides how much firepower the task needs:

| Level | When | Pattern |
|:---:|---|---|
| 🟢 **1 — Direct** | Search, read, a commit | MasterMind alone, 1-3 tool calls |
| 🟡 **2 — Simple** | A refactor, a module | 4-8 tool calls |
| 🟠 **3 — Parallel** | Frontend + backend + tests | Delegation to 2-3 sub-agents |
| 🔴 **4 — Orchestration** | A complete feature | Planner → implementers → reviewer |

And for critical changes (more than 5 files, architecture decisions, deploys) the **human loop** kicks in: plan → wait for your ✅ → implement → wait for your ✅. It never assumes.

---

## 🌙 The autonomous loop

This is what MasterMind does when nobody is talking to it:

<div align="center">

```
     ☀️  DAILY                 🌙  EVERY DAY 10AM           📅  WEEKLY
┌─────────────────┐      ┌─────────────────────┐     ┌──────────────────┐
│  SCOUT · every 6h│      │ DOCTOR · daily 10am │     │ DIGEST · Mon 9am │
│                 │      │                     │     │                  │
│ Explores a batch│      │ Gateway alive?      │     │ What did we      │
│ of your GitHub  │      │ Crons ran?          │     │ learn this week? │
│ stars →         │      │ ChromaDB in sync?   │     │                  │
│                 │      │ Repo synchronized?  │     │ New skills,      │
│ Worth a skill?  │      │                     │     │ numbers, next-   │
│ ├─ YES → creates│      │ Self-heals what is  │     │ week suggestions │
│ └─ NO → skips it│      │ safe, and if all is │     │                  │
│      (with a    │      │ well, stays silent  │     │ report           │
│      reason)    │      │                     │     │                  │
│ commit + push   │      │ commit if needed    │     │                  │
└─────────────────┘      └─────────────────────┘     └──────────────────┘
```

</div>

**Semantic dedup is what makes the loop sustainable:** before creating a skill, the scout searches ChromaDB for an equivalent. If one exists, it skips it and logs the reason. Every skill that enters the system is **new** knowledge, not a duplicate.

---

## 🗂️ The 3 knowledge layers

| Layer | Where it lives | What it holds |
|---|---|---|
| 🧠 **Memory** | `agent/MEMORY.md` + `agent/USER.md` | Projects, preferences, day-to-day lessons. Injected into every session |
| 📚 **Skills** | `agent/skills/` + ChromaDB | Reusable procedures by domain: GIS, transport, dashboards, ML, STEM... |
| 🔒 **Backup** | This repository | All of the above, pushed on every learning cycle |

> [!NOTE]
> The number of skills **is not fixed**: it grows with every scout cycle and every working session. It's a question the system answers, not a number written on a badge.

---

## 🏗️ Repository structure

```
MasterMind/
│
├── 🤖 agent/                  ← the agent
│   ├── skills/                ← skills by domain (indexed in ChromaDB)
│   ├── MEMORY.md              ← project & lesson memory
│   ├── USER.md                ← David's identity and preferences
│   └── SOUL.md                ← the agent's identity (source of truth)
│
├── ⚙️ scripts/                ← the engine
│   ├── consultar-skills.py    ← semantic search
│   ├── indexar-skills.py      ← ChromaDB indexing
│   ├── explorar-stars.py      ← GitHub stars explorer
│   ├── doctor.py              ← system health check
│   └── ...                    ← backup, lifecycle, ebbinghaus...
│
├── 📝 notes/                  ← continuous learning notes
├── 📊 data/                   ← stars-registry.json (pipeline state)
├── 📖 mastermind/             ← internal system documentation
└── 🌐 index.html              ← the public website (GitHub Pages)
```

---

## 🧰 Stack

| Layer | Technology | Role |
|---|---|---|
| **Agent** | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Execution engine: tools, delegation, gateway, cron |
| **Surface** | Hermes Desktop (Windows 11) | Where I talk to MasterMind daily |
| **Models** | [NaN.builders](https://nan.builders) API | `glm5.3-flash` / `qwen3.8-flash` by phase and budget |
| **Embeddings** | `qwen3-embedding` | 4096-dim vectors for semantic search |
| **Vector DB** | [ChromaDB](https://www.trychroma.com) | Persistent and embedded, no server |
| **VCS** | GitHub (`Ntizar/MasterMind`) | Source of truth and backup with history |
| **Gateway** | Hermes Gateway | Keeps cron jobs alive, auto-starts at login |

---

## 🚀 Quick guide (if you were me)

> [!WARNING]
> This is what I would do on **my** machine to rebuild the system. It is not a generic installer.

```bash
# 1. Install Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash   # or the Windows installer

# 2. Clone the system (the repo IS the configuration)
git clone https://github.com/Ntizar/MasterMind ~/Projects/MasterMind

# 3. Install ChromaDB on the system Python
pip install chromadb

# 4. Index the skills (needs embedding API credentials in Hermes' .env)
python scripts/indexar-skills.py --reset

# 5. Check the system breathes
python scripts/doctor.py

# 6. Try semantic search
python scripts/consultar-skills.py "any topic" --json
```

And the health check in action:

```
🩺 Doctor Mastermind — 2026-08-28 14:39

✅ gateway          ✓ process alive, auto-start active
✅ chromadb         indexed: 311 | SKILL.md on disk: 311
✅ stars-registry   last run 2.6h ago | 133 repos processed
✅ git              branch: master | CLEAN

✅ All good
```

---

## 📜 The 12 rules of the system

Distilled from real daily use:

1. **One orchestrator, many specialists** — MasterMind classifies and delegates, skills execute
2. **Skills on demand by meaning** — ChromaDB first, `skill_view()` after
3. **Persistent memory** — nothing is learned twice, nothing is forgotten
4. **GitHub as source of truth** — plain Markdown, no external dependencies
5. **NEVER delete from the repo** — only create or modify
6. **Significant notes** → `notes/YYYY-MM-DD-title.md`
7. **New skills** → `agent/skills/` + reindex ChromaDB
8. **Every important lesson** → commit to the repo
9. **Secrets live only in `.env`** — never in notes, commits or cron prompts
10. **SOUL.md is the source of truth** of the identity
11. **Everything in Spanish** — repos, scripts, crons and reports
12. **Human loop on critical changes** — visible diffs, explicit approval

---

<div align="center">

**Made with ❤️ by [David Antizar](https://github.com/Ntizar)**

*MasterMind is my executor. I am the author.*

[🌐 Website](https://ntizar.github.io/MasterMind/) · [Español](README.md) · [MIT License](LICENSE)

</div>
