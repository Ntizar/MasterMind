---
name: solar-shadow-computation
description: Calculo de sombras solares con Web Workers + Comlink, cache por terraza/dia/franja, footprints OSM, estimacion de alturas de edificios. Derivado de solmad.
version: "1.0.0"
tags: [solar, sombras, web-workers, gis, solmad]
---

# Solar Shadow Computation - Patron de Calculo de Sombras Solares

## Descripcion

Patron para calcular si una ubicacion tiene sol directo en un momento dado, cruzando datos de terrazas/ubicaciones con footprints de edificios de OpenStreetMap y posicion solar via SunCalc.

## Origen

Derivado del repositorio [solmad](https://github.com/Ntizar/solmad) (Madrid Solea) — buscador de terrazas con sol en Madrid.

## Algoritmo

1. Cargar las ubicaciones (terrazas, puntos de interes)
2. Descargar footprints de edificios desde Overpass/OpenStreetMap por zona visible
3. Estimar alturas con `height`, `building:levels * 3.2m` o fallback de `10m`
4. Indexar segmentos de fachadas en un grid dentro de un Web Worker
5. Para cada ubicacion trazar un rayo hacia el sol y comprobar si algun edificio lo tapa
6. Repetir en pasos de tiempo para estimar minutos restantes y ritmo solar del dia
7. Cachear resultados por ubicacion, dia del ano y franja de 15 minutos

## Stack Tecnologico

- **Vite + React + TypeScript**
- **Leaflet** para el mapa
- **Leaflet.markercluster** para 6.200+ terrazas sin lag
- **SunCalc** para posicion solar
- **Web Workers + Comlink** para calculos sin bloquear UI
- **Zustand** para estado global
- **Tailwind** para interfaz

## Cache Solar

```javascript
// Cache por terraza, dia del ano y franja de 15 minutos
const cacheKey = `${terrazzaId}_${dayOfYear}_${quarterHour}`;
// localStorage + data/sun-cache.json via API
```

## Datos y Fuentes

- Terrazas: censo oficial del Ayuntamiento de Madrid (CC BY 4.0)
- Edificios: OpenStreetMap contributors (ODbL)
- Calculo solar: SunCalc
- Proyeccion: EPSG:25830 -> WGS84

## Limitaciones

- No considera arbolado real, toldos, sombrillas
- Overpass puede devolver menos edificios si la red/API esta lenta
- Por eso se trabaja por zona y se cachea

## Implementacion en Hermes

Para replicar este patron:

1. Usar Web Workers para calculos pesados de sombras
2. Implementar cache por ubicacion + dia + franja horaria
3. Usar Overpass API para footprints por zona (no todo el mapa de golpe)
4. Estimar alturas con multiples fuentes: height, levels*3.2, fallback 10m
5. Priorizar rendimiento percibido: primero calculo del punto seleccionado, luego cercanos

## Pitfalls

- **Overpass API rate limit** — trabajar por zona visible, no descargar todo
- **Web Worker** — los calculos deben ir en hilo secundario para no bloquear UI
- **Cache invalidation** — invalidar cache cuando cambian datos de edificios
- **Precision** — comunicar claramente que las sombras son aproximadas
