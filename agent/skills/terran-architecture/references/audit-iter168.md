# Auditoría Iteración 168 — SEC-083 a SEC-095

**Fecha:** 2026-06-23  
**Fase:** 06-security-compliance  
**Issues nuevos:** 13

## Hallazgos

### SEC-083: `audit_log` definida dos veces en ARQUITECTURA.md
- **Línea 216:** definición original sin `org_id`
- **Línea 1382:** definición con `org_id` (fix DATA-002)
- **Impacto:** `CREATE TABLE` duplicado → error "relation already exists"
- **Solución:** Eliminar la definición de línea 216, mantener solo la de línea 1382

### SEC-084: `audit_permiso_cambios()` INSERTA sin `org_id`
- **Línea 3104:** `INSERT INTO audit_log (recurso_id, accion, detalles)` — falta `org_id`
- **Impacto:** Violación de integridad referencial si `org_id` es NOT NULL
- **Solución:** Añadir `org_id` al INSERT, usar `current_org_id()`

### SEC-085: `invalidar_tokens_usuario()` INSERTA sin `org_id`
- **Impacto:** Mismo que SEC-084 — función que INSERTA en audit_log sin org_id
- **Solución:** Revisar TODAS las INSERTs en audit_log y añadir `org_id`

### SEC-086: `token_blacklist` sin auto-cleanup
- **Impacto:** Tabla crece infinitamente, ningún mecanismo de expiración
- **Solución:** Trigger o función que borre tokens > 24h

### SEC-087: `security_log` sin auto-cleanup
- **Impacto:** Tabla crece infinitamente
- **Solución:** Retention policy de 90 días configurable por org

### SEC-088: `login_attempts` sin auto-cleanup
- **Impacto:** Tabla crece infinitamente, problema de privacidad GDPR
- **Solución:** Auto-delete después de 30 días

### SEC-089: `user_action_tracking` sin auto-cleanup
- **Impacto:** Tabla crece infinitamente
- **Solución:** Retention policy de 30 días

### SEC-090: `verificar_rate_limit()` — parámetro shadowing
- **Línea:** `WHERE usuario_id = usuario_id` (self-join)
- **Impacto:** Siempre devuelve true, rate limiting completamente roto
- **Solución:** `WHERE usuario_id = $1` con parámetro posicion

### SEC-091: `sync_departamento_display()` sin filtro `org_id`
- **Impacto:** Sincroniza departamentos de TODAS las organizaciones
- **Solución:** Añadir `WHERE org_id = current_org_id()`

### SEC-092: `check_parent_cycle()` — EXIT prematuro
- **Línea:** `EXIT WHEN depth > 10` — pero depth siempre es 1 en primer loop
- **Impacto:** No detecta ciclos reales, solo limita profundidad
- **Solución:** Revisar lógica de recursión

### SEC-093: `encriptar_dato()` — escape encoding problemático
- **Impacto:** `ENCODE(ENCRYPT(...), 'escape')` puede corromper datos con caracteres especiales
- **Solución:** Usar `ENCODE(ENCRYPT(...), 'hex')` para lossless encoding

### SEC-094: `audit_log` partitioning — BIGINT + composite PK
- **Impacto:** `BIGINT` con secuencia global + PK `(id, timestamp)` → colisiones en particiones
- **Solución:** Usar `BIGSERIAL` con secuencia por partición o `UUID` como PK

### SEC-095: CORS — `credentials: true` + wildcard origin
- **Impacto:** CSRF attacks posibles, vulnerabilidad grave
- **Solución:** Origin whitelist + `credentials: true`
