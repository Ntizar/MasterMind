---
name: adaptive-web-scraping
description: "Usa al scrapear web adaptativo con Scrapling."
version: "2.0.0"
tags: [scraping, scrapling, stealth, python, adaptativo, anti-bot]
related_skills: [llm-friendly-web-crawler, crawlee-web-scraping, browser-use-ai, scrapy-web-scraping]
---

# Scrapling — scraping adaptativo + stealth

> ⚠️ Corrección 2026-09-05 (auditoría): la clase es `StealthyFetcher` (no `StealthFetcher`) y el parser usa `css()/xpath()` que devuelven Selectors con `.get()/.getall()`, no `css_first()/css_all()`. Docs reales: `scrapling.readthedocs.io`.

**Repo:** `https://github.com/D4Vinci/Scrapling` (Python, ~78K⭐).

## When to Use

- Cuando pidas **scraping adaptativo** con evasión anti-bot: cambiar de web a web sin conformar selectores desde cero, con un fetcher "stealth".

## Uso (API real)

```python
from scrapling import Fetcher, StealthyFetcher   # StealthyFetcher (no Stealth)

page = Fetcher().get('https://ejemplo.com')       # o StealthyFetcher().get(...)
# El parser devuelve Selectors:
title = page.css('h1::text').get()                # (NO css_first)
cards = page.css('.product-card').getall()        # (NO css_all)
```

## Pitfalls

- Clase **`StealthyFetcher`**, no `StealthFetcher` (el import `StealthFetcher` da ImportError).
- **No** hay `css_first()`/`css_all()`: usa `.css()`/`.xpath()` + `.get()`/`.getall()` (y `.first`/`.last`).
- Docs: **`scrapling.readthedocs.io`** (scrapling.dev no resuelve).

## Verificación

- `StealthyFetcher().get(url)` → `page.css('h1::text').get()` y confirmar que evita el bloqueo.
