---
name: terral-architecture
description: "Arquitectura completa de TerrAn — ERP municipal con vista 3D, gestión documental, IA y datos en tiempo real. Referencia para hardware, escalabilidad y patrones."
version: 2.0.0
author: David Antizar
tags: [erp, municipal, saas, 3d, gis, postgis, threejs, ai, rag, terran]
---

# TerrAn — Arquitectura de Referencia

## Qué es TerrAn

**Terr**itorio + **An**tizar (+ NaN builders). ERP municipal con vista 3D donde ayuntamientos y empresas gestionan activos físicos y humanos sobre un mapa interactivo de España. Datos en tiempo real (clima, trenes, cámaras), búsqueda semántica con IA, y gestión documental completa.

## Stack tecnológico

| Capa | Tecnología | Versión | Justificación |
|---|---|---|---|
| **Backend** | Node.js + Express | 20 LTS | Rápido de desarrollar, ESM |
| **BD principal** | PostgreSQL + PostGIS | 16+ | GIS nativo, particiones, FTS |
| **Cache** | Redis | 7+ | KPIs, sesiones, posiciones |
| **Documentos** | MinIO (S3 self-hosted) | Latest | PDFs/fotos, no en BD |
| **Búsqueda semántica** | ChromaDB | Latest | Embeddings, RAG |
| **IA** | qwen3.6 vía NaN API | — | Asistente conversacional |
| **Frontend 3D** | Three.js | 0.163+ | Terreno, activos, LOD |
| **Frontend UI** | Vanilla JS + Aurora CSS | — | Estilo David, sin framework |
| **WebSocket** | ws (Node.js) | — | Real-time |
| **PDF extraction** | pdf-parse | — | Extraer texto de PDFs |
| **Deploy** | Docker + NaN Builders | — | Contenedor aislado |
| **Object Storage** | MinIO | — | Alternativa self-hosted a S3 |

## Hardware mínimo recomendado

### Desarrollo local
- 4GB RAM, 2 cores, 40GB disco
- PostgreSQL + Redis + MinIO + Node.js = ~2GB RAM total
- ChromaDB = ~500MB RAM adicional

### Producción (1 ayuntamiento pequeño-medium)
- **Servidor:** 8GB RAM, 4 cores, 200GB SSD
- **PostgreSQL:** 4GB RAM, 100GB SSD (con particiones)
- **Redis:** 1GB RAM
- **MinIO:** 50GB (documentos)
- **Node.js:** 2GB RAM (2 instancias para HA)
- **Total estimado:** ~8GB RAM, 4 cores, 200GB SSD

### Producción (multi-tenant, 10+ ayuntamientos)
- **Servidor:** 32GB RAM, 8 cores, 1TB SSD
- **PostgreSQL:** 16GB RAM (read replica)
- **Redis:** 4GB RAM (cluster)
- **MinIO:** 500GB (documentos)
- **Node.js:** 8GB RAM (4 instancias, load balancer)
- **Total estimado:** ~32GB RAM, 8 cores, 1TB SSD

## Patrones de arquitectura

### Multi-tenant
- Cada ayuntamiento = una `organizacion` con `org_id`
- TODAS las queries filtran por `org_id`
- RLS (Row Level Security) en PostgreSQL para aislamiento
- Un usuario solo ve datos de su organización

### Sistema de Permisos y RBAC (v2 — corregido tras auditoría)

⚠️ **La versión v1 del schema (CHECK constraint con 7 roles fijos + tabla `permisos` con `alcance` como VARCHAR libre) tiene estos problemas graves:**

1. **Roles fijos en CHECK no escalan a multi-tenant** — Cada ayuntamiento necesita roles distintos. No todos tienen alcalde, concejal, inspector.
2. **`permisos.alcance` como VARCHAR(100) plano** — Sin jerarquía, sin validación, se rompe silenciosamente con typos.
3. **Sin herencia de permisos** — Un `operario` de policía no hereda "ver activos" de su rol ni de su departamento.
4. **Sin distinción VER vs EDITAR** — Un alcalde debe poder ver todo pero NO editar salarios ni crear usuarios.
5. **Sin RLS real** — El filtrado está en middleware Node.js, no en PostgreSQL. Un bug en la API expone todos los datos.
6. **Sin lock release automático** — Si un usuario abre un activo, lo bloquea con optimistic locking, y se va → el activo queda bloqueado para siempre.

#### Arquitectura RBAC corregida (3 capas)

