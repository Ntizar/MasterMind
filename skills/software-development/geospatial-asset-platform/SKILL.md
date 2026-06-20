---
name: geospatial-asset-platform
description: "Patrón completo para construir plataformas SaaS de gestión de activos georreferenciados con vista 3D — municipal, hospitalario, logístico. PostgreSQL+PostGIS, Three.js, optimistic locking, audit trail, plugin modules, SaaS por volumen."
version: "1.0.0"
author: David Antizar
tags: [gis, 3d, threejs, postgresql, postgis, saas, asset-management, digital-twin, municipal, plugin-architecture]
---

# Geospatial Asset Platform — Patrón de Plataforma

## Cuándo cargar esta skill

Cuando el usuario pida: gestión de activos georreferenciados, gemelo digital municipal, plataforma de inventarios con mapa 3D, sistema de gestión para ayuntamientos/hospitales/empresas con componente geoespacial, "SimCity con datos reales", asset tracking con mapa, dashboard de inventarios con ubicaciones.

## Concepto

Plataforma SaaS multi-tenant donde organizaciones (ayuntamientos, hospitales, empresas) gestionan activos físicos y humanos sobre un mapa 3D interactivo. Cada activo tiene coordenadas GNSS reales, historial de movimientos, y datos enlazados con APIs públicas (clima, tráfico, trenes, cámaras).

**Diferenciador clave:** Nadie ofrece gestión de activos + vista 3D + datos en tiempo real. Las alternativas son Excel o software GIS carísimo (ArcGIS 50K€/año).

## Arquitectura resumida

```
Frontend 3D (Three.js + DEM terrain + OSM buildings)
    ↕ WebSocket + REST
Backend (Node.js + Express + plugin modules)
    ↕
PostgreSQL + PostGIS (optimistic locking, audit trail)
    ↕
Integraciones (AEMET, Renfe, DGT, Catastro, CCTV)
```

## Principios de BD (NO negociables)

1. **Fuente única de verdad** — UNA tabla `activos` para todo (contenedores, ambulancias, doctores, farolas)
2. **Optimistic locking** — campo `version` en cada registro. Si dos usuarios intentan mover el mismo activo, el segundo recibe error de conflicto
3. **Soft delete** — NUNCA borrar registros, solo `deleted_at`. El audit trail sobrevive
4. **Audit trail completo** — cada mutación genera entrada en `audit_log` con antes/después
5. **Usuario `@sistema`** — usuario ficticio que registra acciones automáticas (no humanas)
6. **JSONB para metadata flexible** — cada tipo de activo tiene campos diferentes en `metadata JSONB`

## Tablas principales

### activos (tabla central)
```sql
CREATE TABLE activos (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES organizaciones(id),
    codigo VARCHAR(50),          -- Código interno del ayuntamiento
    categoria VARCHAR(100),      -- 'infraestructura', 'vehiculo', 'humano', 'equipo'
    tipo VARCHAR(100),           -- 'contenedor', 'ambulancia', 'doctor', 'farola'
    lat DECIMAL(10,7), lng DECIMAL(10,7),
    geometry GEOMETRY(Point, 4326),
    estado VARCHAR(50),          -- 'activo', 'mantenimiento', 'disponible', 'en_mision'
    metadata JSONB DEFAULT '{}', -- Datos específicos por tipo
    parent_id UUID REFERENCES activos(id),  -- Jerarquía (contenedor → camión → almacén)
    version INTEGER DEFAULT 1,   -- Optimistic locking
    deleted_at TIMESTAMPTZ,      -- Soft delete
    created_by UUID, updated_by UUID
);
```

### audit_log (particionado por mes)
```sql
CREATE TABLE audit_log (
    id BIGSERIAL,
    usuario_id UUID,
    accion VARCHAR(50),    -- 'crear', 'mover', 'editar', 'eliminar', 'cambiar_estado'
    recurso VARCHAR(100),  -- tipo de activo
    recurso_id UUID,
    antes JSONB,           -- Snapshot anterior (NULL en INSERT)
    despues JSONB,         -- Snapshot nuevo (NULL en DELETE)
    timestamp TIMESTAMPTZ
) PARTITION BY RANGE (timestamp);
```

### Otras tablas clave
- **movimientos** — historial de desplazamientos (origen → destino, quién, cuándo, evidencia)
- **ordenes_trabajo** — tareas asignadas con prioridad y estado
- **permisos_empleado** — vacaciones, bajas, formaciones
- **formaciones** — certificaciones con caducidad
- **mantenimientos** — preventivo/correctivo/predictivo con costes
- **inspecciones** — controles de calidad con puntuación
- **stock** — materiales de almacén con alertas de stock mínimo
- **fuentes_video** — cámaras CCTV con stream en tiempo real
- **perfiles** — perfiles de personal (médico, policía, bombero) con plantilla mínima/máxima
- **turnos / asignaciones** — gestión de turnos y cobertura

Schema completo: `/root/workspace/geoasset/ARQUITECTURA.md`

## Plugin Module System

Cada dominio (residuos, policía, sanidad, transporte) es un módulo independiente:

