# Overpass API — Paradas de Transporte Público en OpenStreetMap

## Endpoint

```
POST https://overpass-api.de/api/interpreter
Content-Type: application/x-www-form-urlencoded

data=[out:json][timeout:15];(QUERY);out body 50;
```

## Queries útiles

### Paradas de bus en radio
```
[out:json][timeout:15];(
  node["highway"="bus_stop"](S,W,N,E);
  node["public_transport"="stop_position"](S,W,N,E);
  node["public_transport"="platform"](S,W,N,E);
);out body 50;
```

### Metro + Cercanías en radio
```
[out:json][timeout:15];(
  node["railway"="station"](S,W,N,E);
  node["railway"="subway_entrance"](S,W,N,E);
);out body 50;
```

### Tranvía en radio
```
[out:json][timeout:15];(
  node["railway"="tram_stop"](S,W,N,E);
  node["public_transport"="tram_stop"](S,W,N,E);
);out body 50;
```

## Tags disponibles por parada

| Tag | Descripción | Ejemplo |
|-----|-------------|---------|
| `name` | Nombre | "Paseo de la Habana" |
| `operator` | Operador | "EMT Madrid" |
| `network` | Red | "Empresa Municipal de Transportes de Madrid" |
| `network:short` | Abreviatura | "EMT Madrid" |
| `ref` | Código parada | "1223" |
| `highway` | Tipo vía | "bus_stop" |
| `public_transport` | Tipo TP | "platform", "stop_position" |
| `railway` | Tipo ferroviario | "tram_stop", "station" |
| `wheelchair` | Accesibilidad | "yes", "no", "limited" |
| `shelter` | Abrigo | "yes", "no" |
| `bench` | Banco | "yes", "no" |
| `lit` | Iluminación | "yes", "no" |
| `bin` | Papelera | "yes", "no" |
| `tactile_paving` | Pavimento táctil | "yes", "no" |

## Ejemplo real verificado

**Paseo de la Habana 16, Madrid (40.4458, -3.6888), radio 800m:**

Resultado: 12 paradas, incluyendo:
- "Paseo de la Habana" — EMT Madrid, ref 14/27/40/147, 120m
- "Pio XII" — Metro L9, 280m
- "Cardenal Cisneros" — EMT Madrid, ref 14/27, 350m
- "Concha Espina" — EMT Madrid, ref 14/40/147/CE1, 420m
- "Nuevos Ministerios" — Metro+Cercanías (6/8/10/C-1/C-3/C-4/C-7/C-10), 950m

## Pitfalls

1. **Deduplicación** — Una parada puede tener múltiples nodos (platform + stop_position). Usar `Set` por nombre
2. **Bounding box** — `delta = radioM / 111000` (1 grado ≈ 111km). Para lng, multiplicar por `1.3` a latitudes medias
3. **Rate limit** — No documentado oficialmente, pero peticiones cada <1s pueden ser rechazadas
4. **Timeout** — Queries grandes (>10000 nodos) pueden tardar >15s. Reducir radio o filtrar
5. **CORS** — Overpass API permite CORS directo. No necesita proxy

## Comparación con NAP/GTFS

| | Overpass (OSM) | NAP (GTFS) |
|---|---|---|
| Cobertura | Global | Solo España |
| Datos | Ubicación + nombre | Horarios + rutas |
| Actualización | Continua (community) | Diaria/semanal |
| Autenticación | No | API key |
| Formato | JSON | ZIP (CSVs) |
| Uso ideal | "¿Dónde están las paradas?" | "¿A qué hora llega el bus?" |

**Recomendación:** Usar Overpass para ubicación de paradas + NAP/GTFS para horarios. Complementarios.
