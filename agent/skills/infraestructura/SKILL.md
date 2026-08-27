---
name: infraestructura-nodejs
version: "1.0.0"
description: "Patrones de infraestructura para aplicaciones Node.js en producción — cliente HTTP resiliente, cache multicapa, validación de config, health checks, seguridad Helmet/CORS y Docker multistage."
tags: [infraestructura, nodejs, patrones, produccion, http, cache, seguridad, docker, health]
---

# Infraestructura Node.js — Patrones de Producción

Colección de patrones de infraestructura para aplicaciones Node.js en producción. Cada patrón es un bloque independiente que se combina con los demás.

## 1. Cliente HTTP Robusto

Cliente HTTP con reintentos, backoff exponencial + jitter y timeouts. Para consumir APIs externas de forma resiliente.

- **Reintentos:** configurable (default 3), solo para 5xx y errores de red
- **Backoff exponencial:** baseDelay × 2^n, con jitter para evitar thundering herd
- **Timeout agresivo:** 8s por defecto, proporcional al número de requests en paralelo
- **Solo reintentar errores transitorios:** 4xx = error del cliente, no se retryean

## 2. Cache Multicapa (Memoria + Disco)

Patrón de cachear datos de APIs externas en dos capas: memoria (rápida, volátil) y disco (lenta, persistente). Cada capa tiene su propio TTL.

- **Flujo:** memoria → disco → API
- **Promover disco a memoria:** cuando se lee del disco, cargar en memoria
- **TTL uniforme:** mismo TTL en ambas capas para evitar inconsistencias
- **Métricas:** hit rate, misses, tamaño

## 3. Validación Estricta de Config

Validar y centralizar la configuración de una aplicación al arrancar. Falla rápido si falta algo, convierte tipos explícitamente, expone readiness check.

- **Exit early:** si falta variable obligatoria, exit(1) con mensaje claro
- **Renombrar para consistencia:** `ESIOS_API_TOKEN` (externo) → `ESIOS_TOKEN` (interno)
- **Parseo explícito:** `parseInt` para números, `.split(',')` para listas
- **.env.example en Git:** documentación viva de qué necesita el proyecto

## 4. Health Checks + Métricas

Tres endpoints estándar: `/healthz` (liveness), `/readyz` (readiness), `/metrics` (Prometheus).

- **/healthz:** ¿Vivo? Siempre 200 mientras el proceso esté funcionando
- **/readyz:** ¿Listo? 200 o 503 según dependencias externas
- **/metrics:** Formato Prometheus para Grafana/Prometheus scrape

## 5. Seguridad Web (Helmet + CORS)

Configurar seguridad HTTP en Express: CSP, HSTS, CORS por lista blanca, protección contra payloads grandes.

- **CSP mínimo:** solo permitir CDNs que realmente se usan
- **Minimizar 'unsafe-inline':** necesario para Chart.js, pero cada uno es riesgo XSS
- **CORS por lista blanca:** nunca usar `'*'` en producción
- **Cache-busting:** forzar no-cache en HTML/JS para que usuarios descarguen versión reciente

## 6. Docker Multistage para Producción

Dockerfile multistage para Node.js con usuario no-root, health checks y build optimizado.

- **Alpine como base:** imágenes ~5MB vs ~900MB completa
- **npm ci en vez de npm install:** builds 100% reproducibles
- **Usuario no-root:** seguridad por defecto
- **HEALTHCHECK:** permite detectar caídas automáticamente

## Integración entre patrones

```javascript
// 1. Validar config al arrancar
const env = loadEnv(); // validacion-config-estricta

// 2. Crear cliente HTTP robusto
const httpClient = createHttpClient({
  maxRetries: 3, baseDelay: 1000, timeout: 8000
}); // cliente-http-robusto

// 3. Crear cache multicapa
const cache = new MultiLayerCache({ ttlMs: env.CACHE_TTL_MS }); // cache-multicapa

// 4. Configurar seguridad
app.use(helmet({ /* seguridad-web-helmet-cors */ }));

// 5. Exponer health checks
app.get('/healthz', ...); // health-checks-metrics
app.get('/readyz', ...);
app.get('/metrics', ...);

// 6. Deploy con Docker multistage
// (docker-multistage-produccion)
```

## Pitfalls generales

- ❌ Timeout menor que latencia real → funciona en dev (cache), falla en prod (sin cache)
- ❌ Deploy con timeout menor que la latencia real → funciona en dev (cache), falla en prod (sin cache)
- ❌ healthz y readyz iguales → no detectas tokens caídos o APIs fuera de línea
- ❌ CORS con `'*'` en producción → cualquiera puede llamar a tu API
- ❌ `npm install` en vez de `npm ci` → build no reproducible
- ❌ Usuario root en contenedor → si hay vulnerabilidad, el atacante tiene root
- ❌ Sin HEALTHCHECK → la plataforma no detecta si la app está caída
- ❌ CSP demasiado restrictivo → CDNs no cargan (fonts.googleapis.com, cdn.jsdelivr.net)
- ❌ Sin jitter en reintentos → thundering herd: todos reintentan al mismo tiempo