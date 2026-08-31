# Fuentes de batimetría real por API (verificado en sesión Water3J, agosto 2026)

## EMODnet Bathymetry — LA FUENTE que funciona (Europa)
- `https://rest.emodnet-bathymetry.eu/depth_sample?geom=POINT(<lon>+<lat>)` → JSON:
  `{"min":..., "max":..., "avg":-82.58, "smoothed":-81.37, "reference":{...}}`
- `avg` = profundidad media en METROS, **negativa en mar** → usar `Math.abs(avg)`.
- **Sin clave, CORS abierto** (`Access-Control-Allow-Origin` verificado). 1 punto por llamada; rejilla 11×11 = 121 llamadas paralelas OK (~20 s).
- Cobertura: solo mares europeos. Resolución DTM 100 m.
- Cachear en IndexedDB (store `baterias`, clave `bat_lat_lon_ancho_n`).

## Lo que NO funcionó desde el PC de David (no reintentar ciegamente)
- **OpenTopoData (GEBCO)**: bloqueado a nivel ISP — Cloudflare bloqueado por orden judicial LaLiga/Telefónica (bloqueo de IPs Cloudflare en España). curl → SEC_E_UNTRUSTED_ROOT / timeout. Con `-k` llega pero Cloudflare deniega. GEBCO requerirá otro canal o proxy propio.
- **Open-Meteo Elevation**: funciona (sin clave, CORS) pero es DEM de tierra — **devuelve 0.0 en mar**, inservible para batimetría marina.
- En este PC: `python` (uv 3.11) sin red directa (WinError 10051, proxy); `node fetch` falla a Cloudflare; `curl` funciona salvo TLS hacia Cloudflare. **Para probar APIs desde terminal: curl primero.**

## Motor 2D (src/studio/motor2d.js) — decisiones validadas por T14
- Trazado de rayos: `dα/ds = -(1/c)·∂c/∂n` con ∂c/∂n por diferencias finitas perpendiculares al rayo. Convención: α desde +y; para propagar hacia −y usar α0=150° (no 30°).
- Dispersión Airy por Newton sobre ω²=gk·tanh(kh). Verificación: L(20 m, T=10 s) ≈ 121 m (tablas CEM ~120.3) — NO 156 m (ese es el límite en aguas profundas gT²/2π).
- Altura: conservación de flujo de energía `H = H0·√(cg0·b0/(cg·b))` + límite rotura 0.78·h (comparar con margen 1e-3 por redondeo toFixed).
- `frentesIsocronos()` implementado y **ANIMADO en el mapa**: frentes blancos que avanzan cada T/2 vía `propagarFrente` + `frentesIsocronos` + setInterval que alterna opacidad de polylines (guardar el interval en `window.__animFrentes` y limpiarlo antes de re-simular).

## Tanda puertos/animación (verificado en sesión posterior, agosto 2026)
- **Separación b REAL entre rayos**: `calcularSeparaciones(rayos)` mide distancia media a vecinos en cada paso → pasar como `bPorPunto` a `alturaEnRayo`. Convergencia/divergencia por refracción afecta H de verdad (T15 4/4).
- **BUG FÍSICO clave cazado por T15**: la perpendicular al rayo es `n̂ = (cos α, −sin α)`, NO `(-sin α, cos α)` (eso es el propio rayo). Con el bug, taludes rectos y rayos verticales funcionaban "bien" por simetría — solo tests con rayos OBLICUOS + batimetría con gradiente lateral (canal gaussiano) lo destapan. Criterio de test: comparar b final vs b0 con umbral 5%.
- **Resolución adaptable por zoom** (capa2d.js): zoom≥14 (puerto) → 15×15 pts en 1.2 km (~86 m/punto, cerca del límite DTM); 12→13×13/3 km; ≤10→11×11/6-10 km. Leer `mapa.getZoom()` en simular2D.
- Tests con taludes largos: pendiente 0.5·j agota el recorrido en ~5 pasos (sin refracción lateral); usar 0.25·j y rejilla de 120 nodos en y, rayos desde el borde profundo.

## Verificación E2E sin red del usuario
`tests/ver-2d.mjs` (puppeteer+SwiftShader): pulsa el botón 2D, espera ~20 s, lee `#estado2d` y cuenta paths de Leaflet. EMODnet real descargado desde el navegador headless sin errores.
