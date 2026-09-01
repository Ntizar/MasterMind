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
