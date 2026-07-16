---
name: scrapy-web-scraping
description: Framework de scraping web más popular de Python — extensible, asíncrono, con middleware, pipelines y scraping a escala.
version: "1.0.0"
tags: [scraping, web, python, async, crawler, middleware]
---

# Scrapy — Framework de Scraping Web

## Resumen

Framework de scraping web más popular de Python — extensible, asíncrono, con middleware y pipelines. 62k⭐.

## Repo de referencia

- **GitHub:** `github.com/scrapy/scrapy`
- **Lenguaje:** Python
- **Licencia:** BSD

## Instalación

```bash
pip install scrapy
pip install scrapy-splash  # para JavaScript rendering
pip install scrapy-redis   # para distributed scraping
```

## Uso Básico

```python
# spider.py
import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]
    
    def parse(self, response):
        for href in response.css("a::attr(href)").getall():
            yield response.follow(href, self.parse)
        
        yield {
            'title': response.css('h1::text').get(),
            'text': response.css('p::text').getall(),
        }
```

## Ejecutar

```bash
# Salida JSON
scrapy crawl example -o results.json

# Salida CSV
scrapy crawl example -o results.csv

# Con logging detallado
scrapy crawl example -s LOG_LEVEL=DEBUG
```

## Patrones Clave

1. **Middlewares:** Rotación de user-agents, proxies, headers
2. **Pipelines:** Guardar en SQLite, MongoDB, PostgreSQL
3. **Item Loaders:** Transformación y validación de datos
4. **Distributed:** Scrapy-Redis para scraping distribuido
5. **Headless browser:** Splash o Playwright para JS rendering

## Integración con Mastermind

- Reemplaza `BeautifulSoup` + `requests` para scraping a escala
- Ideal para government data pipelines (BOE, BORME, etc.)
- Complementa `firecrawl-web-scraping` (scrapy programable, firecrawl API-based)
- Útil para static-digest-pipeline

## Pitfalls

- **JavaScript:** Scrapy no ejecuta JS. Usa Splash o Playwright para contenido dinámico.
- **Rate limiting:** Configurar `DOWNLOAD_DELAY` para no saturar servidores.
- **Robots.txt:** Respetar robots.txt con `ROBOTSTXT_OBEY = True`.
- **Memory:** Para sitios grandes, usar `itemproc` con pipelines asíncronos.

## Referencias

- [GitHub: scrapy/scrapy](https://github.com/scrapy/scrapy)
- [Docs](https://docs.scrapy.org)
