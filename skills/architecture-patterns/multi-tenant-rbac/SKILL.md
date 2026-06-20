---
name: multi-tenant-rbac
description: "Patrones de diseño para sistemas de permisos multi-tenant en SaaS. Roles por tenant, RLS en BD, herencia, grupos, permisos temporales, admin override, lock release automático. Anti-patrones típicos de SaaS B2B."
version: 1.0.0
author: Mastermind / David Antizar
tags: [saas, rbac, multi-tenant, permissions, security, rls, postgresql, architecture]
---

# Multi-tenant RBAC — Patrones de diseño

## ¿Qué es esto?

Una guía de patrones y anti-patrones para diseñar sistemas de permisos en aplicaciones SaaS multi-tenant. Basado en auditorías reales de arquitecturas SaaS que fallaron en producción.

## Principio fundamental

> **Un sistema de permisos SaaS se diseña para el CASO LÍMITE, no para el caso feliz.**

El caso feliz es "un admin configura permisos y todo funciona". El caso límite es "una cuenta temporal de inspector no se revocó y filtró datos de 3 ayuntamientos".

---

## Los 7 anti-patrones que matan SaaS

### 1. 🔴 Roles fijos en CHECK constraint

```sql
-- ❌ ESTO MATA
rol VARCHAR(50) NOT NULL CHECK (rol IN (
    'superadmin', 'admin', 'directivo', 'jefe_dept', 'operario', 'ciudadano'
));
```

**Problema:** Cada organización tiene estructura distinta. Un ayuntamiento necesita `inspector_medioambiental`, otro necesita `conductor`, otro `supervisor_rutas`. Roles fijos = forzar a todos los clientes al mismo molde.

**Solución:** Tabla por tenant:

```sql
-- ✅ CORRECTO
CREATE TABLE roles_organizacion (
    id UUID PRIMARY KEY,
    org_id UUID NOT NULL REFERENCES organizaciones(id),
    nombre VARCHAR(100) NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 0,         -- 0=admin, 50=operario, 99=lectura
    hereda_de UUID REFERENCES roles_organizacion(id),
    es_admin BOOLEAN DEFAULT false,
    UNIQUE (org_id, nombre)
);
```

### 2. 🔴 Sin RLS en PostgreSQL

**Problema:** Todo el control de acceso está en middleware (Node.js, Python, etc.). Si hay un bug en una ruta API, se exponen datos de TODOS los tenants. **Defensa en profundidad = 0.**

**Solución:** RLS siempre activo:

```sql
-- Función helper
CREATE OR REPLACE FUNCTION app_org_id() RETURNS UUID AS $$
    SELECT NULLIF(current_setting('app.org_id', true), '')::UUID;
$$ LANGUAGE SQL STABLE;

-- RLS en cada tabla
ALTER TABLE activos ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON activos
    FOR ALL USING (org_id = app_org_id());

-- El middleware inyecta el contexto
await pool.query(`SELECT set_config('app.org_id', $1, true)`, [req.user.org_id]);
```

### 3. 🔴 Sin herencia de permisos

**Problema:** Cada usuario/rol necesita permisos explícitos. Con 10 recursos × 4 acciones × 5 roles = 200 combinaciones. Si un operario necesita un permiso nuevo, se lo pones a él pero NO a su jefe.

**Solución:** Herencia de roles via FK recursiva:

```
superadmin (nivel 0) → hereda de NADIE
admin (nivel 10) → hereda de directivo
directivo (nivel 20) → hereda de jefe_dept
jefe_dept (nivel 30) → hereda de operario
operario (nivel 50) → hereda de ciudadano
ciudadano (nivel 99) → hereda de NADIE
```

Al consultar permisos, usar CTE recursivo para recorrer la cadena de herencia. Solo configuras permisos para el nodo base y excepciones.

### 4. 🔴 Sin distinción VER vs EDITAR

**Problema:** Si un rol puede editar un recurso, también puede verlo. Un alcalde (directivo) necesita VER salarios pero NO editarlos. El modelo actual no lo permite.

**Solución:** 4 niveles jerárquicos:

```
NONE  (0) → No ve el recurso
READ  (1) → Solo GET, ni PUT ni POST ni DELETE
WRITE (2) → GET + POST + PUT (crear y editar)
ADMIN (3) → Todo + puede conceder permisos a otros
```

Cada nivel IMPLICA los inferiores: ADMIN tiene WRITE + READ. El middleware verifica: `nivel_requerido <= nivel_tiene`.

### 5. 🔴 Optimistic locking sin release automático

**Problema:** Usuario A abre un activo → `version++`. Usuario A cierra el navegador. Nadie más puede editar ese activo NUNCA. En un equipo de 20 personas, en 1 semana están todos los activos bloqueados.

**Solución:** Lock + timeout + cron:

```sql
-- Añadir columnas de lock
ALTER TABLE activos ADD COLUMN locked_by UUID REFERENCES usuarios(id);
ALTER TABLE activos ADD COLUMN locked_at TIMESTAMPTZ;

-- Cron que libera locks stale (cada 5 min)
CREATE OR REPLACE FUNCTION release_stale_locks() RETURNS INTEGER AS $$
DECLARE
    released INTEGER;
BEGIN
    UPDATE activos SET locked_by = NULL, locked_at = NULL
    WHERE locked_at IS NOT NULL
      AND locked_at < now() - INTERVAL '10 minutes'
      AND deleted_at IS NULL;
    GET DIAGNOSTICS released = ROW_COUNT;
    RETURN released;
END;
$$ LANGUAGE plpgsql;
```