```
Capa 1: PLATAFORMA
┌─────────────────────────────────┐
│  superadmin                     │
│  • Gestiona toda la plataforma  │
│  • Crear organizaciones         │
│  • Configurar tiers/precios     │
│  • Ver logs de todas las orgs   │
└─────────────────────────────────┘

Capa 2: ORGANIZACIÓN (por tenant)
┌─────────────────────────────────┐
│  admin_org (1 por organización) │
│  • Puede TODO en su org         │
│  • Crear/editar/eliminar        │
│    CUALQUIER recurso            │
│  • Gestionar usuarios locales   │
│  • Definir roles personalizados │
│  • Ver audit logs de su org     │
│  • Override de optimistic locks │
├─────────────────────────────────┤
│  roles_personalizados           │
│  (cada organización define      │
│   sus propios roles con         │
│   permisos asignables)          │
└─────────────────────────────────┘

Capa 3: DATOS
┌─────────────────────────────────┐
│  RLS en PostgreSQL (obligatorio)│
│  • org_id en TODAS las queries  │
│  • RLS policies por tabla       │
│  • current_setting('app.*')     │
└─────────────────────────────────┘
```

#### Schema de permisos corregido

```sql
-- ============================================
-- ROLES: ya no son CHECK fijo, son por organización
-- ============================================

CREATE TABLE roles_organizacion (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizaciones(id),
    nombre VARCHAR(100) NOT NULL,           -- 'alcalde', 'concejal', 'inspector_medioambiental'
    nivel INTEGER NOT NULL DEFAULT 0,       -- 0=admin, 10=directivo, 50=operario, 99=lectura
    hereda_de UUID REFERENCES roles_organizacion(id),  -- Herencia: operario hereda de lectura
    es_admin BOOLEAN DEFAULT false,         -- Si true, puede overridear TODO
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (org_id, nombre)
);

-- ============================================
-- PERMISOS: estructurados, no VARCHAR mágico
-- ============================================

CREATE TABLE permisos_rol (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rol_id UUID NOT NULL REFERENCES roles_organizacion(id),
    
    -- Qué recurso
    recurso_categoria VARCHAR(100) NOT NULL,  -- 'contenedor', 'ambulancia', 'doctor', 'usuario', 'documento'
    
    -- Niveles de permiso (jerárquicos: READ < WRITE < DELETE < ADMIN)
    permiso_nivel VARCHAR(20) NOT NULL CHECK (permiso_nivel IN (
        'none',         -- Sin acceso (explícito)
        'read',         -- Solo ver
        'write',        -- Ver + crear + editar (implica read)
        'delete',       -- Ver + editar + borrar (implica write)
        'admin'         -- Todo + conceder a otros (implica delete)
    )),
    
    -- Alcance geográfico/departamental
    alcance_tipo VARCHAR(30) NOT NULL CHECK (alcance_tipo IN (
        'global',           -- Todo el municipio
        'departamento',     -- 'policia', 'sanidad', 'urbanismo'
        'zona',             -- 'centro', 'norte', 'poligono_industrial'
        'propio'            -- Solo activos que creó o tiene asignados
    )),
    alcance_valor VARCHAR(100),  -- Valor concreto: 'policia', 'centro', etc. NULL si alcance_tipo = 'global'
    
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (rol_id, recurso_categoria, alcance_tipo, COALESCE(alcance_valor, '__global__'))
);

-- ============================================
-- PERMISOS ESPECIALES (ad-hoc, para excepciones)
-- ============================================

CREATE TABLE permisos_usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL REFERENCES usuarios(id),
    recurso_categoria VARCHAR(100) NOT NULL,
    permiso_nivel VARCHAR(20) NOT NULL CHECK (permiso_nivel IN ('none', 'read', 'write', 'delete', 'admin')),
    alcance_tipo VARCHAR(30) NOT NULL,
    alcance_valor VARCHAR(100),
    granted_by UUID NOT NULL REFERENCES usuarios(id),
    expira_en TIMESTAMPTZ,  -- NULL = permanente
    motivo TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (usuario_id, recurso_categoria, alcance_tipo, COALESCE(alcance_valor, '__global__'))
);

-- ============================================
-- RLS: aislamiento REAL en PostgreSQL
-- ============================================

-- Función helper
CREATE OR REPLACE FUNCTION app_current_org_id() RETURNS UUID AS $$
    SELECT NULLIF(current_setting('app.org_id', true), '')::UUID;
$$ LANGUAGE SQL STABLE;

CREATE OR REPLACE FUNCTION app_current_user_id() RETURNS UUID AS $$
    SELECT NULLIF(current_setting('app.user_id', true), '')::UUID;
$$ LANGUAGE SQL STABLE;

CREATE OR REPLACE FUNCTION app_is_admin() RETURNS BOOLEAN AS $$
    SELECT current_setting('app.is_admin', true) = 'true';
$$ LANGUAGE SQL STABLE;

-- RLS en activos
ALTER TABLE activos ENABLE ROW LEVEL SECURITY;

-- Policy base: solo activos de mi organización
CREATE POLICY activos_org ON activos
    FOR ALL USING (org_id = app_current_org_id());

-- Policy para admin: puede ver/editar todo en su org
CREATE POLICY activos_admin ON activos
    FOR ALL USING (app_is_admin() AND org_id = app_current_org_id())
    WITH CHECK (true);

-- Policy para operario con alcance de zona
CREATE POLICY activos_zona ON activos
    FOR ALL USING (
        org_id = app_current_org_id()
        AND (
            -- El usuario tiene alcance_zona = valor de activos.zona
            EXISTS (
                SELECT 1 FROM permisos_usuario pu
                JOIN usuarios u ON u.id = pu.usuario_id
                WHERE u.id = app_current_user_id()
                  AND pu.alcance_tipo = 'zona'
                  AND (activos.metadata->>'zona') = pu.alcance_valor
                  AND pu.permiso_nivel IN ('write', 'delete', 'admin')
            )
            OR app_is_admin()
        )
    );

-- ============================================
-- LOCK RELEASE AUTOMÁTICO
-- ============================================

ALTER TABLE activos ADD COLUMN IF NOT EXISTS locked_by UUID REFERENCES usuarios(id);
ALTER TABLE activos ADD COLUMN IF NOT EXISTS locked_at TIMESTAMPTZ;

-- Función de liberación automática (ejecutar cada 5 min vía cron)
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

#### Middleware de autorización (Node.js)

```javascript
// middleware/rls-context.js
// Antes de cada request, inyecta el contexto en PostgreSQL para RLS
async function setRLSContext(req, res, next) {
    if (req.user) {
        await pool.query(`SELECT set_config('app.org_id', $1, true)`, [req.user.org_id]);
        await pool.query(`SELECT set_config('app.user_id', $1, true)`, [req.user.id]);
        await pool.query(`SELECT set_config('app.is_admin', $1, true)`, 
            [req.user.es_admin ? 'true' : 'false']);
    }
    next();
}

