# APIs Gratuitas Sin Auth para DataHub España

## Open-Meteo (todas funcionan, sin CORS, sin key)

### Weather API
```
https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code,wind_direction_10m,sunrise,sunset&daily=sunrise,sunset&timezone=Europe/Madrid
```

### Marine API
```
https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&current=wave_height,wave_direction,swell_wave_height&hourly=wave_height&forecast_days=1
```
⚠️ Solo funciona para coordenadas costeras/marítimas

### Air Quality API (CAMS European)
```
https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,us_aqi,pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide,dust,uv_index&hourly=pm10,pm2_5,nitrogen_dioxide,ozone,carbon_monoxide,sulphur_dioxide&past_days=1&forecast_days=0
```
- `european_aqi`: Índice europeo (0-20 Excelente, 20-40 Bueno, 40-60 Regular, 60-80 Malo, 80-100 Muy malo, >100 Extremadamente malo)
- Datos verificados Madrid: AQI=38, PM2.5=8.8, O3=96, NO2=10.4, CO=126, UV=7.3

## INE (Instituto Nacional de Estadística)

### Tabla 9681: Población por CCAA y sexo
```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/9681?tip=AM&nult=1
```
- 6120 entries
- Campos: Nombre, Sexo, CCAA, Valor (población)
- Sexo: "Hombres", "Mujeres", "Total"
- CCAA: código INE 01-19

### Tabla 2852: Población por provincia y sexo
```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2852?tip=AM&nult=1
```
- 159 entries
- Mismo formato que 9681 pero por provincia

### Otras tablas INE potencialmente útiles
| Tabla | Contenido | Registros esperados |
|-------|-----------|---------------------|
| 39960 | Turismo: pernoctaciones y viajeros | ~500 |
| 4247 | Educación: matriculados por nivel | ~200 |
| 31304 | Empleo: afiliados SS por provincia | ~500 |
| 2852a | Nacimientos y defunciones | ~300 |
| 9684 | Censo de población por municipio | ~8000 |

## USGS Earthquake API
```
https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-01-01&minmagnitude=3&minlatitude=35&maxlatitude=44&minlongitude=-10&maxlongitude=5
```
- Terremotos M3.0+ en España (lat 35-44, lon -10 a 5)
- GeoJSON con propiedades: mag, place, time, url, tsunami, felt, significance

## ESIOS/REE (parcialmente gratuito)

### Funciona sin auth
| Endpoint | Datos |
|----------|-------|
| `api.esios.ree.es/indicators/1001` | PVPC spot €/MWh |
| `api.esios.ree.es/indicators/1293` | Demanda total MW |

### Requiere auth (fallback estático)
| Endpoint | Fallback |
|----------|----------|
| `api.esios.ree.es/indicators/1294` | Renovables 45.2% |

## APIs que necesitan auth (futuras)
| API | Auth | Coste | Datos |
|-----|------|-------|-------|
| AEMET | Key gratuita (registro) | Gratis | Predicción detallada, warnings, rachas |
| Copernicus CAMS | Registro Copernicus | Gratis | Calidad aire histórica, emisiones GEOS-5 |
| Sentinel-5P | Via Copernicus | Gratis | NO2, SO2, CH4, O3, CO troposféricos por satélite |
| Copernicus CDS | Registro | Gratis | Reanalysis ERA5, climatología |
