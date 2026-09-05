---
name: html-demo-pattern-mining
description: 'Use al minar ideas de colecciones de demos HTML.'
version: "1.0.0"
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [frontend, html, css, creative, mining, patterns, github-pages, demo-collection]
    related_skills: [frontend-dashboard-patterns, popular-web-designs, awesome-design-systems]
---

# Html Demo Pattern Mining — Extraer ideas de colecciones de demos

Cuando David manda "pilla este GitHub para copiar ideas" / "graba este repo" y es una **colección de N piezas HTML autocontenidas** (cada una un único `.html` con CSS/JS inline), el objetivo no es clonar el repo sino **minar el catálogo y las técnicas reutilizables**.

## When to Use
- Repos/páginas GitHub Pages del estilo "GPT-6-Astra · 100 HTML Files", "54 design systems", "N one-page experiments".
- Cualquier colección de demos HTML single-file (arte generativo, layout editorial, juguetes de física, interfaces).

## Flujo (comprobado con 100 piezas)

1. **Fetch del index con curl** — `web_extract`/Firecrawl suele devolver **403 sin API key**; `curl -sL <url> -o index.html` funciona directo. El index es un catálogo HTML, no una app.

2. **Parsear las cards** con regex + `html.unescape`. Estructura de card (`<article class="card">`):
   - número: `<span class="num">NNN</span>`
   - título: `<div class="title"><a href="...">TITULO</a></div>`  ← **NO es h2/h3** (regex h2/h3 devuelve vacío)
   - descripción: `<p class="desc">...</p>`
   - prompt original: `<details class="prompt"><blockquote>...</blockquote></details>`
   - Limpiar: quitar tags, unescape, colapsar espacios. Guardar `catalog.json` (num/title/desc/prompt).

3. **Derivar base names** de los `href="NNN-slug.html"` (el index lista cada pieza 2 veces: thumb + botón Open → dedupe, preservar orden).

4. **Descarga masiva** de todos los `.html` + `.txt` (prompts) con `xargs -P 10`:
   ```bash
   cat bases.txt | xargs -P 10 -I{} sh -c 'curl -sL "BASE_URL/{}.html" -o "$0/{}.html" && curl -sL "BASE_URL/{}.txt" -o "$0/{}.txt"' "$DEST"
   ```
   Cada archivo suele ser ~5KB → todo el set son ~1-2MB.

5. **Contar técnicas** con un contador de regex sobre todos los `.html` descargados → tabla de frecuencia (qué patrones se repiten y en qué %). Ver `references/pattern-taxonomy.md` para la taxonomía resultante.

6. **Digerir por tema** (paisaje procedural, arte generativo/canvas, editorial, instrumento/dashboard, juguetes, objetos/museo, rituales, transporte/mapas) y destacar los alineados con los proyectos de David (mapas, tránsito, dashboards de datos → instrumento elegante).

## Pitfalls
- **Firecrawl/web_extract 403** sin API key → usar `curl` directamente sobre el index.
- **Título no está en h2/h3** → está en `<div class="title"><a>`. No perder tiempo con h2/h3.
- **Duplicados en hrefs** → cada pieza sale 2 veces en el index; dedupe con preservación de orden.
- **Windows**: pasar rutas nativas `C:/Users/...` a `curl`/xargs (no `/c/Users/...`); usar `$0` para el destino dentro del `sh -c`.
- **catalog.json**: si el parseo se reescribe sin `prompt_file`, re-derivar bases desde los hrefs del index.

## Referencia
- `references/pattern-taxonomy.md` — taxonomía de técnicas CSS/JS con % de frecuencia sobre un set de 100 piezas + piezas destacadas por categoría.
