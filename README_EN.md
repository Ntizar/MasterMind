<p align="center">
  <img src="assets/banner.svg" alt="Ntizar Mastermind" width="800"/>
</p>

<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>An open-source multi-agent orchestration framework with persistent memory,<br>Ebbinghaus decay, and model routing.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="docs/ARCHITECTURE.md">Architecture</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="README.md">Español</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.1-blue?style=flat-square" alt="Version 3.1"/>
  <img src="https://img.shields.io/badge/agents-11-orange?style=flat-square" alt="11 Agents"/>
  <img src="https://img.shields.io/badge/models-multi--model-green?style=flat-square" alt="Multi-model"/>
  <img src="https://img.shields.io/badge/memory-Ebbinghaus%20decay-purple?style=flat-square" alt="Memory System"/>
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="MIT License"/>
  <img src="https://img.shields.io/badge/web-live-blueviolet?style=flat-square" alt="Web en vivo"/>
  <img src="https://img.shields.io/badge/skills-15-blue?style=flat-square" alt="15 Skills"/>
</p>

---

## Your AI That Actually Remembers

You use AI every day. You copy and paste context. You re-explain your project. You lose learnings between sessions. Your prompts are long, expensive, and fragile.

**What if your AI had a brain?**

Not a chatbot. Not a single prompt. A structured, multi-agent system with persistent memory, specialized roles, and a forgetting curve that keeps your context light and relevant.

**Built for the nan.builders community** — but portable to any agent system.

---

## What is Ntizar Mastermind?

