# Patrones de Diseño ERP para TerrAn

## Patrón 1: Optimistic Locking

Problema: Dos usuarios editan el mismo activo simultáneamente.

```sql
-- Cada activo tiene campo version
ALTER TABLE activos ADD COLUMN version INTEGER DEFAULT 1;

-- UPDATE solo si la versión no ha cambiado
UPDATE activos 
SET lat = $1, lng = $2, version = version + 1, updated_by = $3
WHERE id = $4 AND version = $5 AND deleted_at IS NULL;

-- Si rowCount = 0 → conflicto, otro usuario lo modificó
```

```javascript
// Backend Node.js
async function moverActivo(id, destino, usuarioId, versionActual) {
    const result = await db.query(
        `UPDATE activos SET lat=$1, lng=$2, version=version+1, updated_by=$3
         WHERE id=$4 AND version=$5 AND deleted_at IS NULL`,
        [destino.lat, destino.lng, usuarioId, id, versionActual]
    );
    if (result.rowCount === 0) {
        throw new ConflictError('Este activo está siendo editado por otro usuario. Recarga la página.');
    }
}
```

## Patrón 2: Audit Trail con Usuario del Sistema

```sql
-- Tabla particionada por mes
CREATE TABLE audit_log (
    id BIGSERIAL,
    usuario_id UUID,
    usuario_email VARCHAR(255),  -- Snapshot (el usuario puede ser borrado)
    accion VARCHAR(50),          -- crear, mover, editar, eliminar
    recurso VARCHAR(100),
    recurso_id UUID,
    antes JSONB,                 -- Estado anterior (NULL en INSERT)
    despues JSONB,               -- Estado nuevo (NULL en DELETE)
    ip_address INET,
    timestamp TIMESTAMPTZ DEFAULT now()
) PARTITION BY RANGE (timestamp);

-- Usuario del sistema para acciones automáticas
INSERT INTO usuarios (id, email, nombre, rol) 
VALUES ('00000000-0000-0000-0000-000000000001', 'sistema@terran.local', '@sistema', 'sistema');
```

## Patrón 3: Multi-Tenant con RLS

```sql
-- Row Level Security en PostgreSQL
ALTER TABLE activos ENABLE ROW LEVEL SECURITY;

CREATE POLICY org_isolation ON activos
    USING (org_id = current_setting('app.current_org_id')::uuid);

-- En cada request, establecer el contexto
SET app.current_org_id = 'uuid-del-ayuntamiento';
-- Ahora TODAS las queries filtran automáticamente por org_id
```

## Patrón 4: Plugin Architecture

```javascript
// Cada módulo se registra dinámicamente
const modules = new Map();

function registerModule(config) {
    modules.set(config.name, {
        ...config,
        routes: config.routes || [],
        hooks: config.hooks || {},
        kpis: config.kpis || []
    });
}

// Módulo de residuos
registerModule({
    name: 'residuos',
    assetTypes: ['contenedor', 'camion_recolector'],
    profiles: ['Recolector', 'Supervisor'],
    kpis: [
        { id: 'pct_llenos', formula: 'count_llenos / count_total * 100' }
    ],
    hooks: {
        'asset:moved': async (activo) => {
            if (activo.tipo === 'contenedor') await recalcularRutas(activo.org_id);
        }
    },
    routes: '/api/modules/residuos'
});

// Carga dinámica según config del tenant
for (const modName of tenantConfig.modules) {
    const mod = modules.get(modName);
    if (mod) {
        app.use(mod.routes, mod.handler);
        for (const [event, handler] of Object.entries(mod.hooks)) {
            eventBus.on(event, handler);
        }
    }
}
```

## Patrón 5: Búsqueda Híbrida (FTS + Semántica)

```javascript
async function buscarHibrida(query, orgId) {
    // 1. PostgreSQL full-text search (exacto + stemming)
    const fts = await db.query(
        `SELECT id, titulo, ts_rank(search_vector, plainto_tsquery('spanish', $1)) as rank
         FROM documentos WHERE org_id = $2 AND search_vector @@ plainto_tsquery('spanish', $1)
         ORDER BY rank DESC LIMIT 10`,
        [query, orgId]
    );
    
    // 2. ChromaDB semantic search (significado)
    const sem = await chroma.query({
        queryTexts: [query],
        nResults: 10,
        where: { org_id: orgId }
    });
    
    // 3. Fusionar con RRF (Reciprocal Rank Fusion)
    const K = 60;
    const scores = new Map();
    
    fts.rows.forEach((r, i) => {
        const s = scores.get(r.id) || { id: r.id, score: 0 };
        s.score += 1 / (K + i + 1);
        scores.set(r.id, s);
    });
    
    sem.documents[0].forEach((doc, i) => {
        const docId = sem.metadatas[0][i].doc_id;
        const s = scores.get(docId) || { id: docId, score: 0 };
        s.score += 1 / (K + i + 1);
        scores.set(docId, s);
    });
    
    return [...scores.values()].sort((a, b) => b.score - a.score).slice(0, 10);
}
```

