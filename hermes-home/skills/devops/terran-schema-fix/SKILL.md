---
name: terran-schema-fix
description: "Procedimiento completo para resolver issues de auditoría de TerrAn — cubre las 6 fases (DATA, PERM, ADV, API, PERF, SEC), aplica fixes en docs, verifica y actualiza audit-state.json."
version: 2.0.0
author: David Antizar
tags: [terran, audit, schema, postgresql, data-validation, rbac, security, performance, geoasset]
---

# TerrAn Schema Fix — Resolución Completa de Issues de Auditoría

## Qué es

Procedimiento para resolver issues de validación de datos, permisos, seguridad, rendimiento y API encontrados durante la auto-auditoría cíclica de TerrAn. Cubre las 6 fases del auditor:

| Fase | ID | Qué cubre |
|------|-----|-----------|
| 01 | DATA | Schema, constraints, triggers, tablas de referencia |
| 02 | PERM | RBAC, roles_organizacion, RLS policies, inheritance |
| 03 | ADV | Partitioning, autovacuum, retention policies, tablespaces, triggers |
| 04 | API | Zod validation, Redis rate limiting, error middleware, CORS, Helmet, WebSocket |
| 05 | PERF | Redis cache strategy, connection pooling, Sharp, code splitting, advisory locks |
| 06 | SEC | argon2id/bcrypt hashing, GDPR export, trash can, ChromaDB isolation, HTTPS/TLS |

## Cuándo usar

- La auditoría cíclica de TerrAn (`terran-audit-loop`) encuentra issues
- El usuario pide "resolver issues" o "fixear fases"
- Hay un `audit-state.json` con issues marcados como `open`
- El auditor reporta que una fase no se avanza por acumulación de issues

## Flujo de trabajo (batch)

### Paso 0: Verificar configuración del auditor

```python
import json
with open('/root/workspace/geoasset/audit-state.json') as f:
    state = json.load(f)

max_per_phase = state.get('config', {}).get('max_issues_per_phase', 20)
for phase in state.get('phases', []):
    count = len([i for i in phase.get('issues_found', []) if i.get('status') == 'open'])
    if count > max_per_phase:
        print(f"⚠️ Fase {phase.get('id')} tiene {count} open, max={max_per_phase}")
        # SUBIR max_issues_per_phase a 50+ antes de procesar
```

**Pitfall crítico:** `max_issues_per_phase` por defecto es 20. Si una fase tiene más issues que este límite, el auditor puede truncar o no avanzar. **Siempre subir a 50+** antes de procesar fases con muchos issues (la fase SEC suele tener 30+).

### Paso 1: Identificar issues abiertos por fase

```python
with open('/root/workspace/geoasset/audit-state.json') as f:
    state = json.load(f)

open_issues = {}
for phase in state.get('phases', []):
    phase_id = phase.get('id')
    issues = [i for i in phase.get('issues_found', []) if i.get('status') == 'open']
    if issues:
        open_issues[phase_id] = issues

# open_issues = {
#   'DATA': [{'id': 'DATA-009', 'title': '...', 'severity': 'media', ...}],
#   'PERM': [...],
#   ...
# }
```

### Paso 2: Leer contexto de los archivos de docs

Los fixes se documentan en 3 archivos markdown (NO en BD real):

- `ARQUITECTURA.md` → schema principal, RBAC, seguridad, API standards
- `DOCUMENTOS-Y-IA.md` → schema de documentos, versiones, IA
- `RENDIMIENTO-Y-NEGOCIO.md` → rendimiento, stock, mantenimientos, KPIs

### Paso 3: Aplicar fixes por fase

Cada fase tiene patrones específicos:

#### DATA (Fase 01) — Schema y validación
- Columnas VARCHAR libre → tabla de referencia + FK + CHECK regex
- Arrays sin validación → CHECK array_length + unnest range
- Columnas sin auto-incremento → DEFAULT + trigger por grupo
- Crear tablas faltantes (`activos_humanos`, `audit_log` con partitioning)
- Forzar `org_id` en todas las tablas

