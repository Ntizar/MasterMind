# Exploración de Repos con Estrellas — 2026-05-28

## Resumen del análisis
Se han explorado 50 repositorios con estrella del usuario Ntizar en GitHub. Se ha analizado en profundidad los 15 más relevantes.

## Categorías principales descubiertas

### 1. 🤖 IA / Agentes / Voice (Alta prioridad)
- **stablyai/orca** (⭐3.5k) — IDE multi-agente: orquesta Claude Code, Codex, Grok, OpenCode en paralelo con worktrees. Compatible con Hermes. *Relevante para escalar Mastermind como agente multi-para.*
- **Blaizzy/mlx-vlm** (⭐4.8k) — Vision Language Models en Mac con MLX. Soporta LLaVA, Pixtral, Florence2, Molmo, Paligemma. Fine-tuning incluido. *Útil para capacidades de visión en Mastermind.*
- **microsoft/VibeVoice** (⭐47k) — Voice AI de Microsoft. ASR + TTS unificado. Soporta audio de 60 min en un solo paso. *Alternativa a TTS actual para Mastermind.*
- **jamiepine/voicebox** (⭐28k) — Voice studio local: clonación de voz, dictado, TTS con Qwen3-TTS. *Competidor directo de VibeVoice, más orientado a producto.*
- **K-Dense-AI/scientific-agent-skills** (⭐26k) — 140+ skills de ciencia para agentes. *No aplicable directamente pero referencia el estándar Agent Skills.*

### 2. 🗄️ Datos / Analytics / APIs
- **metabase/metabase** (⭐47k) — BI open source. *Alternativa a Power BI para dashboards de datos de Mastermind.*
- **microsoft/markitdown** (⭐126k) — Convierte cualquier archivo a Markdown. *Ya tenemos skill markitdown, pero útil conocer su escala.*
- **cporter202/API-mega-list** (⭐5.5k) — Catálogo masivo de APIs. *Ya tenemos skill api-mega-list.*
- **crystaldba/postgres-mcp** (⭐2.8k) — MCP server para Postgres con index tuning, explain plans, health checks. *Muy relevante para el stack de Mastermind.*

### 3. 🚌 Transporte / GTFS / Mapas
- **AbelVM/omt-router** (⭐11) — Routing 100% client-side para OpenMapTiles. A*, Dijkstra, Delta-Stepping. *Potencial para Bicimad dashboard sin backend.*
- **WRI-Cities/static-GTFS-manager** (⭐159) — GUI para crear/editar/exportar GTFS. *Útil para proyectos de transporte.*
- **WRI-Cities/payanam** (⭐17) — Mapeo de rutas a GTFS. *Complemento al anterior.*
- **vasile/transit-map** (⭐372) — Simulaciones de mapas de transporte (swisstrains.ch). *Inspiración visual.*
- **MobilityData/awesome-transit** (⭐1.8k) — Lista comunitaria de APIs de transporte. *Recurso de referencia.*

### 4. 🛰️ Satélite / GIS
- **sparkyniner/DRISH-X** (⭐228) — Detección de tráfico vehicular desde satélite Sentinel-2. *Técnica interesante: usa el "spectral smear" de vehículos en movimiento.*
- **Aouei/remote-sensing-satellite-downloader** (⭐4) — Descarga de datos Sentinel-2/Landsat-8. *Utilidad práctica para proyectos de satélite.*
- **orcunkok/AWS-Dem-Downloader** (⭐8) — Descarga de tiles de elevación AWS Terrain. *GIS complementario.*
- **c2g-dev/city2graph** (⭐1.2k) — Transforma relaciones geoespaciales en grafos para GNN. *Avanzado.*

### 5. 🎨 Diseño / CSS
- **Z1Code/glass-refraction** (⭐35) — Liquid Glass design system con React + CSS. SVG refraction, specular highlights. *Complementa la skill liquid-glass-css existente.*
- **alexpate/awesome-design-systems** (⭐24k) — Colección de design systems. *Ya tenemos skill awesome-design-systems.*

### 6. 🛠️ Infraestructura / DevOps
- **NangoHQ/nango** (⭐9.3k) — 800+ APIs integradas con OAuth managed. *Alternativa a nuestra integración de APIs.*
- **google/eng-practices** (⭐23k) — Prácticas de ingeniería de Google. *Ya tenemos skill.*
- **XMihura/Kanvas** (⭐169) — Gestión de proyectos en Obsidian Canvas con agentes IA. *Interesante workflow humano+IA.*
- **htekdev/vidpipe** (⭐166) — Editor de vídeo AI: transcripción, subtítulos, shorts, posts sociales. *Herramienta de contenido.*

### 7. 📚 Recursos educativos
- **686f6c61/Workshop-IA-Agentes-Herramientas** (⭐36) — Workshop completo de IA (438 slides) de Ntizar mismo. Cubre desde backprop hasta agentes en producción. *Propio, referencia interna.*

### 8. 🔬 Ciencia de datos / ML
- **PINTO0309/PINTO_model_zoo** (⭐4.4k) — Modelos convertidos entre frameworks (TF, PyTorch, ONNX, OpenVINO, TFLite, CoreML). *Recurso valioso para deployment.*
- **antoinelame/GazeTracking** (⭐2.6k) — Eye tracking con webcam. *Curioso, no aplicable directamente.*
- **Barath19/Boxer3D** (⭐398) — AR 3D object detection con LiDAR. *No aplicable.*

### 9. 🇪🇸 Proyectos españoles
- **cristobal-GC/electriciPy_market** (⭐31) — Simulador de mercado eléctrico. *Complemento a los dashboards ESIOS.*
- **PabloCastellano/libreborme** (⭐134) — Borme web platform. *Proyecto español interesante.*
- **fitomad/bicimad** (⭐4) — Cliente BiciMad en Swift. *Complemento a la API Bicimad.*

## Hallazgos clave

1. **Orca** es el más relevante para Mastermind: orquestación multi-agente que podría complementar nuestro sistema de subagentes.
2. **VibeVoice** de Microsoft es una alternativa seria a nuestro TTS actual (Álvaro). Soporta ASR + TTS unificado.
3. **Postgres MCP** es muy relevante para nuestro stack — nos daría capacidades avanzadas de DB a nuestros agentes.
4. **Kanvas** ofrece un patrón interesante: Obsidian Canvas + CLI para agentes. Podría inspirar workflows de planificación visual.
5. **DRISH-X** demuestra una técnica creativa para tráfico por satélite que podría ser útil para proyectos de movilidad.
6. El usuario tiene interés claro en: IA/agentes, transporte/GTFS, satélite/GIS, voice AI, y diseño CSS.