## Patrón 6: Document Management

```javascript
// Upload → MinIO + extracción de texto + indexación
async function subirDocumento(file, metadata, orgId) {
    // 1. Subir a MinIO
    const key = `${orgId}/${Date.now()}_${file.originalname}`;
    await minio.putObject('documentos', key, file.buffer);
    
    // 2. Extraer texto si es PDF
    let textoExtraido = null;
    if (file.mimetype === 'application/pdf') {
        const pdfData = await pdfParse(file.buffer);
        textoExtraido = pdfData.text;
    }
    
    // 3. Guardar metadata en PostgreSQL
    const doc = await db.query(
        `INSERT INTO documentos (org_id, titulo, tipo, archivo_url, texto_extraido, ...)
         VALUES ($1, $2, $3, $4, $5, ...) RETURNING *`,
        [orgId, metadata.titulo, metadata.tipo, `s3://documentos/${key}`, textoExtraido]
    );
    
    // 4. Indexar en ChromaDB para búsqueda semántica
    if (textoExtraido && textoExtraido.length > 100) {
        await indexarEnChromaDB(doc.rows[0], textoExtraido);
    }
    
    return doc.rows[0];
}
```

## Patrón 7: Terrain Snapping

```javascript
// Posicionar activos justo sobre el terreno
function snapToTerrain(assetMesh, lat, lng, terrainMesh) {
    const raycaster = new THREE.Raycaster();
    const pos = geoToThreeJS(lat, lng);
    
    raycaster.set(
        new THREE.Vector3(pos.x, 1000, pos.z),  // Rayo desde arriba
        new THREE.Vector3(0, -1, 0)               // Hacia abajo
    );
    
    const hits = raycaster.intersectObject(terrainMesh);
    if (hits.length > 0) {
        assetMesh.position.y = hits[0].point.y + 0.1; // +0.1 para evitar z-fighting
    }
}
```

## Patrón 8: WebSocket para Real-Time

```javascript
// Server: publicar cambios a todos los clientes
eventBus.on('asset:moved', (data) => {
    wsServer.broadcast('asset:moved', {
        id: data.activoId,
        lat: data.destino.lat,
        lng: data.destino.lng,
        estado: data.estado
    });
});

// Client: suscribirse a actualizaciones
const ws = new WebSocket('wss://terran.app/ws');
ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'asset:moved') {
        actualizarPosicionEnMapa(msg.id, msg.lat, msg.lng);
    }
};
```

## Patrón 9: Soft Delete

```sql
-- NUNCA borrar registros, solo marcar
ALTER TABLE activos ADD COLUMN deleted_at TIMESTAMPTZ;

-- Crear vista que excluye borrados
CREATE VIEW activos_vivos AS
SELECT * FROM activos WHERE deleted_at IS NULL;

-- Restricción unique que respeta soft delete
ALTER TABLE activos ADD CONSTRAINT uq_org_codigo 
    UNIQUE (org_id, codigo, deleted_at) WHERE deleted_at IS NULL;
```

## Patrón 10: Materialized Views para KPIs

```sql
-- KPIs pre-computados (refresh cada 5 min, no en cada request)
CREATE MATERIALIZED VIEW mv_kpi_residuos AS
SELECT 
    org_id,
    COUNT(*) FILTER (WHERE tipo = 'contenedor' AND estado = 'lleno') AS llenos,
    COUNT(*) FILTER (WHERE tipo = 'contenedor') AS total,
    ROUND(COUNT(*) FILTER (WHERE tipo = 'contenedor' AND estado = 'lleno')::DECIMAL / 
          NULLIF(COUNT(*) FILTER (WHERE tipo = 'contenedor'), 0) * 100, 1) AS pct_llenos
FROM activos WHERE deleted_at IS NULL
GROUP BY org_id;

-- Refresh periódico
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_kpi_residuos;
```
