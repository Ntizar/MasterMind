---
name: google-maps-scrapper
description: "Usa a scrapear negocios y reviews de Google Maps."
version: "2.0.0"
tags: [google-maps, scraping, negocios, reviews, playwight, python]
related_skills: [google-maps-scrapper, adaptive-web-scraping, scrapers]
---

# Google Maps Scrapper — negocios, reviews y ubicaciones

> ⚠️ Corrección 2026-09-05 (auditoría): hay **dos proyectos**: el repo `zohaibbashir` es un **script CLI con Playwright**; la librería Python `pip install google-maps-scraper` con clase `GoogleMapsScraper` es de **`noworneverev/google-maps-scraper`**. No mezclarlos.

## When to Use

- Cuando pidas **extraer negocios, reviews, coordenadas y horarios de Google Maps** para un análisis de mercado.

## Opciones (distingue cuál usas)

- **Script CLI (Playwright)** — repo zohaibbashir: ejecuta un script que abre Google Maps en un navegador (Playwright) y extrae los resultados.
- **Librería Python** — `pip install google-maps-scraper` + `from google_maps_scraper import GoogleMapsScraper` (repo noworneverev).

## Uso (librería Python)

```python
from google_maps_scraper import GoogleMapsScraper
scraper = GoogleMapsScraper(...)
results = scraper.scrape(...)     # ejemplos por el README del repo
```

## Pitfalls

- **No** confundir los dos proyectos (Playwright CLI vs librería Python).
- Verificar el repo exacto que quieres usar antes de elegir el import.

## Verificación

- Extraer reviews/negocios de una zona y comprobar que los campos (nombre, rating, coord) salen.
