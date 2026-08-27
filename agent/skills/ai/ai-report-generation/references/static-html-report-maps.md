# Static HTML Report with Embedded Leaflet Maps

## Problem
Generate a standalone HTML report with interactive Leaflet maps that works when opened directly (file:// protocol), without requiring a web server. Also generate PDF versions with static map images.

## Solution 1: Inline JS for Interactive HTML

### HTML Structure
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PMST — Company Name</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>/* report CSS */</style>
</head>
<body>
    <!-- Report content -->
    <div id="map-entorno" style="height:400px;border-radius:12px;border:2px solid #e5e7eb"></div>
    
    <!-- ALL map code INLINE, not type="module" -->
    <script>
    // Data embedded as constants
    const MAP_CENTER = [40.4458, -3.6888];
    const PARADAS_TP = [...];
    const GBFS_STATIONS = [...];
    
    // Map initialization (inline, no imports)
    function initMaps() {
        if (typeof L === 'undefined') return;
        
        const map = L.map('map-entorno', { center: MAP_CENTER, zoom: 14 });
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        // Add markers
        PARADAS_TP.forEach(p => {
            L.marker([p.lat, p.lon]).bindPopup(p.nombre).addTo(map);
        });
    }
    
    document.addEventListener('DOMContentLoaded', () => setTimeout(initMaps, 800));
    </script>
</body>
</html>
```

## Solution 2: Static Maps for PDF (Python `staticmap`)

When WeasyPrint generates the PDF, Leaflet maps render as empty boxes because WeasyPrint doesn't execute JS. Solution: generate static map images with Python.

### Pipeline
```
1. report.js → HTML with Leaflet maps
2. gen_static_maps.py → PNG/JPG images via staticmap library
3. gen_pdf_static.py → replace map divs with <img> tags
4. WeasyPrint → PDF with embedded map images
```

### gen_static_maps.py
```python
import staticmap

def generar_mapa(center, paradas, gbfs, isocronas, output_path):
    m = staticmap.StaticMap(800, 600, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    
    # Paradas TP (rojo)
    for p in paradas:
        m.add_marker(staticmap.CircleMarker((p['lon'], p['lat']), '#dc2626', 8))
    
    # BiciMAD (verde/amarillo/rojo por disponibilidad)
    for s in gbfs:
        color = '#16a34a' if s['bikes'] > 5 else '#eab308' if s['bikes'] > 0 else '#dc2626'
        m.add_marker(staticmap.CircleMarker((s['lon'], s['lat']), color, 10))
    
    # Isochronas (polígonos semitransparentes)
    for iso in isocronas:
        m.add_polygon(iso['coords'], fill=iso['color'], outline=iso['color'], width=2)
    
    image = m.render()
    image.save(output_path)
```

### gen_pdf_static.py
```python
import base64, re
from weasyprint import HTML

def reemplazar_mapas_y_generar_pdf(html_path, mapas_dir, output_pdf):
    with open(html_path, 'r') as f:
        html = f.read()
    
    for map_id, img_file in [('map-entorno', 'entorno.jpg'), ('map-tp', 'tp.jpg'), ('map-isocronas', 'isocronas.jpg')]:
        with open(f'{mapas_dir}/{img_file}', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        html = re.sub(
            f'<div id="{map_id}".*?</div>',
            f'<img src="data:image/jpeg;base64,{b64}" style="width:100%;border-radius:12px">',
            html, flags=re.DOTALL
        )
    
    HTML(string=html).write_pdf(output_pdf)
```

### Install
```bash
pip install --break-system-packages weasyprint staticmap Pillow PyPDF2
```

### Resolution
- 800×600 → ~130KB JPG (good for A4)
- 1200×900 → ~300KB JPG (high quality)

## Key Patterns

### 1. Data embedding
Embed all data as JavaScript constants in the HTML. No external JSON files (file:// can't fetch local files).

### 2. Leaflet CDN
Use CDN links for Leaflet CSS/JS. These work in file:// context.

### 3. Inline initialization
All map code must be in a regular `<script>` tag, NOT `<script type="module">`. ES modules are blocked by file:// security.

### 4. DOMContentLoaded + setTimeout
Leaflet needs the DOM to be ready AND the containers to have dimensions. Use `setTimeout(initMaps, 800)` after DOMContentLoaded.

### 5. Overpass API for real data
Fetch real transport stops from Overpass API (works in file:// because it's a cross-origin POST, not a local file read).

## Tested in PLANDEMOVILIDAD

- 3 maps (entorno, isócronas, TP+GBFS)
- 7 paradas TP reales from Overpass
- 8 estaciones BiciMAD from GBFS
- 9 isochrones simulated with urban barriers
- Opens directly with double-click, no server needed
- PDF: 71 pages, 1.2MB with static map images

## Limitations

- CDN links require internet connection
- Overpass API requires internet
- No offline capability (would need to inline all data + tile images)
- PDF generation via WeasyPrint won't render the maps (no JS execution) → use staticmap
