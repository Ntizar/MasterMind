# Patrón API Marina + Weather para Dashboards Geolocalizados

## Open-Meteo Marine API

### Endpoint
```
https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,wave_period,wind_wave_height,swell_wave_height,swell_wave_direction&timezone=Europe/Madrid
```

### Parámetros útiles
- `wave_height` — Altura de olas (m)
- `wave_direction` — Dirección de olas (grados, 0=N, 90=E, 180=S, 270=W)
- `wave_period` — Período de olas (segundos)
- `wind_wave_height` — Altura de olas de viento (m)
- `swell_wave_height` — Altura de oleaje (m)
- `swell_wave_direction` — Dirección de oleaje (grados)

### Función JavaScript para dirección
```javascript
function getDirectionName(degrees) {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'];
    const index = Math.round(degrees / 45) % 8;
    return directions[index];
}
```

### Coordenadas de puertos españoles
```javascript
const portCoordinates = {
    'ALGECIRAS': [36.13, -5.45],
    'VALENCIA': [39.45, -0.32],
    'BARCELONA': [41.34, 2.18],
    'BILBAO': [43.26, -2.93],
    'LAS PALMAS': [28.12, -15.40],
    'TENERIFE': [28.04, -16.24],
    'CARTAGENA': [37.59, -0.98],
    'HUELVA': [37.26, -6.95],
    'A CORUÑA': [43.37, -8.39],
    'GIJÓN': [43.54, -5.66]
};
```

### Errores comunes
- **CORS:** Marine API permite CORS desde Pages (verificado)
- **Coordenadas marítimas:** Para puertos, usar coordenadas exactas del puerto, no del centro de la provincia
- **Fallback:** Si Marine API falla, mostrar "N/D" y ocultar panel de oleaje
- **Rate limits:** Sin límites documentados, pero hacer cache local si se abusa

## Open-Meteo Weather API

### Endpoint
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code,wind_direction_10m&daily=sunrise,sunset&timezone=Europe/Madrid
```

### Códigos WMO (weather_code)
| Código | Condición |
|--------|-----------|
| 0 | Despejado |
| 1-3 | Parcialmente nublado |
| 45-48 | Niebla |
| 51-57 | Lluvia ligera |
| 61-65 | Lluvia moderada |
| 71-77 | Nieve |
| 80-82 | Chubascos |
| 95-99 | Tormentas |

## Patrón de API en cadena (Weather + Marine)

```javascript
async function fetchLocationData(lat, lon) {
    const [weather, marine] = await Promise.all([
        fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code&timezone=Europe/Madrid`),
        fetch(`https://marine-api.open-meteo.com/v1/marine?latitude=${lat}&longitude=${lon}&current=wave_height,wave_direction,wave_period&timezone=Europe/Madrid`)
    ]);
    
    const weatherData = await weather.json();
    const marineData = await marine.json();
    
    return {
        temp: weatherData.current.temperature_2m,
        wind: weatherData.current.wind_speed_10m,
        humidity: weatherData.current.relative_humidity_2m,
        waves: marineData.current?.wave_height || null,
        waveDirection: marineData.current?.wave_direction || null,
        wavePeriod: marineData.current?.wave_period || null
    };
}
```
