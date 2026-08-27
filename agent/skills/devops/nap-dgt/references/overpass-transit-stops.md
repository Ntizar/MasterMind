# Overpass API — Paradas TP reales (alternativa a NAP DGT)

## Problem
La API NAP DGT (CKAN) es útil para datos estáticos de infraestructura, pero para obtener paradas de bus EN TIEMPO REAL en una zona concreta, Overpass API es más fiable y directo.

## Overpass API para paradas TP

### Endpoint
```
POST https://overpass-api.de/api/interpreter
Content-Type: application/x-www-form-urlencoded
```

### Query para paradas de bus en bbox
```
[out:json][timeout:15];(
  node["highway"="bus_stop"](south,west,north,east);
  node["public_transport"="stop_position"](south,west,north,east);
  node["public_transport"="platform"](south,west,north,east);
  node["railway"="tram_stop"](south,west,north,east);
);out body 50;
```

### Datos retornados por cada parada
- `tags.name` — Nombre de la parada (ej: "Metro San Bernardo")
- `tags.operator` — Operador (ej: "Empresa Municipal de Transportes de Madrid")
- `tags.network` — Red (ej: "EMT Madrid")
- `tags.ref` — Número de referencia de la parada
- `tags.bus` — Si es parada de bus ("yes")
- `tags.railway` — Si es tramvia ("tram_stop")
- `tags.wheelchair` — Accesibilidad ("yes"/"no")
- `tags.shelter` — Si tiene abrigo ("yes"/"no")
- `tags.bench` — Si tiene banco ("yes"/"no")
- `lat`, `lon` — Coordenadas exactas

### Ejemplo de fetch en JavaScript
```javascript
async function cargarParadasOSM(lat, lon, radioM = 800) {
    const delta = radioM / 111000;
    const query = `[out:json][timeout:15];(
        node["highway"="bus_stop"](${lat-delta},${lon-delta*1.3},${lat+delta},${lon+delta*1.3});
        node["public_transport"="stop_position"](${lat-delta},${lon-delta*1.3},${lat+delta},${lon+delta*1.3});
    );out body 50;`;
    
    const resp = await fetch('https://overpass-api.de/api/interpreter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'data=' + encodeURIComponent(query)
    });
    const data = await resp.json();
    return data.elements.map(el => ({
        nombre: el.tags?.name || 'Sin nombre',
        lat: el.lat, lon: el.lon,
        operador: el.tags?.operator || el.tags?.network || '',
        ref: el.tags?.ref || '',
        tipo: el.tags?.railway === 'tram_stop' ? 'Tramvia' : 'Bus',
        accesible: el.tags?.wheelchair === 'yes'
    }));
}
```

## NAP DGT — Para datos estructurados de infraestructura

La NAP DGT (https://datos.gob.es) sigue siendo útil para:
- Catálogo completo de estaciones de tren
- Líneas de autobús interurbano
- Datos de frecuencias y horarios (cuando están disponibles)
- Datos de licencias de transporte

**Pero** para paradas de bus URBANO en tiempo real → Overpass API.

## Comparación

| Fuente | Tipo | Latencia | Cobertura | Datos |
|--------|------|----------|-----------|-------|
| Overpass API | REST, público | 1-5s | Global (OSM) | Nombre, tipo, operador, accesibilidad |
| NAP DGT | CKAN, público | 2-10s | España | Infraestructura, líneas, licencias |
| EMT Madrid API | REST, público | <1s | Madrid | Frecuencias en tiempo real |
| TMB API | REST, público | <1s | Barcelona | Frecuencias en tiempo real |

## Pitfalls
- **Rate limiting:** Overpass API tiene rate limits. No hacer >1 request/segundo.
- **Bbox encoding:** El orden es `south,west,north,east` (NO `west,south,east,north`).
- **Duplicados:** Overpass retorna nodos duplicados (una parada puede tener platform + stop_position). Usar `seen` set por nombre.
- **Nombres genéricos:** Algunas paradas se llaman "Parada de autobús" sin nombre útil. Filtrar o agrupar.
