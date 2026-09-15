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

## Tercera opción: py-lead-generation (Madi-S/Lead-Generation)

Paquete en PyPI (**386 ⭐** a 2026-09-15) con API asíncrona y dos motores: Google Maps y **Yelp** (combinación que los otros proyectos de esta sección no ofrecen).

```bash
pip install py-lead-generation
```

```python
import asyncio
from py_lead_generation import GoogleMapsEngine, YelpEngine

async def main():
    eng = GoogleMapsEngine("pizzerias", "Madrid, España", 12)   # zoom = partición del área
    await eng.run()
    eng.save_to_csv()

    y = YelpEngine("Pizza", "Madrid, España")
    await y.run()
    y.save_to_csv("pizza_leads.csv")

asyncio.run(main())
```

Versión antigua archivada dentro del repo: `cd archived/google-maps && python extractor.py` (el README la describe como *dirty/clumsy*).

**Caveats:** pieza patrocinada (CoreClaw) para captar leads; el TODO del repo confirma que **no hay tests, ni CLI/GUI, ni MCP, ni envío de emails/SMS**. Salida solo CSV.

**Patrón reutilizable (independiente de la fuente):** una clase *engine* por plataforma con la misma interfaz (`run()` async + `save_to_csv()`), y el **zoom de Google Maps como parámetro del engine** que fija el área de búsqueda (el troceado fino en rejilla sigue en el TODO del README, **no implementado**).
