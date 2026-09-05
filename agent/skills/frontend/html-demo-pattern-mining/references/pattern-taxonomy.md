# Taxonomía de técnicas — set de 100 demos HTML autocontenidas

Creada al minar "GPT-6-Astra · 100 HTML Files" (GitHub Pages). Cada pieza es un único `.html` de ~5KB con CSS/JS inline, offline, responsive y accesible.

## Frecuencia de técnicas (N=100)

| Técnica | % | Nota |
|---|---|---|
| `letter-spacing` micro (mayúsculas) | 100 | Marca de estilo en casi toda pieza editorial |
| `clamp()` en tipografía | 89 | Tamaños fluidos sin media-queries |
| `grid-template-columns` | 80 | Columnas asimétricas editoriales |
| Gradientes `linear/radial/conic` | 76 | Fondos atmosféricos |
| `input type="range"` (slider) | 44 | Interacción principal de cada pieza |
| `prefers-reduced-motion` | 42 | Accesibilidad |
| `aspect-ratio` | 26 | Proporciones de tarjetas/ilustraciones |
| `<svg>` inline | 26 | Iconos/gráficos sin assets externos |
| `@keyframes` | 18 | Animaciones CSS |
| `filter: blur()` | 16 | Atmósfera/desenfoque de fondo |
| `clip-path: polygon()` | 15 | Siluetas/relieve en capas (montañas) |
| `<canvas>` 2D | 14 | Arte generativo/redes/ondas |
| `requestAnimationFrame` | 11 | Loop de canvas |
| CSS custom props (`--x`) | 10 | Barras de histograma (`--h`) y temas |
| `conic-gradient` | 10 | Discos/ruedas/relojes |
| `writing-mode: vertical-rl` | 7 | Sellos/versos verticales (estética asiática) |
| `backdrop-filter` | 6 | Paneles cristal |
| `mask-image` | 4 | Estrellas/recortes |
| Web Audio (`AudioContext`) | 4 | Sonido sintetizado local |
| `transform` 3D / `perspective` | 4 | Rotación de objetos espaciales |
| `font-variant-numeric: tabular-nums` | 3 | Números tabulares (relojes/datos) |
| `localStorage` | 3 | Diarios guardados localmente |
| `type="checkbox"` toggle | 1 | Toggles día/noche |

## Piezas destacadas por categoría (con su truco)

**Paisaje / atmósfera procedural**
- `001-aurora-observatory` — cintas de aurora con `filter:blur(65px)` + `radial-gradient`, estrellas con `mask-image`, paneles `backdrop-filter`, histograma con barras CSS `--h`, slider que modula el blur. (`The night is alive.` tipografía Georgia serif gigante.)
- `091-ink-mountains` — capas de montaña con `clip-path:polygon()` + `transform:scaleX(-1)` y `translateY` para profundidad; reflejo del agua con `repeating-linear-gradient`; sello/verso con `writing-mode:vertical-rl`; barca animada con `@keyframes`.

**Arte generativo / canvas**
- `044-thought-network` — `<canvas>` 2D + rAF, overlay de texto con `pointer-events:none` para que el canvas siga interactivo; tipografía mono micro; botón "IGNITE A THOUGHT".
- `063-resonance` / `100-organic-wave` — ondas/currentes superpuestos de color translúcido.

**Instrumento / dashboard (patrón dato → instrumento elegante)**
- `001` (aurora), `052-equal` (presión/ hidrostática), `026-tidal-hours`, `033-barometer-room`, `059-split` (timer). Ideal para DataHub/ESIOS: convertir datos en "instrumento" con diales, barras y lectura editorial.

**Tipografía / editorial monumental**
- `002-form-editorial`, `004-dune`, `036-arctic-journal` — masthead serif gigante, grid asimétrico, `clamp()` + `letter-spacing` negativo.

**Juguetes / interacción**
- `055-chroma` (mezclador de color), `065-bloom` (flores radiales), `072-patchwork` (pixel quilt), `083-letter-foundry` (tipografía en movimiento), `097-small-oracle`.

**Objetos / museo**
- `027-cabinet-of-minerals`, `058-object-archive`, `087-marble-room`, `053-type-specimen`.

**Transporte / mapas (más alineados con David)**
- `030-land-in-lines` (workspace cartográfico con contornos), `037-borrowed-skies` (mapa de migración de aves), `061-elsewhere-city-lines` (guía de tránsito), `079-isola` (atlas de islas), `021-somewhere` (hall de salidas con tipografía de transporte), `085-nightjet` (tren nocturno + billete).

## Receta de mintiendo (cómo se contó)
```python
import glob, re, collections
counts = collections.Counter()
for f in glob.glob("*.html"):
    src = open(f, encoding="utf-8", errors="ignore").read()
    for name, pat in PATTERNS.items():
        if re.search(pat, src): counts[name] += 1
```
`PATTERNS` mapea cada nombre a un regex simple (`clip-path`, `mask-image|mask:`, `backdrop-filter`, `<canvas`, `requestAnimationFrame`, `writing-mode:\s*vertical`, `conic-gradient`, `clamp\(`, `prefers-reduced-motion`, `type="range"`, `localStorage`, `AudioContext`, `perspective|rotateX|rotateY`, etc.). Guardar catálogo en `catalog.json` y archivos en la carpeta destino.