#### PERM (Fase 02) — Permisos y RBAC
- Tabla `roles_organizacion` con herencia de permisos
- RLS policies por `org_id` en todas las tablas
- `permisos.alcance` con tabla de referencia + CHECK regex
- `turnos.dias_semana` con CHECK array_length + unnest range

#### ADV (Fase 03) — Avanzado
- Partitioning: `movimientos` por quarter, `documentos` por year
- Autovacuum settings en tablas grandes
- Retention policies con triggers
- Search vector triggers para búsqueda full-text
- Tablespaces para datos geoespaciales

#### API (Fase 04) — API standards
- Zod validation en todos los endpoints
- Redis rate limiting: Global 100/min, Auth 5/min, Write 50/min
- Error middleware con Request IDs
- CORS, Helmet, WebSocket auth, idempotency keys

#### PERF (Fase 05) — Rendimiento
- Redis cache: KPIs (5m), Config (1h), Geo (30m), Sessions (24h)
- Connection pooling: min=5, max=20, idle_timeout=30s
- Sharp para optimización de imágenes
- Code splitting por módulo
- Advisory locks para concurrencia
- Cursor-based pagination

#### SEC (Fase 06) — Seguridad
- Passwords: argon2id (timeCost:3, memoryCost:65536, parallelism:4) o bcrypt (cost 12)
- GDPR export endpoint
- Trash can interface (soft delete)
- ChromaDB isolation por org_id
- HTTPS/TLS settings

### Paso 4: Verificar fixes en docs

```python
with open('/root/workspace/geoasset/ARQUITECTURA.md') as f:
    arquitectura = f.read()

# Ejemplo: verificar que se documentó la tabla alcances
assert 'CREATE TABLE alcances' in arquitectura
assert 'chk_alcance_format' in arquitectura

# Verificar en todos los archivos
files_to_check = {
    'ARQUITECTURA.md': arquitectura,
    'DOCUMENTOS-Y-IA.md': open('/root/workspace/geoasset/DOCUMENTOS-Y-IA.md').read(),
    'RENDIMIENTO-Y-NEGOCIO.md': open('/root/workspace/geoasset/RENDIMIENTO-Y-NEGOCIO.md').read(),
}

# Verificar que cada fix aparece en el archivo correcto
for fix in fixes_applied:
    file_content = files_to_check.get(fix['file'], '')
    assert fix['pattern'] in file_content, f"Fix {fix['id']} no encontrado en {fix['file']}"
```

### Paso 5: Actualizar audit-state.json

```python
import json

with open('/root/workspace/geoasset/audit-state.json') as f:
    state = json.load(f)

for phase in state.get('phases', []):
    for issue in phase.get('issues_found', []):
        if issue.get('id') in fixes_applied_ids:
            # ⚠️ NO filtrar por status == 'open': los issues pueden tener status=null/None
            issue['status'] = 'fixed'
            issue['fixed_in'] = fixes_map[issue['id']]['file']
            issue['fixed_note'] = fixes_map[issue['id']]['note']

with open('/root/workspace/geoasset/audit-state.json', 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
```

### Paso 6: Verificación final

```python
# Contar issues abiertos restantes
total_open = sum(
    1 for phase in state.get('phases', [])
    for issue in phase.get('issues_found', [])
    if issue.get('status') == 'open'
)
print(f"Issues abiertos restantes: {total_open}")
# Debería ser 0 tras resolver todas las fases
```

## Patrones SQL reutilizables

### CHECK regex para formato tipo:valor
```sql
CONSTRAINT chk_formato CHECK (
    columna IS NULL OR columna ~ '^[a-z]+:[a-z0-9_-]+$'
)
```

### CHECK que array no esté vacío
```sql
CONSTRAINT chk_no_vacio CHECK (array_length(columna, 1) > 0)
```

