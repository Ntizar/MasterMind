# Ecosistema de Repos Ntizar — Mapa Completo

**Fecha:** 2026-06-01  
**Tipo:** conocimiento  
**Clusters:** repos-ecosistema, arquitectura, patrones-front, multi-agent, ciencia-datos  
**Decay:** lento  

## Resumen

David Antizar (Ntizar) mantiene un ecosistema de ~25 repos en GitHub que cubren:

1. **Sistemas multi-agente** — NtizarBrainMasterMind (orquestación con memoria Ebbinghaus)
2. **Simuladores científicos** — SistemaElectricoFuturo, IRPFdibujitos, Voynich_Solving
3. **Dashboards de datos públicos** — nap-dashboard, Accidentes2024, datos-gob-watch
4. **Visualizaciones interactivas** — solmad, Madrid3Pixel, OrbitMixer, XVLegislatura, MetalHoverLab
5. **Accesibilidad / IA local** — FreeHands, YoloConteo
6. **Design system** — Ntizar-Aurora, FamilyTree
7. **Herramientas internas** — mastermind, inicio-en-nan, hackaton1, rail-lidar-qa-mvp

## Patrones recurrentes

### Design System: Ntizar Aurora
- **CSS puro**, sin build step, sin dependencias
- Paleta: azul `#2563eb` + naranja `#f97316` sobre fondo oscuro `#0a0f1e`
- Efecto signature: cristal líquido con `backdrop-filter: blur()` + filtros SVG (Chrome/Chromium)
- 3 niveles de glass: sutil, estándar, fuerte
- Tipografía: Inter + JetBrains Mono
- Se comparte entre TODOS los proyectos del ecosistema

### Frontend vanilla vs React
- **Vanilla** (sin frameworks): SolMAD, IRPFdibujitos, Madrid3Pixel, MetalHoverLab, XVLegislatura, Accidentes2024, OrbitMixer, FamilyTree
- **React + Vite**: SolMAD (TypeScript), nap-dashboard, SistemaElectricoFuturo (v3)
- **Sin npm/build**: Los proyectos vanilla usan `python -m http.server` o `npx serve`

### Web Workers + Comlink
- SolMAD usa Web Workers para cálculos de sombras solares sin bloquear UI
- Patrón: `shadows.worker.ts` + `shadowsClient.ts` con Comlink para API type-safe

### Archivos de datos precalculados
- SolMAD: `terrazas.min.json` (preprocesado del CSV del Ayuntamiento)
- IRPFdibujitos: `data/*.json` generados por Python
- nap-dashboard: datos del NAP (Punto de Acceso Nacional)
- XVLegislatura: `data.js` con datos embebidos de 22 ministerios

### Despliegue
- **GitHub Pages**: la mayoría de proyectos estáticos
- **Vercel**: SolMAD (API functions), nap-dashboard, YoloConteo, OrbitMixer
- **NaN.builders**: proyectos activos de Mastermind

### API externa como fuente de datos
- **REE/ESIOS**: SistemaElectricoFuturo (precios, generación, demanda)
- **Ayuntamiento de Madrid**: terrazas (datos.madrid.es)
- **OpenStreetMap/Overpass**: SolMAD (edificios para sombras)
- **SunCalc**: posición solar
- **Sentinel-2 / STAC / TiTiler**: OrbitMixer (imágenes satelitales)
- **NAP transportes.gob.es**: nap-dashboard
- **datos.gob.es**: datos-gob-watch

### Patrones de seguridad
- API keys nunca en código: modal en navegador (nap-dashboard) o Vercel secrets
- GitHub token para contribuciones: fine-grained token, solo repo específico
- Backend proxy para keys sensibles (Vercel Serverless Functions)

## Proyectos destacados por complejidad

### 1. NtizarBrainMasterMind (2 estrellas)
- **11 agentes especializados** con roles definidos
- **Multi-modelo**: Claude Opus/Sonnet/Haiku, GPT-4o, Gemini según complejidad
- **Memoria con decaimiento Ebbinghaus**: R(t) = a/(log(t+1))^b + c
- **Dos capas sincronizadas**: Obsidian (docs) + OpenCode (ejecución)
- **42% menos código** en capa ejecutable vs v2
- **Critic nunca se degrada**: si no hay modelo alto, se omite

