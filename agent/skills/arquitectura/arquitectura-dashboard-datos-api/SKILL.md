---
name: arquitectura-dashboard-datos-api
description: "Arquitectura completa de un dashboard web que consume APIs de datos externas. Patrón inspirado en ESIOS Dashboard — estructura de 5 capas: config, infra, dominio, shared, presentación."
version: 1.1.0
author: Ntizar
references:
  - references/esios-project-structure.md - Proyecto ESIOS de referencia: estructura real, arquitectura en capas, tabla de patrones extraídos y métricas (24.469 líneas, 41 archivos)
license: MIT
metadata:
  hermes:
    tags: [arquitectura, dashboard, api, patron, esios]
    related_skills: [api-cliente-http-robusto, cache-multicapa-memoria-disco, fetch-paralelo-fallos-parciales, servicio-resumen-consolidado]
---

# Arquitectura Dashboard con Datos de APIs Externas

Patrón validado en el proyecto ESIOS Dashboard (24.469 líneas, Node.js + HTML vanilla + Chart.js).

## Flujo completo del dato

```
API externa (ESIOS/REE)
    │
    ▼
[Cliente HTTP] → reintentos, backoff, jitter
    │
    ├──► [Cache Disco] → persiste respuestas (TTL)
    │
    ▼
[Servicio Dominio] → normalización, conversión unidades, merge
    │
    ├──► [Cache Memoria] → LRU con métricas (hits/misses)
    │
    ▼
[API REST] → /api/v1/summary, /api/v1/indicator, /healthz, /readyz
    │
    ▼
[Frontend Vanilla] → state.js → data.js → api.js → render*.js
```

## Principios clave

### 1. Capa de cliente API independiente
- Un solo módulo `clients/api.client.js` que maneja HTTP, reintentos, tokens
- NUNCA mezclar lógica de negocio con fetch
- Siempre cachear antes de retornar

### 2. Cache multicapa defensiva
- **Capa 1 (memoria)**: responde en <1ms, ideal para requests repetidos en misma sesión
- **Capa 2 (disco)**: persiste entre reinicios, reduce peticiones a la API externa
- Ambas con TTL configurable y mecanismo de limpieza

### 3. Dominio separado de infraestructura
- `src/domains/` → lógica de negocio (resumen, forecast, agregación)
- `src/infra/` → caché, clientes HTTP, repositorios
- `src/shared/` → utilidades transversales (timezones, unidades)
- `src/config/` → validación de entorno

### 4. Frontend sin framework, con estado centralizado
- `AppState` global → única fuente de verdad
- Persistencia en URL hash + localStorage
- Carga orquestada desde `data.js`, render delegado a módulos especializados

### 5. Contrato API estable
- Endpoints con nombres en español
- Estructura de respuesta documentada en README
- versionado semántico en los datos

## Cuándo aplicar este patrón

- Dashboards con datos de APIs externas (1 o múltiples fuentes)
- Proyectos que necesitan forecast/análisis sobre datos históricos
- Cuando quieres cache agresiva para no malgastar créditos de API
- Cuando necesitas que funcione sin frameworks pesados (vanilla JS)

## Anti-patrones que evitar

- ❌ Llamar a la API externa desde el frontend (expone tokens)
- ❌ Mezclar lógica de cache con lógica de negocio
- ❌ No validar fechas/timezones (todo dashboard tiene fechas)
- ❌ Un solo punto de fallo en el fetch paralelo (usar Promise.allSettled + fetchIndicatorSafe)

## Referencia

- Proyecto ESIOS Dashboard: github.com/Ntizar/esios-dashboard
- Skills relacionadas: api-cliente-http-robusto, cache-multicapa-memoria-disco, fetch-paralelo-fallos-parciales, servicio-resumen-consolidado