// middleware/permission-check.js
// Verificación adicional a nivel de aplicación (no solo RLS)
function requirePermission(categoria, nivelMinimo, alcanceTipo = null) {
    return async (req, res, next) => {
        if (req.user.es_admin) return next();  // ADMIN puede TODO
        
        const tienePermiso = await checkPermission(
            req.user.id, categoria, nivelMinimo, alcanceTipo, req.params.zona
        );
        
        if (!tienePermiso) {
            return res.status(403).json({
                error: 'permiso_denegado',
                message: `No tienes permiso para ${accionNivel(nivelMinimo)} ${categoria}`,
                required: { categoria, nivelMinimo, alcance: alcanceTipo }
            });
        }
        next();
    };
}
```

#### Verificación de permisos en Node.js

```javascript
// services/permission-query.js
async function checkPermission(userId, categoria, nivelMinimo, alcanceTipo, alcanceValor) {
    const niveles = { 'none': 0, 'read': 1, 'write': 2, 'delete': 3, 'admin': 4 };
    const minNivel = niveles[nivelMinimo];
    
    const { rows } = await pool.query(`
        -- 1. Check permisos del rol del usuario (herencia incluida)
        WITH RECURSIVE roles_chain AS (
            SELECT r.id, r.nivel, r.heredar_de, r.es_admin
            FROM roles_organizacion r
            JOIN usuarios u ON u.rol_id = r.id
            WHERE u.id = $1
            
            UNION ALL
            
            SELECT r.id, r.nivel, r.heredar_de, r.es_admin
            FROM roles_organizacion r
            JOIN roles_chain rc ON r.id = rc.heredar_de
        )
        SELECT MAX(niveles.permiso_valor) AS max_nivel
        FROM permisos_rol pr
        JOIN roles_chain rc ON pr.rol_id = rc.id
        CROSS JOIN (VALUES ($3::INTEGER)) AS niveles(permiso_valor)
        WHERE pr.recurso_categoria = $2
          AND (
              (pr.alcance_tipo = 'global')
              OR (pr.alcance_tipo = $4 AND pr.alcance_valor = $5)
          )
        HAVING MAX(niveles.permiso_valor) >= $3
        
        UNION ALL
        
        -- 2. Check permisos ad-hoc del usuario
        SELECT 1 FROM permisos_usuario pu
        WHERE pu.usuario_id = $1
          AND pu.recurso_categoria = $2
          AND (
              (pu.alcance_tipo = 'global')
              OR (pu.alcance_tipo = $4 AND pu.alcance_valor = $5)
          )
          AND (pu.expira_en IS NULL OR pu.expira_en > now())
          AND (
              CASE pu.permiso_nivel
                  WHEN 'read' THEN 1 WHEN 'write' THEN 2
                  WHEN 'delete' THEN 3 WHEN 'admin' THEN 4
                  ELSE 0
              END
          ) >= $3
    `, [userId, categoria, minNivel, alcanceTipo, alcanceValor]);
    
    return rows.length > 0;
}
```

#### Reglas del sistema de permisos (resumen)

| Aspecto | Regla |
|---------|-------|
| **Admin puede TODO** | `es_admin = true` en el rol → bypass completo de permisos. Puede overridear cualquier restricción. |
| **Nuevos recursos** | Añadir `recurso_categoria` nuevo en `permisos_rol` y la policy RLS correspondiente. No requiere migración de schema. |
| **Roles por tenant** | Cada organización crea sus roles con `roles_organizacion`. Sin límite. |
| **Herencia** | Un rol puede heredar de otro via `heredar_de`. Si un rol base cambia permisos, todos los que heredan se actualizan. |
| **Lock release** | Campo `locked_by` + `locked_at`. Cron cada 5 min libera locks > 10 min. |
| **RLS obligatorio** | Nunca confiar solo en middleware Node.js. PostgreSQL RLS es la última línea de defensa. |
| **Ver vs Editar** | `read` ≠ `write`. Un `directivo` tiene `read` en salarios pero no `write`. |
| **Permisos temporales** | `permisos_usuario.expira_en` para permisos por tiempo limitado (sustituciones, inspecciones). |

### Optimistic locking (v2 — con lock release)
- Campo `version` en cada registro activo
- UPDATE solo si `version = version_actual`
- Si falla → "Este activo está siendo editado por otro usuario"
- **NUEVO:** Campo `locked_by` + `locked_at` para saber QUIÉN lo está editando
- **NUEVO:** Cron cada 5 minutos ejecuta `release_stale_locks()` → libera locks de >10 min
- **NUEVO:** Admin puede forzar unlock con `UPDATE activos SET locked_by = NULL WHERE id = $1`

### Audit trail
- Tabla `audit_log` particionada por mes
- Cada mutación genera entrada con: antes, después, usuario, IP, timestamp
- Usuario `@sistema` para acciones automáticas

### Plugin architecture
- Cada dominio (residuos, policía, sanidad) es un módulo independiente
- Módulo = { assetTypes, profiles, kpis, hooks, routes, dashboard }
- Se cargan dinámicamente según config del tenant

### Hot/Warm/Cold
- Hot (0-3 meses): SSD, queries < 50ms
- Warm (3-12 meses): disco estándar, queries < 500ms
- Cold (> 12 meses): comprimido, acceso bajo demanda

### Document management
- PDFs en MinIO, no en PostgreSQL
- Metadata + texto extraído en BD
- Full-text search (PostgreSQL tsvector) + ChromaDB (semántica)
- Búsqueda híbrida: FTS + embeddings + RRF fusion

## Schema base (resumen)

### Tablas principales
- `organizaciones` — Multi-tenant root
- `usuarios` — Auth + RBAC (7 roles)
- `activos` — Tabla central (físicos + humanos)
- `audit_log` — Particionado por mes
- `movimientos` — Historial de desplazamientos
- `ordenes_trabajo` — Tareas asignadas
- `documentos` — PDFs + metadata + search_vector
- `mantenimientos` — Preventivo/correctivo/predictivo
- `inspecciones` — Calidad + control
- `stock` — Almacén de materiales
- `perfiles` — Perfiles de personal
- `turnos` — Turnos de trabajo
- `asignaciones` — Persona → turno → ubicación
- `permisos_empleado` — Vacaciones, bajas, formaciones
- `fuentes_video` — Cámaras CCTV
- `documento_versiones` — Control de versiones
- `documento_anotaciones` — Comentarios en docs

### Índices críticos
- GIST en `activos.geometry` (consultas espaciales)
- GIN en `documentos.search_vector` (full-text search)
- GIN en `documentos.tags` (búsqueda por etiquetas)
- BTree en `activos(org_id, tipo, estado)` (dashboard)
- BTree en `audit_log(recurso_id, timestamp)` (auditoría)

## Roadmap de desarrollo

### Fase 0 — Planificación (2-4 semanas)
- [ ] Definir schema completo
- [ ] Diseñar API REST
- [ ] Prototipar frontend 3D
- [ ] Elegir hosting definitivo
- [ ] Definir modelo de negocio

### Fase 1 — MVP funcional (2 semanas)
- [ ] PostgreSQL + schema base
- [ ] Express backend + auth JWT
- [ ] API CRUD activos + optimistic locking
- [ ] Three.js terreno DEM + terrain snapping
- [ ] 50 activos demo + dashboard KPIs

### Fase 2 — Gestión completa (3 semanas)
- [ ] Sistema usuarios 5 roles + audit trail
- [ ] CRUD completo (formularios, filtros, paginación)
- [ ] Gestión documental (upload PDF + extracción)
- [ ] Full-text search PostgreSQL
- [ ] Perfiles personal + turnos + asignaciones

### Fase 3 — IA + Real-time (3 semanas)
- [ ] ChromaDB + búsqueda semántica
- [ ] Asistente IA (RAG)
- [ ] WebSocket (posiciones en vivo)
- [ ] Integraciones (AEMET, Renfe, cámaras)
- [ ] Efectos visuales según clima

### Fase 4 — Producción (2 semanas)
- [ ] Tests (unit + integración)
- [ ] Docker + deploy
- [ ] Monitoreo + alertas
- [ ] Documentación API
- [ ] Primer cliente piloto

## Filosofía de desarrollo

### Planificar ANTES de codear
David insiste: **meses de planificación antes de escribir código.** Un ERP mal diseñado se convierte en infierno de deuda técnica. Prioridad:
1. Schema completo de BD
2. API REST diseñada (OpenAPI)
3. Prototipos visuales (sin backend)
4. Hosting definido
5. Modelo de negocio
6. SÓLO ENTONCES empezar a codear

### Nombres en español
David rechaza nombres en inglés para proyectos suyos. Buscar nombres en español que tengan identidad, significado y sean fáciles de recordar. Ejemplo: "TerrAn" = Territorio + Antizar + NaN.

### Evaluar herramientas antes de integrar
Cuando se propone usar una librería/herramienta existente, analizar:
1. Qué hace la herramienta
2. Qué necesita TerrAn que la herramienta NO cubre
3. Qué componentes de la herramienta SÍ se pueden reutilizar
4. Si construir encima aporta más de lo que complica
Ver `references/gis-tool-evaluation.md` para el patrón completo.

## Referencias

- `references/gis-tool-evaluation.md` — Patrón para evaluar herramientas GIS externas (GeoLibre analysis)
- `references/erp-patterns.md` — 10 patrones de diseño ERP: optimistic locking, audit trail, RLS, plugins, búsqueda híbrida, docs, terrain snapping, WebSocket, soft delete, materialized views
- `references/terran-audit-setup.md` — Sistema de auto-auditoría cíclica: cron + state file + 8 fases de auditoría. Creado en sesión 2026-06-11.
- `references/audit-42-issues.md` — Los 42 issues encontrados en las primeras 2 fases de auditoría (Schema 28 + Permisos 14). Archivo vivo.
- `references/security-compliance-audit-checklist.md` — Checklist de los 23 issues de seguridad y compliance (fases 06), verificados contra documentos. Generado iter 90, 2026-06-13.
- `references/security-compliance-issues-detailed.md` — Listado completo de los 36 issues de seguridad (iter 90-106) con distribución por categoría y estado actual.
- `references/usuarios-missing-org-id.md` — Caso concreto: tabla usuarios sin org_id pero RLS policy lo referencia (SEC-064, iter 144). Ver también en skill `terran-schema-fix`.
- `references/business-logic-audit.md` — Los 10 issues encontrados en fase 07 (Lógica de Negocio): importación masiva, tiers, onboarding, pricing, trials. Iter 107.

### Pitfall: JSON encoding en `log-issue` del auditor (iter 90, 2026-06-13)

El script `terran-auditor.py` usa `sys.argv[3]` con `json.loads()` — **no acepta comillas simples dentro del JSON**. Si el JSON contiene `"` o `'`, el shell las escapa mal y `json.loads()` falla con `Unterminated string`.

