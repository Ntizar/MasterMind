---
name: llm-friendly-web-crawler
version: "1.0.0"
description: "Crawling web LLM-friendly con crawl4ai — output optimizado para LLMs, scraping asíncrono, extracción estructurada. Inspirado en unclecode/crawl4ai (⭐71K)."
tags: [crawler, scraping, llm, crawl4ai, web, extraction, async]
---

# Crawler Web LLM-Friendly

## Resumen

[crawl4ai](https://github.com/unclecode/crawl4ai) (⭐71K) es un crawler web open-source diseñado para LLMs. Genera output en markdown limpio, extrae datos estructurados, y soporta estrategias de extracción con LLM.

## Cuándo usar

- Scrapear web y alimentar LLMs con contenido limpio
- Extracción estructurada de páginas (productos, artículos, datos)
- Crawling asíncrono de múltiples sitios en paralelo
- Preparar datos para RAG desde web

## Patrón de uso

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerStrategy

async def crawl_site(url):
    async with AsyncWebCrawler() as crawler:
        # Crawl básico — output markdown limpio
        result = await crawler.arun(url)
        print(f"Markdown: {result.markdown[:500]}")
        print(f"Links: {result.links}")
        return result

# Crawl con extracción estructurada
async def crawl_with_extraction(url, schema):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url,
            extraction_strategy=CrawlerStrategy(
                type="json_schema",
                schema=schema  # JSON schema de qué extraer
            )
        )
        return result.extracted_content  # Datos estructurados

# Schema de extracción
product_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
        "description": {"type": "string"},
        "image": {"type": "string"}
    }
}

# Crawl paralelo de múltiples URLs
async def crawl_multiple(urls):
    async with AsyncWebCrawler() as crawler:
        tasks = [crawler.arun(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

asyncio.run(crawl_site("https://example.com"))
```

## Estrategias de extracción

| Estrategia | Cuándo | Output |
|-----------|-------|--------|
| `markdown` | Content para LLM | Markdown limpio |
| `json_schema` | Datos estructurados | JSON validado |
| `css_selector` | Extracción por CSS | HTML/Text de elementos |
| `xpath` | Extracción por XPath | HTML/Text de nodos |
| `llm_extraction` | Extracción con LLM | JSON desde LLM |

## Pitfalls

- **Rate limiting:** crawl4ai respeta robots.txt por defecto. Desactivar con cuidado.
- **JavaScript:** Sitios SPA necesitan JavaScript rendering. crawl4ai usa Playwright por defecto.
- **Memory:** Crawling de sitios grandes puede consumir mucha memoria. Usar `max_depth` y `max_pages`.
- **Output size:** Markdown de páginas grandes puede superar context window. Truncar o chunk.
- **Async:** Todo es async. Usar `asyncio.run()` o integrar en event loop existente.

## Referencias

- crawl4ai: https://github.com/unclecode/crawl4ai
- Docs: https://docs.crawl4ai.com

---

**Hecho con ❤️ por David Antizar**
