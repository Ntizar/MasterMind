# Multi-API Client-Side Integration — Referencia

Patrón para integrar múltiples APIs externas en un dashboard vanilla JS sin backend.

## Arquitectura

```
index.html (inline script)
  ├── import state.js      → Estado centralizado + IndexedDB
  ├── import api-gbfs.js   → GBFS (bici compartida) — sin key
  ├── import api-ors.js    → ORS (isócronas) — key localStorage
  ├── import api-nominatim.js → Nominatim (geocodificación) — sin key
  └── import report-enrich.js → Enriquece appState con datos reales ANTES de generar informe
```

## Patrón de módulo API con fallback

Cada módulo API sigue el mismo patrón: función principal + fallback seguro.

```javascript
// api-gbfs.js — Sin autenticación, CORS-friendly
const SISTEMAS = [
    { key: 'bicimad', nombre: 'BiciMAD', ciudad: 'Madrid', operador: 'EMT Madrid',
      lat: 40.4168, lng: -3.7038, feed: 'https://transportes.madrid/sites/default/files/edatasets/nuevobicimad.json' },
    { key: 'bicing', nombre: 'Bicing', ciudad: 'Barcelona', operador: 'Barcelona de Serveis Municipals',
      lat: 41.3874, lng: 2.1686, feed: 'https://barcelona-ambicit.herokuapp.com/api/gbfs/v2_3/BicingNacional/gbfs.json' },
];

export function detectarSistemaCercano(lat, lng) {
    let mejor = null, mejorDist = Infinity;
    for (const s of SISTEMAS) {
        const d = haversine(lat, lng, s.lat, s.lng);
        if (d < mejorDist && d < 50000) { mejorDist = d; mejor = s; }
    }
    return mejor;
}

export async function estacionesCercanas(lat, lng, radioM = 1000) {
    const sistema = detectarSistemaCercano(lat, lng);
    if (!sistema) return { estaciones: [], total: 0, sistema: null };
    
    try {
        const resp = await fetch(sistema.feed);
        const data = await resp.json();
        // Parser v2.3: data.data.stations / v3.0: data.data?.['bike_stations']
        const stations = data.data?.stations || data.data?.['bike_stations'] || [];
        const cercanas = stations
            .map(s => ({
                ...s,
                lat: s.lat || s.latitude,
                lng: s.lon || s.lng || s.longitude,
                bicis: s.num_bikes_available || s.bikes_available || 0,
                docks: s.num_docks_available || s.docks_available || 0,
                capacidad: (s.num_bikes_available || 0) + (s.num_docks_available || 0),
                distancia: haversine(lat, lng, s.lat || s.latitude, s.lon || s.longitude || s.lng)
            }))
            .filter(s => s.distancia <= radioM)
            .sort((a, b) => a.distancia - b.distancia);
        
        return { estaciones: cercanas, total: cercanas.length, sistema: sistema.nombre };
    } catch (e) {
        console.warn('GBFS error:', e.message);
        return { estaciones: [], total: 0, sistema: sistema.nombre };
    }
}
```

## Patrón ORS con fallback simulado

```javascript
// api-ors.js — Requiere API key (localStorage) + fallback
export function getOrsKey() { return localStorage.getItem('pmst_ors_api_key'); }
export function setOrsKey(key) { localStorage.setItem('pmst_ors_api_key', key); }

export async function calcularIsocrona(lng, lat, modo = 'coche', minutos = 15) {
    const key = getOrsKey();
    const profile = { coche: 'driving-car', bici: 'cycling-regular', pie: 'foot-walking' }[modo] || 'driving-car';
    
    if (key) {
        try {
            const resp = await fetch(`https://api.openrouteservice.org/v2/isochrones/${profile}`, {
                method: 'POST',
                headers: { 'Authorization': key, 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    locations: [[lng, lat]],
                    range: [minutos * 60],
                    range_type: 'time'
                })
            });
            if (resp.ok) {
                const data = await resp.json();
                const feature = data.features?.[0];
                const area = feature ? turf.area(feature) / 1e6 : 0;
                return { geojson: data, areaKm2: area, success: true, real: true };
            }
        } catch (e) { console.warn('ORS real failed:', e.message); }
    }
    
    // Fallback: polígono simulado con jitter
    return fallbackIsocrona(lng, lat, modo, minutos);
}

function fallbackIsocrona(lng, lat, modo, minutos) {
    const radios = { coche: 0.22, bici: 0.08, pie: 0.03 }; // ~radio base por modo
    const base = radios[modo] * (minutos / 15);
    const coords = [];
    for (let i = 0; i < 48; i++) {
        const angle = (i / 48) * 2 * Math.PI;
        const jitter = base * (0.7 + Math.random() * 0.6); // 70-130% del radio
        coords.push([lng + jitter * Math.cos(angle), lat + jitter * Math.sin(angle) * 0.7]);
    }
    coords.push(coords[0]);
    return {
        geojson: { type: 'FeatureCollection', features: [{
            type: 'Feature', geometry: { type: 'Polygon', coordinates: [coords] },
            properties: { mode: modo, value: minutos }
        }]},
        areaKm2: Math.PI * base * base * 111 * 111 * 0.7,
        success: true, real: false
    };
}
```

## Patrón Nominatim + Overpass POIs

```javascript
// api-nominatim.js — Rate limit 1 req/s, sin key
let lastRequest = 0;
async function rateLimitedFetch(url) {
    const now = Date.now();
    if (now - lastRequest < 1100) await new Promise(r => setTimeout(r, 1100 - (now - lastRequest)));
    lastRequest = Date.now();
    return fetch(url, { headers: { 'User-Agent': 'PLANDEMOVILIDAD/2.0' } });
}