**Solución 1 (recomendada):** Usar `execute_code` con un script Python temporal:
```python
import json, subprocess
issue = {"id": "SEC-064", "title": "Usuarios sin org_id", "severity": "alta", "description": "...", "impact": "...", "proposed_solution": "..."}
json_str = json.dumps(issue, ensure_ascii=False)
result = subprocess.run(
    ["python3", "/hermes-home/scripts/terran-auditor.py", "log-issue", "06-security-compliance", json_str],
    capture_output=True, text=True
)
print(result.stdout)
```

**Solución 2:** Usar unicode escapes (`\u2014` para `—`, `\u201c` para `"`).

**Solución 3:** Escribir el JSON a un archivo y leerlo desde el script con `sys.stdin`.

### Pitfall: `log-issue` requiere phase ID completo (iter 156)

El script acepta el phase ID completo (`06-security-compliance`), NO un prefijo corto (`SEC`). Usar `SEC` devuelve `❌ Fase 'SEC' no encontrada`. **Siempre verificar el ID en `audit-state.json` → `phases[].id`**. Ver `references/audit-tool-usage.md` en skill `terran-schema-fix`.

### Pitfall: RLS enabled SIN policy = todo bloqueado (iter 144)

### Pitfall: RLS enabled SIN policy = todo bloqueado (iter 144)

