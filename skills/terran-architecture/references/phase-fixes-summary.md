# TerrAn — Resumen de Fixes por Fase (2026-06-14)

## Contexto

La auditoría `terran-audit-loop` encontró 105 issues abiertos distribuidos en 6 fases. Se resolvieron todos documentando fixes en los archivos de arquitectura (NO en BD real).

## Fase 01 — DATA (28 issues)

**Archivo:** `ARQUITECTURA.md`, `DOCUMENTOS-Y-IA.md`

- Schema corrections: columnas VARCHAR → tablas de referencia + CHECK regex
- Tabla `activos_humanos` creada
- `audit_log` con partitioning por mes
- Forzar `org_id` en todas las tablas
- Triggers para auto-incremento por grupo
- CHECK constraints para arrays (dias_semana, etc.)

## Fase 02 — PERM (14 issues)

**Archivo:** `ARQUITECTURA.md`

- Tabla `roles_organizacion` con herencia de permisos
- RLS policies por `org_id` en todas las tablas
- `permisos.alcance` con tabla de referencia + CHECK regex
- `turnos.dias_semana` con CHECK array_length + unnest range

## Fase 03 — ADV (12 issues)

**Archivo:** `ARQUITECTURA.md`

- Partitioning: `movimientos` por quarter, `documentos` por year
- Autovacuum settings en tablas grandes
- Retention policies con triggers
- Search vector triggers para búsqueda full-text
- Tablespaces para datos geoespaciales

## Fase 04 — API (9 issues)

**Archivo:** `ARQUITECTURA.md`

- Zod validation en todos los endpoints
- Redis rate limiting: Global 100/min, Auth 5/min, Write 50/min
- Error middleware con Request IDs
- CORS, Helmet, WebSocket auth, idempotency keys

## Fase 05 — PERF (6 issues)

**Archivo:** `RENDIMIENTO-Y-NEGOCIO.md`

- Redis cache: KPIs (5m), Config (1h), Geo (30m), Sessions (24h)
- Connection pooling: min=5, max=20, idle_timeout=30s
- Sharp para optimización de imágenes
- Code splitting por módulo
- Advisory locks para concurrencia
- Cursor-based pagination

## Fase 06 — SEC (36 issues)

**Archivo:** `ARQUITECTURA.md`

- Passwords: argon2id (timeCost:3, memoryCost:65536, parallelism:4) o bcrypt (cost 12)
- GDPR export endpoint
- Trash can interface (soft delete)
- ChromaDB isolation por org_id
- HTTPS/TLS settings
- 19 overlaps con fases anteriores (marcados con referencia)

## Configuración

- `max_issues_per_phase`: 20 → 50 (para permitir que el auditor procese fases con muchos issues)
