# Overpass API — Transporte Público + Validación de Datos

## Consulta Overpass para paradas de TP (verificado 2026-07-14)

```javascript
const query = `
  [out:json][timeout:25];
  (
    node["highway"="bus_stop"](bbox);
    node["public_transport"="stop_position"](bbox);
    node["public_transport"="platform"](bbox);
    node["railway"="station"](bbox);
    node["railway"="tram_stop"](bbox);
  );
  out center;
`;
```

### Endpoints Overpass confiables

| Endpoint | Confiabilidad | Notas |
|----------|--------------|-------|
| `https://overpass-api.de/api/interpreter` | ⚠️ Rate-limited | Principal pero puede bloquear |
| `https://maps.mail.ru/osm/tools/overpass/api/interpreter` | ✅ Mirror ruso | Más estable para batch |
| `https://overpass.kumi.systems/api/interpreter` | ✅ Alternativo | Mirror académico |

### Tipos de transporte en OSM

| Tag OSM | Tipo | Ejemplo |
|---------|------|---------|
| `highway=bus_stop` | Parada de autobús | Bus EMT |
| `public_transport=stop_position` | Posición de parada | Metro, bus |
| `public_transport=platform` | Andén/plataforma | Cercanías |
| `railway=station` | Estación de tren | Metro, Cercanías |
| `railway=tram_stop` | Parada de tranvía | Tranvía Madrid |
| `amenity=bus_station` | Estación de autobuses | Intercity |

### Normalización de tipos

```javascript
function normalizarTipo(stop) {
    const t = stop.tags;
    if (t.railway === 'station') return t.network?.includes('Metro') ? 'Metro' : 'Cercanías';
    if (t.railway === 'tram_stop') return 'Tranvía';
    if (t.highway === 'bus_stop') return 'Autobús urbano';
    if (t.public_transport) return 'Transporte público';
    return 'Desconocido';
}
```

### GBFS — Estaciones de bici compartida

```javascript
const GBFS_URLS = {
    'madrid': 'https://gbfs.link/es/bicimad/stations.json',
    'valencia': 'https://gbfs.link/es/valenbisi/stations.json',
    'barcelona': 'https://gbfs.link/es/bicing/stations.json',
};

// ⚠️ Feeds GBFS pueden caer. SIEMPRE try/catch + "N/D"
async function fetchGBFS(city, lat, lon, radiusM = 1200) {
    try {
        const resp = await fetch(GBFS_URLS[city]);
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        const stations = data.data?.stations || data.stations || [];
        return stations.filter(s => {
            const d = haversine(lat, lon, s.lat, s.lon);
            return d <= radiusM;
        });
    } catch (e) {
        console.warn(`GBFS feed no disponible: ${e.message}`);
        return [];  // ← Devolver array vacío, NO inventar datos
    }
}
```

### Validación de datos en informe

```javascript
class DataValidator {
    constructor() { this.registros = []; }
    
    add(source, field, status, value = null) {
        this.registros.push({ source, field, status, value });
    }
    
    addVerified(source, field, value) {
        this.add(source, field, 'verified', value);
    }
    
    addUnavailable(source, field, reason) {
        this.add(source, field, 'unavailable', null);
    }
    
    toHTML() {
        const verified = this.registros.filter(r => r.status === 'verified');
        const unavailable = this.registros.filter(r => r.status === 'unavailable');
        
        return `
            <ul style="font-size:13px;margin:8px 0">
                ${verified.map(r => `<li>✅ <strong>${r.field}</strong>: ${r.value} (fuente: ${r.source})</li>`).join('')}
                ${unavailable.map(r => `<li>⚠️ <strong>${r.field}</strong>: N/D — ${r.reason || 'Dato no disponible'}</li>`).join('')}
            </ul>
        `;
    }
}
```

## Pitfalls

- **⚠️ GBFS feeds poco fiables:** BiciMAD, Valenbisi, Bicing pueden caer temporalmente. SIEMPRE try/catch + array vacío.
- **⚠️ Overpass API rate limiting:** >50 requests/min puede bloquear. Usar mirror `maps.mail.ru` para batch.
- **⚠️ Nominatim bloquea IP:** Tras ~50 requests, la IP queda bloqueada (429). Usar DB local como primaria.
- **⚠️ Datos inventados en informes:** SIEMPRE marcar "N/D" cuando el dato no es verificado. "N/D" es mejor que un dato falso.
