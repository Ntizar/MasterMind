---
name: osm-infrastructure-mapping
version: "1.0.0"
description: "Motor OSINT para mapear infraestructura del mundo real desde datos OpenStreetMap. Inspirado en ni5arga/sightline (⭐496). Descubre, mapea y visualiza infraestructura crítica."
tags: [osm, osint, infrastructure, mapping, overpass, opendata]
---

# Mapeo de Infraestructura con OSM

## Resumen

Patrón OSINT para descubrir y mapear infraestructura del mundo real (torres, antenas, subestaciones, tuberías, vías) usando datos de OpenStreetMap via Overpass API.

## Cuándo usar

- Mapear infraestructura de telecomunicaciones (antenas, torres)
- Visualizar red eléctrica (subestaciones, líneas de alta tensión)
- Análisis de infraestructura crítica de una zona
- Dashboard de infraestructura con datos abiertos

## Patrón de uso

```javascript
// Query Overpass API para infraestructura específica
async function fetchInfrastructure(bbox, type) {
  const query = `
    [out:json][timeout:25];
    (
      node["power"="tower"](${bbox});
      node["power"="substation"](${bbox});
      way["power"="line"](${bbox});
      node["man_made"="communications_tower"](${bbox});
      node["telecom"="data_center"](${bbox});
    );
    out geom;
  `;
  
  const response = await fetch('https://overpass-api.de/api/interpreter', {
    method: 'POST',
    body: 'data=' + encodeURIComponent(query)
  });
  return response.json();
}

// bbox: south,west,north,east
const infra = await fetchInfrastructure('40.3,-3.8,40.5,-3.6', 'power');

// Renderizar en Leaflet
infra.elements.forEach(el => {
  if (el.type === 'node') {
    L.circleMarker([el.lat, el.lon], {
      radius: 5,
      fillColor: getInfraColor(el.tags),
      fillOpacity: 0.8
    }).addTo(map).bindPopup(formatPopup(el.tags));
  } else if (el.type === 'way' && el.geometry) {
    const latlngs = el.geometry.map(g => [g.lat, g.lon]);
    L.polyline(latlngs, { color: '#f97316', weight: 2 }).addTo(map);
  }
});

function getInfraColor(tags) {
  if (tags.power === 'substation') return '#dc2626';
  if (tags.power === 'tower') return '#f97316';
  if (tags.man_made === 'communications_tower') return '#2563eb';
  return '#6b7280';
}
```

## Tags OSM de infraestructura

| Categoría | Tags | Ejemplo |
|-----------|------|---------|
| Eléctrica | `power=tower`, `power=substation`, `power=line` | Torres de alta tensión |
| Telecom | `man_made=communications_tower`, `telecom=*` | Antenas, data centers |
| Agua | `man_made=pipeline`, `pipeline=water` | Tuberías, depósitos |
| Gas | `man_made=pipeline`, `pipeline=gas` | Gasoductos |
| Ferroviaria | `railway=rail`, `railway=station` | Vías, estaciones |

## Pitfalls

- **Overpass rate limits:** Máximo 2 queries/minute. Cachear resultados.
- **Bbox grande:** Queries muy grandes pueden timeout. Dividir en tiles.
- **Datos incompletos:** OSM no tiene toda la infraestructura. Verificar con fuentes oficiales.
- **Sensibilidad:** Infraestructura crítica puede tener datos limitados en OSM por seguridad.

## Referencias

- sightline: https://github.com/ni5arga/sightline
- Overpass API: https://overpass-api.de/
- OSM Tags: https://wiki.openstreetmap.org/wiki/Map_Features

---

**Hecho con ❤️ por David Antizar**