### CHECK que todos los elementos estén en rango
```sql
CONSTRAINT chk_rango CHECK (
    EXISTS (
        SELECT 1 FROM unnest(columna) AS val
        WHERE val < MIN_VAL OR val > MAX_VAL
    ) = false
)
```

### Trigger auto-incremento por grupo
```sql
CREATE OR REPLACE FUNCTION siguiente_en_grupo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.version IS NULL OR NEW.version = DEFAULT_VAL THEN
        SELECT COALESCE(MAX(version), 0) + 1
        INTO NEW.version
        FROM tabla
        WHERE grupo_id = NEW.grupo_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Partitioning por rango
```sql
-- Movimientos por trimestre
CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    ...
) PARTITION BY RANGE (fecha);

CREATE TABLE movimientos_2026_q1 PARTITION OF movimientos
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');
```

### RLS policy por org_id
```sql
ALTER TABLE activos ENABLE ROW LEVEL SECURITY;

CREATE POLICY activos_org_policy ON activos
    FOR ALL
    USING (org_id = current_setting('app.current_org_id')::UUID);
```

### argon2id hash (documentar en config)
```json
{
    "hashing": {
        "algorithm": "argon2id",
        "params": {
            "timeCost": 3,
            "memoryCost": 65536,
            "parallelism": 4
        }
    }
}
```

## Pitfalls

- **NO es repo git** — `/root/workspace/geoasset` no tiene `.git`. No hacer `git commit`. Documentar en `notes/`.
- **`audit-state.json` usa `phases[].issues_found[]`** — No usar `findings[].sub_findings[]`. Los issues están en fases.
- **Los fixes son en docs, no en BD real** — TerrAn está en fase de diseño. Los cambios son en `ARQUITECTURA.md`, `DOCUMENTOS-Y-IA.md`, `RENDIMIENTO-Y-NEGOCIO.md`.
- **DEFAULT 1 no siempre es correcto** — Si el trigger solo aplica cuando version IS NULL o = DEFAULT, el usuario puede forzar un número específico. Documentar esto.
- **CHECK regex en PostgreSQL es case-sensitive** — `~` es case-sensitive, `~*` es case-insensitive. Usar el correcto según el caso.
- **`max_issues_per_phase` por defecto es 20** — La fase SEC suele tener 30+ issues. **Subir a 50+** antes de procesar. Si una fase tiene más issues que este límite, el auditor puede truncar o no avanzar.
- **Overlaps entre fases** — SEC issues (RLS, org_id enforcement, rate limiting) a menudo ya se resolvieron en DATA, PERM o API. Marcar como fixed en SEC con nota referenciando la fase original.
- **Batch de 100+ issues** — Cuando hay muchos issues abiertos, procesar por fase en orden (DATA → PERM → ADV → API → PERF → SEC). No mezclar fases.
- **Partial UNIQUE para reactivación** — Cuando se cambia `activo BOOLEAN` a `deleted_at TIMESTAMPTZ`, el `UNIQUE(email)` original bloquea reactivar con el mismo email. Usar `UNIQUE(email) WHERE deleted_at IS NULL` (partial index). Esto aplica a `usuarios` y cualquier entity con soft delete + email único.
- **Redefinir roles_organizacion ANTES de usuarios** — Si `usuarios` tiene `rol_id REFERENCES roles_organizacion(id)`, la tabla `roles_organizacion` debe crearse primero en el schema. No basta con documentarlo en comentarios — debe estar en el CREATE TABLE ordenado correctamente.

- **RLS policy referencia columna que no existe (CRÍTICO):** Si una RLS policy referencia `org_id` pero la tabla no tiene la columna, PostgreSQL permite crear la policy pero **falla en runtime** con `column "org_id" does not exist`. Esto es exactamente lo que pasa con la tabla `usuarios` (iter 144): la policy `tenant_isolation_usuarios` referencia `org_id` pero la tabla no la tiene. **Verificación obligatoria:** después de crear/modificar cualquier RLS policy, verificar que la columna referenciada existe: `SELECT column_name FROM information_schema.columns WHERE table_name='usuarios' AND column_name='org_id';`

- **`log-issue` requiere phase ID completo, no prefijo corto:** El script `terran-auditor.py log-issue` acepta el phase ID completo (ej: `06-security-compliance`), NO un prefijo corto (ej: `SEC`). Si se usa `SEC` como phase ID, devuelve `❌ Fase 'SEC' no encontrada`. **Siempre usar el ID completo** como aparece en `audit-state.json` en `phases[].id`. Ver `references/audit-tool-usage.md`.

- **SEC-074 stale en audit state (iter 156):** El `audit-state.json` puede marcar un issue como "no fijado" cuando en realidad YA está fijado en los documentos. El índice `idx_audit_log_org ON audit_log (org_id, timestamp DESC)` existía en línea 1428 pero el state no lo reflejaba. **Siempre verificar en los documentos**, no confiar ciegamente en el estado del auditor.

- **NUNCA confiar en `status: "fixed"` sin verificar en docs (SEC-065 a SEC-074):** El `audit-state.json` puede marcar issues como `fixed` pero las soluciones documentadas tienen errores estructurales: doble coma en SQL (`BIGSERIAL PRIMARY KEY,,`), columnas faltantes referenciadas por RLS policies, funciones que INSERTAN sin org_id. **Verificación obligatoria:** después de marcar un issue como fixed, leer el CREATE TABLE correspondiente en ARQUITECTURA.md y verificar: (1) sintaxis SQL válida (sin dobles comas, sin `//` en SQL), (2) todas las columnas referenciadas existen, (3) las RLS policies referencian columnas que existen, (4) las funciones que INSERTAN en audit_log incluyen org_id.

