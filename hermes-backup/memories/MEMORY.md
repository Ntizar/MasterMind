[regla-critical] NUNCA crear repos sin verificar primero si existen. SIEMPRE intentar git clone primero, si falla → crear. Nombres sensibles a una letra.
§
[proyecto-nogal9] Ntizar/nogal9 (privado). GLAM: 1.218.453€ (28 caps). HTML: ntizar.github.io/nogal9-web.
§
[visor-leaflet-pattern] Visor GTFS con mapa Leaflet interactivo: sidebar 380px + mapa CARTO light, geocodificación Nominatim con dropdown, click en mapa → buscar paradas, círculo radio visual punteado, colores modo transporte (bus=#2563eb, metro=#dc2626, ferro=#16a34a), KPIs grid 3 cols, carga ZIPs con barra progreso, JSZip inline, panel horarios desplegable (clic en parada → rutas + horarios + filtros), auto-carga desde /api/zips vía server.py, sin botones rápidos de ciudades. Visor: GTFSSpain/visor/index.html (136 KB).
§
[proyecto-timeineco] Repo Ntizar/TimeIneco (privado). Original, completo. server.mjs 941 líneas. JS v0.9. Último commit 1f48d81 (22/06): fixes CSV bug, docx vendor lib, ORS timeout 25s, .env.example. Deploy NaN: https://timeineco-ntizar-ntizar.apps.nan.builders/ . NAP_API_KEY debe configurarse en NaN Dashboard > Env. TimeIneco2 borrado (solo local).
§
NAP API (transportes.gob.es): 161 datasets, 662 MB GTFS. 2M viajes, 24K rutas, 191K paradas. Solo GTFS-ZIP descargables como ZIP (otros: GTFS-RT, NetEx, SIRI). Delta semanal ~100-500MB. Visor con auto-carga: server.py + /api/zips + panel horarios. Repo GTFSSpain en /root/workspace/GTFSSpain/ con script descargar-nap.py (full+delta), visor/index.html (136 KB, Leaflet + JSZip inline + panel horarios + auto-carga), cron semanal domingo 06:00 UTC. API key en /root/workspace/TimeIneco/.env (NAP_API_KEY). Repo GitHub privado: Ntizar/GTFSSpain.
§
[proyecto-gbfsspain] Ntizar/GBFSSpain (privado). Visor 68 sistemas GBFS bicicletas España (58 ciudades, 9 plataformas). 38 sistemas v3.0. Catálogo: data/systems.json. Estilo GTFSSpain pero JSON.