---
name: accessibility-map
description: "Patrones para construir mapas de accesibilidad urbana (estilo Close City): travel time maps con POIs, isocronas, transporte público y bicis compartidas. Cobertura de datos, fuentes, y arquitectura de proyecto."
version: "1.0.0"
author: David Antizar
tags: [accessibility, close-city, travel-time, poi, osm-overpass, urban-planning, leaflet]
---

# Mapas de Accesibilidad Urbana — Patrón Close City

## Cuándo cargar esta skill

Cuando el usuario pida: mapas de accesibilidad, travel time maps, "hasta dónde llego en X minutos", análisis de accesibilidad urbana, copiar un proyecto tipo Close City, mapas de servicios públicos, accesibilidad peatonal.

## Concepto

Herramienta web interactiva que muestra **qué zonas de una ciudad son accesibles en X minutos** desde cualquier punto, para diferentes tipos de destinos (supermercados, farmacias, centros de salud, parques, escuelas, transporte público, bicis compartidas).

**Referencia:** [Close City](https://close.city/) — travel time map de Seattle por Henry Spatial Analysis.

## Arquitectura del proyecto

```
project/
├── index.html          # HTML único (frontend)
├── css/
│   └── style.css       # Estilos (header oscuro + sidebar blanca + CARTO light)
├── js/
│   ├── config.js       # Ciudades, modos, destinos, colores, tiempos
│   ├── map.js          # Leaflet Canvas + renderizado isocronas + POIs
│   ├── routing.js      # Motor de isocronas (ORS / OSRM / simulado)
│   ├── pois.js         # Carga de POIs desde Overpass API
│   ├── transit.js      # GTFS/NAP para TP y GBFS para bicis
│   ├── ui.js           # Sidebar, controles, leyenda, export
│   └── main.js         # Orquestador
├── server.mjs          # Proxy Nominatim + proxy ORS
└── SPEC.md             # (ver flujo abajo)
```

## Flujo de desarrollo

1. **Definir scope:** ciudades, modos (caminar/bici/coche/TP), categorías de destino
2. **Mapear fuentes de datos:** qué POIs vienen de Overpass, qué de NAP/GTFS, qué de GBFS
3. **Implementar routing:** isocronas con ORS (o fallback simulado)
4. **Implementar POIs:** Overpass API para categorías genéricas
5. **Implementar transit:** GTFS/NAP para TP, GBFS para bicis
6. **UI:** sidebar con destinos, selector de modo, leyenda de colores, export PDF
7. **Deploy:** GitHub Pages (100% estático) o NaN.builders

## Factibilidad por nivel

### 🟢 MVP (2-3 meses)
- 3-4 ciudades (Madrid, Barcelona, Valencia)
- Modos: caminar + bici (ORS free tier)
- Destinos: 6-8 categorías desde Overpass
- 100% estático, GitHub Pages

### 🟡 V2 con TP real
- 20 ciudades
- + Transporte público con horarios (GTFS/NAP)
- + Bicis compartidas (GBFS)
- Requiere servidor proxy para NAP

### 🔴 V3 Close City completo
- Accesibilidad peatonal real (aceras, rampas, paso de cebra)
- Datos de calidad de vía (CNIG o similar)
- Cobertura nacional
- Requiere datos oficiales, no solo OSM

## Fuentes de datos

### Overpass API (gratuito, sin auth)
Para POIs genéricos: supermercados, farmacias, parques, escuelas, bibliotecas, etc.

Ver `references/data-sources.md` para catálogo completo de tags OSM por categoría.

### NAP (transportes.gob.es)
Para transporte público con horarios reales en España. Ver skill `routing-isochrones` para detalles.

### GBFS
Para bicis compartidas. 68 sistemas en España. Ver skill `routing-isochrones` para catálogo.

### CNIG / Catastro
Para datos de calidad de vía, accesibilidad, infraestructura urbana. No siempre disponibles vía API pública.

## Pitfalls

1. **OSM tiene cobertura desigual en España** — Madrid y Barcelona están bien etiquetados, pueblos pequeños no. Siempre verificar con Overpass antes de comprometer una categoría.
2. **Close City usa POIs curados manualmente** — Overpass es automático pero incompleto. Para producción real, hay que complementar con datos oficiales.
3. **ORS free tier = 2000 req/día** — suficiente para demo/MVP, no para uso intensivo. Para producción, proxy server-side o key de pago.
4. **NAP solo España** — para otros países necesitas GTFS directo de cada operador.
5. **Nominatim rate limit 1 req/s** — debounce todos los inputs de búsqueda.
6. **No confundir distancia con accesibilidad real** — un mapa de isocronas muestra "hasta dónde llego", no "qué tan fácil es llegar". Barreras arquitectónicas, calidad de aceras, semáforos no se capturan en routing estándar.
7. **SPEC antes de codear** — si el usuario pide un proyecto nuevo, activar skill `project-spec-workflow`. Este skill complementa pero no reemplaza el flujo de spec.

## Referencias

- `references/data-sources.md` — Catálogo de tags OSM por categoría de POI, con queries Overpass de ejemplo
- `references/close-city-analysis.md` — Análisis técnico de Close City: stack, features, limitaciones