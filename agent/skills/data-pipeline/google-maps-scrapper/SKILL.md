---
name: google-maps-scrapper
description: Scraping de datos de Google Maps — negocios, reviews, ubicaciones, coordenadas, horarios.
version: "1.0.0"
tags: [scraping, google-maps, business, reviews, geolocation]
---

# Google Maps Scraper

## Resumen

Scraping de datos de Google Maps — negocios, reviews, ubicaciones, coordenadas, horarios. 1k⭐.

## Repo de referencia

- **GitHub:** `github.com/zohaibbashir/Google-Maps-Scrapper`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install google-maps-scraper
# o clonar
git clone https://github.com/zohaibbashir/Google-Maps-Scrapper.git
cd Google-Maps-Scrapper && pip install -r requirements.txt
```

## Uso Básico

```python
from google_maps_scraper import GoogleMapsScraper

scraper = GoogleMapsScraper()

# Buscar negocios
results = scraper.search(
    query="restaurantes Madrid",
    limit=50,
    output_format="csv"
)

# Extraer detalles
for business in results:
    print(f"{business['name']}")
    print(f"  Rating: {business['rating']}")
    print(f"  Reviews: {business['reviews']}")
    print(f"  Location: {business['latitude']}, {business['longitude']}")
    print(f"  Address: {business['address']}")
    print(f"  Phone: {business['phone']}")
    print(f"  Website: {business['website']}")
    print(f"  Hours: {business['hours']}")
```

## Datos Extraíbles

1. **Nombre** del negocio
2. **Rating** y número de reviews
3. **Categoría** (restaurante, tienda, etc.)
4. **Dirección** completa
5. **Coordenadas** (lat/lng)
6. **Teléfono** y website
7. **Horarios** de apertura
8. **Reviews** con texto y puntuación
9. **Fotos** del lugar

## Integración con Mastermind

- Útil para análisis de datos geoespaciales de negocios
- Complementa `osm-infrastructure-mapping` con datos de Google
- Ideal para `competitive-intelligence` — mapear competencia
- Útil para `business-intelligence` con datos reales

## Pitfalls

- **Rate limiting:** Google bloquea rápidamente — usar proxies y delays
- **Legal:** Términos de servicio de Google prohíben scraping
- **CAPTCHA:** Puede aparecer CAPTCHA tras varias búsquedas
- **Inestable:** Cambios en la UI de Google Maps rompen el scraper
- **Geo-restrictions:** Resultados varían por ubicación

## Referencias

- [GitHub: zohaibbashir/Google-Maps-Scrapper](https://github.com/zohaibbashir/Google-Maps-Scrapper)