Habilitar RLS con `ALTER TABLE x ENABLE ROW LEVEL SECURITY` pero NO crear ninguna `CREATE POLICY` **bloquea TODAS las operaciones** (SELECT, INSERT, UPDATE, DELETE) para TODOS los usuarios. No es "sin aislamiento" — es "sin acceso".

Esto afecta a 6+ tablas en TerrAn: stock, mantenimientos, turnos, asignaciones, fuentes_video, perfiles. Todas tenían RLS enabled pero sin policy, lo que hacía el sistema de CCTV, stock, mantenimientos, turnos y perfiles **completamente inaccesible**.

**Regla:** Cada `ALTER TABLE ENABLE ROW LEVEL SECURITY` debe ir inmediatamente seguido de su `CREATE POLICY`. Nunca dejar tablas con RLS enabled pero sin policies.

**Checklist RLS correcto:**
1. `ALTER TABLE x ENABLE ROW LEVEL SECURITY;`
2. `CREATE POLICY tenant_isolation_x ON x FOR ALL USING (org_id = current_org_id());`
3. `CREATE POLICY superadmin_bypass_x ON x FOR ALL USING (EXISTS (SELECT 1 FROM usuarios u JOIN roles_organizacion ro ON u.rol_id = ro.id WHERE u.id = current_user_id() AND ro.es_admin = true));`

