---
name: shepherd-meta-agents
version: "1.0.0"
description: "Shepherd — runtime substrate para meta-agents con traces reversibles tipo Git y copy-on-write fork"
---

# Shepherd — Reversible Agent Execution Traces

## Descripción

Shepherd es un runtime substrate para agents que necesitan inspección, reversibilidad y supervisión. Registra ejecuciones de agents como traces duraderos e inspeccionables, con copy-on-write fork ~5x más rápido que docker commit y ~95% KV-cache reuse en replay.

## Por qué importa para David

- **Meta-agents**: Patrón avanzado de agents que supervisan/optimizan/entrenan otros agents
- **Reversible execution**: Git-like traces permiten replay, fork y revert de cualquier run
- **Copy-on-write**: Fork de workspace ultra-rápido sin duplicar datos
- **KV-cache reuse**: Reutiliza 95% del KV cache en replay → ahorrísimo en inference cost

## Arquitectura

```
Meta-Agent → Supervisor
    ↓
Agent Run (workspace forked copy-on-write)
    ↓
Durable Execution Trace (inspectable, reversible)
    ↓
Meta-Agent: Observe → Fork → Replay → Revert
```

## Instalación

```bash
pip install shepherd-ai
# Requiere Python 3.11+
# macOS: Seatbelt enforcement
# Linux: Landlock enforcement
```

## Integración con proyectos de David

- **Mastermind Orchestration**: Patrón de supervisión de sub-agents con reversibilidad
- **Debugging de agents**: Replay de runs para debugging y optimización
- **Multi-agent training**: Tree RL con MCTS para optimización de agents

## Pitfalls

- Proyecto alpha (junio 2026) → API inestable, puede cambiar
- Requiere Python 3.11+
- Enforcement OS-level (Seatbelt en macOS, Landlock en Linux)
- No tiene docs completas aún, hay que leer el código fuente
- Depende de kernel-level features que pueden no estar disponibles en MicroVM de NaN

## Referencias

- GitHub: https://github.com/shepherd-agents/shepherd
- Docs: https://docs.shepherd-agents.ai/
- Paper: https://arxiv.org/abs/2605.10913
- Paper: https://arxiv.org/abs/2505.10913

## Comparativa de alternativas

- **[shepherd-agents/shepherd](https://github.com/shepherd-agents/shepherd)** — meta-agentes programables con *execution traces* reversibles; implementación de referencia de meta-agentes programables.
