---
name: page-agent-browser-automation
description: "Usa a automatizar el navegador con Page Agent."
version: "2.0.0"
tags: [page-agent, browser, gma, automation, navegador, agente]
related_skills: [browser-use-ai, browser-local-tools, computer-use]
---

# Page Agent — agente GUI de Alibaba que vive en tu página

> ⚠️ Corrección 2026-09-05 (auditoría): la API real usa `new PageAgent({ model, baseURL, apiKey, language })` + `await agent.execute('...')`; no `instructions/llm/mcp` + `agent.on('command', ...)`.

**Repo:** `https://github.com/alibaba/page-agent` (TypeScript, ~29K⭐).

## When to Use

- Cuando pidas **automatizar páginas web con un agente GUI** que vive dentro del navegador (uso de tools de página, soporte MCP).

## Uso (API real)

```js
import { PageAgent } from 'page-agent';
const agent = new PageAgent({
    model: 'qwen',          // configuración de modelo
    baseURL: '...',
    apiKey: '...',
    language: 'es',
});
const result = await agent.execute('busca y pincha el botón X');   // método execute
```

- Agente **in-page** + paquete npm + extensión de Chrome + soporte MCP.

## Pitfalls

- Constructor: **`model/baseURL/apiKey/language`**; no `instructions/llm/mcp`.
- Método: **`await agent.execute('...')`**; no `agent.on('command', ...)`.

## Verificación

- Instanciar con model/API key del proveedor, `agent.execute()` sobre una página y ver que interactúa.
