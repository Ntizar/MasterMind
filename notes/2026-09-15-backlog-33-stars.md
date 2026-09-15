# Backlog de stars — 33 repos en un batch (2026-09-15)

## Contexto

El PC/gateway estuvo apagado del **2026-09-09 17:42 al 2026-09-15 16:30**. Al arrancar, el scheduler lanzó los 13 jobs vencidos a la vez → límite de NaN (5 peticiones paralelas) saturado → **9 jobs fallaron con HTTP 429** (los 4 de script pasaron). El scout de stars acumuló **33 repos nuevos** sin procesar.

**Fix estructural aplicado:** `hermes config set cron.max_parallel_jobs 1` (antes ilimitado). Elimina la avalancha de catch-up, los 429 y de paso los `TERMINAL_CWD write lock` entre jobs con workdir compartido.

## Método

1. Cross-check `GET /users/Ntizar/starred` (380 vivas) contra `data/stars-registry.json` → 33 nuevas.
2. Clasificación por stars/lenguaje + **dedup semántico** contra los 467 skills (ChromaDB).
3. **3 subagentes en paralelo**: cada uno leyó el README real (`gh api .../readme`) de 11 repos + el SKILL.md del skill candidato y devolvió veredicto JSON.
4. Orquestador (Mastermind) aplicó veredictos: 11 skills nuevos, 11 secciones comparativas en skills existentes, 5 referencias, 6 skips.

## Reparto

**Skills nuevos (11):**

| Skill | Categoría | Repo |
|---|---|---|
| mirofish-swarm-simulation | ai | 666ghj/MiroFish |
| minimind-tiny-llm-training | mlops | jingyaogong/minimind |
| fleetbase-logistics-os | mobility | fleetbase/fleetbase |
| inertial-navigation-inslib | geospatial | jnz/INSLIB |
| eubucco-building-stock | geospatial | ai4up/eubucco |
| geospatial-ai-agents | geospatial | microsoft/Planetary-Explorer |
| geospatial-mcp-power-pack | geospatial | aws-samples/sample-geospatial-kiro-power-pack |
| spain-public-procurement | government-data | BquantFinance/licitaciones-espana |
| spanish-electoral-microdata | government-data | JaimeObregon/infoelectoral |
| sam3d-cpp-body-objects | computer-vision | localai-org/sam3d.cpp |
| synthetic-tabular-data-evaluation | data-science | Vicomtech/STDG-evaluation-metrics |

**Upgrades (11)** — sección comparativa/patrón añadida al skill existente:

- `autonomous-ai-agents/hermes-agent` ← deepseek-ai/deepseek-harness (harness "todo es un plugin" sobre Cordis)
- `autonomous-ai-agents/codex` ← DietrichGebert/ponytail (escalera de minimalismo + benchmark con diff real)
- `educational-html-pipeline` ← THU-MAIC/OpenMAIC (curso multiagente → pptx/HTML/MP4)
- `media/voicebox` ← debpalash/VoiceStudio (16 TTS + 11 ASR, API OpenAI-compatible local)
- `geospatial/airsim-simulation` ← carla-simulator/carla (UE5, umbrales de hardware reales)
- `routing-isochrones` ← conveyal/r5 (accesibilidad de oportunidades vs isocronas)
- `data-pipeline/google-maps-scrapper` ← Madi-S/Lead-Generation (py-lead-generation, Google + Yelp)
- `herramientas/browser-local-tools` ← IngenieroSeed/SafeDocument (privacidad impuesta por CSP)
- `government-data-pipelines` ← ctt-gob-es/datos.gob.es (extensiones CKAN + DCAT-AP-ES)
- `data-science/rail-lidar-qa-mvp` ← Vicomtech/SOSDaR24 (dataset de referencia, OpenLABEL + PCD)
- `design-systems-ecosystem` ← acrosa/GridKit (verificación de retícula/ritmo vertical)

**Referencias (5):** Foadsf/vintage-latex (LaTeX editorial), Vicomtech/ArchABM (ABM config-driven, estancado), Vicomtech/dardcollect (provenance FAIR JSON-LD), iamtekson/rasuwa-flood (geoportal config-driven MapLibre), GeiserX/awesome-spain (lista).

**Skips (6):** JuliaLang/julia, maxence-charriere/go-app, conveyal/gtfs-lib (cubierto por node-gtfs), JaimeObregon/jaime.gomezobregon.com, ginopalazzo/spain-open-data, 686f6c61/mattermost-plugin-read-receipts.

## Lecciones

- **El dedup semántico sólo orienta; el README decide.** Scores como `sam3d.cpp → trellis2-img-to-3d 0.747` parecían cobertura y no lo eran (imagen→3D ≠ recuperación de cuerpo/objetos desde vídeo).
- **Los veredictos automáticos se pasan de generosos**: de 15 CREATE propuestos, 4 se degradaron a referencia (repos de 3-17 stars o colecciones de ejemplos). El orquestador filtra; el criterio es "¿lo usaría David en 3 meses?".
- **Un job con workdir + otro job en paralelo = `TERMINAL_CWD write lock`.** Serializar el cron (max_parallel_jobs=1) mata dos bugs con un cambio.