export async function geocodificar(direccion) {
    const resp = await rateLimitedFetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}&countrycodes=es&limit=5`
    );
    return (await resp.json()).map(r => ({
        nombre: r.display_name, lat: parseFloat(r.lat), lng: parseFloat(r.lon)
    }));
}

export async function geocodificarInversa(lat, lng) {
    const resp = await rateLimitedFetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
    );
    const data = await resp.json();
    return {
        nombre: data.display_name, lat, lng,
        barrio: data.address?.suburb || data.address?.neighbourhood,
        ciudad: data.address?.city || data.address?.town,
        provincia: data.address?.state, cp: data.address?.postcode
    };
}

export async function buscarPOIs(lat, lng, tipo = 'all', radioM = 1000) {
    const queries = {
        salud: 'amenity=hospital OR amenity=clinic OR amenity=pharmacy',
        educacion: 'amenity=school OR amenity=university',
        parking: 'amenity=parking',
        tp: 'highway=bus_stop OR railway=tram_stop OR public_transport=platform'
    };
    const q = tipo === 'all' ? Object.values(queries).join(' OR ') : queries[tipo] || tipo;
    const r = radioM / 111000; // metros a grados approx
    const resp = await rateLimitedFetch(
        `https://overpass-api.de/api/interpreter?data=[out:json];(${q}(around:${radioM},${lat},${lng}););out body 30;`
    );
    const data = await resp.json();
    return (data.elements || []).map(e => ({
        id: e.id, tipo: e.tags?.amenity || e.tags?.highway,
        nombre: e.tags?.name || e.tags?.['name:es'] || 'Sin nombre',
        lat: e.lat, lng: e.lon
    }));
}
```

## Patrón de enriquecimiento pre-reporte

```javascript
// report-enrich.js — Carga datos reales ANTES de generar el informe
export async function enrichAppWithAPIs(app) {
    const lat = parseFloat(app.centro?.latitud);
    const lng = parseFloat(app.centro?.longitud);
    if (!lat || !lng) return app;
    
    // 1. GBFS
    const gbfs = window.pmstApp?.gbfs;
    if (gbfs) {
        const result = await gbfs.estacionesCercanas(lat, lng, 1000);
        app.gbfs = { sistema: result.sistema, estaciones: result.estaciones, total: result.total };
    }
    
    // 2. Nominatim — Info centro + POIs
    const nom = window.pmstApp?.nominatim;
    if (nom) {
        app.centroInfo = await nom.geocodificarInversa(lat, lng);
        app.pois = (await nom.buscarPOIs(lat, lng, 'all', 1000)).slice(0, 20);
    }
    
    // 3. ORS — Isochronas multi-modo
    const ors = window.pmstApp?.ors;
    if (ors) {
        app.isocronas = [];
        for (const modo of ['coche', 'bici', 'pie']) {
            for (const min of [10, 15, 30]) {
                const r = await ors.calcularIsocrona(lng, lat, modo, min);
                app.isocronas.push({ modo, minutos: min, areaKm2: r.areaKm2, real: r.real });
                if (r.real) await new Promise(r => setTimeout(r, 400)); // stagger ORS
            }
        }
    }
    
    return app;
}
```

## Integra en el export del informe

```javascript
// En index.html inline script
window.pmstApp.exportPDF = async () => {
    try {
        await enrichAppWithAPIs(window.pmstApp.appState);
    } catch(e) { console.warn('API enrich error:', e.message); }
    return exportPDF();
};
```

## Pitfalls

1. **GBFS v2.3 vs v3.0**: v2.3 anida en `data.data.stations`, v3.0 en `data.data?.['bike_stations']`. Parser ambos.
2. **ORS rate limit**: 2000 req/día gratis. Stagger 400ms entre requests. Fallback simulado sin key.
3. **Nominatim rate limit**: 1 req/s estricto. Rate limiter de 1100ms. User-Agent obligatorio.
4. **Overpass API**: queries complejas con `(around:radio,lat,lng)` pueden ser lentas. Limitar a 30 resultados.
5. **window.pmstApp timing**: los módulos API asignan funciones a `window.pmstApp` pero el inline script sobreescribe. Usar `Object.assign(window.pmstApp, {...})` o dynamic imports.
6. **Lazy init del mapa**: Leaflet + GBFS + paradas = ~500KB. No cargar hasta que el usuario clique en "Mapa".
