# PDF Generation with Embedded Maps

## Problem
HTML reports with interactive Leaflet maps can't be converted to PDF via WeasyPrint/wkhtmltopdf — these tools don't execute JavaScript, so maps render as empty boxes.

## Solution: Static Map Images → Embed → PDF

### Step 1: Generate static map images with `staticmap`
```python
from staticmap import StaticMap, CircleMarker, Line, Polygon

tmap = StaticMap(800, 500, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
tmap.add_marker(CircleMarker((lon, lat), '#2563eb', 12))
tmap.add_line(Line([(lon1, lat1), (lon2, lat2)], '#dc262680', 1))
tmap.add_polygon(Polygon(coords, '#3b82f630', '#3b82f6', 2))
image = tmap.render(zoom=14)
image.save('map.png')
```

### Step 2: Compress to JPEG
```python
from PIL import Image
img = Image.open('map.png').convert('RGB')
img.save('map.jpg', 'JPEG', quality=85, optimize=True)
# PNG: ~700KB → JPEG: ~150KB
```

### Step 3: Embed as base64 in HTML
```python
import base64
with open('map.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
img_tag = f'<img src="data:image/jpeg;base64,{b64}" style="width:100%" />'
```

### Step 4: Replace map containers in HTML
```python
import re
html = re.sub(
    r'<div[^>]*id="map-entorno"[^>]*>.*?</div>\s*(?:<div class="map-legend"[^>]*>.*?</div>)?',
    f'<div style="text-align:center"><img src="data:image/jpeg;base64,{b64}" style="width:100%" /></div>',
    html, flags=re.DOTALL
)
```

### Step 5: Generate PDF with WeasyPrint
```python
from weasyprint import HTML
HTML(string=html).write_pdf('output.pdf')
```

## Installation
```bash
pip install staticmap Pillow weasyprint PyPDF2
```

## Pitfalls
- `staticmap` needs internet to fetch OSM tiles — first render is slow (~5s per map)
- WeasyPrint doesn't support CSS Grid well — use flexbox or inline styles
- Remove Leaflet CSS/JS from HTML before PDF generation (not needed, adds bloat)
- Base64 images bloat HTML size (~33% overhead) — use JPEG quality 80-85
- For multi-page PDFs, WeasyPrint handles page breaks via CSS `@page` and `page-break-after`

## Alternative: Self-contained HTML with inline Leaflet
When the HTML will be opened in a browser (not PDF), use inline `<script>` instead of ES modules:
```html
<script>
const MAP_CENTER = [40.4458, -3.6888];
function initMaps() {
    if (typeof L === 'undefined') return;
    const map = L.map('map-entorno').setView(MAP_CENTER, 14);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
}
document.addEventListener('DOMContentLoaded', () => setTimeout(initMaps, 800));
</script>
```
This avoids ES module import failures when opening the file directly (file:// protocol).

## Realistic Isochrones Pattern
Instead of circles, generate irregular polygons that account for urban barriers:
- 48-point polygon with pseudo-random variation
- 8 directional axes with road-network factors (1.0-1.4)
- Barrier zones that reduce radius (rivers: 0.6, railways: 0.75)
- Transit influence that extends isochrone along metro lines (+25%)
- Area calculation via Shoelace formula

See `js/isochrones-realistas.js` in PLANDEMOVILIDAD for complete implementation.
