# Qué desbloquea el aprendizaje de stars — proyectos nuevos y mejoras a los antiguos

**Fecha:** 2026-09-15 · **Base:** 12 skills nuevos + 11 upgrades del batch 2026-09-15
**Cruce contra:** 60+ repos reales de `github.com/Ntizar` (verificados con `gh repo list`)

---

## A. Mejoras a proyectos VIVOS (concretas y verificables)

### 1. SolMAD ← `eubucco-building-stock` ⭐ la más potente
- **Hoy:** sombras aproximadas desde geometría de OpenStreetMap y solo Madrid; el README admite que las sombras se equivocan por toldos/árboles/fachadas.
- **Con eubucco:** 322 M de huellas UE (27 + Noruega, Suiza, UK) con **altura y nº de plantas reales**, armonizando 55 datasets (62 % registros gubernamentales). DOI Zenodo verificado.
- **Mejora doble:** (a) geometría con altura real → sombras mejor calculadas; (b) **salir de Madrid**: Barcelona, Valencia, Sevilla, Bilbao, Málaga. SolMAD deja de ser una web de Madrid y pasa a ser un producto multi-ciudad.
- **Esfuerzo:** medio (una capa de datos + adaptar el solver de sombras, que ya está aislado).

### 2. gobierno-ia ← `mirofish-swarm-simulation` + `minimind-tiny-llm-training` ⭐
- **Hoy:** los ministros conversan por rondas vía ficheros, sin memoria individual persistente ni grafo de conocimiento.
- **Con MiroFish:** GraphRAG sobre la semilla (programa electoral, presupuesto) + **personas con memoria individual y colectiva** + informe de predicción al final. Es exactamente lo que tu simulación quiere ser: los ministros recordarían lo que votaron hace 20 sesiones.
- **Con minimind:** modelo de 64M entrenado desde cero para las tareas triviales (clasificar, etiquetar, resumir tuits) → dejas de gastar cuota NaN en eso.
- **Esfuerzo:** MiroFish = alto (reasignar el motor de turnos); minimind = bajo si solo quieres experimentar.

### 3. DataHubEspana ← `spain-public-procurement` + `spanish-electoral-microdata` + upgrade `datos.gob.es`
- **Licitaciones:** 44,4 M de registros (2000-2026, ~2,3 GB) cruzables con TED. Capa nueva: **"quién gana qué" por organismo, adjudicatario, importe y CCAA**. Doble uso: producto público y análisis interno para Ineco.
- **Electoral:** microdatos del Ministerio del Interior decodificados a nivel **mesa/sección** (la fuente oficial usa formatos propietarios) → mapa de resultados con detalle quirúrgico.
- **Catálogo nacional:** el upgrade de `government-data-pipelines` con las 9 extensiones CKAN y **DCAT-AP-ES** permite ingerir datos.gob.es de forma estándar en vez de a medida.
- **Esfuerzo:** medio por capa; las tres son independientes y se pueden añadir de una en una.

### 4. ISOTime / Time / PLANDEMOVILIDAD ← upgrade `r5` en `routing-isochrones`
- **Hoy:** isócronas ("¿a dónde llego en 30 min?").
- **Con r5:** **accesibilidad a oportunidades** ("¿a cuántos puestos de trabajo / hospitales / comercios llego en 30 min?"). Es la métrica que pide un PMST/PTST y la que da valor a un plan de movilidad.
- **Esfuerzo:** bajo-medio (nuevo indicador sobre la misma red).

### 5. era-visor / CIAF-visor ← `inertial-navigation-inslib` + upgrade SOSDaR24
- **Hoy:** base plana de 349 informes con análisis v3 (cronología, causas, material rodante).
- **Con INS lib (C11, sin heap, Kalman de raíz cuadrada, QA DO-178):** **reconstrucción de trayectoria** del tren en tramos con GNSS degradado o mudo (túneles, trincheras) — el escenario típico de una investigación ferroviaria. Los informes dan velocidad y posición; el filtro reconstruye lo que falta.
- **Con SOSDaR24:** dataset de referencia con etiquetas OpenLABEL + nube de puntos → valida el QA LiDAR que ya tienes en `rail-lidar-qa-mvp`.
- **Esfuerzo:** alto (es un módulo numérico nuevo), pero es el que más diferenciaría el visor.

### 6. prospeccion-mvp ← upgrade `py-lead-generation` en `google-maps-scrapper`
- **Hoy:** descubrimiento de webs locales vía OSM.
- **Con Google + Yelp leads:** negocios con teléfono/email/categoría/valoraciones sin depender solo de OSM. Más leads, con datos de contacto, para demos en GitHub Pages.
- **Esfuerzo:** bajo (fuente de datos adicional en un pipeline que ya existe).

### 7. kit72money / kit72h ← upgrade `VoiceStudio` en `voicebox`
- 16 voces TTS + 11 ASR **locales** con API OpenAI-compatible → locuciones de shorts gratis y sin cuota, en lugar de APIs de pago.
- **Esfuerzo:** bajo (sustituir el proveedor de voz en el pipeline).

