---
name: agent-memory
version: "1.0.0"
description: >
  Memory and context engines for AI agents — persistent memory across sessions,
  fact extraction from conversations, user profiles, hybrid RAG+memory search,
  temporal reasoning, contradiction handling, and automatic forgetting.
author: Mastermind (autonomous discovery)
date: 2026-06-02
tags: [ia, agent-memory, context, rag, persistent-memory]
---

# Agent Memory — Memory Engines para Agentes IA

## Visión General

Los agentes IA olvidan todo entre conversaciones. Los motores de memoria resuelven esto:

- **Extracción de facts** — Aprende de conversaciones, extrae hechos estructurados
- **Perfiles de usuario** — Contexto estable + actividad reciente, acceso ~50ms
- **Búsqueda híbrida** — RAG + memoria personal en una sola query
- **Razonamiento temporal** — Facts que cambian con el tiempo, contradicciones
- **Olvido automático** — Facts caducados se eliminan solos
- **Conectores** — Sync con Drive, Gmail, Notion, GitHub, etc.

## Herramientas Conocidas

### Supermemory
- **URL:** https://github.com/supermemoryai/supermemory
- **Estrellas:** ~24k | **Lenguaje:** TypeScript
- **Benchmarks:** #1 en LongMemEval, LoCoMo, ConvoMem
- **Features:** Memory extraction, user profiles, hybrid search, connectors (Drive, Gmail, Notion, GitHub), multi-modal extractors (PDF, OCR, video transcription, AST-aware code chunking)
- **SDK:** npm + pip
- **Infra:** Cloudflare Workers + KV + Pages
- **Dashboard:** https://console.supermemory.ai

```typescript
// Extract memory from conversation
import { Supermemory } from 'supermemory';
const sm = new Supermemory({ apiKey: 'key' });
const memory = await sm.extract({ messages: [...] });
const profile = await sm.getProfile('user-123');
const results = await sm.search({ query: '...', memory: true, knowledge: true });
```

### Otras herramientas en el ecosistema
- **Mem0** — Memory layer for LLM apps (Python/TS)
- **Zep** — Memory service for AI agents (self-hosted + cloud)
- **LangChain Memory** — Built-in conversation memory patterns
- **Semantic Memory** — Memory via vector embeddings

## Patrones de Integración

### Patrón 1: Memory como capa de contexto
```
Conversación → Memory Engine → Facts + Profile
                                    ↓
                            Antes de cada turno:
                            getProfile(user_id) → Contexto en prompt
```

### Patrón 2: Hybrid Search (RAG + Memory)
```
Query → Hybrid Search → [Docs RAG] + [Personal Memory] → Combined context
```

### Patrón 3: Connector Auto-sync
```
Conectores → Webhooks → Auto-sync → Memory actualizada en tiempo real
```

## Casos de Uso para Mastermind

1. **Memoria persistente entre sesiones** — Mastermind recuerda preferencias, historial, contexto
2. **Perfiles de usuario** — David Antizar como usuario con facts estables
3. **Integración con herramientas** — Notion, GitHub, Drive como fuentes de contexto
4. **RAG mejorado** — Combinar docs del proyecto + memoria personal

## Decisiones

| Criterio | Supermemory | Mem0 | Zep |
|----------|------------|------|-----|
| Hosting | Cloud (Cloudflare) | Self-hosted/cloud | Self-hosted/cloud |
| SDK | npm + pip | Python + TS | Python + TS |
| Benchmarks | #1 en 3 benchmarks | — | — |
| Conectores | Drive, Gmail, Notion, GitHub, OneDrive | — | Slack, Notion, Drive |
| Multi-modal | PDF, OCR, video, code | Text | Text |

## Referencias

- [Supermemory docs](https://supermemory.ai/docs)
- [Supermemory quickstart](https://supermemory.ai/docs/quickstart)
- [Supermemory Discord](https://supermemory.link/discord)
- [LongMemEval benchmark](https://github.com/xiaowu0162/LongMemEval)
- [LoCoMo benchmark](https://github.com/snap-research/locomo)
- [ConvoMem benchmark](https://github.com/Salesforce/ConvoMem)
