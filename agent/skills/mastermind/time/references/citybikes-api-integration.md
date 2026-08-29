# CityBikes API — Integración Time v5.0

## API Overview
- **URL base:** `https://api.citybik.es/v2/`
- **Auth:** Ninguna (API abierta)
- **Formato:** JSON

## Endpoints
- `GET /networks` → lista de redes
- `GET /networks/{id}` → estaciones de una red
- `GET /citybikes/city/:cityName` → buscar redes por ciudad

## Redes España principales
Madrid=BiciMAD(642), Barcelona=Bicing(543), Valencia=Valenbisi, Sevilla=Sevici, Bilbao=Bilbaobizi+Bizkaibizi, Zaragoza=Bizi, Palma=Bicipalma, San Sebastián=Dbizi, Vitoria=MugiBIKE, Pamplona=nbici, Santander=TUeBICI, Gijón, Girona=Girocleta, Valladolid=BIKI, Burgos=BiciBur, Logroño=BiciLog, Castellón=Bicicas, Alicante=Bicielx + 52 más

## Funciones módulo (js/citybikes.js)
```javascript
const stations = await CityBikes.getStationsForCity('madrid');
const nearby = CityBikes.stationsWithinRadius(stations, lat, lng, 500);
const summary = CityBikes.summarizeNearby(nearby);
// → { count, total_bikes, total_slots, min_distance_m, avg_bikes, networks, availability_pct }
```

## Server endpoints
```
GET /citybikes/networks          → Lista de redes (cache 5min)
GET /citybikes/:networkId        → Estaciones de una red (cache 60s)
GET /citybikes/city/:cityName    → Buscar redes por ciudad
```
