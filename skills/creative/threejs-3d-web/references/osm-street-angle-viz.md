# OSM Street Angle Visualization Pattern

**Source:** Keiryosha Dynamic Roads (https://keiryosha.com/dynamic_roads/) — adapted for Spanish cities
**Project:** Ntizar/CallesDinamicas (https://github.com/Ntizar/CallesDinamicas)

## Concept
Classify every street in a city by its principal bearing angle (0-180° from North), assign colors per 15° bin (12 bins), render as an interactive visualization with a scroll-driven morph from "map view" to "pattern view" (treemap layout).

## Data Pipeline

### 1. Fetch from Overpass API
**Working endpoint (2026-07):**
```
POST https://maps.mail.ru/osm/tools/overpass/api/interpreter
Content-Type: application/x-www-form-urlencoded
Body: data=[out:json][timeout:90];way["highway"](S,W,N,E);out body geom;
```

**⚠️ Official `overpass-api.de` returns 403/406 from servers.** The mail.ru mirror works reliably. Also try `overpass.kumi.systems` with proper User-Agent.

**User-Agent required:** `"CallesDinamicas/1.0 (David Antizar)"` or similar. No parentheses in some endpoints.

### 2. Bounding Box Calculation
```python
def radius_to_bbox(lat, lon, radius_m):
    dlat = radius_m / 111320
    dlon = radius_m / (111320 * math.cos(math.radians(lat)))
    return lat-dlat, lon-dlon, lat+dlat, lon+dlon
```

### 3. Bearing Computation
```python
def compute_bearing(lat1, lon1, lat2, lon2):
    # Azimuth from North, clockwise, 0-360
    # For streets: use first→last point, then % 180 (undirected)
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    return (math.degrees(math.atan2(x, y)) + 360) % 360

angle = bearing % 180  # Streets are undirected
```

### 4. Color Bins (12 × 15°)
```javascript
const BIN_COLORS = [
  "#1565c0", // 0°-15°   N    blue
  "#00838f", // 15°-30°  NNE  teal
  "#2e7d32", // 30°-45°  NE   green
  "#7cb342", // 45°-60°  ENE  light green
  "#f9a825", // 60°-75°  E    amber
  "#ef6c00", // 75°-90°  ESE  orange
  "#d84315", // 90°-105° SE   deep orange
  "#c2185b", // 105°-120°SSE  pink
  "#8e24aa", // 120°-130°S    purple
  "#5e35b1", // 135°-150°SSW  deep purple
  "#3949ab", // 150°-165°SW   indigo
  "#0277bd", // 165°-180°WSW  blue
];
```

## Rendering: Canvas 2D > Three.js for Line-Heavy Data

**Key finding:** Canvas 2D `ctx.beginPath()` + batch `stroke()` significantly outperforms Three.js `LineSegments` for this type of visualization (10K-20K line segments, all 2D).

**Why Canvas 2D wins here:**
- Batched rendering: group by (bin, tier), single `stroke()` per group
- No geometry upload overhead to GPU
- Instant text rendering for labels
- File size: 14KB HTML vs 600KB+ Three.js

**When Three.js is better:**
- Actual 3D rotation/perspective needed
- Need for WebGL post-processing (bloom, etc.)
- Interactive camera controls (orbit, zoom in 3D)

## Morphing Animation: Map → Pattern

### Pattern Layout (Squarified Treemap + Shelf-Packing)

**⚠️ CRITICAL (David correction 2026-07-06):** A naive 4×3 grid with streets centered at their centroid produces TINY DOTS — streets collapse to a single point. The correct approach is **squarified treemap + shelf-packing** where streets fill the entire cell densely.

**Step 1: Squarified Treemap** — Cell sizes proportional to total road length per bin:
```javascript
// Each bin gets a rect proportional to its total km
// Sort bins by area descending, then split recursively
function squarify(items, x, y, w, h) {
  // items: [{idx, area}] sorted desc by area
  // Recursively split: try horizontal vs vertical cut
  // Pick the split that minimizes worst aspect ratio
  // Returns: [{idx, x, y, w, h}]
}
```

**Step 2: Shelf-Packing** — Streets densely fill each cell like books on a shelf:
```javascript
// For each bin's cell:
// 1. Sort streets by length descending (longest first)
// 2. Rotate each street by bin angle: rotAngle = (bin * 15 + 7.5) * PI / 180
// 3. Compute rotated bounding box: rw = |w*cos| + |h*sin|, rh = |w*sin| + |h*cos|
// 4. Pack in rows: curX += rw+1; if curX > cellW → new row (curX=0, curY += rowH+1)
// 5. Translate street so its bbox origin sits at (curX, curY) within cell
```

**Why this works:** Each cell becomes a dense block of parallel colored lines — the "fingerprint" of that angle bin. The visual effect is a mosaic of textured rectangles, not scattered dots.

**David's preference:** Pattern cells should have subtle borders (#e0e0e0) and light backgrounds (#f5f5f5) to show the treemap structure clearly.

### Scroll-Driven Transition
```javascript
// Each road has a stagger delay based on distance from center
const delay = Math.sqrt(dx*dx + dy*dy) * 0.3;
// Interpolate per-road with cubic ease-in-out
const t = easeIO(Math.min(1, Math.max(0, globalT * 1.3 - delay)));
pts[i] = mapPos[i] + (patternPos[i] - mapPos[i]) * t;
```

### Easing Function
```javascript
function easeIO(t) { return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2; }
```

## Circular Viewport
```css
#viewport {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: min(82vw, 82vh);
  height: min(82vw, 82vh);
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 60px rgba(37,99,235,0.12);
  border: 1px solid rgba(255,255,255,0.08);
}
```

## Verified Spanish City Data (2026-07-06)

| City | Streets | Total km | Radius | Bounding Box |
|------|---------|----------|--------|-------------|
| Madrid | 11,498 | 840 km | 2000m | 40.40,-3.72 → 40.44,-3.69 |
| Barcelona | 19,832 | 1,092 km | 2000m | 41.37,2.15 → 41.40,2.19 |
| Santander | 6,944 | 376 km | 1500m | 43.45,-3.83 → 43.48,-3.79 |

**Barcelona has ~2× Madrid's streets** — denser grid (Eixample) + Gothic Quarter complexity.

## Data Format
```json
{
  "city": "Madrid",
  "center": [40.4168, -3.7038],
  "radius": 2000,
  "count": 11498,
  "total_km": 840.4,
  "streets": [
    {"a": 45.2, "l": 230.0, "t": 1, "c": [x1,y1,x2,y2,...]},
    ...
  ]
}
```
- `a`: angle in degrees (0-180)
- `l`: length in meters
- `t`: tier (0=primary, 1=secondary, 2=minor)
- `c`: flat coordinate array in local meters (centered on city)

## Design: White Background Aurora (David Preference)

**David rejected dark backgrounds for data viz:** "quiero un diseño mas ntizar aurora con fondo blanco". The original Keiryosha uses dark bg, but David's style is:
- Background: `#fafafa` (warm white)
- Text: `#1a1a2e` (near-black)
- Accents: `#2563eb` (Aurora blue) for active states
- Borders: `#e5e5e5` subtle dividers
- Font: Inter, lightweight (300-600)
- Buttons: white bg with border, active = blue fill
- Stats bar: muted text with bold numbers
- Attribution: "Hecho con ❤️ por David Antizar"

**Circular viewport was dropped in v2** — the full-width layout with treemap looks better and is easier to read. Keep it unless David asks for the circle back.

## Pitfalls

- **⚠️ CLUSTERING AT CENTROID = TINY DOTS:** If you center each street at its bounding box centroid within the treemap cell, all streets collapse to a point. Use shelf-packing instead (see Pattern Layout above). David: "los agrupa todos en el mismo punto por lo que no queda tan bonito"
- **⚠️ OSM FOOTPATH FLOOD:** 86% of `highway=*` data is footpaths/steps (type 2). Barcelona: 19,832 total → only 2,791 substantial roads. Without filtering, the treemap is dominated by tiny segments. Filter: keep types 0 (motorway/trunk) + 1 (primary/secondary/tertiary). This makes the visual denser and more meaningful.
- **⚠️ MATCH REFERENCE FIRST:** Before implementing, open the reference site and study its exact visual output. David: "la agrupacion no se parece en nada al original". The correct flow is: study → implement matching technique → THEN apply styling.
- **⚠️ Canvas2D > Three.js FOR 2D LINES:** David: "no tiene sentido" about 3D. For 10K-20K 2D segments, Canvas2D is 40x smaller (14KB vs 600KB+), faster, and simpler. Three.js only if real 3D rotation/post-processing is needed.
- **⚠️ PRESERVE INTERACTIONS ON REFACTOR:** When rewriting code, don't drop existing features. David: "ya no se cambia con la rueda" (scroll wheel was accidentally removed in v3).
- **Overpass API 403:** Official endpoint blocks server IPs. Use `maps.mail.ru` mirror.
- **`totalKm` vs `total_km`:** JSON uses snake_case (`total_km`), JS code may expect camelCase. Match keys exactly.
- **Data file size:** Barcelona JSON = 1.9MB (19K streets × coords). Acceptable for GitHub Pages but optimize for mobile.
- **Highway types:** footway ~40%, residential ~12%, service ~10%. Filter by type if you want only drivable roads.
- **Treemap cell gaps:** Use `GAP=4px` between cells with subtle borders — without gaps the pattern looks like a mess of colored lines with no structure.
- **Shelf-pack overflow:** Streets that don't fit in a cell are skipped (`continue`), not clipped. This is correct — the longest streets dominate the visual.
