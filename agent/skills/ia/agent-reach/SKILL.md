---
name: agent-reach
description: "Usa a dar acceso de plataformas a agentes con Agent-Reach."
version: "2.0.0"
tags: [agent-reach, cli, integration, agentes, plataformas, herramientas]
related_skills: [agent-reach, mcp, hermes-agent, multi-agent]
---

# Agent-Reach — dar a los agentes acceso a plataformas (CLI)

> ⚠️ Corrección 2026-09-05 (auditoría): la v1 describía una SDK Python `from agent_reach import ReachClient` con `api_key` y `client.search()` — **no existe**. Agent-Reach es un **CLI** (`agent-reach install/doctor/uninstall`) que orquesta CLIs externas (twitter-cli, gh, bili-cli, OpenCLI, rdt-cli, MCP). El README advierte NO instalar el paquete PyPI homónimo (no es este proyecto).

**Repo:** `https://github.com/Panniantong/Agent-Reach` (Python, ~78K⭐).

## When to Use

- Cuando quieras que un **agente IA acceda a plataformas** externas (redes, GitHub, búscadores…) mediante CLIs integradas.

## Uso (CLI real)

```bash
agent-reach install      # instala las CLIs externas integradas
agent-reach doctor       # diagnostica el estado
# agent-reach uninstall también existe
```

- Orquesta CLIs externas (twitter-cli, gh, bili-cli, OpenCLI, rdt-cli, MCP); **no hay API key propia ni tarifa**.

## Plataformas soportadas (real)

Web, YouTube, RSS, búsqueda web, GitHub, Twitter/X, Bilibili (B站), Reddit, Facebook, Instagram, Xiaohongshu (小红书), LinkedIn, V2EX. *(NO Google/Gmail/Amazon/Discord/Notion/Wikipedia/Spotify.)*

## Pitfalls

- **No** `from agent_reach import ReachClient` ni `ReachClient(api_key=...)` — es un CLI, no una SDK Python.
- **No** instalar el paquete `agent-reach` de PyPI (no es este proyecto).
- Plataformas: la lista real es la de arriba, no la de la v1.

## Verificación

- `agent-reach doctor` tras `install`; comprobar que las CLIs integradas aparecen listas.
