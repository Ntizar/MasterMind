## Maratón nocturno 2026-09-01 — batches de aprendizaje

### Batch — 01:26
- Explorados: OpenMined/PySyft (10019, Python) — decisión: SKIP dedup (federated learning/privacidad ya cubierto por security/presidio-pii y mlops/*; no encaja en proyectos de David)
- chakra-core/ChakraCore (9258, JavaScript) — decisión: SKIP dedup (motor JS embebido C++, sin relevancia; score 0.48 contra page-agent/ai-agent-sandbox-runtime, lejos del stack de David)
- trycompai/crm (9166, TypeScript) — decisión: SKIP dedup (CRM agéntico → score 0.82 contra productivity/airtable + sales-account-intelligence + huly-crm-erp-platform)
- oso95/scroll-world (8848, JavaScript) — decisión: SKIP dedup (ES el propio repo del skill existente creative/scroll-world-3d-landing — score 0.85)
- simplifaisoul/osiris (8152, TypeScript) — decisión: SKIP dedup (dashboard OSINT tiempo real → geospatial/osint-live-globe score 0.67 + traffic-digital-twin-cctv)
- Pendientes restantes: 148

### Batch — 01:52
- Explorados: alirezamika/autoscraper (7924, Python) — decisión: SKIP dedup (skill autoscraper ya existe, score 0.93)
- meituan-longcat/LongCat-Video (7727, Python) — decisión: SKIP dedup (video-gen-from-topic 0.85; release de modelo con 2 .py, sin patrones reutilizables)
- lwthiker/curl-impersonate (6917, Python) — decisión: SKIP dedup (skill curl-impersonate ya existe, score 0.85)
- LiamGvchi/gc-minimal-zine-poster (6797, sin lang) — decisión: SKIP sin código (skill de prompts para Codex; overlap creativo 0.75, no es proyecto de software)
- graphhopper/graphhopper (6654, Java) — decisión: SKIP dedup (skill graphhopper-routing ya existe, score 0.77)
- Pendientes restantes: 154 (categoría pending en registry; este batch convirtió 5 pending→skip)

### Batch — 02:01
- Explorados: cursor/plugins (6382, TypeScript) — decisión: SKIP dedup (especificación de plugins Cursor para agentes IA; solapamiento 0.69 con autonomous-ai-agents/hermes-agent + agent-canvas; ficheros md/json sin patrones de código reutilizables para el stack de David)
- ByteDance-Seed/Depth-Anything-3 (6239, Python) — decisión: SKIP dedup (duplicado exacto: skill depth-anything-3 ya existe, score 0.83)
- erincatto/box3d (6223, C) — decisión: SKIP dedup (motor física 3D; skill creative/box3d-renderer ya lo cubre, score 0.69)
- valhalla/valhalla (6141, C++) — decisión: SKIP dedup (skill valhalla-routing ya existe + routing-isochrones + graphhopper-routing cubren isócronas/matrix)
- Gentleman-Programming/gentle-ai (6112, Go) — decisión: SKIP dedup (CLI de workflows/review para coding agents; solapamiento 0.79 con claude-code + opencode + requesting-code-review + google-eng-practices)
- Pendientes restantes: 138

### Batch — 02:25
- Explorados: chaitanyagiri/munder-difflin (5870, JavaScript) — decisión: SKIP dedup (harness multi-agente local con mailbox/memoria/orquestación → hermes-agent 0.77 + agent-memory + mastermind-orchestration ya cubren el patrón; Electron pre-release, no es nuestro stack)
- dimforge/rapier (5698, Rust) — decisión: SKIP dedup (motor de física 2D/3D; creative/box3d-renderer 0.62 + threejs skills cubren física en web para los proyectos 3D de David)
- gosom/google-maps-scraper (5677, Go) — decisión: SKIP dedup (duplicado exacto: skill data-pipeline/google-maps-scrapper ya existe, score 0.87)
- AhmadIbrahiim/Website-downloader (5291, HTML) — decisión: SKIP dedup (duplicado exacto: skill data-pipeline/website-downloader ya existe, score 0.84; wrapper wget+express+socket.io demasiado simple)
- ZzzLc0405/photo-abstract-editorial (5168, sin lang) — decisión: SKIP sin código (skill de prompts Codex foto→panel abstracto; solo .md/.jpg, licencia CC BY-NC-SA no comercial, overlap creativo 0.62)
- Pendientes restantes: 159 (categoría pending en registry; este batch convirtió 5 pending→skip)

### Batch — 02:50
- Explorados: streetcomplete/StreetComplete (4779, Kotlin) — decisión: SKIP dedup (skill geospatial/street-complete ya existe, score 0.84; app Android fuera del stack de David)
- lumina-ai-inc/chunkr (4139, Rust) — decisión: SKIP dedup (skill chunkr-ai 0.81 + ocr-and-documents 0.84 + pdf-llm-extraction/mineru/liteparse cubren documento→RAG)
- mutonby/openshorts (3788, Python) — decisión: SKIP dedup (video-gen-from-topic 0.89 + video-processing 0.87 + video-use-agentic-editing + agentic-video-pipeline cubren clips verticales IA)
- unclebob/swarm-forge (3452, Clojure) — decisión: SKIP dedup (orquestación multi-agente cubierta por mastermind-orchestration 0.72 + hermes-agent 0.73 + delegate_task nativo; Clojure+tmux no es nuestro stack)
- synthetic-sciences/openscience (3370, TypeScript) — decisión: SKIP dedup (duplicado exacto: ia/openscience-ai-workbench ya existe, 0.71 + scientific-agent-skills 0.77)
- Pendientes restantes: 128

### Batch — 03:00
- Explorados: opentripplanner/OpenTripPlanner (2724, Java) — decisión: SKIP dedup (skill routing-isochrones/opentripplanner-otp ya cubre planificación multimodal GTFS+OSM; el score top 0.80 fue productivity/maps pero OTP server no aporta patrón nuevo para el stack de David)
- ShinMegamiBoson/OpenPlanter (2437, Python) — decisión: SKIP dedup (agente investigación OSINT con knowledge graph → agent-reach 0.74 + llm-wiki 0.73 + rag-knowledge-base cubren el patrón; además sin pushes desde marzo)
- shepherd-agents/shepherd (2386, Python) — decisión: SKIP dedup (duplicado exacto: skill ia/shepherd-meta-agents ya existe, score 0.75)
- numba/llvmlite (2292, Python) — decisión: SKIP dedup (binding LLVM interno de Numba; numba-jit-acceleration cubre el caso de uso real; sin patrones accionables, niche de compiladores)
- cartesiancs/map3d (2268, TypeScript) — decisión: SKIP dedup (duplicado exacto: skill geospatial/map3d-r3f ya existe, score 0.76)
- Pendientes restantes: 123 (según --json del script; este batch convirtió 5 pending→skip, 0 skills)

### Batch — 03:28
- Explorados: hieunc229/mailflare (2142, TypeScript) — decisión: SKIP dedup (inbox email self-hosted Cloudflare Workers+D1+R2 → nango 0.59 + email-inbox-triage 0.59 + himalaya cubren el dominio; además infra de email no es el stack de David)
- oil-oil/oil-motion (2129, Python) — decisión: SKIP dedup (skill de animación interactiva con frames de vídeo IA → hyperframes-html-video 0.76 + scroll-world-3d-landing 0.72 + video-use-agentic-editing cubren el patrón completo)
- MapleTechLabs/maple (1741, TypeScript) — decisión: SKIP dedup (duplicado exacto: skill devops/maple-observability ya existe, score 0.72 — creado en batch previo)
- nasa-gibs/worldview (1694, JavaScript) — decisión: SKIP dedup (visor satelital WMTS/OpenLayers → ign-wmts-tiles 0.72 + satellite-gis-patterns + osint-live-globe + geolibre cubren el patrón; app legendaria pero sin patrón nuevo para nosotros)
- SegFault42/HeliosGen (1674, TypeScript) — decisión: SKIP dedup (workflow builder visual de nodos para IA generativa → comfyui 0.76 cubre exactamente el mismo patrón de pipelines de nodos; además dependiente de kie.ai de pago)
- Pendientes restantes: 118 (según --json del script; este batch convirtió 5 pending→skip, 0 skills)

### Batch — 03:51
- Explorados: elayadesign/ai-design-skills (1669, sin lang) — decisión: SKIP dedup (colección de SKILL.md de diseño para agentes IA, solo 6 ficheros md → popular-web-designs 0.91 + claude-design 0.87 + ai-website-cloner cubren landing+design systems; además es casi awesome-list sin código)
- steipete/birdclaw (1640, TypeScript) — decisión: SKIP dedup (archivo Twitter/X → SQLite local + MCP read-only → social-media/xurl 0.70 + agent-reach 0.67 cubren acceso a tweets y el patrón SQLite+MCP ya está documentado en mcp/native-mcp y postgres-mcp; niche de auto-hosting de X)
- roryclear/clearcam (1527, Python) — decisión: SKIP dedup (detección+tracking+notificaciones en cámaras RTSP → computer-vision/cctv-yolo 0.69 + geospatial/traffic-digital-twin-cctv 0.75 cubren exactamente el pipeline YOLO/CLIP sobre CCTV)
- PKU-VCL-3DV/SLAM3R (1352, Python) — decisión: SKIP dedup (reconstrucción 3D densa en tiempo real desde RGB → computer-vision/r3-reconstruction 0.64 + depth-anything-3 0.60 + colmap-view + gush3r-3d cubren reconstrucción 3D; research CVPR sin integración práctica con el stack web de David)
- PurpleDoubleD/locally-uncensored (1323, TypeScript) — decisión: SKIP dedup (estudio local AI chat+imagen+vídeo+agente → comfyui 0.79 + video-gen-from-topic 0.82 + voicebox/llama-cpp cubren el dominio; envolvente Tauri sobre backends existentes, sin patrón nuevo; contenido "abliterated" fuera de alcance)
- Pendientes restantes: 113 (según --json del script; este batch convirtió 5 pending→skip, 0 skills)

### Batch — 04:03
- Explorados: SikandarJODD/svelte-animations (1226, Svelte) — decisión: SKIP dedup (catálogo de componentes Magic/Aceternity UI portados a Svelte → ui-animation-taste 0.62 + popular-web-designs 0.60 + aurora-design-system cubren animación UI; además Svelte no es el stack de David, y el repo viejo remite a SikandarJODD/animations para Svelte 5)
- alex-hyperagent/hyperagent-public-skills (1119, sin lang) — decisión: SKIP dedup (15 ficheros JSON sueltos, sin README ni código → hub-skill-discovery 0.83 + addyosmani-agent-skills 0.76 + hermes-agent-skill-authoring cubren catálogo de skills de agente; es una colección, no un patrón)
- localai-org/depth-anything.cpp (1090, C++) — decisión: SKIP dedup (port ggml de Depth Anything 2/3 → depth-anything-3 0.75 cubre el modelo y llama-cpp 0.63 el patrón GGUF/CPU; exports glb/COLMAP/PLY ya documentados en colmap-view y r3-reconstruction)
- autowarefoundation/vision_pilot (874, C++) — decisión: SKIP dedup (stack ADAS L2 end-to-end sobre ROS2, por debajo del umbral de 1000⭐ y fuera del ámbito web/GIS de David → cctv-yolo + traffic-digital-twin-cctv + airsim-simulation 0.57 cubren CV sobre conducción)
- ankandrew/fast-alpr (788, Python) — decisión: SKIP dedup (duplicado exacto: skill data-science/fast-alpr ya existe, score 0.81)
- Pendientes restantes: 108 (según --json del script; este batch convirtió 0 en skills, 0 skills creados, 5 skips dedup)

### Batch — 04:25
- Explorados: scottstts/Threejs-Awesome-Graphics-Agent-Skills (771, JavaScript) — decisión: SKIP dedup (duplicado exacto: skill threejs-awesome-graphics-agent-skills ya existe, score 0.84)
- Braffolk/fable5-world-demo (709, TypeScript) — decisión: SKIP dedup (duplicado exacto: geospatial/fable5-webgpu-procedural ya cubre LAAS, score 0.83; el patrón WebGPU+TSL+verificación headless está documentado ahí + webgl-headless-verification)
- SanshruthR/CCTV_YOLO (688, Python) — decisión: SKIP dedup (demo Gradio de un solo fichero YOLOv5n6 sobre stream CCTV → computer-vision/cctv-yolo + traffic-digital-twin-cctv 0.73 cubren el pipeline; el truco infer-baja-res/dibujo-alta-res es una línea de escala; por debajo del umbral 1000⭐)
- anthropics/html-effectiveness (645, HTML) — decisión: SKIP (galería de 21 ejemplos HTML sueltos sin código reutilizable ni patrones de pipeline → claude-design 0.71 + html-artifact-integrity + educational-html-pipeline cubren "HTML como output format"; es una lista curada de ejemplos, quality gate de awesome-list aplica)
- openinframap/openinframap (597, TypeScript) — decisión: SKIP dedup (duplicado exacto: geospatial/openinframap ya existe, score 0.74 contra consulta + osm-infrastructure-mapping 0.88 cubre el stack PostGIS/imposm3/tegola/maplibre)
- Pendientes restantes: 103 (según --json del script; 5 skips dedup, 0 skills creados)

### Batch — 04:50
- harvard-lil/perma (531, JavaScript) — decisión: SKIP dedup (duplicado exacto: data-pipeline/perma-archiving ya cubre Perma.cc, score 0.82; perma-archiving + website-downloader documentan el patrón de archiving permanente)
- uav4geo/GeoDeep (510, Python) — decisión: SKIP dedup (duplicado exacto: geospatial/geodeep ya existe en la lista de skills, score 0.69 + satellite-ai-vision y rs-change-detection cubren detección/segmentación en ráster)
- NVIDIA-AI-IOT/nanoowl (507, Python) — decisión: SKIP dedup (OWL-ViT zero-shot detection: moondream-vlm 0.83 + segment-anything + rf-detr cubren open-vocab detection; TensorRT/Jetson es infra NVIDIA específica fuera del stack de David, y <1000⭐)
- BlinkTagInc/node-gtfs (503, TypeScript) — decisión: SKIP dedup (duplicado exacto: routing-isochrones/node-gtfs ya existe, score 0.83; transit-data-pipelines y gtfs-manager cubren el flujo SQLite/Postgres GTFS+RT)
- majidmanzarpour/threejs-procedural-dungeon (494, JavaScript) — decisión: SKIP dedup (duplicado exacto: skill threejs-procedural-dungeon ya indexado, score 0.71; seed-three + fable5-webgpu-procedural cubren generación procedural determinista)
- Pendientes restantes: 98 (5 skips dedup, 0 skills creados)

### Batch — 05:00
- Explorados: reearth/reearth-visualizer (442, TypeScript) — decisión: SKIP dedup (duplicado exacto: geospatial/reearth-visualizer ya existe como skill, score 0.72 + reearth-flow 0.72; WebGIS Cesium/digital twin ya cubierto junto a cesium-3d-tiles y threejs-3d-maps)
- SikandarJODD/cnblocks (426, Svelte) — decisión: SKIP dedup (colección de blocks de marketing Svelte/shadcn → popular-web-designs 0.90 + awesome-design-systems cubren el patrón; sin stack propio de David que es vanilla JS, <1000⭐)
- appica-dev/appica-ui (400, TypeScript) — decisión: SKIP dedup (librería React/Tailwind: popular-web-designs 0.76 + design-systems-ecosystem + shadcn ecosistema cubren; 2 meses de vida, <1000⭐ y React no es el stack de David)
- victortassinari/FossFLOW (355, React) — decisión: SKIP dedup (diagramas isométricos de infraestructura → creative/architecture-diagram 0.84 + excalidraw 0.85 + editorial-diagrams cubren el espacio de diagramas; fork de Isoflow, <1000⭐)
- SikandarJODD/animations (342, Svelte) — decisión: SKIP dedup (port Svelte de Magic UI/Spell UI → ui-animation-taste + popular-web-designs 0.78 cubren patrones de animación; mismo autor que cnblocks ya descartado, <1000⭐)
- Pendientes restantes: 93 (5 skips dedup, 0 skills creados)

### Batch — 05:25
- Explorados: SikandarJODD/ai-elements (310, Svelte) — decisión: SKIP dedup (port no oficial de Vercel AI Elements a Svelte → popular-web-designs 0.77 + claude-design + shadcn ecosistema cubren componentes UI para chat IA; Svelte no es el stack de David y <1000⭐)
- KevinXu02/R3 (309, Python) — decisión: SKIP dedup (duplicado exacto: skill computer-vision/r3-reconstruction ya existe, score 0.72; depth-anything-3 + colmap-view refuerzan cobertura)
- ad-freiburg/pfaedle (289, C++) — decisión: SKIP dedup (duplicado exacto: skill mobility/pfaedle-routing ya existe, score 0.77; gtfs2shp 0.87 + transit-data-pipelines cubren el flujo shapes GTFS↔GIS)
- SantanderAI/gen-fraud-graph (281, Python) — decisión: SKIP (generador de grafos sintéticos de fraude AML para benchmark GNN: dominio financiero-fraude fuera del scope de proyectos de David, sin dup real (top dspy 0.56) pero <1000⭐ y patrón no reutilizable en GIS/transporte/dashboards)
- SikandarJODD/form-builder (251, Svelte) — decisión: SKIP dedup (form builder SvelteKit+Superforms+Zod → popular-web-designs 0.59 + adela-new-module cubren el espacio; Svelte+zod no es el stack de David, <1000⭐)
- Pendientes restantes: 88 (según --json del script; 5 skips, 0 skills creados)
