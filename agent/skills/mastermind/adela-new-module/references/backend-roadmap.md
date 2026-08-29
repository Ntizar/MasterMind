# Roadmap: Adela como Backend Enterprise

> **Origen:** Sesión 2026-06-15 — David Antizar
> **Propósito:** Transformar Adela de ecosistema de piezas básicas a backend framework enterprise
> **Estado:** Pendiente de implementar

## Filosofía

El roadmap no es crear módulos aislados, sino **un stack cohesivo donde cada capa se apoya en la anterior**:

```
API Layer ───→ Adela_pagination · Adela_router
     ↑
Seguridad ───→ Adela_security · Adela_rateLimit · Adela_validation
     ↑
Observabilidad → Adela_logger · Adela_errors
     ↑
Escalabilidad ─→ Adela_db_pg · Adela_cache_redis
     ↑
     Core existente (Adela_auth · Adela_health · Adela_ai · Adela_db · Adela_cache · Adela_http · ...)
```

## FASE 1 (2 semanas): SEGURIDAD

### Adela_security
- **Helmet**: headers de seguridad HTTP (CSP, X-Frame-Options, HSTS, etc.)
- **CSRF**: tokens anti-CSRF para formularios y APIs
- **CORS**: configuración granular de orígenes permitidos
- **Sanitización**: limpieza de inputs contra XSS/inyección
- API: `createSecurity(config?) → Security` con middleware Express
- Dependencias: `helmet`, `csrf-csrf` (o similar ligero)
- Tests: mínimo 15

### Adela_rateLimit
- **Sliding window**: ventana deslizante por IP/usuario
- **Redis backend**: rate limiting distribuido (fallback a memoria)
- **Tiers**: configuración por ruta (pública, auth, admin)
- **Headers**: RateLimit-Remaining, Retry-After
- API: `createRateLimiter(config?) → rateLimitMiddleware`
- Dependencias: opcional — Redis client si se usa caché distribuida
- Tests: mínimo 12

### Adela_validation
- **Schemas Zod**: validación declarativa de inputs
- **Middleware Express**: `validate(schema)` para req.body, req.query, req.params
- **Mensajes**: errores en castellano
- **Saneamiento**: trim, lowercasing, default values
- API: `createValidator(schemas) → { validate, sanitize }`
- Dependencias: `zod`
- Tests: mínimo 15

## FASE 2 (1 semana): OBSERVABILIDAD

### Adela_logger
- **Niveles**: debug, info, warn, error, fatal
- **Salida dual**: consola (desarrollo) + archivo rotativo (producción)
- **Formato JSON**: cada log como objeto parseable (timestamp, level, module, message, context)
- **Rotación**: por tamaño (10MB) o tiempo (diario), con retención configurable
- **Correlación**: request ID injection via AsyncLocalStorage
- API: `createLogger(config?) → Logger`
- Dependencias: ninguna (Node fs nativo + process)
- Tests: mínimo 15

### Adela_errors
- **Jerarquía**: AppError, ValidationError, AuthError, NotFoundError, RateLimitError
- **Middleware Express**: error handler centralizado con stack trace controlado
- **Códigos**: error.code estandarizado para frontend
- **Recovery**: graceful degradation (no crash ante errores no críticos)
- API: `createErrorHandler(config?) → { errorMiddleware, AppError, ... }`
- Dependencias: ninguna
- Tests: mínimo 12

## FASE 3 (2 semanas): ESCALABILIDAD

### Adela_db_pg
- **PostgreSQL adapter**: mismo interfaz que Adela_db (sqlite), pero para Postgres
- **Pool de conexiones**: gestión de pool con pg-pool
- **Migraciones**: reutilizar sistema de migraciones de Adela_db
- **Transacciones**: soporte nativo de BEGIN/COMMIT/ROLLBACK
- API: `createPgAdapter(config?) → PgAdapter` (interfaz compatible con Adela_db)
- Dependencias: `pg`
- Tests: mínimo 15 (con testcontainers o mock)

### Adela_cache_redis
- **Caché distribuida**: mismo interfaz que Adela_cache, pero con Redis
- **TTL**: expiración automática de claves
- **Fallback**: timeout de Redis → fallback a memoria
- **Patrones**: cache-aside, rate limiting distribuido
- API: `createRedisCache(config?) → RedisCache` (interfaz compatible con Adela_cache)
- Dependencias: `ioredis`
- Tests: mínimo 12

## FASE 4 (1 semana): API LAYER

### Adela_pagination
- **Cursor-based**: paginación por cursor (recomendada para lists grandes)
- **Offset-based**: paginación por offset (compatible con tablas SQL)
- **Middleware**: parseo automático de query params (?cursor, ?limit, ?offset)
- **Metadata**: total, hasMore, nextCursor en cada respuesta
- API: `createPagination(config?) → { paginate, cursorPaginate, offsetPaginate }`
- Dependencias: ninguna
- Tests: mínimo 15

### Adela_router
- **Versionado**: `/v1/`, `/v2/` automático
- **OpenAPI/Swagger**: generación de spec desde schemas Zod
- **Route groups**: agrupación de rutas con prefijo + middleware común
- **Docs UI**: Swagger UI embebido en `/docs`
- API: `createRouter(config?) → Router` (wrapper de Express.Router)
- Dependencias: `swagger-ui-express`, `zod-to-json-schema` (o similar)
- Tests: mínimo 15

## Stack de dependencias entre fases

```
Adela_router ─────────────→ Adela_pagination
     ↑                            ↑
     ├── Adela_security           │
     ├── Adela_rateLimit ─────────┘
     ├── Adela_validation
     ├── Adela_logger
     └── Adela_errors
              ↑
         Adela_db_pg · Adela_cache_redis
              ↑
    (módulos existentes: Adela_auth, Adela_health, Adela_ai, Adela_db, Adela_cache, Adela_http, ...)
```

## Orden de implementación recomendado

1. `Adela_validation` (base para security y router)
2. `Adela_logger` (base para todo — empezar a loguear desde el principio)
3. `Adela_errors` (base para express middleware)
4. `Adela_security` (usa validation + logger)
5. `Adela_rateLimit` (usa cache_redis o logger)
6. `Adela_db_pg` (independiente)
7. `Adela_cache_redis` (independiente)
8. `Adela_pagination` (independiente)
9. `Adela_router` (usa validation + security + logger + pagination)

## Criterio de calidad por módulo

| Aspecto | Mínimo |
|---------|--------|
| Tests | 12+ |
| TypeScript strict | ✅ |
| Zero runtime deps | ✅ o justificadas |
| README con arquitectura | ✅ |
| TODO en castellano | ✅ |
| Repo privado en GitHub | ✅ |
| Integración documentada | ✅ |