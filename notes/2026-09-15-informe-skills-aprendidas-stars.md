# Informe — Skills aprendidas del pipeline Stars Explorer

**Fecha:** 2026-09-15 · **Ámbito:** backlog acumulado 2026-09-09 → 2026-09-15 (33 repos)
**Fuente:** `data/stars-registry.json` + `notes/2026-09-15-backlog-33-stars.md`

---

## 1. Contexto: por qué hubo backlog

El PC/gateway estuvo **apagado del 09-09 17:42 al 15-09 16:30** (6 días). Al arrancar, el scheduler lanzó los **13 jobs vencidos en el mismo tick** → se superó el límite de NaN (5 peticiones LLM en paralelo) → **9 jobs fallaron con `HTTP 429 max_parallel_requests`**. El scout de stars acumuló **33 repos nuevos** sin procesar.

**Fix estructural aplicado:**

```bash
hermes config set cron.max_parallel_jobs 1
```

Elimina la avalancha de catch-up, los 429 y, de paso, el `TERMINAL_CWD write lock` entre jobs con workdir compartido. Detalle en `mastermind-system-ops/references/cron-catchup-429.md`.

---

## 2. Método del batch

1. **Cross-check** `GET /users/Ntizar/starred` (380 stars vivas) contra el registry → 33 repos nuevas.
2. **Clasificación** por stars/lenguaje + **dedup semántico** contra los ~467 skills (ChromaDB, `consultar-skills.py`).
3. **3 subagentes en paralelo** (límite NaN ≤4 por oleada): cada uno leyó el README real (`gh api repos/{o}/{r}/readme`) de 11 repos + el SKILL.md candidato y devolvió veredicto JSON.
4. **Orquestador** aplicó veredictos: 12 skills nuevos/reclasificados, 11 secciones comparativas, 4 referencias, 6 skips.
5. **Auditoría de calidad** posterior: 22 textos verificados contra fuente primaria → 14 OK, 8 corregidos.

---

## 3. Skills nuevas (12)

| Skill | Dominio | Repo fuente | Qué aporta |
|---|---|---|---|
| `mirofish-swarm-simulation` | ai | 666ghj/MiroFish | Simulación de sociedades de agentes con memoria: de una semilla construye GraphRAG → personas con memoria → informe de predicción |
| `minimind-tiny-llm-training` | mlops | jingyaogong/minimind | Ciclo completo de entrenamiento (pretrain→SFT→LoRA→DPO→PPO/GRPO→RL agéntico) de un LLM de 64M en una sola GPU doméstica |
| `fleetbase-logistics-os` | mobility | fleetbase/fleetbase | Back-office logístico self-hosted: pedidos, flota, zonas de servicio, tracking en vivo y routing OSRM |
| `inertial-navigation-inslib` | geospatial | jnz/INSLIB | Librería C11 sin dependencias ni heap: fusión IMU+GNSS+barómetro con Kalman de raíz cuadrada; QA nivel DO-178. Para GNSS degradado (túneles, ferrocarril) |
| `eubucco-building-stock` | geospatial | ai4up/eubucco | 322 M de huellas de edificios UE (altura + plantas) armonizando 55 datasets; clave para sombras solares fuera de Madrid |
| `geospatial-ai-agents` | geospatial | microsoft/Planetary-Explorer | Patrón multi-agente geoespacial: pregunta en natural → agente STAC → raster → agente de visión. Datos satelitales gratis (Planetary Computer, NASA VEDA) |
| `geospatial-mcp-power-pack` | geospatial | aws-samples/sample-geospatial-kiro-power-pack | 21 paquetes: hub + `geo-common` + 19 servidores MCP (56 herramientas), con router de orquestación discover→process→analyze |
| `spain-public-procurement` | government-data | BquantFinance/licitaciones-espana | 44,4 M de registros de licitación pública española (2000-2026) + cruce reproducible con TED; incluye `references/umbrales-sara.md` |
| `spanish-electoral-microdata` | government-data | JaimeObregon/infoelectoral | Espejo + decodificador de los microdatos del Ministerio del Interior (formatos propietarios) a nivel de mesa/sección |
| `sam3d-cpp-body-objects` | computer-vision | localai-org/sam3d.cpp | Port C++23/GGML de SAM 3D Body: malla y pose humana (MHR) en CPU/Vulkan, sin Python ni CUDA |
| `synthetic-tabular-data-evaluation` | data-science | Vicomtech/STDG-evaluation-metrics | Metodología de 3 ejes (resemblance / utility / privacy) para saber si un dataset sintético sirve sin filtrar datos reales |
| `software-open-source-espana` | reference | GeiserX/awesome-spain | Catálogo CC0 con 37 categorías de software open source español. **Promovido de referencia a skill** en la auditoría: evita escribir conectores que ya existen |

