# Fuentes de datos para mapas de accesibilidad urbana

## Overpass API — Tags OSM por categoría de POI

### Supermercados y alimentación
```
node["shop"="supermarket"]({{bbox}});
node["shop"="convenience"]({{bbox}});
node["shop"="greengrocer"]({{bbox}});
node["shop"="marketplace"]({{bbox}});
```

### Farmacias
```
node["amenity"="pharmacy"]({{bbox}});
```

### Centros de salud
```
node["amenity"="hospital"]({{bbox}});
node["amenity"="clinic"]({{bbox}});
node["amenity"="doctors"]({{bbox}});
node["healthcare"="centre"]({{bbox}});
```

### Parques y áreas verdes
```
node["leisure"="park"]({{bbox}});
node["landuse"="grass"]({{bbox}});
node["natural"="wood"]({{bbox}});
way["leisure"="park"]({{bbox}});
```

### Escuelas
```
node["amenity"="school"]({{bbox}});
node["amenity"="kindergarten"]({{bbox}});
node["amenity"="university"]({{bbox}});
node["amenity"="college"]({{bbox}});
```

### Bibliotecas
```
node["amenity"="library"]({{bbox}});
```

### Transporte público
```
node["highway"="bus_stop"]({{bbox}});
node["railway"="tram_stop"]({{bbox}});
node["railway"="subway_entrance"]({{bbox}});
node["railway"="station"]({{bbox}});
```

### Servicios públicos
```
node["amenity"="townhall"]({{bbox}});
node["amenity"="post_office"]({{bbox}});
node["amenity"="bank"]({{bbox}});
node["amenity"="cafe"]({{bbox}});
node["amenity"="restaurant"]({{bbox}});
```

### Ciclovías e infraestructura ciclista
```
way["highway"="cycleway"]({{bbox}});
way["cycleway"="lane"]({{bbox}});
way["cycleway"="track"]({{bbox}});
```

### Query Overpass de ejemplo (Madrid, 2km radio)
```
[out:json][timeout:30];
(
  node["shop"="supermarket"](40.39,-3.73,4.44,-3.66);
  node["amenity"="pharmacy"](40.39,-3.73,4.44,-3.66);
  node["amenity"="park"](40.39,-3.73,4.44,-3.66);
  node["amenity"="school"](40.39,-3.73,4.44,-3.66);
);
out body;
>;
out skel qt;
```

## GBFS — Bicis compartidas en España

68 sistemas GBFS en España. Todos públicos, sin auth.

Ver skill `routing-isochrones` > sección GBFS para catálogo completo y URLs.

## NAP — Transporte público España

Ver skill `routing-isochrones` > sección GTFS + NAP para detalles completos.

## CNIG — Instituto Geográfico Nacional

- **PNOA:** ortofotos aéreas
- **Cartografía Digital de Referencia:** calles, edificios, usos de suelo
- **Ortoíndice:** índice de ortofotos
- **Sede CNIG:** https://www.cnig.es
- **Servicio web WMS/WFS:** disponible pero requiere registro

## Limitaciones de datos abiertos en España

1. **Calidad de vía (aceras, rampas)** — No existe en OSM de forma consistente. Solo en ciudades piloto.
2. **Accesibilidad peatonal real** — No se captura en routing estándar. Close City probablemente lo hace con datos propios.
3. **Señalización y semáforos** — Parcialmente en OSM, no fiable para análisis de accesibilidad.
4. **Datos oficiales fragmentados** — Cada comunidad autónoma tiene sus propios portales de datos abiertos. No hay un catálogo nacional unificado (excepto NAP para transporte público).