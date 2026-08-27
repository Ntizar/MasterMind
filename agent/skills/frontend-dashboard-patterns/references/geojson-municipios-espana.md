# GeoJSON de Municipios Españoles — Fuentes y Workarounds

## Fuentes intentadas (2026-06-18) — TODAS FALLARON

| Fuente | URL | Resultado |
|--------|-----|-----------|
| codeforspain/city-geojson | raw.githubusercontent.com/codeforspain/city-geojson/master/municipios.geojson | 404 |
| codeforspain (otra ruta) | .../municipalities/28_madrid.geojson | 404 |
| codeforspain (api.github.com) | api.github.com/repos/codeforspain/city-geojson/contents/ | Not Found |
| opendata-pmm/municipios | raw.githubusercontent.com/opendata-pmm/municipios/master/municipios.geojson | 404 |
| semmler23/municipios-geodata | raw.githubusercontent.com/semmler23/municipios-geodata/main/municipios.geojson | 404 |
| Fonsloper/municipios-espana | raw.githubusercontent.com/Fonsloper/municipios-espana/main/municipios.geojson | 404 |
| NeuroForge1/Municipios | raw.githubusercontent.com/NeuroForge1/.../Municipios.geojson | 404 |
| CodeandoMexico | raw.githubusercontent.com/CodeandoMexico/municipios-geojson/main/28.geojson | 404 |
| AguaDB | raw.githubusercontent.com/AguaDB/municipios/main/28_madrid.json | 404 |
| npm geojson-municipios | npm install geojson-municipios | 404 |
| Datos Abiertos CM WFS | datos.comunidad.madrid/geoserver/wfs?... | HTML response (not JSON) |
| IGN INSPIRE WFS | www.ign.es/wfs-inspire-muni?... | No output |
| datos.gob.es | datos.gob.es/apidata/catalog/dataset/... | JSON metadata, no GeoJSON |
| GADM level 2 | geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_2.json | 52 features (provinces, no municipalities) |
| GADM level 3 | geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_ESP_3.json | 369 features but NAME_1='ComunidaddeMadrid' only has 6 (all 'n.a.') |
| Overpass API | overpass-api.de/api/interpreter?data=... | Timeout / no output |

## Workaround: Hexágonos desde centroides

Cuando no hay GeoJSON descargable, generar polígonos hexagonales simplificados:

```python
import json, math

def generate_hex(lat, lng, size_km=3):
    km_per_deg_lat = 111.32
    km_per_deg_lng = 111.32 * math.cos(math.radians(lat))
    r_lat = size_km / km_per_deg_lat
    r_lng = size_km / km_per_deg_lng
    angles = [0, 60, 120, 180, 240, 300]
    coords = []
    for a in angles:
        rad = math.radians(a)
        coords.append([lng + r_lng * math.cos(rad), lat + r_lat * math.sin(rad)])
    coords.append(coords[0])
    return coords

# Generar para cada municipio
features = []
for c in centroids:
    coords = generate_hex(c['lat'], c['lng'])
    features.append({
        'type': 'Feature',
        'properties': {'CODMUN': c['cod'], 'NOMBRE': c['name']},
        'geometry': {'type': 'Polygon', 'coordinates': [coords]}
    })
geojson = {'type': 'FeatureCollection', 'features': features}
```

## Fuentes que SÍ funcionan (pero con limitaciones)

1. **GADM** (geodata.ucdavis.edu) — funciona para provinces (level 2), pero level 3 no tiene municipios individuales para Madrid
2. **Centroides manuales** — siempre funciona si tienes códigos INE + coords

## Recomendación

Para municipios españoles, las mejores opciones son:
1. **Descargar de datos abiertos de la comunidad autónoma** (WFS con CQL_FILTER por provincia)
2. **Usar la API del IGN** (wfs-inspire) — puede requerir autenticación o headers específicos
3. **Hexágonos desde centroides** — workaround rápido y funcional para choropleths
4. **Voronoi desde centroides** — mejor que hexágonos pero requiere library D3-delaunay
