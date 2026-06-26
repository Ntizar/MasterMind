# Plan de Ecosistema `@nous/*` — 2026-06-14

## Contexto

David quiere construir proyectos multi-usuario (ERPs, SaaS) sin arrastrar deuda técnica entre proyectos. Propone un ecosistema de módulos reutilizables como LEGO, similar a Aurora Design System pero para backend.

## Análisis de GitHub Stars (99 stars)

### Temas recurrentes identificados

1. **Arquitectura modular/plugin-based** — QueAI (plug-and-play Docker modules), NocoBase (business systems), Huly (all-in-one)
2. **Multi-tenant/multi-usuario** — Twenty (CRM), EspoCRM, SuiteCRM, Huly
3. **API integrations como producto** — Nango (10K stars), Postgres MCP
4. **Data privacy/security** — Microsoft Presidio (8.6K stars)
5. **3D + geoespacial** — GeoLibre, Three.js, maptalks.three
6. **AI Agent ecosystem** — Supermemory (27K), SkillSpector

### Dirección confirmada

Sistemas de negocio modulares con integraciones de APIs, multi-usuario, 3D/geoespacial, y seguridad de datos.

## Auditoría de Proyectos

### MasterFit v4 — CRÍTICA (no extraer)
- Monolito de 1022 líneas
- PINs en texto plano
- SQL injection potencial
- Sin tests
- Sync GitHub en cada write

### ESIOS Dashboard v2 — MODERADA (candidato)
- Arquitectura modular con 7 servicios
- Tests Jest
- Cache memory+disk con métricas
- Health checks
- IDs de indicadores duplicados (menor)

### TerrAn — NINGUNA (solo docs)
- 110K+ caracteres de documentación
- Arquitectura ambiciosa pero sin código
- Riesgo de over-engineering

## Auditoría Detallada Módulo por Módulo

### 🔴 P0 — Base

| Módulo | Semáforo | Código Fuente | Líneas | Tests | Calidad |
|--------|----------|---------------|--------|-------|---------|
| **`Adela_env`** | 🟡 | ESIOS `src/config/env.js` | 35 | 21 líneas | Básico, hardcodea ESIOS_API_TOKEN |
| **`Adela_time`** | 🟢 | ESIOS `src/shared/time/madrid.js` | 215 | 62 líneas | Excelente: 9 funciones, edge cases, validación ISO |
| **`Adela_http`** | 🟢 | ESIOS `src/infra/clients/esios.client.js` | 236 | — | Muy bueno: batching, retries, backoff, jitter |

### 🟡 P1 — Infraestructura

| Módulo | Semáforo | Código Fuente | Líneas | Tests | Calidad |
|--------|----------|---------------|--------|-------|---------|
| **`Adela_cache`** | 🟢 | ESIOS `memory-cache.js` + `disk-cache.js` | 184 | — | Dual cache con métricas, TTL, stats |
| **`Adela_health`** | 🟡 | ESIOS `server.js` (~2 endpoints) | 20 | — | Mínimo: healthz + readyz, sin checks modulares |
| **`Adela_auth`** | 🔴 | MasterFit `server.js` (1022 líneas total) | ~80 | — | **CRÍTICO:** PINs texto plano, SQL injection, sin bcrypt |

### 🟢 P2 — Productividad

| Módulo | Semáforo | Código Fuente | Líneas | Tests | Calidad |
|--------|----------|---------------|--------|-------|---------|
| **`Adela_export`** | 🟡 | ESIOS `csv.repository.js` | 65 | — | Solo CSV, pdfkit en deps pero sin usar |
| **`Adela_ai`** | 🟡 | ESIOS `report.service.js` | 210 | — | Específico de ESIOS, NaN API solo |
| **`Adela_db`** | ❌ | No existe | 0 | — | Crear desde cero (SQLite → PostgreSQL) |

### 🔵 P3 — Mejora

| Módulo | Semáforo | Código Fuente | Líneas | Tests | Calidad |
|--------|----------|---------------|--------|-------|---------|
| **`Adela_i18n`** | ❌ | No existe | 0 | — | Crear desde cero, es-ES por defecto |

## Deuda Técnica de Proyectos Fuente

