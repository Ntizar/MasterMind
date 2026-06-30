---
name: terran-architecture
description: "Arquitectura completa de TerrAn — ERP municipal con vista 3D, gestión documental, IA y datos en tiempo real. Referencia para hardware, escalabilidad, RBAC y patrones."
version: "2.1.0"
author: David Antizar
tags: [erp, municipal, saas, 3d, gis, postgis, threejs, ai, rag, terran, architecture]
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
| **Deploy** | Docker + NaN Builders | — | Contenedor aislado |

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
-- ROLES: ya no son CHECK fijo, son por organización
CREATE TABLE roles_organizacion (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizaciones(id),
    nombre VARCHAR(100) NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 0,
    hereda_de UUID REFERENCES roles_organizacion(id),
    es_admin BOOLEAN DEFAULT false,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (org_id, nombre)
);

-- PERMISOS: estructurados, no VARCHAR mágico
CREATE TABLE permisos_rol (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rol_id UUID NOT NULL REFERENCES roles_organizacion(id),
    recurso_categoria VARCHAR(100) NOT NULL,
    permiso_nivel VARCHAR(20) NOT NULL CHECK (permiso_nivel IN ('none','read','write','delete','admin')),
    alcance_tipo VARCHAR(30) NOT NULL CHECK (alcance_tipo IN ('global','departamento','zona','propio')),
    alcance_valor VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (rol_id, recurso_categoria, alcance_tipo, COALESCE(alcance_valor, '__global__'))
);
```

### Optimistic locking (v2)
- Campo `version` en cada registro activo
- **NUEVO:** `locked_by` + `locked_at` para saber QUIÉN lo está editando
- **NUEVO:** Cron cada 5 min libera locks > 10 min

### Plugin architecture
- Cada dominio es un módulo independiente
- Módulo = { assetTypes, profiles, kpis, hooks, routes, dashboard }
- Se cargan dinámicamente según config del tenant

### Hot/Warm/Cold
- Hot (0-3 meses): SSD, queries < 50ms
- Warm (3-12 meses): disco estándar, queries < 500ms
- Cold (> 12 meses): comprimido, acceso bajo demanda

## Filosofía de desarrollo

### Planificar ANTES de codear
Meses de planificación antes de escribir código. Prioridad:
1. Schema completo de BD
2. API REST diseñada (OpenAPI)
3. Prototipos visuales (sin backend)
4. Hosting definido
5. Modelo de negocio
6. SÓLO ENTONCES empezar a codear

### Nombres en español
NUNCA inglés para proyectos propios de David. "TerrAn" = Territorio + Antizar + NaN.

### Evaluar herramientas antes de integrar
1. Qué hace la herramienta
2. Qué necesita TerrAn que la herramienta NO cubre
3. Qué componentes SÍ se pueden reutilizar
4. Si construir encima aporta más de lo que complica

## Referencias

- `references/gis-tool-evaluation.md` — Patrón para evaluar herramientas GIS externas
- `references/erp-patterns.md` — 10 patrones de diseño ERP
- `references/terran-audit-setup.md` — Sistema de auto-auditoría cíclica
- `references/security-compliance-audit-checklist.md` — 23 issues de seguridad y compliance
- `references/security-compliance-issues-detailed.md` — 36 issues de seguridad detallados
- `references/usuarios-missing-org-id.md` — Caso: tabla usuarios sin org_id (SEC-064)
- `references/business-logic-audit.md` — 10 issues de lógica de negocio
- `references/business-logic-audit-iter161.md` — Iter 161: 4 nuevos issues BL-011 a BL-014
- `references/audit-iteration-165.md` — Iter 165: 82 issues en seguridad
- `references/audit-iteration-181.md` — Iter 181: 12 nuevos issues (SEC-096 a SEC-101, BL-015 a BL-020)

### Pitfalls críticos

- **No asumir "gemelo digital 3D"** — El 80% de TerrAn es backend ERP, no 3D
- **PostgreSQL JSONB no es una DB dentro de la DB** — normalizar datos consultados frecuentemente
- **Roles fijos en CHECK no escalan** — Usar tabla `roles_organizacion` con `org_id`
- **Permisos con VARCHAR libre es trampa** — Usar `alcance_tipo ENUM + alcance_valor VARCHAR`
- **Sin herencia de permisos = duplicación masiva** — Usar `heredar_de`
- **Lock sin release = activos muertos** — `locked_by` + `locked_at` + cron de release
- **RLS no es opcional** — Middleware puede tener bugs. PostgreSQL RLS es la última línea de defensa
- **Audit log sin org_id = fuga multi-tenant** — Todos los logs deben tener org_id
- **JWT sin revocación = acceso post-despedido** — TTL 15 min + refresh + token_blacklist
- **Ley 39/2015 + eIDAS obligatorios** — Firma electrónica sin validez legal hace el sistema inútil

### Pitfall: BIGSERIAL con doble coma (SEC-096, iter 181)

En las líneas 3050 y 3305 de ARQUITECTURA.md: `BIGSERIAL PRIMARY KEY,,` (doble coma). Error de sintaxis SQL que impide crear las tablas security_log y login_attempts. **Verificación:** grep -n `,,` en ARQUITECTURA.md para encontrar dobles comas.

### Pitfall: security_log/login_attempts sin org_id (SEC-097, iter 181)

Las tablas security_log y login_attempts NO tienen columna org_id pero tienen RLS policies que refieren `app_current_org_id()`. Las policies no funcionan porque la columna no existe. **Solución:** añadir `org_id UUID NOT NULL` y actualizar las policies.

### Pitfall: DEFAULT_POLICIES en JS sin tabla BD (SEC-100, iter 181)

RENDIMIENTO-Y-NEGOCIO.md define DEFAULT_POLICIES en JavaScript pero no hay tabla retention_policies en BD. Las políticas están hardcodeadas en código, no son configurables por el cliente. **Solución:** crear tabla retention_policies (org_id, tabla, dias_retencion, accion, activo).

### Pitfall: getTier() hardcodeado en JS (SEC-101, iter 181)

La función getTier() referencia `tier.price`, `tier.maxActivos` pero no hay tabla tiers en el schema. Todo está hardcodeado en JavaScript. **Solución:** crear tabla tiers + suscripciones + getTier() hace query real a BD.

### Pitfall: superadmin_bypass debe cubrir TODAS las tablas (iter 144)

Cada tabla con RLS debe tener un superadmin_bypass. Un superadmin debe poder TODO en su organización.

### Pitfall: activos_humanos sin org_id, sin RLS, sin encriptación (iter 144)

La tabla activos_humanos tiene datos sensibles (DNI, NSS, datos médicos) que DEBE tener: org_id, RLS enabled + policy, y encriptación de campos sensibles con pgcrypto.

### Pitfall: RLS enabled SIN policy = todo bloqueado (iter 144)

Habilitar RLS sin crear políticas bloquea TODAS las operaciones. Cada `ALTER TABLE ENABLE ROW LEVEL SECURITY` debe ir inmediatamente seguido de su `CREATE POLICY`.

## TerrAn Schema Fix — Resolución de Issues de Auditoría (absorbido de `terran-schema-fix`)

### Procedimiento de 6 fases
El auditor cíclico de TerrAn (`terran-audit-loop`) encuentra issues en 6 fases:
| Fase | ID | Qué cubre |
|------|-----|-----------|
| 01 | DATA | Schema, constraints, triggers, tablas de referencia |
| 02 | PERM | RBAC, roles_organizacion, RLS policies, inheritance |
| 03 | ADV | Partitioning, autovacuum, retention policies, tablespaces, triggers |
| 04 | API | Zod validation, Redis rate limiting, error middleware, CORS, Helmet, WebSocket |
| 05 | PERF | Redis cache strategy, connection pooling, Sharp, code splitting, advisory locks |
| 06 | SEC | argon2id/bcrypt hashing, GDPR export, trash can, ChromaDB isolation, HTTPS/TLS |

### Flujo de trabajo
1. **Verificar `max_issues_per_phase`** en `audit-state.json` — subir a 50+ (default 20 es insuficiente para SEC)
2. **Identificar issues abiertos** por fase desde `audit-state.json`
3. **Aplicar fixes** en 3 archivos de docs (NO en BD real): `ARQUITECTURA.md`, `DOCUMENTOS-Y-IA.md`, `RENDIMIENTO-Y-NEGOCIO.md`
4. **Verificar fixes** en docs con assertions
5. **Actualizar `audit-state.json`** — marcar issues como `fixed`
6. **Verificación final** — contar issues abiertos restantes (debe ser 0)

### Patrones SQL reutilizables
- **CHECK regex:** `CONSTRAINT chk_formato CHECK (columna ~ '^[a-z]+:[a-z0-9_-]+$')`
- **CHECK array no vacío:** `CONSTRAINT chk_no_vacio CHECK (array_length(columna, 1) > 0)`
- **CHECK rango:** `EXISTS (SELECT 1 FROM unnest(columna) WHERE val < MIN OR val > MAX) = false`
- **Trigger auto-incremento por grupo:** COALESCE(MAX(version), 0) + 1
- **Partitioning por rango:** PARTITION BY RANGE (fecha) con tablas hijas por trimestre/año
- **RLS policy por org_id:** `USING (org_id = current_setting('app.current_org_id')::UUID)`
- **Partial UNIQUE:** `UNIQUE(email) WHERE deleted_at IS NULL` para reactivación de usuarios

### Pitfalls críticos
- **NO es repo git** — `/root/workspace/geoasset` sin `.git`
- **Fixes en docs, no en BD real** — TerrAn en fase de diseño
- **Overlaps entre fases** — SEC issues ya resueltos en DATA/PERM/API
- **BIGSERIAL con doble coma** (SEC-096) — `BIGSERIAL PRIMARY KEY,,`
- **security_log/login_attempts sin org_id** (SEC-097) — añadir columna + actualizar policies
- **password_history en texto plano** (SEC-098) — encriptar con pgcrypto
- **getTier() hardcodeado sin tabla tiers** (SEC-101) — crear tabla tiers + suscripciones
- **RLS policy referencia columna inexistente** — verificar con `information_schema.columns`
- **NUNCA confiar en `status: "fixed"` sin verificar en docs** — doble verificación obligatoria
- **Documentos inconsistentes entre sí** — sincronizar ARQUITECTURA.md con RENDIMIENTO-Y-NEGOCIO.md
- **CREATE POLICY y ON <table> en misma línea** — usar `line.split('ON')[1].split()[0]`
- **docs_content truncado a ~30KB** — siempre leer archivos directamente con `read_file()`