### 8. Aurora-7 ← upgrade `GridKit` en `design-systems-ecosystem`
- Verificación programática de retícula y ritmo vertical → complementa tu `audit-aurora.py` con una comprobación de espaciado/tipografía que hoy no hace.
- **Esfuerzo:** bajo.

### 9. dna-analyzer / herramientas locales ← upgrade `SafeDocument` en `browser-local-tools`
- CSP que **impone** la privacidad (bloquea exfiltración por política, no por promesa) → tu "100 % en el navegador, sin guardar datos" pasa de afirmación a garantía técnica auditable.
- **Esfuerzo:** bajo.

### 10. DeSumarIntegrar / DibujoTecnico ← upgrade `OpenMAIC` en `educational-html-pipeline`
- Pipeline de curso multiagente → genera PPTX, HTML y **MP4**. Tus 94 HTML de matemáticas se convierten en curso con vídeo/descargables.
- **Esfuerzo:** medio.

### 11. Water3J / drish-es ← `geospatial-ai-agents`
- Ingesta satelital **gratis y sin suscripción** (Planetary Computer / NASA VEDA) vía STAC, más un agente de visión que razona sobre el raster.
- **Water3J:** validar el modelo de oleaje contra altimetría real (Sentinel-3) en vez de solo tests sintéticos. **drish-es:** Sentinel-2 por STAC sin pipeline de descarga propio.
- **Esfuerzo:** medio.

### 12. MasterMind ← upgrades `deepseek-harness` (hermes-agent) y `ponytail` (codex)
- Patrón "todo es un plugin" sobre Cordis y escalera de minimalismo con benchmark por diff → ideas directas para el propio orquestador.
- **Esfuerzo:** bajo (documental, informa decisiones).

---

## B. Proyectos NUEVOS que ahora sabes hacer

| Idea | Skills que la habilitan | Por qué tiene valor |
|---|---|---|
| **Visor de licitaciones públicas de España** — "¿quién gana qué y por cuánto?" | `spain-public-procurement` | 44,4 M registros ya resueltos; dato que no existe bien servido en ninguna web pública |
| **SolMAD multi-ciudad** (o "SunEU") | `eubucco-building-stock` | El solver ya existe; el dato de alturas UE lo desbloquea sin coste |
| **Visor conversacional** — "¿qué pasó aquí?" en lenguaje natural sobre tu mapa | `geospatial-mcp-power-pack` (19 MCP + router) + `geospatial-ai-agents` | Convertir cualquier visor tuyo en asistente; patrón reutilizable en 5 proyectos |
| **Micro-LLM propio entrenado en una GPU** | `minimind-tiny-llm-training` | Entender el ciclo completo + modelo local para tareas baratas |
| **Simulador de opinión/sociedad** (más allá del gobierno) | `mirofish-swarm-simulation` | Personas con memoria + informe de predicción: contenido y análisis |
| **Demo de back-office logístico self-hosted** | `fleetbase-logistics-os` | Pedidos, flota, tracking y OSRM sin SaaS — útil para prospección de clientes de movilidad |
| **Análisis de vídeo de estaciones/CCTV sin Python ni CUDA** | `sam3d-cpp-body-objects` | Pose y malla humana en C++/GGML: encaja en investigaciones y digital twins |
| **Sello de privacidad para tus herramientas** | `browser-local-tools` (SafeDocument) + `synthetic-tabular-data-evaluation` | CSP verificable + métrica de fuga: publicable |
| **Navegación inercial para embedded** | `inertial-navigation-inslib` | Fuera de lo ferroviario: cualquier trayectoria sin GNSS |

---

## C. Prioridad recomendada (impacto / esfuerzo)

1. **eubucco → SolMAD multi-ciudad** — el solver existe, el dato es gratis y el salto de producto es grande.
2. **r5 → accesibilidad en ISOTime/Time/PLANDEMOVILIDAD** — métrica vendible, coste bajo.
3. **MiroFish → memoria real en gobierno-ia** — arregla la debilidad estructural de la simulación.
4. **Licitaciones + electoral → DataHubEspana** — dos capas nuevas con dato único y poco código de ingesta.
5. **VoiceStudio → voz local en kit72money** — quita dependencia de pago en un pipeline vivo.
6. **py-lead-generation → más leads en prospeccion-mvp** — alimenta el pipeline que genera ingresos.

---

## D. Honestidad: lo que NO aporta gran cosa (todavía)

- `inertial-navigation-inslib`, `sam3d-cpp-body-objects` y `synthetic-tabular-data-evaluation` son **nicho real**: potentes en su escenario (ferrocarril, visión sin Python, RGPD) pero no de uso diario. No forzar su uso.
- `software-open-source-espana` no es un proyecto: es un **atajo** para no reescribir conectores que ya existen (útil justo antes de empezar cualquier web de datos españoles).
- `spanish-electoral-microdata` rinde solo si el dato se puede citar con fuente y fecha; sirve para análisis, no para webs con ambición comercial.

---

*Hecho con ❤️ por David Antizar — Mastermind, 2026-09-15*
