---
name: metabase-dashboards-embebidos
description: "Patrón de dashboards embebidos con Metabase (47K⭐) — SQL queries, API REST, embedding, Metabot AI, y multi-base de datos. Ideal para BI sin servidor propio de frontend."
version: 2.0.0
author: Ntizar + Mastermind
---

# Metabase — Dashboards Embebidos con BI

Plataforma de Business Intelligence open-source (47K⭐) que permite crear dashboards interactivos desde SQL o constructor visual, embekerlos en apps propias, y exponerlos via API REST.

## Arquitectura

```
Bases de datos (PostgreSQL, MySQL, BigQuery, etc.)
        │
        ▼
    ┌─────────────┐
    │   Metabase   │ ← Metabot AI, SQL, Constructor visual
    │   Server     │
    └──────┬──────┘
           │
     ┌─────┴──────┐
     ▼             ▼
API REST       Embedding
(preguntas,    (iframe o
 dashboards,   JWT signed
 tarjetas)     en tu web)
```

## Instalación Rápida

```bash
# Docker (recomendado)
docker run -d -p 3000:3000 \
  -e MB_DB_TYPE=postgres \
  -e MB_DB_DBNAME=metabase \
  -e MB_DB_HOST=localhost \
  -e MB_DB_USER=metabase \
  -e MB_DB_PASS=secret \
  --name metabase metabase/metabase:latest

# O con docker-compose
```

## Patrón: API REST — Consultar datos desde Node.js

```javascript
// Consultar una pregunta (card) existente via API
const METABASE_URL = 'https://metabase.tudominio.com';
const API_KEY = process.env.METABASE_API_KEY;

async function queryCard(cardId, params = {}) {
  const resp = await fetch(`${METABASE_URL}/api/card/${cardId}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-KEY': API_KEY,
    },
    body: JSON.stringify({ parameters: params }),
  });
  if (!resp.ok) throw new Error(`Metabase ${resp.status}: ${await resp.text()}`);
  return resp.json(); // { data: { rows: [...], cols: [...] } }
}

// Ejemplo: query datos de ventas
const ventas = await queryCard(42, { mes: '2026-05' });
console.log(ventas.data.rows); // [[1234, "Mayo", 45000], ...]
```

## Patrón: Embedding Seguro con JWT

Embeber dashboards en tu app sin que los usuarios vean la interfaz de Metabase.

```javascript
const jwt = require('jsonwebtoken');

const METABASE_SECRET = process.env.METABASE_EMBEDDING_SECRET;
const METABASE_SITE_URL = 'https://metabase.tudominio.com';

function getEmbeddedUrl(dashboardId, params = {}) {
  const payload = {
    resource: { dashboard: dashboardId },
    params,
    exp: Math.round(Date.now() / 1000) + 60 * 10, // 10 min
  };
  const token = jwt.sign(payload, METABASE_SECRET);
  return `${METABASE_SITE_URL}/embed/dashboard/${token}#bordered=false&titled=false`;
}

// Render en frontend
// <iframe src="${getEmbeddedUrl(5, { tienda: 'Madrid' })}"
//   width="100%" height="800" frameborder="0"></iframe>
```

## Patrón: Metabot AI (consulta en lenguaje natural)

```javascript
// Preguntar a Metabase en lenguaje natural
async function askMetabase(question, databaseId) {
  const resp = await fetch(`${METABASE_URL}/api/mbac`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-KEY': API_KEY,
    },
    body: JSON.stringify({
      database_id: databaseId,
      question,
    }),
  });
  return resp.json(); // { answer: "...", sql: "...", visualization: "..." }
}

// Uso: askMetabase("¿Cuántas estaciones BiciMAD tienen menos de 3 bicis?")
```

## Patrón: Alertas Programadas

```javascript
// Crear alerta por email cuando un resultado cambia
async function createAlert(cardId, channel = 'email') {
  await fetch(`${METABASE_URL}/api/alert`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-KEY': API_KEY,
    },
    body: JSON.stringify({
      card: { id: cardId },
      channels: [{ channel_type: channel }],
      alert_condition: 'goal',
      alert_first_only: false,
    }),
  });
}
```

## Buenas prácticas

1. **Dos modos de consulta** — SQL (control total) o constructor visual (no-code)
2. **embedding JWT** — más seguro que embedding público, filtrar por usuario
3. **API Key para server-to-server** — no exponer en frontend
4. **Caché de resultados** — Metabase cachea queries (configurable)
5. **Metabot solo para queries simples** — SQL nativo para consultas complejas
6. **Parámetros con tipo** — fecha, número, texto, categoría, ubicación

## Tabla comparativa: Metabase vs ESIOS Dashboard

| Aspecto | Metabase | ESIOS Dashboard |
|---------|----------|----------------|
| **Query** | SQL / visual builder | API REST custom |
| **Frontend** | Auto-generado + embed | Custom (vanilla JS) |
| **Base datos** | 25+ (Postgres, MySQL, etc.) | API externa (no DB) |
| **Cache** | Integrado | Custom (memoria + disco) |
| **Auth** | Email, SSO, JWT embedding | Token API + env vars |
| **Alertas** | Email, Slack, webhook | N/A |
| **Cuando usar** | Datos en DB, BI general | APIs específicas, control total |

## Pitfalls

- ❌ **No exponer API Key** — Metabase API key da acceso de admin
- ❌ **embedding JWT expira** — regenerar token antes de que caduque
- ❌ **Caché demasiado larga** — datos stale para dashboards en tiempo real
- ❌ **Metabot sin contexto** — necesita nombres de tablas claros en la DB
- ❌ **Muchos embeddings** — cada iframe carga recursos del servidor

## Referencia

- Web: https://metabase.com
- Repo: https://github.com/metabase/metabase (47K⭐)
- API Docs: https://www.metabase.com/docs/latest/api-documentation
- Skills relacionadas: backend/endpoints-dashboard-rest, frontend/estado-persistencia