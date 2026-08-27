---
name: agent-reach
version: "1.0.0"
description: "Agent-Reach — herramienta para dar a los agentes IA acceso a 13+ plataformas web. Lectura y escritura en cualquier web (internet, APIs, redes sociales). 34K⭐."
tags: [agents, ai, web, scraping, automation, multi-platform, internet]
---

# Agent-Reach — Multi-Platform Agent Access

## Resumen

Agent-Reach permite a agentes IA **leer y escribir** en 13+ plataformas web como si fueran un navegador programático. Diseñado para agentes autónomos que necesitan interactuar con servicios web reales.

## Plataformas soportadas

- 🔍 **Google** — búsqueda y resultados
- 🐦 **Twitter/X** — tweets, perfiles, timeline
- 🐙 **Reddit** — posts, comentarios
- 📧 **Gmail** — leer, buscar, filtrar correos
- 📺 **YouTube** — búsqueda, canales, metadatos
- 🛒 **Amazon** — productos, precios, reviews
- 💼 **LinkedIn** — perfiles, búsqueda
- 💬 **Discord** — mensajes, canales
- 🐙 **GitHub** — issues, PRs, repos
- 📝 **Notion** — páginas, bases de datos
- 📰 **Wikipedia** — artículos, búsqueda
- 🎵 **Spotify** — playlists, tracks
- 🌐 **Any URL** — scraping genérico

## Arquitectura

```
Agente IA
   ↓ (API simple)
Agent-Reach SDK
   ↓
┌──────┬──────┬──────┬──────┐
│Google│Twitter│GitHub│ ... │
└──────┴──────┴──────┴──────┘
   ↓
Respuesta estructurada (JSON)
```

## Uso

```python
from agent_reach import ReachClient

client = ReachClient(api_key="...")

# Buscar en Google
results = client.search("latest AI news")

# Leer tweets de un usuario
tweets = client.read_twitter("elonmusk", limit=20)

# Buscar en GitHub
repos = client.search_github("langchain")
```

## Integración con Mastermind

- **Web research:** Búsqueda y extracción multi-plataforma
- **Social monitoring:** Seguimiento de tendencias
- **Data collection:** Scraping estructurado de webs

## Referencia

- Repo: `Panniantong/Agent-Reach`
- README incluye SKILL.md para uso como skill de agente