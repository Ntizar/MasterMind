---
name: skills-catalogo-completo
description: "Catálogo completo de skills del sistema Mastermind — ESIOS Dashboard (20 patrones) + APIs nocturnas (10 skills mejoradas). Patrones reutilizables para dashboards, APIs, agentes, visión, voz y GIS."
version: 2.0.0
author: Ntizar + Mastermind
---

# Catálogo de Skills — Mastermind System

> Skills extraídas y mejoradas a partir del proyecto [esios-dashboard](https://github.com/Ntizar/esios-dashboard) y APIs/tools descubiertos en sesiones nocturnas.
> Organizadas por categoría, con código real, arquitectura y ejemplos reutilizables.

---

## 🏗️ Arquitectura General

| Skill | Descripción | ⭐ Aprendizaje |
|-------|-------------|---------------|
| [arquitectura-dashboard-datos-api](arquitectura/arquitectura-dashboard-datos-api.md) | Patrón completo API → cache → dominio → REST → frontend | ESIOS |

---

## 🔧 Infraestructura

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [api-cliente-http-robusto](infraestructura/api-cliente-http-robusto.md) | Cliente HTTP con reintentos, backoff + jitter | ESIOS |
| [cache-multicapa-memoria-disco](infraestructura/cache-multicapa-memoria-disco.md) | Cache memoria + disco con TTL y métricas | ESIOS |
| [env-validacion-estricta](infraestructura/env-validacion-estricta.md) | Validación env vars con exit early + health checks | ESIOS |
| [docker-multistage-produccion](infraestructura/docker-multistage-produccion.md) | Dockerfile multistage para NaN.builders | ESIOS |
| [health-checks-metrics](infraestructura/health-checks-metrics.md) | /healthz, /readyz, /metrics | ESIOS |
| [seguridad-helmet-cors](infraestructura/seguridad-helmet-cors.md) | Helmet CSP + CORS + cache-busting CDNs | ESIOS |

---

## 🖥️ Backend / Dominio

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [fetch-paralelo-fallos-parciales](backend/fetch-paralelo-fallos-parciales.md) | Promise.allSettled + safe wrapper para N indicadores | ESIOS |
| [conversion-unidades-api-externa](backend/conversion-unidades-api-externa.md) | Conversión valores crudos (×10, ×1000) a humanos | ESIOS |
| [servicio-resumen-consolidado](backend/servicio-resumen-consolidado.md) | Resumen desde N series horarias con merge + stats | ESIOS |
| [endpoints-dashboard-rest](backend/endpoints-dashboard-rest.md) | Endpoints REST en español | ESIOS |
| [forecast-montecarlo-escenarios](backend/forecast-montecarlo-escenarios.md) | Monte Carlo + escenarios heurísticos | ESIOS |
| [nango-integracion-apis](backend/nango.md) | 🔄 **Mejorado** — 800+ APIs con OAuth managed, sync, proxy MCP | 🌙 Nocturno |
| [awesome-transport-datos](backend/awesome-transit.md) | 🔄 **Mejorado** — GTFS + GBFS + GTFS-RT + Haversine | 🌙 Nocturno |

---

## 🎨 Frontend

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [frontend-estado-persistencia](frontend/frontend-estado-persistencia.md) | AppState + URL hash + localStorage | ESIOS |
| [frontend-orquestacion-carga](frontend/frontend-orquestacion-carga.md) | AbortController, auto-refresh, render por secciones | ESIOS |
| [frontend-api-client-errores](frontend/frontend-api-client-errores.md) | Fetch genérico con manejo de errores | ESIOS |
| [frontend-tabs-navegacion](frontend/frontend-tabs-navegacion.md) | Tabs con teclado + redibujado de charts | ESIOS |
| [frontend-config-mapa-colores](frontend/frontend-config-mapa-colores.md) | techMap + INDICATORS_CONFIG centralizados | ESIOS |
| [frontend-fechas-timezone-local](frontend/frontend-fechas-timezone-local.md) | Fechas DST-safe para Europe/Madrid | ESIOS |

---

## 🧪 Testing

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [testing-jest-mocks-api](testing/testing-jest-mocks-api.md) | Jest + mocks HTTP + fixtures | ESIOS |

---

## 🤖 IA / Agentes

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [orca-multi-agente-orquestacion](ia/orca.md) | 🔄 **Mejorado** — Orquestación multi-agente con worktrees, DAG, gates | 🌙 Nocturno |
| [mlx-vlm-vision-local](ia/mlx-vlm.md) | 🔄 **Mejorado** — Visión local Mac: LLaVA, Pixtral, Florence-2, fine-tuning | 🌙 Nocturno |

---

## 🗄️ Datos / BI

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [metabase-dashboards-embebidos](data/metabase.md) | 🔄 **Mejorado** — BI embebido: SQL, embedding JWT, API REST, Metabot | 🌙 Nocturno |

---

## 🛠️ DevOps

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [postgres-mcp-servidor](devops/postgres-mcp.md) | 🔄 **Mejorado** — PostgreSQL como MCP con DTA index tuning | 🌙 Nocturno |
| [vidpipe-pipeline-video](devops/vidpipe.md) | 🔄 **Mejorado** — Pipeline vídeo AI 7 capas: transcripción → shorts → publicación | 🌙 Nocturno |

---

## 🗺️ GIS / Satélite

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [deteccion-satelite-sentinel](gis/deteccion-satelite.md) | 🆕 **Nuevo** — Procesamiento Sentinel-2: DRISH-X tráfico, NDVI, descarga | 🌙 Nocturno |

---

## 🔊 Audio / Voz

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [voicebox-estudio-voz-local](audio/voicebox.md) | 🔄 **Mejorado** — TTS multi-motor local, clonación zero-shot, MCP, REST | 🌙 Nocturno |

---

## Leyenda

| Icono | Significado |
|-------|-------------|
| ESIOS | Skill extraída del proyecto esios-dashboard (patrón validado 24K líneas) |
| 🌙 Nocturno | Skill descubierta/mejorada en sesiones nocturnas de aprendizaje autónomo |
| 🔄 **Mejorado** | Skill reescrita con patrón ESIOS: arquitectura, código real, ejemplos, pitfalls |
| 🆕 **Nuevo** | Skill creada desde cero con el patrón ESIOS |

---

## 💡 Para próximos proyectos (ej: BiciMAD + Mapa)

El flujo que usaría:

| Paso | Skills necesarias |
|------|-------------------|
| 1. Planificar arquitectura | `arquitectura-dashboard-datos-api` |
| 2. Cliente HTTP | `api-cliente-http-robusto` + `cache-multicapa-memoria-disco` |
| 3. Fetch 2 APIs en paralelo | `fetch-paralelo-fallos-parciales` (GBFS + CKAN) |
| 4. Servicio de fusión | `servicio-resumen-consolidado` (merge por station_id) |
| 5. Endpoints REST | `endpoints-dashboard-rest` + geo queries |
| 6. Frontend | `frontend-estado-persistencia` + `frontend-orquestacion-carga` |
| 7. Mapa Leaflet | Patrón de `awesome-transport-datos` (Haversine + clusters) |
| 8. Testing | `testing-jest-mocks-api` |
| 9. Deploy | `docker-multistage-produccion` + `seguridad-helmet-cors` |