```javascript
// modules/residuos/index.js
module.exports = {
    name: 'residuos',
    assetTypes: [{ tipo: 'contenedor', modelo3d: 'contenedor_240l' }],
    profiles: [{ nombre: 'Recolector', departamento: 'residuos' }],
    kpis: [{ id: 'pct_llenos', formula: '...' }],
    hooks: {
        'asset:moved': async (activo) => { /* recalcular rutas */ }
    },
    routes: '/api/modules/residuos'
};
```

Carga dinámica en server.js: solo módulos habilitados para el tenant se registran.

## Rendimiento con datos masivos

### Proyecciones de tamaño (1 tenant grande, 5 años)
- Activos + personal: ~70 MB
- Audit log: ~50 GB (particionado por mes)
- Movimientos: ~5 GB
- Total: ~70 GB → manejable con PostgreSQL

### Estrategia Hot/Warm/Cold
- **Hot (SSD):** datos últimos 3 meses + tablas de activos (siempre)
- **Warm (estándar):** datos 3-12 meses
- **Cold (archivado):** datos > 12 meses, comprimidos, export a S3

### Optimizaciones
1. **Partitioning por mes** en audit_log y movimientos (pg_partman)
2. **Materialized Views** para KPIs (refresh cada 5 min, no en cada request)
3. **Redis cache** para posiciones en tiempo real (TTL 10s) y KPIs (TTL 5 min)
4. **Índices GIST** en geometry para queries espaciales (bounding box, radio)
5. **JSONB** comprimido vía TOAST (~60-70% reducción)

## SaaS Pricing (modelo híbrido: volumen + features)

| Tier | Activos | Módulos | Usuarios | Precio/mes |
|---|---|---|---|---|
| Starter | 500 | 2 | 3 | 199€ |
| Professional | 5.000 | Todos | 15 | 799€ |
| Enterprise | 25.000 | Todos + APIs | 50 | 2.499€ |
| Municipio Grande | 100.000 | Todo + Cámaras | ∞ | 5.999€ |

Add-ons: Cámaras (99€/cámara), Renfe (199€), AEMET (149€), App móvil (499€)

ROI para cliente: ahorro ~95K€/año vs coste 30K€/año → ROI 3.2x

## 3D Visualization Layer

- **Terreno:** DEM Copernicus 30m → Three.js mesh
- **Edificios:** OpenStreetMap footprints + heights → extruir
- **Activos:** InstancedMesh (1 modelo × N copias) + LOD
- **Terrain snapping:** Raycaster contra DEM para posicionar activos sin que floten ni se hundan
- **Clima real:** AEMET → iluminación solar + partículas lluvia/niebla
- **Trenes:** Renfe API → meshes moviéndose en tiempo real
- **Cámaras:** RTSP streams → popup 3D al hacer click

## Integraciones públicas

| Fuente | Qué aporta | Coste |
|---|---|---|
| OpenStreetMap | Edificios, carreteras, POIs | Gratis |
| DEM Copernicus/SRTM | Elevación terreno 30m | Gratis |
| AEMET | Clima en tiempo real | Gratis (API pública) |
| Renfe | Posición trenes Cercanías | Gratis (API pública) |
| Catastro | Coordenadas oficiales | Gratis (API pública) |
| Sentinel-2 (Copernicus) | Texturas satélite, NDVI | Gratis |

## Pitfalls

- **NO usar SVG para >500 polígonos en el mapa 2D** — usar Canvas renderer (Leaflet) o Three.js para 3D
- **NO calcular KPIs en cada request** — usar materialized views con refresh cada 5 min
- **NO cachear mutaciones** — solo cache en Redis para reads. Writes siempre a BD
- **NO borrar registros** — soft delete + partición detach para archivado
- **Optimistic locking NO es opcional** — sin él, dos operarios mueven el mismo contenedor y se pierde estado
- **JSONB metadata NO debe tener keys dinámicas por usuario** — el schema de metadata está definido por tipo de activo, no por el usuario
- **Terrain snapping debe ser OBLIGATORIO** — cada activo se posiciona justo sobre el terreno via raycaster. Sin esto, las cosas flotan o se hunden

## Overlap con otros skills

- **`espanatlas-architecture`** — cubre patrón 2D (Leaflet + Canvas + TopoJSON + lazy loading). Este skill cubre 3D + asset management. Complementarios, no redundantes.
- **`threejs-3d-web`** — cubre rendering Three.js (scene, camera, materials, LOD). Este skill usa Three.js pero se enfoca en la plataforma completa (BD + API + 3D + negocio).
- **`refactor-nodejs-monolith`** — cubre modularización Node.js. Este skill aplica ese patrón al contexto específico de módulos de dominio GIS.

## Referencias

- `/root/workspace/geoasset/ARQUITECTURA.md` — Schema completo de BD, estructura de directorios, plugin system, terrain snapping
- `/root/workspace/geoasset/RENDIMIENTO-Y-NEGOCIO.md` — Performance architecture, data projections, SaaS pricing model, extended data model (HR, maintenance, inspections, stock, cameras)
