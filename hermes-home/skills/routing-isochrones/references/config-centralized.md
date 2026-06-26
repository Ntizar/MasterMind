# Configuración Centralizada — Patrón TimeIneco

## Cuándo usar
Cuando una app consume múltiples APIs externas (ORS, OTP, NAP, geocodificación) y necesita configuración centralizada.

## Patrón

```javascript
// js/config.js
export const CONFIG = Object.freeze({
    ORS: {
        baseUrl: 'https://api.openrouteservice.org',
        key: import.meta.env?.ORS_API_KEY || '',
        profiles: { car: 'driving-car', bike: 'cycling-regular', foot: 'foot-walking' }
    },
    OTP: {
        baseUrl: 'http://localhost:8080/otp/routers/default',
        enabled: false
    },
    NAP: {
        baseUrl: 'https://nap.transportes.gob.es/api/v2',
        apiKey: import.meta.env?.NAP_API_KEY || ''
    },
    NOMINATIM: {
        baseUrl: 'https://nominatim.openstreetmap.org',
        maxRequestsPerSecond: 1
    },
    WORK_SCHEDULE: {
        morningArrival: { start: 7.5, end: 9.5 },
        eveningDeparture: { start: 15.5, end: 17.5 }
    }
});
```

## Ventajas
- Un solo lugar para cambiar endpoints, API keys, thresholds
- `Object.freeze()` previene mutaciones accidentales
- `import.meta.env` para variables de build (Vite, esbuild, etc.)
- Fallback a `''` si no hay variable de entorno

## Pitfall
`import.meta.env` solo funciona con bundler. En vanilla JS puro, usar `window.CONFIG` o pasar config como parámetro.