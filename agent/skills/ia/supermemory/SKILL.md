---
name: supermemory
description: "Usa a Supermemory como memoria semántica de agentes."
version: "2.0.0"
tags: [memoria, supeparamemory, rag, agentes, mcp, api, typescript]
related_skills: [supermemory, memory-context-engine, agent-memory, rag-knowledge-base]
---

# Supermemory — memoria semántica para agentes (servicio + cliente API)

> ⚠️ Corrección 2026-09-05 (auditoría): el repo es **TypeScript** (app + motor de memoria + API REST + MCP server + extensión de navegador), y la clase `SuperMemory()`/`.store()`/`.search()` NO existe. El paquete PyPI es un cliente REST (`Supermemory(api_key=...)` con `client.search.documents(...)`), o se self-hostea.

**Repo:** `https://github.com/supermemoryai/supermemory` (TypeScript, ~29K⭐).

## When to Use

- Cuando quieras dar **memoria semántica persistente** a un agente (guardar/recuperar hechos con búsqueda), vía servicio o self-host.

## Uso

Es un **servicio/app con API HTTP** (o MCP server), no una librería local autocontenida.

**Cliente Python (PyPI, generado con Stainless):**

```python
from supermemory import Supermemory
client = Supermemory(api_key="...")
result = client.search.documents(q="...")     # buscar por query
```

**Self-host / MCP:**

```bash
curl -fsSL https://supermemory.ai/install | bash
# o usar el MCP server que expone el repo
```

## Pitfalls

- **No** `from supermemory import SuperMemory`; la clase es **`Supermemory`** (con `api_key`) y la API es `client.search.documents(q=...)`, no `.store()`/`.search()`.
- El repo es **TypeScript**, no Python.
- **No** es "SQLite + numpy mínimo": es un servicio con API HTTP (o self-host).

## Verificación

- Crear el cliente con `api_key`, guardar y buscar un documento; o correr el MCP server del repo.
