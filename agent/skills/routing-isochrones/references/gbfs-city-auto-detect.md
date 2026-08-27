# GBFS City Auto-Detection by Proximity

**Session:** PLANDEMOVILIDAD Fase 3B (2026-07-14)

## Concept

Automatically detect which GBFS system to use based on the user's coordinates, without requiring them to select a city manually.

## Pattern

```javascript
const SISTEMAS_GBFS = {
    madrid:     { nombre: 'BiciMAD',       discovery: 'https://madrid.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',     ciudad: { lat: 40.4168, lng: -3.7038 } },
    barcelona:  { nombre: 'Bicing',        discovery: 'https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',  ciudad: { lat: 41.3874, lng: 2.1686 } },
    valencia:   { nombre: 'Valenbisi',     discovery: 'https://valencia.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',   ciudad: { lat: 39.4699, lng: -0.3763 } },
    sevilla:    { nombre: 'Sevici',        discovery: 'https://sevilla.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',    ciudad: { lat: 37.3891, lng: -5.9845 } },
    zaragoza:   { nombre: 'Bizi',          discovery: 'https://zaragoza.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',   ciudad: { lat: 41.6488, lng: -0.8891 } },
    bilbao:     { nombre: 'Bilbao Bizi',   discovery: 'https://bilbao.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',     ciudad: { lat: 43.2630, lng: -2.9350 } },
    coruna:     { nombre: 'Bicicoruña',    discovery: 'https://coruna.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json',     ciudad: { lat: 43.3623, lng: -8.4115 } },
    valladolid: { nombre: 'Valladolid',    discovery: 'https://valladolid.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json', ciudad: { lat: 41.6523, lng: -4.7245 } }
};

function detectarSistemaCercano(lat, lng, radioKm = 50) {
    let mejor = null, mejorDist = Infinity;
    for (const [key, sistema] of Object.entries(SISTEMAS_GBFS)) {
        const dist = haversine(lat, lng, sistema.ciudad.lat, sistema.ciudad.lng) / 1000;
        if (dist < radioKm && dist < mejorDist) {
            mejorDist = dist;
            mejor = { key, ...sistema, distancia: dist };
        }
    }
    return mejor; // null if no system within radioKm
}
```

## Usage

```javascript
// Auto-detect from office location
const sistema = detectarSistemaCercano(40.4168, -3.7038); // → { key: 'madrid', nombre: 'BiciMAD', ... }

// With custom radius
const sistema = detectarSistemaCercano(39.4699, -0.3763, 100); // → Valencia/Valenbisi

// Use in station search
const estaciones = await estacionesCercanas(lat, lng, 1000); // auto-detects system
```

## Notes

- All 8 systems use the same GBFS v3.0 URL pattern: `https://{city}.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- These are operated by Getaround (formerly nextbike/Cyclocity) and use the same infrastructure
- Discovery URL returns feeds for: station_information, station_status, system_information, gbfs_versions, vehicle_types
- No API key needed — all feeds are public
- Rate limit: poll station_status max every 30 seconds