### 2. SistemaElectricoFuturo (1 estrella)
- **Simulador 8.760 horas/año** con trayectoria 2026-2035
- **17 escenarios** realistas (cierre nuclear, VE masivo, crisis gas, etc.)
- **Demand model**: residencial, servicios, industria, VE, bombas de calor, H2
- **Storage avanzado**: degradación baterías, bombeo con reserva estacional
- **Policy**: tope ibérico, CfDs, peajes dinámicos, PVPC
- **Monte Carlo**: `montecarlo.js` para escenarios de riesgo
- **Módulos**: simulator, demand, storage, policy, scenarios, trajectory, nuclear, weather, charts

### 3. FreeHands (MVP)
- **Control sin manos**: gaze + gestures + voice desde webcam
- **MediaPipe** para hand tracking y gaze
- **Voice**: faster-whisper local
- **MultimodalFusion**: IDLE → ACTIVE → CONFIRMING → COOLDOWN
- **Safety**: open palm derecho 2s = kill switch
- **Duck test**: página pública que no usa cámara del navegador

### 4. SolMAD (3 estrellas)
- **6.200 terrazas** de Madrid con cálculo de sol en tiempo real
- **Web Worker + Comlink** para sombras sin bloquear UI
- **Overpass API** para edificios OSM (footprints + alturas estimadas)
- **SunCalc** para posición solar
- **Cache**: localStorage + JSON via API (15 min granularity)
- **Contribuciones**: PRs desde rama `solmad/review-contributions`
- **Three.js** para intro cinematográfica

### 5. nap-dashboard (1 estrella)
- **Parser GTFS en browser** con fflate (descompresión ZIP en memoria)
- **Selector semanal**: lógica completa GTFS (calendar_dates > calendar)
- **React 19 + TypeScript + Vite 5 + Tailwind 4**
- **TanStack Query v5** para caché
- **Proxy Vercel** para API key del NAP

### 6. IRPFdibujitos (1 estrella)
- **Código MIT, datos CC0** — ultra abierto
- **Motor Python** con 47 tests pytest
- **Web vanilla** — sin npm, sin build
- **Progresividad en frío**: concepto divulgativo clave
- **Auditoría abierta**: convoca fiscalistas a revisar el código
- **Parámetros normativos** por año (2012-2026)

### 7. OrbitMixer (2 estrellas)
- **Comparador satelital** Sentinel-2 con split viewer
- **100% free APIs**: Earth Search STAC, TiTiler, OpenTopoData, Nominatim
- **AI analysis** opcional con OpenRouter (Gemini)
- **Hand gesture control** con MediaPipe
- **Vercel Serverless Functions** para API
- **Búsqueda STAC** con cloud cover filtering

### 8. YoloConteo (MVP)
- **YOLOv8n ONNX** ejecutado en navegador con WebGPU → WASM fallback
- **Counter bidireccional** con línea virtual
- **Tracker IoU** para seguimiento
- **Modelo ~12MB** descargado una vez y cacheado
- **Desplegado en Vercel** — accesible desde móvil

## Tecnologías más usadas

| Tecnología | Proyectos | Uso |
|---|---|---|
| Ntizar Aurora CSS | Todos | Design system |
| Leaflet | SolMAD, nap-dashboard, OrbitMixer, XVLegislatura | Mapas |
| SunCalc | SolMAD | Posición solar |
| MediaPipe | FreeHands, OrbitMixer | Hand/gaze tracking |
| Web Workers + Comlink | SolMAD | Cálculos sin bloquear UI |
| React + Vite | SolMAD, nap-dashboard, Madrid3Pixel | UI framework |
| D3.js | XVLegislatura | Visualizaciones |
| Plotly | SistemaElectricoFuturo | Gráficos |
| ONNX Runtime Web | YoloConteo | IA en navegador |
| fflate | nap-dashboard | Descompresión ZIP en browser |
| Zustand | SolMAD | Estado global |
| TanStack Query | nap-dashboard | Caché de datos |
| Tailwind | SolMAD, nap-dashboard, Madrid3Pixel | Estilos |
| Three.js | SolMAD | Intro 3D |
