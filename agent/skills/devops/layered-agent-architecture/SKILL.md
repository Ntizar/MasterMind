---
name: layered-agent-architecture
version: "1.0.0"
description: "Patrón de arquitectura de agentes LLM en capas (L0-pure → L7-app) inspirado en vidpipe. Define cómo estructurar sistemas multi-agente con separación clara."
tags: [devops, architecture, multi-layer, agents]
---

# Arquitectura de Agentes en Capas

## Cuándo usar

- Diseñas un sistema multi-agente con separación clara de responsabilidades
- Necesitas organizar un proyecto con múltiples tipos de agentes
- Quieres que cada agente pueda usar un modelo LLM diferente con coste controlado
- El proyecto crece y necesitas escalabilidad en la arquitectura

## Cuándo NO usar

- Tienes un solo agente simple → la arquitectura en 8 capas es overkill
- El proyecto es pequeño (<500 líneas de código de agente) → estructura plana es suficiente
- No necesitas agentes con herramientas personalizadas → un loop simple de LLM basta

## Estructura de Capas

```
src/
├── L0-pure/          # Tipos, schemas, utilidades sin dependencias
├── L1-infra/         # Logger, paths, filesystem, config, procesos
├── L2-clients/       # Clientes externos (OpenAI, Copilot SDK, APIs)
├── L3-services/      # Servicios de negocio (LLM provider, cost tracking)
├── L4-agents/        # Agentes LLM (extienden BaseAgent)
├── L5-assets/        # Modelos de activos
├── L6-pipeline/      # Orquestación de pipeline (ETL de agentes)
└── L7-app/           # CLI, SDK, file watchers, commands
```

## Patrón BaseAgent

Cada agente extiende `BaseAgent` e implementa:
- `getTools()` — Herramientas que expone al LLM
- `handleToolCall()` — Dispatch de tool calls
- `run(userMessage)` — Ejecutar el agente

## Patrones Clave

- **Tool Registration:** Tools como JSON Schema, handlers en agente concreto
- **Model Per-Agent:** Cada agente puede usar modelo diferente
- **Asset Pipeline:** Cada agente produce Assets, pipeline conecta agentes

## Referencia

- [htekdev/vidpipe](https://github.com/htekdev/vidpipe) — Implementación completa
