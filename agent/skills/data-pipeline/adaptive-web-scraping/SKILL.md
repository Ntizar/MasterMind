---
name: adaptive-web-scraping
version: "1.0.0"
description: "Scraping web adaptativo con Scrapling — framework que maneja todo desde una sola request, con detección de cambios, anti-bot bypass y auto-matching. Inspirado en D4Vinci/Scrapling (⭐68K)."
tags: [scraping, web, adaptive, anti-bot, scraping, python]
---

# Scraping Web Adaptativo

## Resumen

[Scrapling](https://github.com/D4Vinci/Scrapling) (⭐68K) es un framework de web scraping adaptativo que maneja todo desde una sola request: detección de cambios en selectores, anti-bot bypass, auto-matching de elementos, y recuperación automática cuando la web cambia.

## Cuándo usar

- Scrapear sitios que cambian de estructura frecuentemente
- Bypass de anti-bot (Cloudflare, reCAPTCHA)
- Scraping robusto que no se rompe cuando cambia el HTML
- Extracción de datos con auto-recuperación

## Patrón de uso

```python
from scrapling import Fetcher, StealthFetcher

# Fetch básico
fetcher = Fetcher()
page = fetcher.get("https://example.com")

# Selector adaptativo — sobrevive cambios de HTML
title = page.css_first("h1::text")
# Si el selector cambia, Scrapling busca automáticamente el elemento similar

# Stealth mode — bypass anti-bot
stealth = StealthFetcher()
page = stealth.fetch("https://protected-site.com")

# Auto-matching de elementos
products = page.css_all(".product-card")
for product in products:
    name = product.css_first(".name::text")
    price = product.css_first(".price::text")
    print(f"{name}: {price}")

# Extracción con recuperación automática
# Scrapling guarda el estado del HTML y si cambia,
# busca automáticamente el elemento más similar
```

## Features clave

| Feature | Descripción |
|---------|-------------|
| Adaptive matching | Si un selector cambia, busca elemento similar automáticamente |
| Anti-bot bypass | StealthFetcher con fingerprinting real de navegador |
| Auto-recovery | Recuperación automática cuando la web cambia estructura |
| Single request | Todo desde una request, sin necesidad de configuración compleja |
| CSS + XPath | Soporta ambos tipos de selectores |

## Pitfalls

- **StealthFetcher:** Requiere Playwright. Más lento pero bypassa anti-bot.
- **Rate limiting:** Respetar rate limits del sitio. Scrapling no lo hace automáticamente.
- **Memory:** Páginas grandes consumen memoria. Usar `stream=True` para HTML grande.
- **Legal:** Verificar ToS del sitio antes de scrapear. Algunos sitios prohíben scraping.

## Referencias

- Scrapling: https://github.com/D4Vinci/Scrapling
- Docs: https://scrapling.dev

---

**Hecho con ❤️ por David Antizar**
