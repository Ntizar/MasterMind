[proyectos] nogal9 (GLAM 1.2M€); GTFSSpain (GTFS+NAP, privado); DataHubEspana (17 pestañas, Open-Meteo/INE/USGS; lección: incrementos, commit por cambio, tab-panels hermanos, no subagentes >3000 líneas); GBFSSpain (68 GBFS, 58 ciudades); ISOTime (isócronas ORS/OSRM, boundary 72dirs); kaizen-design-system (#1A4488/#CB1823, kz-*); fuentes movilidad: MITMA S3, NAP DGT, mapas.fomento ArcGIS.
§
[usuario] David Antizar (Ntizar). Español siempre. Sistema 'MasterMind'. Atribución: 'Hecho con ❤️ por David Antizar' — Mastermind ejecutor, David autor.
§
Python sistema (chromadb): C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe. Python por defecto = venv Hermes sin pip/chromadb. ChromaDB Mastermind: ~/.mastermind/chromadb, colección mastermind-skills, qwen3-embedding (NaN, dim 4096). NaN API exige User-Agent custom en urllib (403 sin él).
§
[entorno] Repos en ~/Projects. Repo MasterMind en ~/Projects/MasterMind ('* -text'). Koldo retirado. NUNCA borrar del repo, todo castellano. Gateway startup item (Hermes_Gateway.vbs). Crons: scout 6h + weekly-digest lun 9h + doctor diario. NO citar número de skills (cambia a diario, nunca consistente).
§
[era-visor] Visor accidentes ferroviarios EU (~/Projects/era-visor, Ntizar/era-visor, README completo). Pipeline: scrape→PDF→md→json→v2 (ATP/subsistema)→v3 (cronologia/infra/causas/lecciones; limpia indice md, /no_think, 8000 tok)→geocodificar_via (PK red ADIF)→revisar (localizacion+IA vs md)→consolidar (CIAF gana, fusiona v2/v3). ES: 426 inf, 316 sobre via. Siguiente: v3 en DB, ficha detalle, fase 2 DE.
§
Aurora v6.1: --nz-gradient-aurora monocromo azul — David rechaza la mezcla azul→naranja ('gradiaente'), azul sólido para titulares. Packs v6: ntizar.three.css + three-scenes.js (icosaedro/grafo/particulas/anillos) + aurora-live.js (glass interactivo .nz-glass-liquid-live). design-system/ntizar.css de MasterMind deprecado; Ntizar-Aurora clonado en ~/Projects/Ntizar-Aurora.
§
[qwen NaN] Prompts con llaves JSON: .replace('{var}',...) nunca .format() (KeyError). /no_think + max_tokens>=8000 (razonamiento corta JSON a 4000). json.loads(strict=False).