# Open-Meteo — APIs gratuitas sin autenticación

Todas las APIs de Open-Meteo son gratuitas y no requieren API key.

## Endpoints principales

### Weather Forecast
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code,precipitation,pressure_msl,cloud_cover,visibility,wind_gusts_10m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=Europe/Madrid&forecast_days=7
```

### Soil Temperature & Moisture
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm&past_days=1
```

### Air Quality (CAMS European)
```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,us_aqi,pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide,dust,uv_index&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide&past_days=1&forecast_days=0
```

### Pollen (incluido en Air Quality)
```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&hourly=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&past_days=1
```

### Marine (oleaje)
```
https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,swell_wave_height&hourly=wave_height&forecast_days=1
```

### Flood Risk
```
https://flood-api.open-meteo.com/v1/flood?latitude={lat}&longitude={lon}&daily=river_discharge&past_days=7&forecast_days=7
```

## Datos de ejemplo (Madrid, 2026-06-30)

| Endpoint | Valor |
|----------|-------|
| Temperatura | 31.6°C |
| Presión MSL | 1020.7 hPa |
| Presión superficie | 947.7 hPa |
| Nubosidad | 0% |
| Visibilidad | 45120 m |
| Ráfagas | 18.4 km/h |
| UV Index | 8.2 |
| AQI Europeo | 38 |
| PM2.5 | 8.8 µg/m³ |
| Polen gramen | 6.6 gr/m³ |
| Caudal río | 1.7 m³/s |
| Temp suelo 6cm | 29.0°C |
| Humedad suelo 0-1cm | 0.084 m³/m³ |

## Notas
- **Marine solo funciona en coordenadas costeras/marítimas**
- **Flood devuelve datos de ríos cercanos** — para ciudades sin río grande, los valores son bajos (1-2 m³/s)
- **Pollen**: en verano, gramen y olivo son los más altos en España
- **Soil moisture**: valores típicos 0.05-0.30 m³/m³
