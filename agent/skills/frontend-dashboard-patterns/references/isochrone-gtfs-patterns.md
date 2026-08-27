# Router de Isocronas y GTFS — Referencia

Patrones para calcular isocronas y horarios de transporte público.

## OpenRouteService (ORS)

### Isocronas

```javascript
const resp = await fetch(`${ORS.baseUrl}/v2/isochrones/${lng},${lat}`, {
    method: 'POST',
    headers: {
        'Authorization': apiKey,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        locations: [[lng, lat]],
        profile: 'driving-car',  // 'foot-walking', 'cycling-regular'
        range: [3600],  // 1 hora en segundos
        range_type: 'time',
        units: 'm'
    })
});
```

### Perfiles disponibles

| Profile | Uso | Limitaciones gratis |
|---------|-----|---------------------|
| `driving-car` | Coche | 2.500 req/día |
| `foot-walking` | Andando | 2.500 req/día |
| `cycling-regular` | Bicicleta | 2.500 req/día |
| `public-transport` | Transporte público | Requiere OTP |

## GTFS — Parser básico

```javascript
function parseGTFSFile(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split('\t');
    return lines.slice(1).map(line => {
        const values = line.split('\t');
        const record = {};
        headers.forEach((h, i) => record[h] = values[i] || '');
        return record;
    });
}
```

### Archivos GTFS necesarios

- **stops.txt** — Paradas/estaciones
- **routes.txt** — Líneas (bus, metro, tren)
- **trips.txt** — Viajes individuales
- **stop_times.txt** — Horarios de paso
- **calendar.txt** / **calendar_dates.txt** — Fechas de servicio

## Filtrado por horarios laborales

```javascript
// Horario laboral: 7:30 - 9:30
const morningArrivals = stopTimes.filter(st => {
    const time = parseGTFSHour(st.arrival_time); // "07:45:00" → 7.75
    return time >= 7.5 && time <= 9.5;
});

// Horario laboral: 16:30 - 18:30
const eveningArrivals = stopTimes.filter(st => {
    const time = parseGTFSHour(st.arrival_time);
    return time >= 16.5 && time <= 18.5;
});

function parseGTFSHour(timeStr) {
    const [h, m, s] = timeStr.split(':').map(Number);
    return h + m / 60 + s / 3600;
}
```

## Filtrado por proximidad

```javascript
function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// Paradas a menos de 400m
const nearbyStops = stops.filter(s => haversine(lat, lon, s.lat, s.lon) < 400);
```

## Casos reales: TimeIneco

- **ors.js** — Implementa `resolve()` y `getIsochrones()` para ORS
- **gtfs.js** — Parser GTFS + motor de horarios laborales
- **plugins.js** — Sistema de registro y orquestación
- **main.js** — Orquestador principal
