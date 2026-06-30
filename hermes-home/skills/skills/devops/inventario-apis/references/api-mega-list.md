# API-mega-list — Referencia

## Origen

- **Repo:** https://github.com/cporter202/API-mega-list
- **Licencia:** catálogo público de APIs organizadas por categoría
- **Total estimado:** ~25.822 APIs (actualizado 2026-06-16)

## Formato del catálogo (CRÍTICO)

El README.md del catálogo usa **tablas HTML**, NO listas markdown:

```markdown
| [🎙️ Podcast Episode Ideas Creator](https://apify.com/...) | Description text... |
| [🌸 Tweets / X - Scraper](https://apify.com/...) | Description text... |
```

**Regex para parsear:** `r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^\|]+?)\s*\|'`

Cada fila tiene: nombre (con emoji), URL, descripción. El nombre puede incluir precios (`- $0.5 per 1k`) o `(Rental)` que deben limpiarse.

## Mapeo de secciones del catálogo a carpetas (SECCION_MAP)

El script `procesar-apis.py` mapea encabezados `## Nombre` del README a carpetas:

| Encabezado catálogo | Carpeta |
|---|---|
| `## Agents` | agentes-ia |
| `## AI` | ia |
| `## Automation` | automatizacion |
| `## Business` | negocios |
| `## Developer Tools` | dev-tools |
| `## Ecommerce` | ecommerce |
| `## Integrations` | integraciones |
| `## Jobs` | empleo |
| `## Lead Generation` | lead-gen |
| `## MCP Servers` | mcp-servers |
| `## News` | noticias |
| `## Open Source` | open-source |
| `## Other` | otras |
| `## Real Estate` | inmuebles |
| `## SEO Tools` | seo |
| `## Social Media` | redes-sociales |
| `## Travel` | viajes |
| `## Videos` | videos |

## Proceso de procesamiento

Cada API se procesa generando:
1. Un subdirectorio con nombre slugificado en la categoría correspondiente
2. Un `README.md` con informe detallado de la API
3. Un `datos.json` con datos estructurados
4. Actualización de `estado.json` con métricas

## Estado del inventario

Archivo maestro: `/tmp/inventario-apis/estado.json`
- `total_estimado`: APIs totales en el catálogo
- `procesadas`: APIs procesadas en total
- `categorias`: diccionario con métricas por categoría
- `api_procesadas`: lista plana de nombres de APIs procesadas

## Scripts del proyecto

- `/opt/hermes-work/inventario-apis/procesar-apis.py` — Procesador principal (5 APIs por ejecución)
- `/opt/hermes-work/inventario-apis/crear-estructura.py` — Crear estructura de categorías (uso único, inicialización)
- `/tmp/inventario-apis/estado.json` — Estado actual del procesamiento