---

## 4. Upgrades a skills existentes (11 secciones comparativas)

| Skill existente | Repo añadido | Aporte |
|---|---|---|
| `autonomous-ai-agents/hermes-agent` | deepseek-ai/deepseek-harness | Harness "todo es un plugin" sobre Cordis |
| `autonomous-ai-agents/codex` | DietrichGebert/ponytail | Escalera de minimalismo + benchmark con diff real |
| `educational-html-pipeline` | THU-MAIC/OpenMAIC | Curso multiagente → pptx/HTML/MP4 |
| `media/voicebox` | debpalash/VoiceStudio | 16 TTS + 11 ASR con API OpenAI-compatible local |
| `geospatial/airsim-simulation` | carla-simulator/carla | UE5 + umbrales reales de hardware |
| `routing-isochrones` | conveyal/r5 | Accesibilidad a oportunidades vs isócronas |
| `data-pipeline/google-maps-scrapper` | Madi-S/Lead-Generation | `py-lead-generation`, Google + Yelp |
| `herramientas/browser-local-tools` | IngenieroSeed/SafeDocument | Privacidad impuesta por CSP |
| `government-data-pipelines` | ctt-gob-es/datos.gob.es | Extensiones CKAN + DCAT-AP-ES (9 extensiones) |
| `data-science/rail-lidar-qa-mvp` | Vicomtech/SOSDaR24 | Dataset de referencia, OpenLABEL + PCD |
| `design-systems-ecosystem` | acrosa/GridKit | Verificación de retícula y ritmo vertical |

**Referencias (4):** Foadsf/vintage-latex · Vicomtech/dardcollect · iamtekson/rasuwa-flood · (ArchABM descartado por estancado en 2023).
**Skips (6):** julia, go-app, gtfs-lib (ya cubierto), blog personal, spain-open-data, plugin read-receipts.

---

## 5. Auditoría de calidad: 14 OK · 8 corregidos

Los textos se redactaron desde resúmenes verificados y aun así **el 36 % tenía al menos un error**. Ejemplos corregidos:

| Ítem | Error | Corrección |
|---|---|---|
| `minimind-tiny-llm-training` | "≈3 € de GPU"; "YaRN exige reentrenar" | ≈0,4 $ (2,31 h a ~1,3 ¥/h); YaRN se activa **en inferencia** |
| `eubucco-building-stock` | `subtype`/año sin ground truth | GT real 17,3 % y 15,6 % |
| `geospatial-ai-agents` | "frontend autorizado Esri ArcGIS" | React propio; ArcGIS es opcional |
| `geospatial-mcp-power-pack` | "21 servidores MCP" | 21 **paquetes** (hub + common + 19 MCP); uno de pago |
| `google-maps-scrapper` | 383 ⭐; troceado como feature | 386 ⭐; el troceado está en el TODO |
| `browser-local-tools` | 860 líneas; CSP en línea 1 | 1.180 líneas/55 KB; CSP en línea 4 |
| `synthetic-tabular-data-evaluation` | ">30 notebooks" | **108 notebooks**, 6 datasets |
| `government-data-pipelines` | "único commit de código"; 8 extensiones | v0.1.0/2017 → v2.0.0/2026; faltaba `ckanext-dge-scheming` (9) |

---

## 6. Métricas del sistema (a 2026-09-15)

- **Registry:** 385 entradas procesadas · **181 con skill creado/asociado**
- Reparto: 101 upgrade · 76 domain · 10 tool · 6 reference · 4 pattern · 2 skill · 186 skip
- **Ciclo de vida del pipeline:** 63 runs · 310 repos explorados
- Skills creados por semana ISO: W25 → 54 · W35 → 37 · W36 → 76 · W37 → 2 · **W38 → 12**
- Índice vectorial: ~467 skills en ChromaDB (`~/.mastermind/chromadb`, colección `mastermind-skills`)

---

## 7. Lecciones del ciclo

1. **El dedup semántico solo orienta; el README decide.** Un score alto puede ser falso positivo: `sam3d.cpp` puntuaba 0,747 contra `trellis2-img-to-3d` y no lo cubría (imagen→3D ≠ cuerpo/objetos desde vídeo).
2. **Los veredictos automáticos son generosos:** de 15 CREATE propuestos, 4 se degradaron a referencia (repos de 3-17 ⭐ o colecciones de ejemplos). El filtro final es "¿lo usaría David en 3 meses?".
3. **Autenticar cifras contra la fuente primaria no es opcional.** Los resúmenes heredan números viejos del README y matices invertidos.
4. **Serializar los crons mata dos bugs con un cambio** (`max_parallel_jobs=1`): el 429 de NaN y el lock de `TERMINAL_CWD`.

---

*Hecho con ❤️ por David Antizar — pipeline Stars Explorer*
