# 2026-09-03 — Inspiración web: doboku-map y el patrón "monitor de grandes obras"

## Origen
David pasó varias webs para inspirarse. La joya: **https://doboku-map.h1den.com/** — "JAPAN CIVIL WORKS MONITOR", mapa de 150 grandes proyectos de obra civil de Japón. David quiere replicarlo **para España**.

## Anatomía técnica de doboku-map (verificada descargando su código)
- Stack: **Leaflet 1.9.4 (CDN) + tiles GSI pale (`cyberjapandata.gsi.go.jp/xyz/pale`) + un solo JSON** (`data/projects.json`, 346KB, 150 proyectos). HTML estático puro, sin backend.
- `app.js` minificado (~32KB) y `app.css` (~25KB). Todo vanilla JS.
- Estructura del JSON por proyecto:
  - `id, name, category, pref (prefectura), lat, lng, operator, cost, period`
  - `status_summary` (resumen narrativo), `progress_pct` (nullable), `progress_note`
  - `news[]` (date AAAA-MM, title, url), `sources[]` (label, url), `youtube[]` (title, url, date)
  - `lines[]` — geometría polilínea (trazado de la obra: vía, autopista...) + campo `planned`
- Categorías equilibradas: 鉄道 (ferrocarril 37), 道路 (carreteras 38), ダム・河川 (pantanos/ríos 37), 港湾・空港 (puertos/aeropuertos 38).
- UI (del HTML): pantalla **boot** con líneas tipo terminal y reloj en vivo, **ticker** superior deslizante, **sidebar** con pestañas (lista/filtros), buscador, chips por categoría, `select` de orden, contador, **dock inferior** con estadísticas (barras de coste por categoría, barras por prefectura, histograma de progreso), **detalle** por proyecto con fuentes/noticias/YouTube, esquinas tipo HUD (`cb tl/tr/bl/br`), coordenadas en vivo, vignette + scanline, toast, botón compartir.

## Traducción España (ideas para el "Mapa de Grandes Infraestructuras de España")
- Tiles: **IGN España raster** — `https://www.ign.es/wmts/mapa-raster?layer=MTN&...` o CARTO light gratis; también PNOA ortofoto como capa alternativa.
- Datos: Adif (corredores, estudio informativo), Ministerio de Transportes, Fomento, SEPI/ACIES (presas), Aena (aeropuertos), Puertos del Estado, cada obra con fuentes oficiales y noticias.
- Categorías espejo: ferrocarril (AVE/corredores), carreteras (autovías A-), agua (presas/trasvases/desaladoras), puertos y aeropuertos. Metros regionales podrían ser 5ª categoría.
- Fuentes de noticias: DGT, BOE, MITMA, prensa local. El valor del site es la **curación manual tipo redactor** (resúmenes narrativos + fechas), no el scraping.

## Otras webs de la tanda
- `code.gouv.fr/sill` — catálogo francés de software libre recomendado para administración. Idea replicable: "SILL español" con datos en JSON.
- `miaai-lab.github.io/Fable-5.1-100-HTML-Files` — 100 HTML autocontenidos de estudio (aurora glass, generative art...), cada uno con su prompt original visible. Buen banco de técnicas CSS puras (conic-gradient, mix-blend-mode, feTurbulence).
- Tweet @sauda_coder — lista de 50 webs de datos en vivo: zoom.earth, flightradar24, windy, lightningmaps, submarinecablemap, pudding.cool, observablehq, listen.hatnote... Para APIs gratuitas de España ver skill `api-mega-catalog` y `boe-borme-api`.
- Tweet de @vib3coded inaccesible (X requiere login).
