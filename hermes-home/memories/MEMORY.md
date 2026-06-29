[proyecto-nogal9] Ntizar/nogal9 (privado). GLAM: 1.218.453€ (28 caps). HTML: ntizar.github.io/nogal9-web.
§
[visor-leaflet-pattern] Visor GTFS con Kaizen v4.0. Repo: Ntizar/GTFSSpain (privado).
§
[proyecto-timeineco] Repo Ntizar/TimeIneco2 (privado). Sucesor de TimeIneco. URL actual: https://time-ntizar-ntizar.apps.nan.builders/ (Time v1). Plan maestro en AUDITORIA-Y-PLAN.md. 10 capas: mapa+geocoding, GTFS real NAP, isócrónas ORS, demografía INE, vivienda Idealista, GBFS CityBikes, costes, CO₂, teletrabajo, informes DOCX+CSV+SHP. Click = resultado completo. Stack: Vanilla JS + Leaflet + Kaizen CSS. 161 datasets NAP, 74 redes GBFS. APIs: ORS, IGN WMTS, Nominatim, CityBikes, INE, Idealista, AEAT.
§
NAP API (transportes.gob.es): 161 datasets, 662 MB GTFS. Repo GTFSSpain Ntizar/GTFSSpain (privado). Cron domingo 06:00 UTC. API key en /root/workspace/TimeIneco/.env.
§
[proyecto-gbfsspain] Ntizar/GBFSSpain (PÚBLICO). Visor 68 sistemas GBFS bicicletas España (58 ciudades, 9 plataformas). 38 sistemas v3.0. Catálogo: data/systems.json. GitHub Pages: https://ntizar.github.io/GBFSSpain/ . Workflow pages.yml (build_type: workflow). Estilo GTFSSpain pero JSON.
§
[proyecto-ciaf-visor] CIAF-visor LIMPIO (2026-06-29). 13 MB (de 330+), 57 archivos. Solo JSONs: reports/YYYY.json, memorias/YYYY.json, index.json. Frontend: frontend/index.html (inline CSS+JS). Workflow pages.yml. Repo: Ntizar/CIAF-visor. Skill: ciaf-data-pipeline.
§
[proyecto-kaizen-design-system] Ntizar/kaizen-design-system (privado). Kaizen Design System v2.0 — CSS corporativo para Equipo Kaizen Ineco. Colores OFICIALES: Azul #1A4488 (Pantone 7687 C), Rojo #CB1823 (Pantone 485 C), Azul Medio #3463AC, Azul Claro #6B96CF. CDN: cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css. Clases: kz-*. index-standalone.html para vista previa.