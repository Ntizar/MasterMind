# TerrAn — 42 Issues de Auditoría (Fases 01-02)

> Generado el 2026-06-12 por Mastermind. Auditoría iteración #70.
> Archivo vivo — se actualiza con cada fase auditada.

## Resumen

| Fase | Issues | Estado |
|------|--------|--------|
| 01 — Estructura del Schema | 28 (6 🔴, 10 🟡, 4 🟢) | ✅ Completada |
| 02 — Permisos y RBAC | 14 (6 🔴, 7 🟡, 1 🟢) | ✅ Completada |
| 03 — Modelo de Datos Avanzado | 14 (4 🔴, 8 🟡, 2 🟢) | ✅ Completada |
| 04 — API y Backend | 12 (3 🔴, 9 🟡, 0 🟢) | ✅ Completada |
| 05 — Rendimiento | 8 (1 🔴, 5 🟡, 2 🟢) | ✅ Completada |
| 06 — Seguridad y Compliance | 20 (11 🔴, 9 🟡, 0 🟢) | 🔴 Activa |
| 07 — Lógica de Negocio | 0 | ⏳ Pendiente |
| 08 — UX y Flujos | 0 | ⏳ Pendiente |
| **Total** | **96** | |

---

## Fase 01: Estructura del Schema (28 issues)

### 🔴 Alta severidad (6)

| ID | Título | Solución |
|----|--------|----------|
| DATA-001 | `lat/lng` redundantes con `geometry` — desincronización posible | Eliminar columnas, usar solo `geometry`. O computed columns: `ST_Y(geometry)`, `ST_X(geometry)` |
| DATA-003 | DNI en JSONB metadata — problema GDPR | Tabla separada `activos_humanos` con campos estructurados + encriptación. JSONB solo para datos no personales |
| DATA-004 | Sin restricción de ciclo en `parent_id` | `CHECK (parent_id IS NULL OR parent_id != id)` + trigger que verifique ancestros recursivos |
| DATA-018 | `password_hash VARCHAR(255)` no future-proof para argon2id | Cambiar a `TEXT` |
| DATA-020 | `audit_log` no tiene `org_id` — violación multi-tenant | Añadir `org_id`. Incluir en clave de partición |
| DATA-022 | `permisos` no tiene `org_id` — permisos globales | Añadir `org_id`. O heredar del usuario automáticamente |

### 🟡 Media severidad (10)

| ID | Título | Solución |
|----|--------|----------|
| DATA-006 | JSONB con campos consultados frecuentemente (`capacidad_litros`, `tipo_residuo`, etc.) | Columnas normales o tabla separada por tipo de activo |
| DATA-008 | Soft-delete con BOOLEAN (`activo`) vs `deleted_at` | Unificar a `deleted_at TIMESTAMPTZ`. `UNIQUE(email) WHERE deleted_at IS NULL` |
| DATA-010 | `turnos.dias_semana INTEGER[]` sin validación de valores | `CHECK (array_length(dias_semana,1) > 0 AND EVERY(dias_semana BETWEEN 0 AND 6))` |
| DATA-011 | `documento_versiones.version` sin auto-increment | Trigger BEFORE INSERT: `version = COALESCE(MAX(version)+1, 1)` por documento |
| DATA-017 | `subtipo` sin dependencia validada con `tipo` | Tabla `tipos_activos(org_id, tipo, subtipo)` con FK compuesta |
| DATA-021 | `ordenes_trabajo.activos_ids UUID[]` sin FK — datos huérfanos | Tabla `orden_trabajo_activos(orden_id FK, activo_id FK, UNIQUE)` |
| DATA-024 | Materialized views (`mv_kpi_residuos`) sin índices | `CREATE INDEX idx_mv_kpi_org ON mv_kpi_residuos(org_id)` |
| DATA-026 | `stock.almacen_id` sin `ON DELETE SET NULL` | Añadir `ON DELETE SET NULL` en FK |
| DATA-027 | `movimientos.orden_trabajo_id UUID` sin FK | `FOREIGN KEY (orden_trabajo_id) REFERENCES ordenes_trabajo(id) ON DELETE SET NULL` |
| DATA-028 | Columna con caracteres no latinos: `firma数字化` | Renombrar a `firma_digital` |
| DATA-029 | Sin sistema de migrations de BD | Usar `node-pg-migrate` o similar. Cada cambio = migration con up/down |