| Proyecto | Problema | Severidad | Impacto |
|----------|----------|-----------|---------|
| **MasterFit** | Monolito 1022 líneas (todo mezclado: auth, DB, CRUD, IA, export) | 🔴 Crítico | No extraer nada directo |
| **MasterFit** | PINs en texto plano | 🔴 Crítico | Reescribir auth completo con bcrypt |
| **MasterFit** | SQL injection potencial (campos dinámicos sin validación) | 🔴 Crítico | No reusar queries existentes |
| **MasterFit** | Sin tests, sin contrato verificable | 🟡 Importante | Reescribir con tests desde cero |
| **ESIOS** | env.js hardcodea ESIOS_API_TOKEN como único required | 🟢 Menor | Fácil de generalizar |
| **ESIOS** | esios.client.js hardcodea URL, headers y token name de ESIOS | 🟢 Menor | Fácil de generalizar |
| **ESIOS** | package.json tiene pdfkit como dep pero no se usa para PDF | 🟢 Menor | Añadir export PDF real |

## Plan de Implementación por Fases

### Fase 1: Base (semana 1) — P0
```
Adela_env → Crear desde cero con validación estricta, defaults, .env automático
Adela_time → Extraer de ESIOS madrid.js, añadir isWeekend/nextBusinessDay/timeAgo
Adela_http → Extraer de ESIOS esios.client.js, generalizar (URL configurable, headers custom)
```

### Fase 2: Infraestructura (semana 2) — P1
```
Adela_cache → Unificar memory + disk cache bajo interfaz común { get, set, delete, clear, metrics }
Adela_health → Estandarizar healthz/readyz con checks modulares registrables
Adela_auth → REESCRIBIR: bcrypt + JWT + refresh tokens + middleware Express + rate limiting
```

### Fase 3: Productividad (semana 3) — P2
```
Adela_export → Ampliar CSV → JSON + PDF (usar pdfkit ya disponible) + ZIP batch
Adela_ai → Generalizar proxy LLM: NaN + OpenRouter + OpenAI compatible
Adela_db → Abstracción driver-agnóstica: SQLite (sql.js) → PostgreSQL + migraciones versionadas
```

### Fase 4: Polish (semana 4) — P3 + CI/CD
```
Adela_i18n → Locales JSON, t() function, detección automática de locale
CI/CD → GitHub Actions lint+test, npm publish, README sección Integración
```

## Template de Módulo (con detalles)

```
@nous/{nombre}/
├── package.json          # name: "@nous/{nombre}", version: "1.0.0"
├── README.md             # Quick start + API reference + Integración con otros módulos
├── src/
│   ├── index.ts          # Exports públicos
│   ├── impl.ts           # Implementación
│   └── types.ts          # Interfaces públicas
├── tests/
│   └── impl.test.ts      # Tests obligatorios (cobertura mínima 80%)
└── dist/                 # Build output (JS + .d.ts)
```

## Recomendaciones Clave

1. **Empezar por Adela_time** — es el más maduro, código listo, tests existentes. Victoria rápida.
2. **Adela_auth NO se extrae de MasterFit** — reescribir completo con bcrypt + JWT.
3. **TypeScript first** — tipos para todo, JS vanilla compatible con JSDoc.
4. **Un repo por módulo** — `github.com/Ntizar/Adela_time`, etc.
5. **Test coverage mínimo 80%** antes de considerar un módulo "estable".
6. **Zero dependencies entre módulos** — cada módulo funciona standalone.

## Decisiones Pendientes

1. **Namespace:** `@nous/*` (NosUnus = "Nosotros Uno")
2. **Monorepo vs Multi-repo:** Monorepo con workspaces primero
3. **TypeScript vs JS vanilla:** TypeScript first con build
4. **Deploy:** npm privado en NaN

## Template de Módulo

```
@nous/{nombre}/
├── package.json          # name: "@nous/{nombre}", version: "1.0.0"
├── README.md             # Quick start + API reference
├── src/
│   ├── index.ts          # Exports públicos
│   ├── impl.ts           # Implementación
│   └── types.ts          # Interfaces públicas
├── tests/
│   └── impl.test.ts      # Tests obligatorios
└── dist/                 # Build output (JS + .d.ts)
```

## Principios No Negociables

1. Zero dependencies entre módulos
2. Tests obligatorios para cada módulo
3. SemVer estricto
4. README con ejemplos de quick start
5. TODO en castellano
6. NO extraer deuda técnica — reescribir desde cero
