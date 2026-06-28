---
name: terral-hardware-sizing
description: "Dimensionado de hardware para Terral — cómo calcular RAM, CPU, disco y ancho de banda según volumen de datos, usuarios concurrentes yfeatures activas."
version: 1.0.0
author: David Antizar
tags: [hardware, sizing, postgresql, performance, scaling, saas]
---

# Dimensionado de Hardware para Terral

## Fórmulas de cálculo

### RAM necesaria por componente

```
PostgreSQL = (active_data_gb × 0.25) + (max_connections × 10MB) + shared_buffers
Redis = num_sessions × 0.01GB + (num_cached_keys × 0.001GB)
Node.js = num_instances × 512MB
MinIO = num_files × 0.001GB (solo metadatos)
ChromaDB = num_embeddings × 0.002GB
```

### Disco necesario

```
PostgreSQL_base = (num_rows × avg_row_size) × 1.5  (con índices)
PostgreSQL_audit = num_mutations_per_month × 0.0005GB × 12
Documentos = num_docs × avg_doc_size × retention_years
Total = PostgreSQL + Documentos + OS_overhead(20GB) + logs(10GB)
```

### CPU necesaria

```
Para 100 queries/segundo = 2 cores mínimo
Para 1000 queries/segundo = 4 cores
Para 10000 queries/segundo = 8 cores + read replicas
```

## Tablas de referencia por volumen

### Tier 1: Pueblo pequeño (5K habitantes)

| Métrica | Valor |
|---|---|
| Activos | 500 |
| Personal | 50 |
| Usuarios concurrentes | 3-5 |
| Audit entries/mes | 10.000 |
| Documentos/año | 500 PDFs |
| **RAM total** | **4GB** |
| **CPU** | **2 cores** |
| **Disco** | **40GB SSD** |
| **Coste estimado** | **20-40€/mes** (VPS) |

**Componentes:**
- PostgreSQL: 1GB RAM, 20GB SSD
- Redis: 256MB RAM
- Node.js: 512MB RAM (1 instancia)
- MinIO: 10GB
- ChromaDB: 1GB RAM

### Tier 2: Ciudad mediana (50K habitantes)

| Métrica | Valor |
|---|---|
| Activos | 5.000 |
| Personal | 500 |
| Usuarios concurrentes | 20-30 |
| Audit entries/mes | 100.000 |
| Documentos/año | 5.000 PDFs |
| **RAM total** | **8GB** |
| **CPU** | **4 cores** |
| **Disco** | **200GB SSD** |
| **Coste estimado** | **80-150€/mes** (VPS) |

**Componentes:**
- PostgreSQL: 4GB RAM, 100GB SSD
- Redis: 1GB RAM
- Node.js: 1GB RAM (2 instancias)
- MinIO: 50GB
- ChromaDB: 2GB RAM

### Tier 3: Ciudad grande (300K habitantes)

| Métrica | Valor |
|---|---|
| Activos | 20.000 |
| Personal | 3.000 |
| Usuarios concurrentes | 100-200 |
| Audit entries/mes | 500.000 |
| Documentos/año | 25.000 PDFs |
| **RAM total** | **32GB** |
| **CPU** | **8 cores** |
| **Disco** | **1TB SSD** |
| **Coste estimado** | **300-600€/mes** (cloud) |

**Componentes:**
- PostgreSQL: 16GB RAM, 500GB SSD (read replica: 8GB)
- Redis: 4GB RAM (cluster)
- Node.js: 4GB RAM (4 instancias, load balancer)
- MinIO: 200GB
- ChromaDB: 4GB RAM

### Tier 4: Multi-tenant (10+ ayuntamientos)

