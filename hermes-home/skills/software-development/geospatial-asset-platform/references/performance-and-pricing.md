# Performance Architecture — Geospatial Asset Platform

## Data Size Projections (1 tenant grande, 5 años)

| Tipo | Registros/mes | 5 años | Tamaño |
|---|---|---|---|
| Activos (estáticos) | ~50K | 50K | ~50 MB |
| Personal | ~10K | 10K | ~20 MB |
| Audit log | ~200K | ~12M | ~50 GB |
| Movimientos | ~10K | ~600K | ~5 GB |
| Mantenimientos | ~15K | ~900K | ~8 GB |
| **Total** | — | — | **~70 GB** |

Multi-tenant (todos los clientes): ~750 GB a 5 años → un SSD de 1TB.

## Hot / Warm / Cold Strategy

| Tier | Qué contiene | Acceso |
|---|---|---|
| 🔥 Hot (SSD) | Últimos 3 meses + tablas activos/personal (siempre) | < 50ms |
| 🌡️ Warm (estándar) | 3-12 meses (audit, movimientos, órdenes) | < 500ms |
| ❄️ Cold (archivado) | > 12 meses, comprimidos, export S3 | Bajo demanda |

### Archivado automático
```sql
-- Detach partición antigua
ALTER TABLE audit_log DETACH PARTITION audit_log_2025_01;
-- Crear tabla comprimida
CREATE TABLE audit_log_cold (LIKE audit_log INCLUDING ALL);
-- Mover datos
INSERT INTO audit_log_cold SELECT * FROM audit_log_2025_01;
-- Export + delete
COPY (SELECT * FROM audit_log_cold) TO '/archive/audit_2025_01.csv' WITH CSV;
```

## Redis Cache Strategy

| Qué se cachea | TTL | Qué NO se cachea |
|---|---|---|
| Posiciones de activos (tiempo real) | 10s | Mutaciones (writes siempre a BD) |
| KPIs del dashboard | 5 min | Audit log |
| Lista de activos por org | 1 min | Datos de formación/vacaciones |
| Sesiones de usuario | 24h | — |

## Index Strategy

```sql
-- Dashboard: "activos de mi org por tipo/estado"
CREATE INDEX idx_activos_org_tipo ON activos (org_id, tipo, estado) WHERE deleted_at IS NULL;

-- Mapa: bounding box query
CREATE INDEX idx_activos_bbox ON activos USING GIST (geometry) WHERE deleted_at IS NULL;

-- Próximos mantenimientos
CREATE INDEX idx_mant_proxima ON mantenimientos (proxima_revision) WHERE estado IN ('pendiente','completado');

-- Stock bajo mínimo
CREATE INDEX idx_stock_alertas ON stock (org_id) WHERE cantidad_actual <= cantidad_minima;
```

## Retention Policies por tenant

```javascript
const RETENTION = {
    ayuntamiento: { audit_log: '3 years', movimientos: '5 years', inspecciones: '10 years' },
    hospital:     { audit_log: '5 years', inspecciones: 'indefinido', formaciones: 'indefinido' },
    empresa:      { audit_log: '2 years', movimientos: '3 years' }
};
```

## SaaS Pricing Tiers

| Tier | Activos | Módulos | Usuarios | Historial | Precio |
|---|---|---|---|---|---|
| 🌱 Starter | 500 | 2 | 3 | 6 meses | 199€/mes |
| 🏢 Professional | 5.000 | Todos | 15 | 2 años | 799€/mes |
| 🏛️ Enterprise | 25.000 | Todos + APIs | 50 | 5 años | 2.499€/mes |
| 👑 Municipio Grande | 100.000 | Todo + Cámaras | ∞ | 10 años | 5.999€/mes |

Add-ons: Cámaras 99€/cámara, Renfe 199€, AEMET 149€, App móvil 499€, Backup 99€, Data warehouse 799€

Overage: activos extra a 2 céntimos/unidad, storage extra a 10€/GB

## ROI para cliente

| Coste actual | GeoAsset | Ahorro |
|---|---|---|
| 2 personas admin inventarios: 60K€/año | Automatizado | 60K€ |
| ArcGIS: 50K€/año | GeoAsset 30K€/año | 20K€ |
| Pérdidas activos: 10K€/año | Tracking GPS | 10K€ |
| Multas normativas: 5K€/año | Alertas automáticas | 5K€ |
| **Total ahorro: 95K€/año vs coste 30K€/año → ROI 3.2x** |
