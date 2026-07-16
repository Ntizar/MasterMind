---
name: autoscraper
description: AutoScraper — scraping web automático con IA, aprende patrones de selección y extrae datos sin código.
category: data-pipeline
---

# AutoScraper — Scraping Web con IA

## Qué es

AutoScraper es una herramienta de scraping que usa patrones de aprendizaje para extraer datos:
- **Pattern learning** — aprende patrones de selección de la página
- **No code** — no requiere selectors CSS o XPath
- **Adaptive** — se adapta a cambios en la estructura de la página
- **Fast** — basado en requests + pattern matching

## Instalación

```bash
pip install autoscraper
```

## Uso básico

```python
from autoscraper import AutoScraper

# Crear scraper aprendiendo de ejemplos
wanted_list = ['Price', 'Rating', 'Reviews']
response = requests.get('https://example.com/product')
scraper = AutoScraper()
result = scraper.build(response.text, wanted_list)

# Extraer de nueva página
new_response = requests.get('https://example.com/product2')
new_result = scraper.run(new_response.text)
print(new_result)
```

## Casos de uso para David

- **Web scraping** — extraer datos de sites sin API
- **Data collection** — recoger datos estructurados de la web
- **Integration** — usar con crawlee para scraping robusto
- **Anti-detection** — usar con curl-impersonate

## Pitfalls

- No funciona bien con contenido JS-renderizado (usa requests, no browser)
- Los patrones pueden romperse si la página cambia
- No maneja autenticación/login
- Combinar con Playwright/Selenium para JS sites

## Referencias

- Repo: `github.com/alirezamika/autoscraper` (7K⭐)
