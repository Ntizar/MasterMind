# Open-Meteo API — Trampas y Patterns

## Parámetros current vs daily

**CRÍTICO:** Algunos parámetros SOLO existen en `daily`, NO en `current`.

### Parámetros current (disponibles)
- `temperature_2m` — temperatura actual
- `relative_humidity_2m` — humedad relativa
- `wind_speed_10m` — velocidad del viento
- `wind_direction_10m` — dirección del viento
- `wind_gusts_10m` — ráfagas
- `weather_code` — código meteorológico WMO
- `precipitation` — precipitación actual
- `cloud_cover` — nubosidad
- `surface_pressure` — presión superficial
- `visibility` — visibilidad

### Parámetros daily (NO disponibles en current)
- `sunrise` — amanecer
- `sunset` — atardecer
- `temperature_2m_max` — temperatura máxima
- `temperature_2m_min` — temperatura mínima
- `precipitation_sum` — precipitación diaria
- `precipitation_probability_max` — prob. máx. lluvia

### Fórmula correcta para clima + amanecer/atardecer
```
?current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code&daily=sunrise,sunset&timezone=Europe/Madrid
```

### Fórmula INCORRECTA (causa error silencioso)
```
?current=temperature_2m,...,weather_code,sunrise,sunset&daily=sunrise,sunset
```
**Error:** La API devuelve 400 pero el fetch no lanza excepción si no se verifica `res.ok`.

## Air Quality API
```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,us_aqi,pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide,dust,uv_index&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide&past_days=1&forecast_days=0
```

## Marine API
```
https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,wave_period,swell_wave_height&hourly=wave_height,wave_direction&forecast_days=1&timezone=auto
```

## Flood API
```
https://flood-api.open-meteo.com/v1/flood?latitude={lat}&longitude={lon}&daily=river_discharge&past_days=7&forecast_days=7
```

## Pollen (via Air Quality API)
```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen
```

## Soil (via Forecast API)
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm
```

## WMO Weather Codes
```javascript
const WMO_CODES = {
    0: 'Despejado', 1: 'Principalmente despejado', 2: 'Parcialmente nublado', 3: 'Nublado',
    45: 'Niebla', 48: 'Niebla con escarcha',
    51: 'Lluvia ligera', 53: 'Lluvia moderada', 55: 'Lluvia intensa',
    61: 'Lluvia', 63: 'Lluvia moderada', 65: 'Lluvia fuerte',
    71: 'Nieve ligera', 73: 'Nieve moderada', 75: 'Nieve fuerte',
    80: 'Chubascos ligeros', 81: 'Chubascos moderados', 82: 'Chubascos fuertes',
    85: 'Chubascos de nieve', 86: 'Chubascos fuertes de nieve',
    95: 'Tormenta', 96: 'Tormenta con granizo', 99: 'Tormenta fuerte con granizo'
};
```
