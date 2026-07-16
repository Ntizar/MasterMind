---
name: browser-use-ai
description: Framework de browser automation con IA — navega, interactúa y extrae datos de webs de forma autónoma.
version: "1.0.0"
tags: [browser, automation, AI, scraping, web, agents]
---

# Browser Use — Browser Automation con IA

## Resumen

Framework de browser automation con IA que navega, interactúa y extrae datos de webs de forma autónoma. 101k⭐.

## Repo de referencia

- **GitHub:** `github.com/browser-use/browser-use`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install browser-use
```

## Uso Básico

```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="Busca el precio de Bitcoin en CoinGecko y devuélvelo",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Patrones Clave

1. **Tareas naturales:** Describe lo que quieres en lenguaje natural
2. **Navegación autónoma:** El agente navega por la web sin scraping manual
3. **Interacción completa:** Clicks, fills, scrolls, downloads
4. **Multi-step:** Puede realizar tareas complejas en varios pasos
5. **Headless mode:** Funciona sin interfaz gráfica

## Integración con Mastermind

- Reemplaza `scrapy` para webs que requieren JavaScript
- Ideal para webs con login, CAPTCHAs, o contenido dinámico
- Complementa `firecrawl-web-scraping` (browser use interactivo, firecrawl estático)
- Útil para government data pipelines

## Pitfalls

- **Lento:** Más lento que scraping directo (requiere LLM para cada paso)
- **Costoso:** Cada paso consume tokens de LLM
- **Inestable:** Cambios en la UI de la web pueden romper las tareas
- **Rate limiting:** Los navegadores automáticos pueden ser bloqueados

## Referencias

- [GitHub: browser-use/browser-use](https://github.com/browser-use/browser-use)