- **Documentos inconsistentes entre sí (SEC-068):** ARQUITECTURA.md puede tener RLS completo pero RENDIMIENTO-Y-NEGOCIO.md no. Si un desarrollador implementa siguiendo RY-NEGOCIO.md, el sistema se despliega sin RLS. **Verificación obligatoria:** después de aplicar fixes en ARQUITECTURA.md, verificar que RENDIMIENTO-Y-NEGOCIO.md y DOCUMENTOS-Y-IA.md también contienen los cambios críticos (RLS, org_id, funciones RLS). Si no, sincronizar.

- **RLS policy detection: CREATE POLICY y ON <table> en la misma línea:** Al buscar policies en ARQUITECTURA.md, `CREATE POLICY nombre ON tabla` puede estar en la MISMA línea (no en líneas separadas). Usar `line.split('ON')[1].split()[0]` para extraer el nombre de la tabla, NO buscar en líneas adyacentes. Esto afecta la detección de tablas con RLS enabled pero sin policy.

- **docs_content truncado a ~30KB en auditor run:** El script `terran-auditor.py run` devuelve `docs_content` truncado. **Siempre leer archivos directamente con `read_file()`** para verificación real. El `docs_content` solo sirve para búsqueda rápida.

### Pitfall: BIGSERIAL con doble coma (SEC-096, iter 181)

En las líneas 3050 y 3305 de ARQUITECTURA.md: `BIGSERIAL PRIMARY KEY,,` (doble coma). Error de sintaxis SQL que impide crear las tablas security_log y login_attempts. **Verificación:** grep -n `,,` en ARQUITECTURA.md para encontrar dobles comas.

### Pitfall: security_log/login_attempts sin org_id (SEC-097, iter 181)

Las tablas security_log y login_attempts NO tienen columna `org_id` pero tienen RLS policies que refieren `app_current_org_id()`. Las policies no funcionan porque la columna no existe. **Solución:** añadir `org_id UUID NOT NULL` a ambas tablas y actualizar las policies.

### Pitfall: password_history almacena password_hash sin encriptar (SEC-098, iter 181)