### Pitfall: superadmin_bypass debe cubrir TODAS las tablas (iter 144)

El superadmin_bypass solo existía en la tabla `activos`. Un superadmin no podía gestionar usuarios de su propia organización, ni ver organizaciones, ni acceder a turnos, asignaciones, perfiles, stock, mantenimientos, fuentes_video, ni activos_humanos.

**Regla:** Cada tabla con RLS debe tener un superadmin_bypass. El superadmin de una organización debe poder TODO en su organización.

**Verificación:** Ejecutar `grep -r 'superadmin_bypass ON' ARQUITECTURA.md` y comparar con `grep -r 'ENABLE ROW LEVEL SECURITY' ARQUITECTURA.md`. Cada tabla con RLS debe tener un bypass correspondiente.

### Pitfall: activos_humanos sin org_id, sin RLS, sin encriptación (iter 144)

La tabla `activos_humanos` (DNI, NSS, datos médicos, aptitud física, colección de sangre) tiene TRES fallos simultáneos:
1. Sin columna `org_id` → fuga de datos entre organizaciones
2. Sin RLS enabled → datos de salud expuestos sin defensa en profundidad
3. Sin encriptación (pgcrypto) → DNI/NSS/texto plano → violación RGPD Art. 9

**Regla:** Cualquier tabla que almacene datos personales sensibles DEBE tener: org_id, RLS enabled + policy, y encriptación de campos sensibles con pgcrypto.

### Pitfall: security_log, login_attempts, password_history sin org_id (iter 144)

Las tablas de seguridad (security_log, login_attempts, password_history) no tienen org_id. Un admin de una organización pequeña puede ver los logs de seguridad de TODAS las organizaciones.

**Regla:** TODAS las tablas, incluyendo logs de seguridad, deben tener org_id y RLS. Los logs de seguridad son datos sensibles que deben estar aislados por tenant.

### Pitfalls conocidos

