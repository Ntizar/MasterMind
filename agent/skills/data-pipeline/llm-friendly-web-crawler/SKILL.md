---
name: llm-friendly-web-crawler
description: "Usa al crawlear web LLM-friendly con crawl4ai."
version: "2.0.0"
tags: [crawler, crawl4ai, web, llm, scraping, markdown, pydantic]
related_skills: [firecrawl-web-scraping, adaptive-web-scraping, crawlee-web-scraping, browser-use-ai]
---

# Crawl4AI — crawling web LLM-friendly

> ⚠️ Corrección 2026-09-05 (auditoría): la clase `CrawlerStrategy` NO existe y `result.markdown` es un objeto, no un string. API real = `BrowserConfig`/`CrawlerRunConfig` + strategies `JsonCssExtractionStrategy`/`LLMExtractionStrategy`.

**Repo:** `https://github.com/unclecode/crawl4ai` (Python, ~81K⭐).

## When to Use

- Cuando pidas **crawling LLM-friendly**: extraer contenido de una web en markdown/JSON listo para meter en un LLM.

## Uso (API real)

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy, LLMExtractionStrategy

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://ejemplo.com", config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS))
    md = result.markdown.raw_markdown        # markdown es un OBJETO con .raw_markdown / .fit_markdown
    print(md[:500])
```

Extracción estructurada:

```python
schema = {...}
strategy = JsonCssExtractionStrategy(schema, verbose=True)   # o LLMExtractionStrategy(...)
```

## Pitfalls

- **No existe** `CrawlerStrategy` — usa `JsonCssExtractionStrategy`/`LLMExtractionStrategy`.
- `result.markdown` es un objeto: `.raw_markdown`/`.fit_markdown`, no `[:500]` a secas.
- El core es `AsyncWebCrawler` + `CrawlerRunConfig` (o `BrowserConfig`).

## Verificación

- `await crawler.arun(url)` y leer `result.markdown.raw_markdown`. Para extracción con schema, `JsonCssExtractionStrategy`.