### 🟢 Baja severidad (4)

| ID | Título | Solución |
|----|--------|----------|
| DATA-012 | `codigo_INE VARCHAR(5)` sin CHECK de formato | `CHECK (codigo_INE ~ '^[0-9]{5}$')` |
| DATA-013 | `movimientos.fotos TEXT[]` sin metadatos | Tabla `movimiento_fotos(movimiento_id, url, descripcion, tipo, orden)` |
| DATA-014 | `organizaciones.config JSONB` sin schema validation | Documentar schema en comentarios o tabla key/value |
| DATA-023 | `modelo_3d` sin validación de formato de archivo | Ruta relativa completa o tabla `modelos_3d(id, nombre, ruta, formato)` |
| DATA-025 | `bbox_lat/lng DECIMAL` sin precisión explícita | Cambiar a `DECIMAL(10,7)` como el resto de coordenadas |

---

## Fase 02: Permisos y RBAC (14 issues)

### 🔴 Alta severidad (6)

| ID | Título | Solución |
|----|--------|----------|
| PERM-001 | **Roles fijos en CHECK constraint** — no personalizables por tenant | Eliminar CHECK. Tabla `roles_organizacion(org_id, nombre, nivel, hereda_de)` |
| PERM-002 | **Sin RLS en PostgreSQL** — defensa en profundidad = 0 | `ALTER TABLE activos ENABLE ROW LEVEL SECURITY` + policies por `org_id` |
| PERM-003 | **Sin herencia de permisos** — cada rol es un silo | `roles_organizacion.hereda_de` → FK recursiva. `superadmin > admin > directivo > jefe > operario > ciudadano` |
| PERM-004 | **No existe VER vs EDITAR** — misma capacidad para todo | 4 niveles: `NONE → READ → WRITE → ADMIN`. READ permite GET pero no PUT/PATCH/DELETE |
| PERM-005 | **Optimistic locking sin release** — navegador cerrado = bloqueo permanente | `locked_by` + `locked_at`. Cron cada 5 min libera locks > 10 min |
| PERM-007 | **No hay ADMIN override** — admin no puede saltarse restricciones | `bypass_security BOOLEAN` + flag `BYPASS` en audit_log. Conceder solo temporalmente |

### 🟡 Media severidad (7)

| ID | Título | Solución |
|----|--------|----------|
| PERM-006 | `permisos.alcance VARCHAR` sin estructura — typos rompen silenciosamente | `alcance_tipo ENUM(global,departamento,zona,propio)` + `alcance_valor VARCHAR` |
| PERM-008 | Sin permisos por objeto individual — "operario solo Zona Centro" | `recurso_especifico_id UUID` opcional + RLS con `ST_Within` para zonas geográficas |
| PERM-009 | Cambios en permisos NO se auditan | Integrar en audit middleware + trigger en tabla `permisos` |
| PERM-010 | Sin grupos de usuarios — 10 policías = 10 configs | Tabla `grupos(org_id, nombre)` + `grupo_usuarios(grupo_id, usuario_id)` |
| PERM-011 | Sin permisos temporales — 80% filtraciones son cuentas caducadas no revocadas | `fecha_expiracion TIMESTAMPTZ` + cron + trigger que deniegue acceso automático |
| PERM-012 | Sin rate limiting — un script mueve 10K activos/min | 100 acc/hora operario, 1000 admin. Redis + HTTP 429 |
| PERM-014 | `departamento NULL` deja usuarios sin filtro | `DEFAULT 'sin_asignar'` o NOT NULL con CHECK |

### 🟢 Baja severidad (1)

| ID | Título | Solución |
|----|--------|----------|
| PERM-013 | Nuevos recursos requieren cambio de código | Permisos 100% data-driven. Módulo registra tipos en `asset_types` desde UI |

---

## Fase 06: Seguridad y Compliance (20 issues)

> Generado el 2026-06-12 por Mastermind. Auditoría iteración #70.

### 🔴 Alta severidad (11)

