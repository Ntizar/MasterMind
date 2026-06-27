---
title: Exploración de repos con estrellas de Ntizar
date: 2026-05-28
tags: [github, exploration, learning, repos, stars]
---

# Exploración de repos con estrellas de Ntizar — 2026-05-28

## Resumen

Se exploraron 50 repositorios con estrellas del usuario Ntizar en GitHub. Se analizaron en profundidad 8 repositorios de mayor relevancia para el sistema Mastermind.

## Repos Explorados

### 1. microsoft/markitdown (125K⭐)
- Conversión universal de documentos a Markdown
- Soporta PDF, DOCX, PPTX, XLSX, imágenes, audio, HTML, CSV, JSON, XML, ZIP, EPUB, YouTube
- Integraciones con Azure Document Intelligence y Content Understanding
- Plugin system extensible
- **Relevancia para Mastermind**: Alta — ingestión de documentos para RAG/LLMs
- **Skill creada**: markitdown (ya existía, verificada actualizada)

### 2. NangoHQ/nango (9K⭐)
- Plataforma para construir integraciones de productos con IA
- 800+ APIs pre-configuradas con auth, token refresh, scopes
- SDKs: Node.js, Python, Go, TypeScript
- Soporte nativo para MCP
- Funciones: Auth, Proxy, Sync, Actions, Webhooks, Unified APIs
- **Relevancia para Mastermind**: Media-Alta — integraciones de APIs externas para agentes

### 3. htekdev/vidpipe (166⭐)
- Pipeline de procesamiento de vídeo con IA
- 14 etapas: transcripción, silence removal, captions, shorts, social media, blog
- Arquitectura en 8 capas (L0-L7) con agentes especializados
- LLM providers: Copilot (default), OpenAI, Claude
- Integración con Late API para publicación automática
- **Relevancia para Mastermind**: Media — pipeline de contenido de vídeo

### 4. MobilityData/awesome-transit (1.7K⭐)
- Lista curada de estándares de transporte público abierto
- Cubre: GTFS, GTFS-RT, MDS, GBFS, OpenTripPlanner
- **Relevancia para Mastermind**: Alta — ecosistema BiciMad/transporte Madrid

### 5. jamiepine/voicebox (28K⭐)
- Estudio de voz AI local-first
- 7 motores TTS: Qwen3-TTS, Qwen CustomVoice, LuxTTS, Chatterbox, Chatterbox Turbo, HumeAI TADA, Kokoro
- Clonación de voz zero-shot, dictado global, STT con Whisper
- MCP server integrado
- **Relevancia para Mastermind**: Alta — alternativa local a ElevenLabs para TTS de Mastermind
- **Skill creada**: voicebox

### 6. crystaldba/postgres-mcp (2.8K⭐)
- PostgreSQL como servidor MCP
- 9 herramientas: schemas, objetos, SQL, EXPLAIN, health checks, index tuning
- Dos modos: unrestricted (dev) y restricted (producción)
- Algoritmo DTA (Microsoft) + LLM optimizer para indexación
- **Relevancia para Mastermind**: Alta — acceso seguro a PostgreSQL por agentes
- **Skill creada**: postgres-mcp

### 7. metabase/metabase (47K⭐)
- Herramienta BI open-source
- Query builder visual + SQL editor
- Metabot (IA), Agent API, MCP Server
- 20+ conectores de bases de datos
- Embedding robusto (modular, full-app, white-label)
- **Relevancia para Mastermind**: Media — análisis de datos para dashboards

### 8. nagix/mini-tokyo-3d + vasile/transit-map
- mini-tokyo-3d (4K⭐): Mapa 3D en tiempo real del transporte de Tokyo
- transit-map (372⭐): Simulaciones de mapas de transporte
- Tecnologías: Three.js, D3, WebGL, D3-geo-projection
- **Relevancia para Mastermind**: Media-Alta — visualización de transporte público 3D

## Ecosistema GTFS Identificado
Ntizar tiene 8 repos relacionados con transporte/GTFS:
- MobilityData/awesome-transit (1.7K⭐)
- WRI-Cities/static-GTFS-manager (159⭐)
- WRI-Cities/payanam (17⭐)
- OneBusAway/onebusaway-gtfs-realtime-visualizer (68⭐)
- fitomad/bicimad (4⭐)
- vasile/transit-map (372⭐)
- gabrielAHN/gtfs-viz (49⭐)
- BlinkTagInc/gtfs-to-html (225⭐)

Esto confirma un interés profundo en el ecosistema de transporte público y GTFS.

## Intereses Confirmados de Ntizar
Basado en los 50 repos con estrellas:

1. **Agentes AI / Hermes Agent** — hermes-agent (170K⭐), scientific-agent-skills (26K⭐)
2. **Integraciones de APIs** — nango (9K⭐), API-mega-list (5K⭐)
3. **Transporte público / GTFS** — 8 repos en este ecosistema
4. **Voces AI / TTS** — voicebox (28K⭐), VibeVoice (47K⭐)
5. **Documentos / Markitdown** — 125K⭐
6. **Video processing** — vidpipe (166⭐)
7. **BI / Datos** — metabase (47K⭐)
8. **PostgreSQL / MCP** — postgres-mcp (2.8K⭐)
9. **Diseño / CSS** — awesome-design-systems (24K⭐), glass-refraction (35⭐)
10. **Satélite / GIS** — DRISH-X (228⭐), remote-sensing-satellite-downloader (4⭐)

## Skills Creadas/Actualizadas
- ✅ **postgres-mcp** — nueva skill
- ✅ **voicebox** — nueva skill
- ✅ **markitdown** — ya existía, verificada actualizada

## Notas
- La exploración automática de repos con estrellas es un patrón valioso para mantener el conocimiento del sistema actualizado
- Los intereses de Ntizar muestran una dirección clara hacia: agentes AI, transporte público, voces AI y herramientas de productividad