La tabla `password_history` almacena `password_hash TEXT NOT NULL` en texto plano. Si se filtra, se pierden TODAS las contraseñas pasadas. **Solución:** encriptar con pgcrypto o tabla separada con acceso restringido.

### Pitfall: DEFAULT_POLICIES en JS sin tabla retention_policies en BD (SEC-100, iter 181)

RENDIMIENTO-Y-NEGOCIO.md define DEFAULT_POLICIES en JavaScript pero no hay tabla retention_policies en BD. Las políticas están hardcodeadas en código. **Solución:** crear tabla `retention_policies (org_id, tabla, dias_retencion, accion, activo)`.

### Pitfall: getTier() hardcodeado sin tabla tiers (SEC-101, iter 181)

La función `getTier(orgId)` referencia `tier.price`, `tier.maxActivos` pero no hay tabla tiers en el schema. Todo está hardcodeado en JavaScript. **Solución:** crear tabla `tiers` + `suscripciones` + `getTier()` query real a BD.

### Pitfall: POST /api/activos sin verificación de límite de tier (BL-019, iter 181)

El endpoint POST /api/activos no verifica si el org ha alcanzado el límite de su tier. Un cliente Starter puede crear 10.000 activos sin pagar más. **Solución:** middleware que cuente activos actuales vs tier.max_activos antes de cada POST.

### Pitfall: Tablas turnos/asignaciones sin endpoints de gestión (BL-020, iter 181)

Las tablas existen en el schema pero no hay endpoints de gestión (POST/PUT/GET). Son inútiles sin CRUD. **Solución:** añadir endpoints POST /api/turnos, PUT /api/turnos/:id, POST /api/turnos/:id/asignar, GET /api/turnos/activos, GET /api/turnos/disponibilidad.

## Referencias

- `references/schema-fix-examples.md` — Ejemplos concretos de fixes aplicados en sesiones reales
- `references/phase-fixes-summary.md` — Resumen de fixes aplicados por fase (2026-06-14)
- `references/rls-helpers-pattern.md` — Patrón de funciones RLS auxiliares (current_user_id, current_user_email, current_org_id) con SECURITY DEFINER
- `references/usuarios-missing-org-id.md` — Caso concreto: tabla usuarios sin org_id pero RLS policy lo referencia (SEC-064)
- `references/audit-verification-pattern.md` — Patrón de verificación post-fix: 4 pasos para confirmar que un fix documentado es real y funcional (no solo un comentario). Cubre sintaxis SQL, columnas referenciadas, funciones INSERT, sincronización entre documentos.
- `references/audit-tool-usage.md` — Referencia de comandos del auditor (`log-issue`, `run`, `advance`), formato de phase IDs, pitfall de JSON encoding, estructura de `audit-state.json`.
- `references/audit-iter168.md` — Iteración 168 (2026-06-23): 13 nuevos issues SEC-083 a SEC-095. Incluye: tabla audit_log duplicada, INSERTs sin org_id, tablas sin auto-cleanup (token_blacklist, security_log, login_attempts, user_action_tracking), parámetro shadowing en verificar_rate_limit(), sync_departamento_display sin org_id, check_parent_cycle con EXIT prematuro, escape encoding problemático, partitioning BIGINT+composite PK, CORS wildcard+credentials.
- `references/audit-iteration-181.md` — Iteración 181: 12 nuevos issues (SEC-096 a SEC-101, BL-015 a BL-020). Incluye: doble coma en BIGSERIAL PRIMARY KEY,, (SEC-096), security_log/login_attempts sin org_id (SEC-097), password_history sin encriptar (SEC-098), DEFAULT_POLICIES en JS sin tabla retention_policies (SEC-100), getTier() hardcodeado sin tabla tiers (SEC-101), módulos sin tabla modulos_disponibles (BL-015), add-ons sin tabla de configuración (BL-016), sin tabla trials (BL-017), solo export RGPD sin export funcional (BL-018), POST /api/activos sin verificación de límite de tier (BL-019), turnos/asignaciones sin endpoints (BL-020).
