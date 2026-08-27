---
name: firecrawl-web-scraping
description: API open-source para convertir cualquier página web en datos limpios (Markdown o JSON estructurado) optimizados para AI agents — scraping, crawling, batch processing.
version: "1.0.0"
tags: [scraping, web, AI, agents, markdown, data-extraction, crawler]
---

# Firecrawl — API de Scraping Web para AI Agents

## Resumen

Firecrawl convierte cualquier página web en datos limpios (Markdown o JSON estructurado) optimizados para AI agents. 142K⭐.

## Instalación

```bash
# Docker (recomendado)
docker pull firecrawl/firecrawl
docker run -p 3000:3000 firecrawl/firecrawl

# Python SDK
pip install firecrawl-py

# Node.js SDK
npm install @mendable/firecrawl-js
```

## Uso Básico

### Python SDK
```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-xxx")

# Scraping simple → Markdown
data = app.scrape_url("https://ejemplo.com", params={"formats": ["markdown"]})

# Crawling completo de un sitio
crawl = app.crawl_url("https://ejemplo.com", params={
    "limit": 100,
    "scrapeOptions": {"formats": ["markdown", "html"]}
})

# Lote de URLs
batch = app.batch_scrape_urls(["https://a.com", "https://b.com"],
                               {"formats": ["json"]})
```

### Node.js SDK
```javascript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({apiKey: 'fc-xxx'});
const data = await app.scrapeUrl('https://ejemplo.com', {formats: ['markdown']});
```

## Patrones Clave

1. **HTML → Markdown**: Limpieza automática de HTML a texto limpio
2. **JSON Structured Output**: Extraer datos con schema definido
3. **Crawling con límites**: `limit`, `maxDepth`, `ignoreSitemap`
4. **Batch processing**: Múltiples URLs en paralelo
5. **Webhook support**: Para crawls largos asíncronos

## Integración con Mastermind

- Reemplaza `curl` + `BeautifulSoup` para scraping web
- Ideal para government data pipelines (BOE, BORME, etc.)
- Complementa `government-cms-scraping` (Firecrawl genérico, CMS scraping específico)
- Útil para static-digest-pipeline

## Referencia

- Repo: https://github.com/firecrawl/firecrawl
- Docs: https://docs.firecrawl.dev
- API: https://api.firecrawl.dev