Ntizar Mastermind is an **open-source multi-agent orchestration framework** built on [OpenCode](https://opencode.ai) + [Obsidian](https://obsidian.md). It transforms your workflow from "one conversation at a time" to a **persistent, self-improving intelligence system**.

```
You give a task
    │
    ▼
The ORCHESTRATOR classifies it (type, complexity, domain)
    │
    ▼
Selects the OPTIMAL FLOW (2 to 10 agents)
    │
    ▼
Each AGENT runs on the best model for its role
    │
    ▼
Results are REVIEWED, CRITIQUED, and SYNTHESIZED
    │
    ▼
Learnings are ARCHIVED with an expiration curve
    │
    ▼
Next session starts smarter, not from scratch
```

### Quick Comparison

| Feature | Traditional Prompting | **Ntizar Mastermind v3.1** |
|---|---|---|
| Context | Lost each session | **Persistent memory with intelligent decay** |
| Agents | Single personality | **11 specialized agents with defined roles** |
| Models | One model does everything | **Each agent uses its optimal model** |
| Cost | Full context always | **40-60% savings via intelligent loading** |
| Quality | No review process | **Mandatory review + adversarial critic** |
| Learning | Starts from zero | **Accumulates patterns, skills, and knowledge** |
| Control | AI decides everything | **Human-in-the-loop at every checkpoint** |
| Portability | Not portable | **Cross-platform: Linux, macOS, Windows/WSL** |

---

## The 11 Agents

| # | Agent | Role | Think of it as... |
|---|-------|------|-------------------|
| 00 | **Orchestrator** | Classifies tasks, designs flows, delegates | The CEO |
| 01 | **Classifier** | Evaluates complexity, domain, ambiguity | Triage |
| 02 | **Explorer** | Reads context without modifying anything | The Scout |
| 03 | **Planner** | Defines strategy, steps, success criteria | The Architect |
| 04 | **Spec Writer** | Converts plan into executable spec | The Contract Lawyer |
| 05 | **Implementer** | Executes the spec, produces deliverables | The Builder |
| 06 | **Reviewer** | PASS/FAIL validation against criteria | Quality Inspector |
| 07 | **Critic** | Adversarial review — finds what others miss | The Devil's Advocate |
| 08 | **Synthesizer** | Transforms reports into readable results | The Translator |
| 09 | **Archiver** | Distills learnings with decay metadata | The Librarian |
| 10 | **Librarian** | Maintains the knowledge graph and system health | The Gardener |

> **The Critic is never degraded.** If the best model is unavailable, the Critic is skipped entirely rather than run on an inferior model. Quality over quantity.

> **New in v3.1:** The Critic is activated automatically when ≥1 objective criterion is met (complexity ≥4, ≥3 retries, ≥3 files, high impact, reviewer WARNINGs, or explicit human request).

---

## Multi-Model Architecture

Each agent uses the right model for its job:

```
Orchestrator + Critic    ──►  Claude Opus / GPT-4o       (high reasoning)
Explorer                 ──►  Gemini 2.5 Pro              (1M token context)
Implementer              ──►  Claude Opus / Sonnet         (code generation)
Reviewer                 ──►  Claude Sonnet / Flash        (concrete criteria)
Synthesizer + Archiver   ──►  Claude Haiku / Flash         (mechanical tasks)
```

**Result:** Same output quality, 40-60% less cost. You choose the models — the system proposes, you confirm.

---

## Memory That Forgets (On Purpose)

Each learning has a **decay type** based on Ebbinghaus forgetting curve:

```
R(t) = a / (log(t+1))^b + c
```

| Type | 30 days | 90 days | 180 days | Use |
|------|---------|---------|----------|-----|
| **Permanent** | 100% | 100% | 100% | System rules, fundamental patterns |
| **Slow** | 71% | 58% | 48% | Reusable technical patterns |
| **Normal** | 52% | 37% | 29% | Specific problem solutions |
| **Fast** | 30% | 18% | 12% | One-off fixes, temporary context |

Only learnings that are **relevant to the current task** AND **haven't decayed below threshold** are loaded. Old irrelevant knowledge fades naturally. Critical patterns persist forever.

---

## Two-Layer Architecture

v3 innovation: **zero duplication** between documentation and execution.

```
agents/                         .opencode/agents/
(Documentation Layer — Obsidian)    (Executable Layer — OpenCode)
 │                                  │
 │  Rich context, wikilinks,       │  Minimal YAML config,
 │  missions, interconnections     │  operational instructions,
 │                                  │  model assignment
 │                                  │
 └── Source of truth               └── Execution engine
      (human-readable)                  (machine-executable)
```

The `.opencode/` files reference the Obsidian docs for full context. **42% token reduction** in the executable layer vs v2.

---

## Ecosystem Skills

15 documented skills for reusable patterns:

### Core (HIGH)
| Skill | Domain |
|-------|--------|
| `multi-agent-orchestration` | 11-agent orchestration with 3 adaptive flows |
| `two-layer-architecture` | Documental/executable pattern with zero duplication |
| `ebbinghaus-memory-system` | Memory with forgetting curve, intelligent index |
| `adversarial-critic` | Critic agent with 6 objective activation criteria |
| `system-verification-portability` | Cross-platform verification, .gitignore, portability |

### Flow & Communication (MEDIUM)
| Skill | Domain |
|-------|--------|
| `adaptive-flow-selection` | Short/medium/long flow selection by complexity |
| `structured-report-protocol` | Structured reports between agents |
| `collaborative-decision-protocol` | Collaborative decision-making protocol |
| `intelligent-index-loading` | Index with relevance signals and decay |
| `skill-maintenance-protocol` | Librarian active re-learning |

### Templates & Deploy (MEDIUM)
| Skill | Domain |
|-------|--------|
| `spec-template-pattern` | Verifiable specs with forbidden verbs |
| `learning-template-pattern` | Learning distillation with clusters and decay |
| `review-template-pattern` | PASS/FAIL validation with categorized findings |
| `nan-builders-deploy` | Static deploy for nan.builders + GitHub Pages |

### Clusters (MEDIUM)
| Skill | Domain |
|-------|--------|
| `dynamic-clusters-pattern` | Dynamic clusters and knowledge network |

---

## Quick Start

### Prerequisites

- [Obsidian](https://obsidian.md) (free)
- [OpenCode](https://opencode.ai) (CLI for AI-assisted development)
- At least one AI model API key

### Installation

```bash
# 1. Clone
git clone https://github.com/Ntizar/NtizarBrainMasterMind.git
cd NtizarBrainMasterMind

# 2. Open as Obsidian vault
#    (File → Open vault → Open folder as vault)

# 3. Configure API keys in OpenCode
#    (see OpenCode docs for setup)

# 4. Verify installation
./verify-system.sh    # Linux/macOS/WSL
# or
./verify-system.bat   # Windows

# 5. Start
opencode
# Then: /ntizar-start
```

### First Task

```bash
# Once started, simply give it a task:
"Create a landing page for my portfolio with dark mode"
```

The orchestrator will classify, propose a flow, wait for your confirmation, and execute the full pipeline.

---

## Project Structure

```
NtizarBrainMasterMind/
├── AGENTS.md                  # System entry point
├── index.html                 # 🌐 Official website (GitHub Pages)
├── verify-system.sh           # Cross-platform verifier (Linux/macOS/WSL)
├── verify-system.bat          # Windows verifier
├── .gitignore                 # Ignore Obsidian cache, IDE, OS files
├── CHANGELOG.md               # Change history
├── .nojekyll                  # Disable Jekyll on GitHub Pages
├── skills/                    # 🆕 15 documented skills
│   ├── multi-agent-orchestration.md
│   ├── two-layer-architecture.md
│   ├── ebbinghaus-memory-system.md
│   ├── adversarial-critic.md
│   ├── dynamic-clusters-pattern.md
│   ├── system-verification-portability.md
│   ├── intelligent-index-loading.md
│   ├── structured-report-protocol.md
│   ├── adaptive-flow-selection.md
│   ├── collaborative-decision-protocol.md
│   ├── skill-maintenance-protocol.md
│   ├── spec-template-pattern.md
│   ├── learning-template-pattern.md
│   ├── review-template-pattern.md
│   └── nan-builders-deploy.md
│
├── agents/                    # DOCUMENTATION LAYER (Obsidian)
│   ├── 00-orchestrator.md     # ... through 10-librarian.md
│   ├── session-prompt.md      # Activation prompt
│   ├── state/                 # System config + session state
│   ├── templates/             # Intake, spec, review templates
│   ├── skills/                # Domain skills (4 active)
│   ├── learnings/             # Patterns with decay metadata
│   └── projects/              # Project hubs + clusters
│
├── .opencode/                 # EXECUTION LAYER (OpenCode)
│   ├── agents/                # YAML agent configs
│   └── commands/              # /ntizar-start, /ntizar-status, etc.
│
├── learning-platform/         # Brain Academy — interactive platform
├── design-system/             # Liquid Glass CSS (1,379 lines)
├── docs/                      # Extended documentation
└── assets/                    # SVG banner
```

---

## Roadmap

### v3.1 current (June 2026)
- [x] Two-layer architecture
- [x] 11 specialized agents
- [x] Multi-model per agent
- [x] Ebbinghaus decay memory
- [x] 15 documented skills
- [x] Cross-platform verification
- [x] Full .gitignore
- [x] CHANGELOG.md
- [x] Objective Critic activation (6 criteria)
- [x] Clean session state
- [x] Full portability (no absolute paths)
- [x] Brain Academy v3.0
- [x] Liquid Glass Design System

### v3.2 — Metrics & Observability
- [ ] System metrics dashboard (tokens, PASS/FAIL, retries)
- [ ] Automatic metric logging per cycle
- [ ] Agent performance analysis
- [ ] Quality degradation alerts

### v4.0 — Collaborative Intelligence
- [ ] Multi-user knowledge sharing
- [ ] Skills marketplace
- [ ] Cross-project pattern detection
- [ ] Visual flow editor
- [ ] Benchmark suite

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Open areas:
- 🧩 **New skills** — playbooks for your domain
- ⚡ **Agent optimizations** — better prompts, smarter flows
- 🌐 **Learning platform** — content, translations, accessibility
- 🔌 **MCP Integration** — multi-agent protocol work for v3.2
- 📊 **Metrics & observability** — performance dashboard
- 📖 **Documentation** — tutorials, guides, videos
- 🧪 **Testing** — benchmarks and quality metrics

---

## License

MIT License — see [LICENSE](LICENSE).

Use this system, fork it, improve it. If it saves you time, pass it on.

---

<p align="center">
  Made with <span style="color: #f97316;">♡</span> by <strong><a href="https://github.com/Ntizar">David Antizar</a></strong>
  <br/>
  <sub>Ntizar Mastermind — because a mastermind isn't a single genius, but a group of specialized minds working together.</sub>
</p>
