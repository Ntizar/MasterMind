# Database Schema Patterns — Geospatial Asset Platform

## Optimistic Locking (prevenir doble movimiento)

```sql
-- Campo version en tabla activos
ALTER TABLE activos ADD COLUMN version INTEGER DEFAULT 1;

-- Update con check de versión
UPDATE activos SET lat=$1, lng=$2, version=version+1, updated_at=now()
WHERE id=$3 AND version=$4 AND deleted_at IS NULL;
-- Si rowCount=0 → conflicto: "otro usuario modificó este registro"
```

```javascript
// En el service
async function moverActivo(client, activoId, destino, usuarioId) {
    const { rows: [activo] } = await client.query(
        'SELECT * FROM activos WHERE id=$1 AND deleted_at IS NULL', [activoId]
    );
    const result = await client.query(
        `UPDATE activos SET lat=$1, lng=$2, geometry=ST_Point($1,$2),
         version=version+1, updated_at=now(), updated_by=$3
         WHERE id=$4 AND version=$5 AND deleted_at IS NULL`,
        [destino.lat, destino.lng, usuarioId, activoId, activo.version]
    );
    if (result.rowCount === 0) throw new ConflictError('Activo modificado por otro usuario');
}
```

## Audit Trail con usuario @sistema

```sql
-- Crear usuario del sistema
INSERT INTO usuarios (id, email, password_hash, nombre, rol)
VALUES ('00000000-0000-0000-0000-000000000001', 'sistema@geoasset.local',
        'SYSTEM_HASH', '@sistema', 'sistema');

-- Tabla audit particionada por mes
CREATE TABLE audit_log (
    id BIGSERIAL, usuario_id UUID, usuario_email VARCHAR(255),
    accion VARCHAR(50), recurso VARCHAR(100), recurso_id UUID,
    antes JSONB, despues JSONB,
    ip_address INET, user_agent TEXT, timestamp TIMESTAMPTZ DEFAULT now()
) PARTITION BY RANGE (timestamp);
```

## Terrain Snapping (nada flota ni se hunde)

```javascript
// Three.js raycaster contra DEM
function snapToTerrain(mesh, lat, lng, terrainMesh) {
    const pos = geoToThreeJS(lat, lng);
    const raycaster = new THREE.Raycaster();
    raycaster.set(new THREE.Vector3(pos.x, 1000, pos.z), new THREE.Vector3(0, -1, 0));
    const hits = raycaster.intersectObject(terrainMesh);
    if (hits.length > 0) {
        mesh.position.y = hits[0].point.y + 0.1; // +0.1 para evitar z-fighting
    }
}
```

## Plugin Module Registration

```javascript
// modules/<name>/index.js
module.exports = {
    name: 'residuos',
    assetTypes: [{ tipo: 'contenedor', modelo3d: 'contenedor_240l' }],
    profiles: [{ nombre: 'Recolector', departamento: 'residuos' }],
    kpis: [{ id: 'pct_llenos', formula: '...' }],
    hooks: { 'asset:moved': async (activo) => recalcularRutas(activo.org_id) },
    routes: '/api/modules/residuos'
};

// Carga en server.js
async function loadModules(orgConfig) {
    for (const modName of orgConfig.modules) {
        const mod = require(`./modules/${modName}`);
        app.use(mod.routes, mod.routesHandler);
        for (const [event, handler] of Object.entries(mod.hooks)) eventBus.on(event, handler);
    }
}
```

## Materialized Views para KPIs

```sql
CREATE MATERIALIZED VIEW mv_kpi_residuos AS
SELECT org_id,
    COUNT(*) FILTER (WHERE tipo='contenedor' AND estado='lleno') AS llenos,
    COUNT(*) FILTER (WHERE tipo='contenedor') AS total,
    ROUND(COUNT(*) FILTER (WHERE tipo='contenedor' AND estado='lleno')::DECIMAL /
          NULLIF(COUNT(*) FILTER (WHERE tipo='contenedor'),0) * 100, 1) AS pct_llenos
FROM activos WHERE deleted_at IS NULL GROUP BY org_id;

-- Refresh cada 5 min (cron, NO en cada request)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_kpi_residuos;
```

## Partitioning por mes (pg_partman)

```sql
CREATE EXTENSION pg_partman;
SELECT partman.create_parent(
    p_parent_table := 'public.audit_log',
    p_control := 'timestamp',
    p_type := 'native',
    p_interval := 'monthly'
);
-- Crea particiones automáticamente: audit_log_2026_01, audit_log_2026_02, etc.
```