### 6. 🟡 Sin admin override auditable

**Problema:** Cuando hay que saltarse la norma (ej: mover un activo en mantenimiento para una emergencia), el admin no tiene mecanismo. Acaba haciendo SQL directo en producción (¡peligro!).

**Solución:** Flag de bypass + auditoría:

```sql
ALTER TABLE usuarios ADD COLUMN bypass_security BOOLEAN DEFAULT false;
```

El middleware verifica: si `bypass_security = true`, salta los checks de permisos, pero el audit_log incluye `flag: 'BYPASS'`. El superadmin puede conceder bypass solo temporalmente (con expiración).

### 7. 🟡 Permisos con VARCHAR mágico sin estructura

```sql
-- ❌ ESTO ROMPE SILENCIOSAMENTE
alcance VARCHAR(100)  -- 'dept:policia', 'zona:centro', 'global'
```

Un typo `'dept:polica'` vs `'dept:policia'` crea un permiso que nunca funciona. Sin error, sin alerta, sin logs.

**Solución:** Estructurar el alcance:

```sql
alcance_tipo VARCHAR(30) NOT NULL CHECK (alcance_tipo IN (
    'global', 'departamento', 'zona', 'propio'
)),
alcance_valor VARCHAR(100),  -- 'policia', 'centro', NULL si global
```

---

## Patrones que SÍ funcionan

### Grupos de usuarios

Los permisos se asignan a grupos, no a usuarios. Un usuario hereda de TODOS sus grupos.

```sql
CREATE TABLE grupos (
    id UUID PRIMARY KEY,
    org_id UUID NOT NULL REFERENCES organizaciones(id),
    nombre VARCHAR(100) NOT NULL,
    UNIQUE (org_id, nombre)
);

CREATE TABLE grupo_usuarios (
    grupo_id UUID NOT NULL REFERENCES grupos(id),
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    PRIMARY KEY (grupo_id, usuario_id)
);

-- Los permisos se asignan a grupos o a usuarios (caso excepcional)
CREATE TABLE permisos_asignacion (
    id UUID PRIMARY KEY,
    org_id UUID NOT NULL,
    recurso_categoria VARCHAR(100) NOT NULL,
    permiso_nivel VARCHAR(20) NOT NULL,
    alcance_tipo VARCHAR(30) NOT NULL,
    alcance_valor VARCHAR(100),
    grupo_id UUID REFERENCES grupos(id),
    usuario_id UUID REFERENCES usuarios(id),
    granted_by UUID NOT NULL,
    expira_en TIMESTAMPTZ,
    CHECK (
        (grupo_id IS NOT NULL AND usuario_id IS NULL)
        OR (grupo_id IS NULL AND usuario_id IS NOT NULL)
    )
);
```

### Permisos temporales

El 80% de las filtraciones de datos son cuentas temporales nunca revocadas.

```sql
permisos_asignacion.expira_en TIMESTAMPTZ  -- NULL = permanente
```

El middleware verifica en cada request:
```sql
WHERE (expira_en IS NULL OR expira_en > now())
```

Cron diario que notifica al admin_org sobre permisos próximos a expirar y permisos ya expirados.

### Rate limiting por acción de usuario

Un operario no debería poder mover 10.000 activos en 1 minuto.

- **Por rol:** operario = 100 acc/hora, admin = 1000 acc/hora
- **Implementación:** Redis + SLIDING WINDOW
- **Respuesta:** HTTP 429 con `Retry-After` header
- **Configurable por tenant** (algunos necesitan más)

### Nuevos recursos data-driven

Cuando se añade un módulo (ej: "drones"), no debe requerir release de software:

1. El módulo registra sus tipos de recurso en una tabla `asset_types`
2. Los permisos ya aceptan cualquier `recurso_categoria`
3. El admin configura permisos desde UI sin código nuevo

---

## Arquitectura de verificación (3 capas)

```
Capa 1: RLS en PostgreSQL (defensa última)
  └─ Filtra por org_id automáticamente

Capa 2: Middleware de autorización
  └─ Verifica: ¿tiene permiso para esta acción en este recurso?
     └─ 4 niveles + herencia + grupos + permisos temporales

Capa 3: Bypass flag + auditoría
  └─ Admin puede overridear pero queda registrado
```

Las 3 capas son independientes. Si falla la Capa 2, la Capa 1 sigue protegiendo. Si falla la Capa 1, la Capa 2 sigue protegiendo.

---

## Checklist para auditar un sistema de permisos

- [ ] ¿Los roles son configurables por tenant? ¿O hay CHECK fijo?
- [ ] ¿Hay RLS en PostgreSQL (o equivalente en BD)?
- [ ] ¿Los roles heredan permisos? ¿O cada rol necesita config explícita?
- [ ] ¿Hay distinción READ vs WRITE vs ADMIN?
- [ ] ¿Los optimistic locks tienen release automático con timeout?
- [ ] ¿Hay admin override auditable (bypass flag)?
- [ ] ¿Los alcances de permisos están estructurados? ¿O son VARCHAR mágico?
- [ ] ¿Hay grupos de usuarios?
- [ ] ¿Hay permisos temporales con expiración?
- [ ] ¿Hay rate limiting por usuario/rol?
- [ ] ¿Los cambios en permisos se auditan?
- [ ] ¿Nuevos tipos de recurso se pueden añadir sin código?

---

## Referencias

- `terral-architecture` — Caso real de aplicación de estos patrones en TerrAn (ERP municipal SaaS)
- `terral-architecture/references/audit-42-issues.md` — 14 issues de permisos encontrados en auditoría real