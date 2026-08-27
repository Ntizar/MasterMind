# Static Map PDF Pipeline

## Problem
WeasyPrint cannot execute JavaScript, so Leaflet maps in HTML reports render as empty boxes in the generated PDF.

## Solution: Python `staticmap` library

Generate static map images from OpenStreetMap tiles, then embed them as `<img>` tags before PDF generation.

### Dependencies
```bash
pip install --break-system-packages weasyprint staticmap Pillow PyPDF2
```

### Step 1: Generate static maps (gen_static_maps.py)

```python
import staticmap
import json

def generar_mapa_paradas(center, paradas, output_path):
    """Mapa de paradas de transporte público"""
    m = staticmap.StaticMap(800, 600, 
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    
    # Paradas TP (rojo)
    for p in paradas:
        marker = staticmap.CircleMarker((p['lon'], p['lat']), '#dc2626', 8)
        m.add_marker(marker)
    
    # Centro (azul grande)
    m.add_marker(staticmap.CircleMarker((center[1], center[0]), '#2563eb', 14))
    m.add_text((center[1], center[0]), '🏢 Centro', 24, '#1e40af', 'bold')
    
    image = m.render()
    image.save(output_path)
    return output_path

def generar_mapa_gbfs(center, gbfs_stations, output_path):
    """Mapa de estaciones BiciMAD con colores por disponibilidad"""
    m = staticmap.StaticMap(800, 600,
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    
    for s in gbfs_stations:
        bikes = s.get('bikesAvailable', 0)
        color = '#16a34a' if bikes > 5 else '#eab308' if bikes > 0 else '#dc2626'
        marker = staticmap.CircleMarker((s['lon'], s['lat']), color, 10)
        m.add_marker(marker)
    
    m.add_marker(staticmap.CircleMarker((center[1], center[0]), '#2563eb', 14))
    image = m.render()
    image.save(output_path)

def generar_mapa_isocronas(center, isocronas, output_path):
    """Mapa de isócronas con polígonos irregulares"""
    m = staticmap.StaticMap(800, 600,
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')
    
    colors = {
        ('coche', 10): '#3b82f6', ('coche', 15): '#2563eb', ('coche', 30): '#1d4ed8',
        ('bici', 10): '#22c55e', ('bici', 15): '#16a34a', ('bici', 30): '#15803d',
        ('pie', 10): '#eab308', ('pie', 15): '#ca8a04', ('pie', 30): '#a16207',
    }
    
    for iso in isocronas:
        key = (iso['modo'], iso['minutos'])
        color = colors.get(key, '#6b7280')
        coords = iso['coords']
        # staticmap expects [(lon, lat), ...]
        coords_lonlat = [(c[1], c[0]) for c in coords]
        m.add_polygon(coords_lonlat, fill=color, outline=color, width=2)
    
    m.add_marker(staticmap.CircleMarker((center[1], center[0]), '#2563eb', 14))
    image = m.render()
    image.save(output_path)
```

### Step 2: Replace maps in HTML and generate PDF (gen_pdf_static.py)

```python
import base64, re
from weasyprint import HTML

def reemplazar_mapas(html_content, mapas_dir):
    """Replace Leaflet map divs with static <img> tags"""
    replacements = [
        ('map-entorno', 'entorno.jpg'),
        ('map-tp', 'tp.jpg'),
        ('map-isocronas', 'isocronas.jpg'),
    ]
    
    for map_id, img_file in replacements:
        with open(f'{mapas_dir}/{img_file}', 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        
        # Replace div with img
        pattern = f'<div id="{map_id}"[^>]*>.*?</div>'
        replacement = f'<img src="data:image/jpeg;base64,{b64}" style="width:100%;border-radius:12px;border:2px solid #e5e7eb">'
        html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    return html_content

def generar_pdf(html_path, mapas_dir, output_pdf):
    with open(html_path, 'r') as f:
        html = f.read()
    
    html = reemplazar_mapas(html, mapas_dir)
    
    # Remove Leaflet CSS/JS (not needed for static images)
    html = re.sub(r'<link[^>]*leaflet[^>]*>', '', html)
    html = re.sub(r'<script[^>]*leaflet[^>]*></script>', '', html)
    
    HTML(string=html).write_pdf(output_pdf)
    print(f'PDF generado: {output_pdf}')
```

### Resolution Guide

| Size | File Size | Quality | Use Case |
|------|-----------|---------|----------|
| 600×450 | ~80KB | OK | Quick preview |
| 800×600 | ~130KB | Good | A4 report (standard) |
| 1200×900 | ~300KB | High | A4 report (high quality) |
| 1600×1200 | ~500KB | Excellent | A3 or poster |

### Pitfalls

1. **Tile server rate limiting** — OSM tile servers limit requests. Add delays between map generations or use a local tile cache.
2. **Map bounds** — `staticmap` auto-fits to markers. If markers are clustered, the map may be too zoomed in. Add explicit bounds if needed.
3. **Polygon winding order** — `staticmap` expects coordinates in `(lon, lat)` order, not `(lat, lon)`. This is the opposite of Leaflet.
4. **Base64 size** — Embedding images as base64 increases HTML size by ~33%. For a 130KB JPEG, the base64 string is ~173KB. Total HTML may reach 200-250KB.
5. **WeasyPrint CSS** — WeasyPrint supports most CSS3 but not flexbox gap, CSS variables, or some grid features. Test the PDF layout separately.