- **No asumir que es un "gemelo digital" de visualización** — Cuando el usuario describe "ver cosas en un mapa", preguntar PRIMERO sobre la lógica de negocio (CRUD, inventarios, contratos, personal). El 80% de TerrAn es backend ERP, no 3D.
- **PostgreSQL JSONB no es una DB dentro de la DB** — usar tablas normalizadas para datos consultados frecuentemente
- **Optimistic locking falla silenciosamente** — siempre devolver error claro al usuario
- **ChromaDB embeddings costosos** — indexar solo documentos > 1KB, no notas cortas
- **PDFs españoles son un desastre** — encoding, formatos variados, scanning
- **Multi-tenant sin RLS = agujero de seguridad** — SIEMPRE filtrar por org_id
- **Audit log crece rápido** — particionar por mes desde el día 1
- **Three.js con muchos objetos** — InstancedMesh + LOD siempre
- **GIS tools ≠ ERP tools** — Herramientas como GeoLibre son GIS puros. No tienen auth, audit, CRUD de activos, ni gestión documental. No construir un ERP encima de un GIS.
- **Roles fijos en CHECK no escalan** — Cada tenant necesita roles distintos. Usar tabla `roles_organizacion` en lugar de CHECK constraint.
- **Permisos con VARCHAR libre es trampa** — `alcance VARCHAR(100)` sin estructura → bugs silenciosos por typos, sin validación. Usar `alcance_tipo ENUM + alcance_valor VARCHAR`.
- **Sin herencia de permisos = duplicación masiva** — Si cada usuario necesita permiso explícito, hay cientos de filas en `permisos`. Usar herencia de roles via `heredar_de`.
- **Lock sin release = activos muertos** — Si un usuario abre un activo y cierra el navegador, el optimistic locking lo bloquea para siempre. Añadir `locked_by` + `locked_at` + cron de release.
- **RLS no es opcional** — El middleware Node.js puede tener bugs. PostgreSQL RLS es la última línea de defensa. Siempre habilitarlo.
- **Audit log con snapshots completos crece 10x más rápido** — Guardar solo el diff de campos que cambiaron, no el snapshot entero. Calcular: 200K acciones/mes × 2KB = 400MB/mes.
- **JSONB en activos.metadata para datos de personal = no consultable** — No poner formaciones, permisos, puestos en JSONB. Usar tablas relacionadas si necesitas hacer queries sobre ellos.
- **Datos sensibles en JSONB sin encriptar** — DNI, datos médicos, permisos de armas en metadata JSONB texto plano. Violación RGPD Art. 9. Usar pgcrypto o tabla separada encriptada.
- **Audit log sin org_id = fuga multi-tenant** — Sin org_id en audit_log, no se puede filtrar por organización. Un admin del Ayuntamiento A ve el audit de todos.
- **JWT sin revocación = acceso post-despedido** — Token JWT stateless sin blacklist = usuario despedido sigue accesible. TTL 15 min + refresh + token_blacklist.
- **Sin RLS = dependencia total del middleware** — Sin Row-Level Security en PostgreSQL, un bug en Express expone TODOS los datos de TODOS los tenants. RLS es la última línea de defensa.
- **Ley 39/2015 + eIDAS obligatorios** — Firma electrónica sin validez legal hace el sistema inútil para administración pública. Integrar FNMT/Cl@ve.

### Pitfall: SQL injection en pool.query() con string concatenation (SEC-075, iter 156)

Línea 3239 de ARQUITECTURA.md:
```javascript
await pool.query('UPDATE usuarios SET email = anonimiz$' || usuarioId || '@geoasset.local, nombre = 'Usuario Eliminado', apellidos = NULL WHERE id = $1', [usuarioId]);
```
DOS errores simultáneos:
1. **SQL injection**: `usuarioId` concatenado directamente en la string de query.
2. **Error de sintaxis**: comillas simples anidadas sin escape (`'Usuario Eliminado'` dentro de una string entre comillas simples).

**Solución:** Usar parámetros posicionales para todo:
```javascript
await pool.query(
    "UPDATE usuarios SET email = $1 || '@geoasset.local', nombre = $2, apellidos = NULL WHERE id = $3",
    [usuarioId, 'Usuario Eliminado', usuarioId]
);
```

### Pitfall: pgcrypto functions con SECURITY DEFINER (SEC-077, iter 156)

Las funciones `encriptar_dato()` y `desencriptar_dato()` (líneas 1170-1185) usan `SECURITY DEFINER`, ejecutándose como superuser. Cualquier usuario con EXECUTE puede desencriptar datos de CUALQUIER org.

**Solución:** Restringir EXECUTE a roles específicos o eliminar SECURITY DEFINER. Si se necesita, crear funciones separadas por org_id.

### Pitfall: audit_log INSERT sin org_id en múltiples funciones (SEC-079, iter 156)

Además de `invalidar_tokens_usuario`, la función `anonimizarUsuario` (línea 3252) también INSERTA en audit_log sin org_id. **TODAS** las funciones que INSERTAN en audit_log deben incluir org_id.

