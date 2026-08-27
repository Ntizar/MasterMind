# ESIOS Dashboard — Estructura de proyecto real

Proyecto de referencia que generó 20 patrones extraíbles. 24.469 líneas totales.

```
esios-work/
├── server.js                    # Express: bootstrap, middlewares (Helmet, CORS, logger),
│                                #   routes mount, /healthz, /readyz, /metrics
├── Dockerfile                   # Multi-stage (node:20-alpine), usuario no-root, HEALTHCHECK
├── .env.example                 # Template de variables de entorno
├── .dockerignore                # Excluye .env, node_modules, .git
├── package.json                 # Express, helmet, dotenv, csv, pdfkit, jest
├── public/
│   ├── index.html               # Single-page dashboard (tabs + gráficos + tabla)
│   ├── css/
│   │   └── styles.css           # Liquid glass + azul #2563eb + naranja #f97316
│   └── js/
│       ├── config.js            # Constantes: colores, techKeys, techLabels, endpoints
│       ├── state.js             # AppState: persistencia vía URL hash + localStorage
│       ├── utils.js             # formatNum, getMadridHour, avg, fmtHora, priceColor...
│       ├── api.js               # Cliente fetch genérico con errores, timeout, retry
│       ├── data.js              # Orquestación: carga paralela + auto-refresh + fallos parciales
│       ├── render.js            # Render HTML: tabs, resumen, tabla horaria, estado
│       ├── render-charts.js     # Chart.js: precio, demanda, generación, CO2, previsiones
│       └── ui.js                # UI: skeletons, loading, errores, tooltips
├── src/
│   ├── config/
│   │   └── env.js               # Validación estricta con exit early
│   ├── domains/
│   │   ├── energy/
│   │   │   ├── energy.service.js      # Datos energéticos: precios, demanda, generación
│   │   │   └── summary.service.js      # Resumen consolidado desde N series horarias
│   │   ├── forecast/
│   │   │   ├── price-forecast.service.js  # Predicción con Monte Carlo multicescenario
│   │   │   └── montecarlo.service.js      # Simulación Monte Carlo pura (1000 iteraciones)
│   │   └── reports/
│   │       └── report.service.js      # Generación de informes vía IA (NAN_API_KEY)
│   ├── infra/
│   │   ├── cache/
│   │   │   ├── memory-cache.js   # Cache en memoria con TTL, métricas
│   │   │   └── disk-cache.js     # Cache en disco para datos pesados
│   │   └── clients/
│   │       ├── esios.client.js   # Cliente HTTP ESIOS con retry, backoff, jitter
│   │       └── nan.client.js     # Cliente HTTP NAN API para informes IA
│   ├── jobs/
│   │   └── sync-indicators.js    # Sincronización nocturna de indicadores ESIOS
│   └── shared/
│       ├── esios-units.js        # Conversión de unidades: ×1, ×10, ×1000, especiales
│       ├── time/
│       │   └── madrid.js         # Timezone Europe/Madrid, hora solar/horaria
│       ├── io/
│       │   ├── csv.repository.js     # Persistencia CSV local
│       │   └── cache-bust.js         # Cache-busting endpoint (/js/cache-bust.js)
│       └── validation/
│           └── date.validator.js # Validación de fechas formato YYYY-MM-DD
├── data/
│   ├── all-esios-indicators.json
│   ├── esios-indicator-index.json
│   └── esios-indicator-index.md
├── scripts/
│   ├── fetch-esios.js           # Script para fetch de indicadores ESIOS
│   ├── montecarlo.js            # Script CLI de montecarlo
│   └── telegram/                # Envío de informes a Telegram
├── tests/
│   ├── services/
│   │   ├── summary.service.test.js   # Tests de resumen consolidado
│   │   ├── energy.service.test.js    # Tests de energía
│   │   └── montecarlo.service.test.js # Tests de Monte Carlo
│   └── clients/
│       └── esios.client.test.js # Tests de cliente HTTP con mocks
└── .github/
    └── workflows/
        └── deploy.yml           # CI/CD para NaN.builders
```

## Arquitectura en capas

```
┌─────────────────────────────────────────────────────┐
│                  PUBLIC (frontend)                   │
│  index.html → config.js → state.js → api.js        │
│             → data.js → utils.js → render.js        │
│             → render-charts.js → ui.js              │
│             → styles.css (liquid glass)             │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/JSON
┌──────────────────────▼──────────────────────────────┐
│               SERVER (Express + Middleware)          │
│  Helmet → CORS → Logger → Router → /healthz        │
│  /readyz → /api/esios/* → /metrics                 │
└──────┬─────────────────────────┬────────────────────┘
       │                         │
┌──────▼──────────┐    ┌────────▼────────────────────┐
│    DOMAIN        │    │      INFRASTRUCTURE          │
│  energy/         │    │  cache/: memory-cache       │
│  forecast/       │    │           disk-cache         │
│  reports/        │    │  clients/: esios.client     │
│  summary.service │    │            nan.client        │
└──────┬───────────┘    └────────┬────────────────────┘
       │                         │
       └──────────┬──────────────┘
                  │
         ┌────────▼────────┐
         │   SHARED        │
         │  esios-units.js │
         │  time/madrid.js │
         │  io/csv.*.js    │
         │  validation/*   │
         └─────────────────┘
```

## Patrones clave extraídos

| Patrón | Skill asociado |
|---|---|
| Arquitectura 5 capas | `arquitectura-dashboard-datos-api` |
| Cliente HTTP con retry + jitter | `api-cliente-http-robusto` |
| Cache en memoria + disco con TTL | `cache-multicapa-memoria-disco` |
| Validación de env con exit early | `env-validacion-estricta` |
| Docker multi-stage non-root | `docker-multistage-produccion` |
| Health + readiness checks | `health-checks-metrics` |
| Helmet + CORS + CSP | `seguridad-helmet-cors` |
| Fetch paralelo con fallos parciales | `fetch-paralelo-fallos-parciales` |
| Conversión de unidades API externa | `conversion-unidades-api-externa` |
| Resumen consolidado desde N series | `servicio-resumen-consolidado` |
| Endpoints REST en español | `endpoints-dashboard-rest` |
| Monte Carlo con escenarios | `forecast-montecarlo-escenarios` |
| Estado + persistencia URL hash | `frontend-estado-persistencia` |
| Orquestación carga + auto-refresh | `frontend-orquestacion-carga` |
| Cliente fetch genérico frontend | `frontend-api-client-errores` |
| Tabs navegación teclado | `frontend-tabs-navegacion` |
| Mapa colores + etiquetas centralizado | `frontend-config-mapa-colores` |
| Fechas en timezone local | `frontend-fechas-timezone-local` |
| Tests con mocks HTTP + fixtures | `testing-jest-mocks-api` |

## Métricas del proyecto

- **Total archivos**: 41
- **Total líneas**: 24.469
- **Lenguajes**: JavaScript (77%), CSS (12%), HTML (8%), Markdown (3%)
- **Frontend**: 8 ficheros JS modulares (~3.000 líneas)
- **Backend**: 12 ficheros src/ (~4.000 líneas)
- **Tests**: 4 ficheros (~1.200 líneas)
- **Cobertura**: 24/24 tests passing