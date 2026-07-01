---
name: browser-use-agent-automation
description: Framework para automatizar navegadores web con agentes IA — Playwright-based, multi-LLM, MCP support. 102K⭐.
version: "1.0.0"
tags: [browser, automation, AI, agents, playwright, MCP, LLM]
---

# Browser Use — Automatización de Navegador para AI Agents

## Resumen

Browser Use permite a agentes IA interactuar con navegadores web de forma natural. Usa Playwright bajo el capó, soporta múltiples LLMs y MCP. 102K⭐.

## Instalación

```bash
pip install browser-use
playwright install
```

## Uso Básico

### Python
```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="Busca el precio del gas natural en ESIOS y dame el resultado",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Con Playwright directo
```python
from browser_use import Browser

browser = Browser()
page = await browser.get_context().get_page("https://esios.ree.es")
# Interactuar con la página como un agente IA
```

## Patrones Clave

1. **Task-driven navigation**: El agente decide acciones basándose en la tarea
2. **DOM understanding**: Lee el DOM y toma decisiones
3. **Multi-LLM support**: OpenAI, Anthropic, Ollama, Groq, etc.
4. **MCP integration**: Soporte para Model Context Protocol
5. **Screenshot-based reasoning**: Usa screenshots para entender la UI
6. **Action types**: click, type, go_to_url, go_back, scroll, read_page

## Integración con Mastermind

- Complementa la browser tool de Hermes (automatización programática vs IA-driven)
- Útil para tareas donde el agente necesita "navegar" por webs complejas
- Puede automatizar dashboards ESIOS, BOE, etc.
- **Diferencia con dogfood**: dogfood es QA exploratorio; browser-use es automatización de tareas por agentes IA

## Referencia

- Repo: https://github.com/browser-use/browser-use
- Docs: https://docs.browser-use.com