---
name: osint-live-globe
description: Use al construir globo 3D con feeds OSINT en vivo.
version: 1.0.0
tags: [cesium, osint, geospatial, real-time, satellite-tracking, 3d-globe]
---

# God's Eye View — globo 3D con feeds OSINT en vivo

Simulador de satélite espía en el navegador con **datos reales públicos**: vuelos, barcos, satélites, terremotos y cámaras públicas sobre un globo fotorealista Cesium. Repo: https://github.com/bilawalsidhu/gods-eye-view (14k+ ⭐, JavaScript + Vite + cesium-vite-plugin).

## Stack del patrón
- **Cesium** con `vite-plugin-cesium` (globo fotorealista + terreno).
- **satellite.js**: propagación orbital SGP4 desde TLE públicos (Celestrak) para posiciones de satélites en tiempo real.
- **@mapbox/vector-tile**: decodificación de tiles MVT/PBF para capas densas (tráfico, AIS).
- **WebSocket**: streaming de posiciones vivas (ADS-B/aisstream) al globo.
- **egm96-universal**: corrección de altitud geoidal para cálculos reales de visibilidad.

## Patrones reutilizables
1. **Una capa = un feed público**: aislar cada fuente (ADS-B, AIS, terremotos USGS, TLE) en su propio módulo con su propio polling/streaming; el globo solo consume entidades.
2. **Marcar lo modelado**: cuando no hay feed en vivo, renderizar vista modelada claramente etiquetada (honestidad de datos como feature).
3. **Degradación elegante**: capas con API key opcional se ocultan, no rompen el arranque.
4. **Voz + agente**: control manos libres del visor vía agente en tiempo real (opcional sobre el núcleo).

## Fuentes públicas usadas (gratis)
TLE de Celestrak (satélites), ADS-B (vuelos), AIS (barcos), USGS (sismos), cámaras públicas.

## Pitfalls
- Cesium necesita token Ion para assets fotorealistas: sin él, degradar a imagery open (OSM/Esri World).
- Los feeds WebSocket tienen límites gratuitos: cachear y batchear actualizaciones de entidades.
- Actualizar miles de entidades por frame mata el render: actualizar por lote temporal (dirty-flag), no por mensaje.

## Verificación
- Comprobar que ≥2 capas en vivo muestran posiciones coherentes (ej.: un vuelo real moviéndose).
- Latencia feed→globo < unos segundos en capas streaming.

## Comparativa de alternativas

- **[NVlabs/Eagle (LocateAnything)](https://github.com/NVlabs/Eagle)** — fine-tuning de VLM con prompts visuales para geolocalizar una imagen (geolocalización cartográfica), un complemento de geolocalización para OSINT/geo-forensics sobre el globo.
- **[Blackleets/aegis](https://github.com/Blackleets/aegis)** — centro de mando OSINT: recon toolkit (DNS, WHOIS, SSL, CVE), panel de analista IA y dossiers de fusión; enfoque de "puesto de mando" frente al globo en vivo.
- **[ShinMegamiBoson/OpenPlanter](https://github.com/ShinMegamiBoson/OpenPlanter)** — resolución de entidades entre datasets heterogéneos (registros mercantiles, contratos, lobbying) mediante delegación recursiva de subagentes; útil para enlazar entidades sobre el mapa.
