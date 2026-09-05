---
name: firecrawl-web-scraping
description: "Usa al scrapear y crawl web con Firecrawl SDK."
version: "2.0.0"
tags: [scraping, firecrawl, web, api, crawl, ai, sdk]
related_skills: [llm-friendly-web-crawler, firecrawl-web-scraping, crawlee-web-scraping, browser-use-ai]
---

# Firecrawl — scraping y crawling con IA (SDK actual)

> ⚠️ Corrección 2026-09-05 (auditoría): la clase `FirecrawlApp` ya no existe y el paquete Node cambió. API actual = `Firecrawl` con `scrape/crawl/batch_scrape`.

**Repo:** `https://github.com/firecrawl/firecrawl` (TypeScript, ~177K⭐).

## When to Use

- Cuando pidas **scrapear** o **crawlear** (con IA) una web y obtener contenido limpio (markdown/JSON).
- Para convertir páginas a LLM-friendly (por eso encaja con `llm-friendly-web-crawler`).

## Uso (Python SDK)

```python
from firecrawl import Firecrawl

app = Firecrawl(api_key="fc-...")   # la SDK actual usa la clase Firecrawl
resp = app.scrape("https://ejemplo.com")        # scrape de una URL
# app.crawl(url) / app.batch_scrape(urls) también existen
```

## Uso (Node.js)

```bash
npm install firecrawl          # (ya NO es @mendable/firecrawl-js)
```

```js
import { Firecrawl } from 'firecrawl';
const app = new Firecrawl({ apiKey: 'fc-...' });
const data = await app.scrape('https://ejemplo.com');
```

## Pitfalls

- La clase es **`Firecrawl`**, no `FirecrawlApp`; métodos **`scrape`/`crawl`/`batch_scrape`**, no `scrape_url`/`crawl_url`/`batch_scrape_urls`.
- Paquete Node: **`npm install firecrawl`** (el antiguo `@mendable/firecrawl-js` es legacy).
- Requiere `api_key` (frecuentemente de pago para uso intensivo).

## Verificación

- `app.scrape(url)` y comprobar que devuelve `markdown`/`metadata` limpio.
