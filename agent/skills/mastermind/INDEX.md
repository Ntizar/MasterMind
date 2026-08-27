---
name: skills-catalogo
description: "Catálogo completo de skills extraídos del proyecto ESIOS Dashboard — patrones reutilizables para APIs, dashboards, forecast, frontend y testing."
version: 1.0.0
author: Ntizar
---

# Catálogo de Skills — ESIOS Dashboard

> 20 skills extraídas del proyecto [esios-dashboard](https://github.com/Ntizar/esios-dashboard) (24.469 líneas, Node.js + vanilla JS + Chart.js).
> Proyecto de referencia para todos los próximos dashboards con APIs externas.

## Arquitectura 🏗️

| Skill | Descripción |
|-------|-------------|
| [arquitectura-dashboard-datos-api](arquitectura/arquitectura-dashboard-datos-api.md) | Patrón completo: desde la API externa hasta el dashboard renderizado |

## Infraestructura 🔧

| Skill | Descripción |
|-------|-------------|
| [api-cliente-http-robusto](infraestructura/api-cliente-http-robusto.md) | Cliente HTTP con reintentos, backoff exponencial y jitter |
| [cache-multicapa-memoria-disco](infraestructura/cache-multicapa-memoria-disco.md) | Cache en memoria + disco con TTL y métricas de hit rate |
| [env-validacion-estricta](infraestructura/env-validacion-estricta.md) | Validación de variables de entorno con exit early y health checks |
| [docker-multistage-produccion](infraestructura/docker-multistage-produccion.md) | Dockerfile multistage para NaN.builders con usuario no-root |
| [health-checks-metrics](infraestructura/health-checks-metrics.md) | /healthz, /readyz y /metrics para monitorización |
| [seguridad-helmet-cors](infraestructura/seguridad-helmet-cors.md) | Helmet CSP + CORS + cache-busting para CDNs (Chart.js, Google Fonts) |

## Backend / Dominio 🖥️

| Skill | Descripción |
|-------|-------------|
| [fetch-paralelo-fallos-parciales](backend/fetch-paralelo-fallos-parciales.md) | Promise.allSettled con safe wrapper para N indicadores en paralelo |
| [conversion-unidades-api-externa](backend/conversion-unidades-api-externa.md) | Conversión de valores crudos (×10, ×1000) a unidades humanas |
| [servicio-resumen-consolidado](backend/servicio-resumen-consolidado.md) | Resumen consolidado desde múltiples series horarias con merge y stats |
| [endpoints-dashboard-rest](backend/endpoints-dashboard-rest.md) | Endpoints REST en español: summary, indicator, monthly, yearly, forecast |
| [forecast-montecarlo-escenarios](backend/forecast-montecarlo-escenarios.md) | Monte Carlo + escenarios heurísticos con drivers externos |

## Frontend 🎨

| Skill | Descripción |
|-------|-------------|
| [frontend-estado-persistencia](frontend/frontend-estado-persistencia.md) | AppState global + URL hash + localStorage |
| [frontend-orquestacion-carga](frontend/frontend-orquestacion-carga.md) | AbortController, auto-refresh, renderizado por secciones |
| [frontend-api-client-errores](frontend/frontend-api-client-errores.md) | Cliente fetch genérico con manejo de errores y signal |
| [frontend-tabs-navegacion](frontend/frontend-tabs-navegacion.md) | Sistema de pestañas con atajos de teclado y redibujado de charts |
| [frontend-config-mapa-colores](frontend/frontend-config-mapa-colores.md) | techMap + INDICATORS_CONFIG centralizados con colores y órdenes |
| [frontend-fechas-timezone-local](frontend/frontend-fechas-timezone-local.md) | Utilidades de fecha/hora DST-safe para Europe/Madrid |

## Testing 🧪

| Skill | Descripción |
|-------|-------------|
| [testing-jest-mocks-api](testing/testing-jest-mocks-api.md) | Tests con Jest, mocks de API HTTP y fixtures de datos |

---

# ¿Cómo usar estas skills?

1. **Navega por categorías** — cada skill tiene código real extraído del proyecto
2. **Usa las skills en Hermes** — se cargan automáticamente en el sistema Mastermind
3. **Para nuevos proyectos**: sigue el patrón `arquitectura-dashboard-datos-api.md` como guía general, luego consulta cada capa según la necesites

# Próximos proyectos

- Dashboard con 2 APIs + mapa (Leaflet/MapLibre)
- Forecast con más drivers externos
- Pipeline de datos automatizado (cron + API)