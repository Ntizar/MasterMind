# TerrAn — Seguridad y Compliance Issues (Iter 90-106)

## Resumen

Auditoría iterativa de la fase 06 (Seguridad y Compliance) contra los 3 documentos de arquitectura. Iter 106 reportó 36 issues activos, 0 fijados.

## Issues por iteración

### Iter 90 (23 issues originales)

| ID | Severidad | Título |
|---|---|---|
| SEC-001 | Alta | password_hash sin hash real — SYSTEM_HASH en usuario sistema |
| SEC-002 | Alta | Sin RLS (Row-Level Security) en PostgreSQL |
| SEC-003 | Alta | Audit log sin org_id — violación multi-tenant |
| SEC-004 | Alta | Audit log con snapshots JSONB completos |
| SEC-005 | Alta | Sin mecanismo de exportación de datos (RGPD Art. 20) |
| SEC-006 | Alta | Sin interfaz de recuperación de soft delete |
| SEC-007 | Alta | Sin política de retención de datos implementada |
| SEC-008 | Alta | Datos personales sensibles en JSONB sin encriptar |
| SEC-009 | Alta | JWT sin mecanismo de revocación |
| SEC-010 | Media | Cámaras CCTV con campo publica BOOLEAN sin restricciones |
| SEC-011 | Alta | WebSocket sin autenticación documentada |
| SEC-012 | Media | Sin protección CSRF |
| SEC-013 | Media | Sin logging de seguridad |
| SEC-014 | Media | Ley 39/2015 — Sin firma electrónica |
| SEC-015 | Media | Sin encriptación TLS/SSL documentada |
| SEC-016 | Alta | Sin backup strategy documentada |
| SEC-017 | Alta | API sin rate limiting |
| SEC-018 | Media | Campos de metadata sin control de acceso granular |
| SEC-019 | Media | Soft delete UNIQUE riesgo duplicados |
| SEC-020 | Media | Sin política de contraseñas |
| SEC-021 | Media | updated_at sin trigger |
| SEC-022 | Alta | config JSONB sin encriptación |
| SEC-023 | Alta | Sin política de datos personales (RGPD Art. 17) |

### Iter 106 (13 issues nuevos)

| ID | Severidad | Título |
|---|---|---|
| SEC-024 | Alta | Roles hardcodeados en CHECK — no escalan a multi-tenant |
| SEC-025 | Alta | Tabla permisos sin org_id — permisos globales |
| SEC-026 | Alta | Desactivar usuario no invalida sesiones activas |
| SEC-027 | Media | Sin algoritmo de hash de contraseñas especificado |
| SEC-028 | Media | Sin tabla de permisos temporarios |
| SEC-029 | Alta | ChromaDB sin aislamiento multi-tenant |
| SEC-030 | Media | URLs de streams de cámaras expuestas en la API |
| SEC-031 | Media | Sin sistema de migraciones con rollback |
| SEC-032 | Media | Regex de validación de alcance insuficiente |
| SEC-033 | Baja | Enumeración de emails vía feedback diferenciado |
| SEC-034 | Alta | Sin lockout tras intentos fallidos de login |
| SEC-035 | Media | Upload de documentos sin validación MIME |
| SEC-036 | Media | Sin política CORS documentada |

## Distribución por categoría

### Multi-tenant isolation (4 issues)
- SEC-002: Sin RLS
- SEC-003: Audit log sin org_id
- SEC-025: Tabla permisos sin org_id
- SEC-029: ChromaDB sin aislamiento

### Authentication/Authorization (6 issues)
- SEC-009: JWT sin revocación
- SEC-011: WebSocket sin auth
- SEC-024: Roles hardcodeados
- SEC-026: activo=false no invalida sesiones
- SEC-034: Sin lockout
- SEC-028: Sin permisos temporarios

### Data protection (5 issues)
- SEC-004: Snapshots completos en audit
- SEC-008: JSONB sin encriptar
- SEC-022: config JSONB sin encriptar
- SEC-005: Sin exportación
- SEC-023: Sin derecho al olvido

### Infrastructure security (5 issues)
- SEC-015: Sin TLS
- SEC-016: Sin backup
- SEC-017: Sin rate limiting
- SEC-036: Sin CORS
- SEC-012: Sin CSRF

### Compliance (4 issues)
- SEC-014: Ley 39/2015
- SEC-007: Sin retención
- SEC-005: RGPD Art. 20
- SEC-023: RGPD Art. 17

## Estado actual (iter 106)

- **Total issues:** 36
- **Fijados:** 0
- **Fase:** NO completada (tiene issues activos)
- **Progreso general:** 5/8 fases completadas

## Notas de auditoría

- El límite `max_issues_per_phase: 20` es insuficiente. La fase acumuló 36 issues.
- La estructura de salida de `terran-auditor.py run` varía entre iteraciones (objeto plano vs array `phases[]`).
- Los issues de seguridad son los más numerosos y críticos del proyecto completo.
