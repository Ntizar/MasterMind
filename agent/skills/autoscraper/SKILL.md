---
name: autoscraper
description: "Usa al scrapear con AutoScraper (aprende patrones)."
version: "2.0.0"
tags: [scraping, autoscraper, python, aprieta, ml, web, patrones]
related_skills: [adaptive-web-scraping, scrapy-web-scraping, crawlee-web-scraping, google-maps-scrapper]
---

# AutoScraper — scraping que aprende patrones por ti

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 usaba `scraper.run(texto)` — **inexistente**. La API real para re-extraer de una página nueva es `get_result_similar()`/`get_result()`.

**Repo upstream:** `https://github.com/alirezamika/autoscraper` (MIT, Python, ~7.9K⭐).

## When to Use

- Cuando pidas **scrapear** una web sin escribir selectores a mano: le das ejemplos de lo que quieres y aprende el patrón.
- Para sitios con estructura estable donde el selector cambia poco; ideal para prototipos rápidos.

## Uso

```python
import requests
from autoscraper import AutoScraper

url = 'https://ejemplo.com'
# Pasas ejemplos de lo que quieres extraer y la página de donde aprender
wanted_list = ['ejemplo de texto a extraer']
scraper = AutoScraper()
result = scraper.build(url, wanted_list)   # aprende el patrón

# Re-extraer de una página nueva (misma estructura):
req = requests.get('https://ejemplo.com/otra-pagina')
scraper.get_result_similar(req.text)       # <- API real (NO scraper.run)
```

- `build(url, wanted_list)` acepta el HTML/código de la página.
- Para extracción exacta: `get_result()` / `get_result_exact()`.

## Pitfalls

- La API es **`get_result_similar()`** (o `get_result`/`get_result_exact`); **no existe `scraper.run()`**.
- Importar `requests` al usar `requests.get(...)`.
- Solo aprende patrones de sitios con estructura repetitiva; webs dinámicas (JS) necesitan browser automation.

## Verificación

- `scraper.build(url, wanted_list)` → `get_result_similar(req.text)` y comprobar que devuelve el mismo tipo de datos en una página distinta del mismo sitio.