| Métrica | Valor |
|---|---|
| Activos totales | 100.000+ |
| Personal total | 20.000+ |
| Usuarios concurrentes | 500+ |
| Audit entries/mes | 2.000.000+ |
| Documentos total | 500.000+ PDFs |
| **RAM total** | **64-128GB** |
| **CPU** | **16-32 cores** |
| **Disco** | **2-5TB SSD** |
| **Coste estimado** | **1.000-3.000€/mes** (cloud) |

**Componentes:**
- PostgreSQL: 32GB RAM, 1TB SSD (2 read replicas)
- Redis: 8GB RAM (cluster 3 nodos)
- Node.js: 8GB RAM (6-8 instancias)
- MinIO: 500GB (cluster)
- ChromaDB: 8GB RAM (cluster)
- Load balancer: Nginx/HAProxy

## Proyecciones de crecimiento

### Crecimiento de audit_log

```
Pueblo pequeño:  10K entries/mes × 12 = 120K/año × 5 años = 600K entries ≈ 3GB
Ciudad mediana:  100K entries/mes × 12 = 1.2M/año × 5 años = 6M entries ≈ 30GB
Ciudad grande:   500K entries/mes × 12 = 6M/año × 5 años = 30M entries ≈ 150GB
```

### Crecimiento de documentos

```
Pueblo pequeño:  500 PDFs/año × 2MB avg × 5 años = 5GB
Ciudad mediana:  5.000 PDFs/año × 3MB avg × 5 años = 75GB
Ciudad grande:   25.000 PDFs/año × 5MB avg × 5 años = 625GB
```

### Cuándo escalar

| Señal | Acción |
|---|---|
| CPU > 80% sostenido 15 min | Añadir cores o read replica |
| RAM > 85% | Añadir RAM o optimizar queries |
| Disco > 80% | Añadir disco o archivar datos cold |
| Queries > 500ms p95 | Optimizar índices o añadir cache |
| Conexiones > 80% max | Añadir PgBouncer o read replica |
| WebSocket > 1000 concurrentes | Redis pub/sub + cluster Node.js |

## Proveedores recomendados (España/Europa)

### Para desarrollo
- **Local:** Docker en la microVM actual (1vCPU, 2GB)
- **Limitación:** Solo para pruebas, no para producción real

### Para producción (Tier 1-2)
- **OVH VPS:** 8GB/4cores/200GB = ~35€/mes
- **Hetzner Cloud:** 8GB/4cores/160GB = ~30€/mes
- **DigitalOcean:** 8GB/4cores/160GB = ~48€/mes

### Para producción (Tier 3-4)
- **AWS RDS PostgreSQL:** db.r6g.large (16GB) = ~200€/mes
- **Google Cloud SQL:** db-custom-8-32768 = ~250€/mes
- **Self-hosted en Hetzner Dedicated:** AX102 (128GB, 16cores) = ~80€/mes

### Para documentos
- **MinIO self-hosted:** Gratis (en el mismo servidor)
- **AWS S3:** 0.023€/GB/mes (1TB = 23€/mes)
- **Backblaze B2:** 0.005€/GB/mes (1TB = 5€/mes)

## Optimizaciones de rendimiento

### PostgreSQL
```sql
-- shared_buffers = 25% de RAM total
shared_buffers = '4GB'          -- Para servidor 16GB

-- work_mem para queries complejas
work_mem = '64MB'               -- Para ORDER BY, GROUP BY, JOINs

-- effective_cache_size = 75% de RAM
effective_cache_size = '12GB'

-- maintenance_work_mem para VACUUM/CREATE INDEX
maintenance_work_mem = '1GB'

-- random_page_cost para SSD
random_page_cost = 1.1          -- SSD es casi secuencial

-- max_connections (considerar PgBouncer)
max_connections = 100
```

### Redis
```
maxmemory: 2GB
maxmemory-policy: allkeys-lru
tcp-keepalive: 300
```

### Node.js
```
--集群模式 (cluster)
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;
if (cluster.isPrimary) {
    for (let i = 0; i < numCPUs; i++) cluster.fork();
}
```