**Solución:** Revisar TODAS las INSERTs en audit_log y añadir `org_id`. Usar `current_org_id()` para obtener el org_id del contexto actual.

### Pitfall: password_history trigger referencia NEW.id inconsistente (SEC-078, iter 156)

El trigger `verificar_password_history()` usa `NEW.id` en lugar de `NEW.usuario_id`. Si el trigger está en la tabla `usuarios`, `NEW.id` funciona pero es confuso. Si se mueve el trigger a otra tabla, falla.

**Solución:** Usar `NEW.usuario_id` consistentemente. Documentar claramente dónde está attached el trigger.

### Pitfall: JSON encoding en `log-issue` del auditor (iter 90, 2026-06-13)

El script `terran-auditor.py` usa `sys.argv[3]` con `json.loads()` — **no acepta comillas simples dentro del JSON**. Si el JSON contiene `"` o `'`, el shell las escapa mal y `json.loads()` falla con `Unterminated string`.

**Solución:** Usar `execute_code` con `json.dumps(issue, ensure_ascii=False)` para generar el JSON, luego pasarlo al comando. O usar unicode escapes (`\u2014` para `—`, `\u201c` para `"`).

### Pitfall: Estado del auditor — la fase activa no tiene key `current_phase`

El `audit-state.json` usa un array `phases[]` con un flag `clear: true` en las fases ya auditadas. La fase activa es la que tiene `clear: false` (o ausencia del flag). No hay key `current_phase` en la raíz.

Para leer el estado: iterar `phases[]` y buscar la que tenga `clear == false` o `clear == null`.

### Pitfall: max_issues_per_phase=20 es insuficiente para fases de seguridad

La config del auditor tiene `max_issues_per_phase: 20` pero una fase de seguridad/compliance puede tener 30-50 issues reales. El límite NO impide que se acumulen más issues — simplemente no se aplica. La fase 06 acumuló 36 issues (iter 106). **Subir el límite a 100+** para evitar confusiones.

### Pitfall: Formato de salida de `terran-auditor.py run` varía entre iteraciones

En algunas iteraciones, el `run` devuelve `phase` como un objeto plano con `issues_already_found` y `issues_already_fixed` directamente. En otras, devuelve `phases` como array. **Siempre verificar ambas estructuras** al parsear la salida. En iter 106, la estructura plana fue la correcta: `data['phase']['issues_already_found']`.

### Pitfall: ChromaDB sin aislamiento multi-tenant

ChromaDB no tiene RLS ni aislamiento de base de datos. Los documentos indexan con `org_id` en metadatos, pero si la consulta ChromaDB no filtra por `org_id` correctamente (o hay un bug en el código Node.js), un usuario puede ver embeddings de documentos de otra organización. **Solución:** filtrar `org_id` en Node.js ANTES de enviar query a ChromaDB, con verificación estricta. O usar colecciones separadas por `org_id`.

### Pitfall: Tabla permisos sin org_id — permisos globales entre organizaciones

La tabla `permisos` no tiene columna `org_id`. Los permisos de un usuario son GLOBALES, no específicos de su organización. Un usuario del Ayuntamiento A con permiso sobre 'contenedor' podría acceder a contenedores del Ayuntamiento B. **Solución:** añadir `org_id UUID NOT NULL` a la tabla permisos.

### Pitfall: Roles hardcodeados en CHECK constraint — no escalan a multi-tenant

La tabla `usuarios` tiene `CHECK (rol IN ('superadmin','admin','directivo','jefe_dept','operario','ciudadano','sistema'))`. Esto impide que cada ayuntamiento defina sus propios roles. Además, no hay `org_id` en la tabla `usuarios`, no se puede filtrar por organización. **Solución:** mover roles a tabla `roles_organizacion` con `org_id`, eliminar CHECK constraint.

### Pitfall: Fixes marcados como "fixed" pueden tener errores estructurales (iter 146)

El `audit-state.json` puede marcar issues como `fixed` pero las soluciones documentadas tienen errores: dobles comas en SQL (`BIGSERIAL PRIMARY KEY,,`), columnas faltantes referenciadas por RLS policies, funciones que INSERTAN sin org_id, documentos inconsistentes entre sí. **NUNCA confiar en `status: "fixed"` sin verificar en los documentos.** Verificar: (1) sintaxis SQL válida, (2) columnas referenciadas existen, (3) RLS policies referencian columnas existentes, (4) funciones INSERTAN con org_id, (5) documentos sincronizados. Ver `references/audit-verification-pattern.md` en skill `terran-schema-fix`.
