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

## Comparativa de alternativas

**Actualizado 2026-09-01** a raíz de las stars de David. Ya no solo "cloud vs self-hosted": Engram demostró que la memoria de agente también puede ser un binario local cero-dependencias vía MCP.

| Criterio | Engram | Supermemory | Mem0 | Zep |
|----------|--------|-------------|------|-----|
| Stars (2026-09-01) | ~6.250 | ~28K | ~30K+ | ~8K+ |
| Modelo | Self-hosted, binario Go único | Cloud (Cloudflare) + SDK | Self-hosted/cloud | Self-hosted/cloud |
| Almacenamiento | SQLite + FTS5 (~/.engram/engram.db) | KV + vectores | Vector DB externa | Postgres + vectores |
| Integración agente | MCP stdio nativo (Claude Code, OpenCode, Codex, Cursor, VS Code…) | SDK npm/pip + API | SDK Python/TS | SDK + API |
| Dependencias | Ninguna (no Node/Python/Docker) | Cloud o infra propia | Python/TS + vector store | Servidor + Postgres |
| Búsqueda | Full-text FTS5 (léxica) | Semántica/híbrida (embeddings) | Semántica | Semántica + temporal |
| Windows | `go install` o binario (antivirus puede avisar) | N/A (API) | pip | Docker |

**Cuándo usar cada cuál:**
- **Engram** → memoria local inmediata para un coding agent con MCP, sin infra ni llaves API; contratos de sesión explícitos (`mem_session_summary` como handoff tras compactación). Ideal para equipos/PCs donde la privacidad y el offline importan (patrón muy cercano a cómo Hermes guarda sus memories).
- **Supermemory/Mem0** → memoria semántica multiusuario con user profiles, connectors y reasoning temporal; cuando hace falta escalar o compartir memoria entre servicios.
- **Zep** → servicio self-hosted con API cuando se quiere memoria centralizada con razonamiento temporal sobre Postgres.

### Engram — patrón operativo (lo reutilizable)

- **El agente decide, no el volcado:** `mem_save` solo tras trabajo significativo (bugfix, decisión, patrón), formato What/Why/Where/Learned. Nunca tool output crudo.
- **`topic_key` estable** (p.ej. `architecture/auth-model`) → los temas evolutivos se actualizan bajo la misma clave en vez de crear memorias compitientes.
- **Divulgación progresiva en 3 capas:** `mem_search` (preview) → `mem_timeline` (contexto cronológico alrededor) → `mem_get_observation` (contenido completo) — minimiza tokens de contexto.
- **Handoff de sesión:** al terminar, `mem_session_summary` (Goal/Discoveries/Accomplished/Next Steps/Files); al arrancar, `mem_context` inyecta la sesión previa automáticamente.
- **Registro con un comando:** `engram setup <agente>` escribe la entrada MCP (`mcpServers`/`servers`/objeto `mcp` según cliente) y el Memory Protocol, idempotente.

## Referencias

- [Engram](https://github.com/Gentleman-Programming/engram) (⭐6.2K, Go, MIT, push 2026-09-01) — docs clave: `docs/ARCHITECTURE.md`, `docs/AGENT-SETUP.md`, `docs/INSTALLATION.md`
- [Supermemory docs](https://supermemory.ai/docs)
- [Supermemory quickstart](https://supermemory.ai/docs/quickstart)
- [Supermemory Discord](https://supermemory.link/discord)
- [LongMemEval benchmark](https://github.com/xiaowu0162/LongMemEval)
- [LoCoMo benchmark](https://github.com/snap-research/locomo)
- [ConvoMem benchmark](https://github.com/Salesforce/ConvoMem)