| ID | Título | Solución |
|----|--------|----------|
| SEC-001 | `password_hash` sin hash real — `SYSTEM_HASH` literal | Usar bcrypt (coste 12) o argon2id. Usuario @sistema con `password_hash NULL` |
| SEC-002 | Sin RLS en PostgreSQL — aislamiento solo en middleware | RLS en TODAS las tablas con policies `org_id = current_setting('app.org_id')` |
| SEC-003 | Audit log sin `org_id` — violación multi-tenant | Añadir `org_id NOT NULL`. Inyectar en middleware. Incluir en partición |
| SEC-004 | Snapshots JSONB completos exponen DNI, datos médicos | Guardar solo diff de campos cambiados. Excluir campos sensibles del audit |
| SEC-005 | Sin exportación de datos (RGPD Art. 20) | Endpoint `GET /api/export/{org_id}` con JSON/CSV estructurado |
| SEC-006 | Sin recuperación de soft delete — borrados son permanentes | Interfaz "Papelera" + botón restaurar + auto-limpieza configurable |
| SEC-007 | Sin política de retención implementada | Tabla `retention_policies` + cron diario + acciones (archivar/anonimizar/eliminar) |
| SEC-008 | DNI, datos médicos en JSONB sin encriptar | Tabla separada `datos_personales_sensibles` + encriptación pgcrypto |
| SEC-009 | JWT sin revocación — usuario despedido sigue accesible | Access token 15 min + refresh token + tabla `token_blacklist` |
| SEC-011 | WebSocket sin autenticación — cualquiera recibe posiciones | JWT en query param. Verificar org_id. Rate limit por conexión |
| SEC-016 | Sin backup strategy — crash = pérdida total | Backup diario + incremental hora. Copias en S3. Test restauración trimestral |
| SEC-017 | API sin rate limiting — fuerza bruta posible | express-rate-limit con Redis. 5 intentos/min login, 100 req/min global |

### 🟡 Media severidad (9)

| ID | Título | Solución |
|----|--------|----------|
| SEC-010 | Cámaras CCTV `publica BOOLEAN` sin control | RBAC para acceso. Eliminar campo publica. Endpoint separado con token público |
| SEC-012 | Sin protección CSRF | JWT en header Authorization (CSRF no aplica) o CSRF token + SameSite cookie |
| SEC-013 | Sin logging de seguridad — no hay detección de intrusiones | Tabla `security_log`. Alertas >10 fallos login desde misma IP |
| SEC-014 | Firma electrónica sin Ley 39/2015 / eIDAS | Integrar FNMT/Cl@ve. Tabla `firma_electronica` con hash + certificado |
| SEC-015 | Sin TLS/SSL documentado | HTTPS + Let's Encrypt + HSTS + TLS PostgreSQL `sslmode=require` |
| SEC-018 | Metadata con datos personales sin control granular | Endpoint separado para datos sensibles. API filtra campos según permiso |
| SEC-019 | Soft delete UNIQUE risk — duplicados al restaurar | Verificar código no en uso antes de restaurar. Tabla `reserved_codes` |
| SEC-020 | Sin política de contraseñas | 12 chars mínimo + haveibeenpwned + expiración 90 días + bloqueo 5 intentos |

---

## Lecciones aprendidas para futuras fases

1. **Multi-tenant no es añadir `org_id` y ya** — hay que pensar en RLS, aislamiento de audit, permisos por tenant, routing de sesiones
2. **JSONB es el Diablo** — seductor al principio (flexible!), doloroso cuando hay que consultar, migrar o proteger datos
3. **Las constraints en CHECK son frágiles** — para catálogos que cambian por tenant, usar tablas, no CHECK
4. **El audit_log NO puede ser una tabla normal** — particionar por mes desde el día 1
5. **El optimistic locking sin release es peor que no tener locking** — bloquea activos permanentemente en equipos de >1 persona
6. **Los permisos no se diseñan para el caso feliz** — se diseñan para el caso "qué pasa si el middleware tiene un bug"
7. **Seguridad NO es fase 8** — se debe diseñar desde el día 1. GDPR, RLS, encriptación, backups, rate limiting son requisitos de arquitectura, no "mejoras posteriores"
8. **Los datos sensibles (DNI, salud) necesitan capa de encriptación** — no basta con "no mostrarlos en la UI". Deben encriptarse en reposo (pgcrypto) y tener acceso diferenciado
9. **JWT stateless sin blacklist = acceso post-despedido** — siempre implementar token revocación con TTL corto
10. **Ley 39/2015 + eIDAS son obligatorios** — firma electrónica sin validez legal hace el sistema inútil para administración pública