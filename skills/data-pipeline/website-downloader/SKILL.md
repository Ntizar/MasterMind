---
name: website-downloader
description: Descargar sitios web completos para análisis offline — scraping batch de sitios enteros.
version: "1.0.0"
tags: [downloader, website, scraping, batch, offline, analysis]
---

# Website Downloader

## Resumen

Descargar sitios web completos para análisis offline — scraping batch de sitios enteros. 4k⭐.

## Repo de referencia

- **GitHub:** `github.com/AhmadIbrahiim/Website-downloader`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install website-downloader
# o clonar
git clone https://github.com/AhmadIbrahiim/Website-downloader.git
cd Website-downloader && pip install -r requirements.txt
```

## Uso Básico

```python
from website_downloader import WebsiteDownloader

downloader = WebsiteDownloader()

# Descargar sitio completo
downloader.download(
    url="https://ejemplo.com",
    output_dir="./sites/ejemplo",
    max_depth=3,
    max_pages=100,
    follow_links=True,
    save_images=True,
)

# Descargar con filtros
downloader.download(
    url="https://docs.ejemplo.com",
    output_dir="./docs",
    file_types=[".html", ".css", ".js"],
    exclude_patterns=["/admin/*", "/login"],
)
```

## Patrones Clave

1. **Multi-depth:** Controlar profundidad de crawl
2. **Filtros:** Excluir paths, tipos de archivo, dominios externos
3. **Preservar estructura:** Mantener árbol de directorios original
4. **Imágenes:** Descargar assets, CSS, JS, imágenes
5. **Análisis offline:** Procesar HTML descargado con BeautifulSoup

## Integración con Mastermind

- Útil para descargar documentación completa para análisis
- Complementa `firecrawl-web-scraping` — descarga local vs API
- Ideal para `static-digest-pipeline` con fuentes locales
- Perfecto para análisis de sitios con `llm-friendly-web-crawler`

## Pitfalls

- **Legal:** Verificar términos de servicio antes de descargar
- **Tamaño:** Sitios grandes pueden ocupar GBs
- **Robots.txt:** Respetar robots.txt del sitio objetivo
- **Rate limiting:** Configurar delays entre requests
- **Links rotos:** Algunos recursos pueden no estar disponibles

## Referencias

- [GitHub: AhmadIbrahiim/Website-downloader](https://github.com/AhmadIbrahiim/Website-downloader)
