---
name: mirofish-swarm-simulation
description: "Simula sociedades de agentes con memoria y saca informe."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [multi-agent, simulacion, graphrag, swarm, opinion, informes]
    related_skills: [agent-graph-architecture, mastermind-orchestration, graphify-codebase-graph]
---

# MiroFish — motor de enjambre multiagente

Motor de "inteligencia de enjambre" (AGPL-3.0) que monta un **mundo digital paralelo**: de una semilla (noticia, informe, texto) construye un grafo de conocimiento, genera **personas con memoria** y las deja interactuar para extraer un informe de predicción.

## Pipeline de 5 etapas (patrón reutilizable)

1. **Graph Building** — GraphRAG sobre la semilla + inyección de memoria individual y colectiva.
2. **Environment Setup** — extracción de entidades y generación de personas (agentes).
3. **Simulación dual en paralelo** — auto-parse del objetivo; dos mundos que se comparan.
4. **ReportAgent** — agente con toolset sobre el entorno post-simulación que redacta el informe.
5. **Chat con cualquier agente** del mundo simulado (auditoría de por qué decidió lo que decidió).

## Stack real (verificado)

- Backend **Flask** (`flask>=3.0`, `flask-cors`) en `:5001`; frontend en `:3000`.
- Motor de simulación: **OASIS de CAMEL-AI** (`camel-oasis==0.2.5`, `camel-ai==0.2.78`).
- Memoria de largo plazo: **Zep Cloud** (`zep-cloud==3.25.0`).
- Requisitos: Node 18+ y Python 3.11-3.12 con `uv`.

```bash
npm run setup:all      # root + frontend + backend (uv sync)
npm run dev            # arranca todo (o npm run backend / npm run frontend)
docker compose up -d   # alternativa contenedorizada
```

Configuración por `.env`: `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME` (cualquier endpoint compatible con el SDK OpenAI) y `ZEP_API_KEY`.

## Pitfalls

- **Consumo de LLM altísimo**: el propio README avisa de probar simulaciones de **<40 rondas** antes de escalar.
- **Zep Cloud es remoto**: choca con el criterio de stacks 100% locales de David. `LLM_BASE_URL` admite cualquier endpoint compatible con el SDK OpenAI (un servidor local tipo Ollama encajaría, aunque el README no lo menciona explícitamente), pero la memoria GraphRAG sigue siendo del servicio.
- Licencia **AGPL-3.0**: revisar antes de incrustarlo en un producto.

## Encaje en Mastermind

- Patrón de **personas con memoria temporal dinámica** exportable a simulaciones de opinión (no solo chat multi-perfil como Gobierno IA).
- Útil como referencia de arquitectura para `agent-graph-architecture` (grafo de agentes con estado) y para informes largos vía ReportAgent.

## Referencia

- Repo: `666ghj/MiroFish` (~73.570 ⭐, Python, consultado 2026-09-15).
