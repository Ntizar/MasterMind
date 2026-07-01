[proyecto-nogal9] Ntizar/nogal9 (privado). GLAM: 1.218.453€ (28 caps). HTML: ntizar.github.io/nogal9-web.
§
[visor-leaflet-pattern] Visor GTFS con Kaizen v4.0. Repo: Ntizar/GTFSSpain (privado).
§
[proyecto-datahub-espana] DataHubEspana (PÚBLICO). 17 pestañas, 30+ gráficos, 12+ APIs. v2.4: Polen, Inundaciones, Suelo, Pronóstico 7d. APIs: Open-Meteo (weather/marine/air-quality/flood/soil/pollen), INE, USGS. Click provincia → sync total. Repo: Ntizar/DataHubEspana. Pages: ntizar.github.io/DataHubEspana/.
§
[cuidado-datahub] David: "no planteas crecimiento sin romper". Patrón: cambios incrementales, commit por cambio, verificar JS braces tras CADA patch. DOM nesting: tab-panels HERMANOS, no hijos. Verificar balance regex. NO subagentes >3000 líneas. GitHub Pages: CDN cachea 2-5 min tras push.
§
NAP API (transportes.gob.es): 161 datasets, 662 MB GTFS. Repo GTFSSpain Ntizar/GTFSSpain (privado). Cron domingo 06:00 UTC. API key en /root/workspace/TimeIneco/.env.
§
[proyecto-gbfsspain] Ntizar/GBFSSpain (PÚBLICO). Visor 68 sistemas GBFS bicicletas España (58 ciudades, 9 plataformas). 38 sistemas v3.0. Catálogo: data/systems.json. GitHub Pages: https://ntizar.github.io/GBFSSpain/ . Workflow pages.yml (build_type: workflow). Estilo GTFSSpain pero JSON.
§
[proyecto-isotime] Ntizar/ISOTime (PÚBLICO). Isócronas reales España. IGN WMTS + ORS + OSRM (sin key). Andando/coche 5-90min. Export GeoJSON+SHP. Pages: ntizar.github.io/ISOTime/. OSRM: boundary detection 72dirs (NO convex hull).
§
[proyecto-kaizen-design-system] Ntizar/kaizen-design-system (privado). Kaizen Design System v2.0 — CSS corporativo para Equipo Kaizen Ineco. Colores OFICIALES: Azul #1A4488 (Pantone 7687 C), Rojo #CB1823 (Pantone 485 C), Azul Medio #3463AC, Azul Claro #6B96CF. CDN: cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css. Clases: kz-*. index-standalone.html para vista previa.
§
[fuentes-movilidad-gov] 3 fuentes: (1) MITMA S3 movilidad-opendata.mitma.es, CSVs+gz desde 2022. Skill: opendata-movilidad-mitma. (2) NAP DGT nap.dgt.es, CKAN DATEX2. Skill: nap-dgt. (3) Visor Hermes mapas.fomento.gob.es, ArcGIS REST. Skill: visor-hermes-fomento.