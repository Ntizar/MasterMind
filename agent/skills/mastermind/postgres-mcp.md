# Postgres MCP Pro

**URL:** https://github.com/crystaldba/postgres-mcp
**Categoría:** DevOps/Infra
**Estrellas:** 2,802
**Lenguaje:** Python

## ¿Qué hace?
Postgres MCP Pro es un servidor **Model Context Protocol (MCP)** de código abierto creado por [Crystal DBA](https://www.crystaldba.ai) que conecta bases de datos PostgreSQL con agentes de IA (Claude, Cursor, Windsurf, etc.) para **administración, análisis y optimización del ciclo completo de vida de la BD**: desde codificación y testing hasta deployment, tuning y mantenimiento en producción.

A diferencia de otros servidores MCP de Postgres que solo permiten ejecutar queries, Postgres MCP Pro añade herramientas deterministas de optimización basadas en algoritmos clásicos probados:

- **Database Health** — Checks deterministas de salud: buffer cache hit rate, conexiones, vacuum health (prevención de transaction ID wraparound), sequence limits, replication lag, constraint validation, index health (duplicados, no usados, bloated).
- **Index Tuning** — Implementa una versión del **Anytime Algorithm** (inspirado en Microsoft SQL Server Database Tuning Advisor). Explora miles de índices candidatos usando un enfoque greedy con análisis Pareto para encontrar la mejor combinación de índices que balancee rendimiento vs. costo de almacenamiento.
- **Query Plans** — EXPLAIN plans con soporte para **índices hipotéticos** (vía `hypopg`) que simulan el impacto de índices sin crearlos realmente.
- **Schema Intelligence** — Herramientas para explorar schemas, objetos y detalles de tablas (columnas, constraints, índices) para que el agente IA genere SQL correcto.
- **Safe SQL Execution** — Dos modos de acceso:
  - **Unrestricted** (dev): acceso total read/write
  - **Restricted** (prod): solo lectura con parseo SQL profundo vía `pglast` que rechaza COMMIT, ROLLBACK, DDL, DML y funciones no permitidas. Timeout configurable por query.
- **Index Tuning by LLM** (experimental) — Optimización iterativa de índices usando un LLM externo (OpenAI) que propone índices, se valida con `hypopg`, y se retroalimenta hasta converger.

Soporta tres transportes MCP: **stdio**, **SSE** y **streamable-http**. Usa `psycopg3` + `libpq` para conexiones async.

## Casos de uso
1. **Optimización de rendimiento con IA**: Un equipo genera una app con un asistente IA, pero las queries ORM son lentas. Con Postgres MCP Pro + Cursor, el agente puede analizar queries lentas, obtener recomendaciones de índices y aplicar optimizaciones en minutos.
2. **Health checks automatizados**: Ejecutar `analyze_db_health` periódicamente para detectar índices duplicados, tablas que necesitan VACUUM, secuencias al borde de su límite, lag de replicación, etc.
3. **Tuning de índices sin riesgo**: Usar `explain_query` con `hypothetical_indexes` para simular el impacto de nuevos índices sin modificar la base de datos real.
4. **Análisis de workload**: `analyze_workload_indexes` identifica las queries más costosas del workload y recomienda índices óptimos automáticamente.
5. **Integración segura en producción**: Usar modo `--access-mode=restricted` para permitir que agentes IA ejecuten queries de lectura segura sin riesgo de modificar datos.
6. **Diagnóstico de queries lentas**: `get_top_queries` con `sort_by=total_time` o `sort_by=resources` para identificar las queries que más consumen.

## Snippets útiles

### Instalar con pipx
```bash
pipx install postgres-mcp
```

### Instalar con Docker
```bash
docker pull crystaldba/postgres-mcp
```

### Ejecutar con Docker
```bash
docker run -i --rm \
  -e DATABASE_URI="postgresql://user:pass@localhost:5432/mydb" \
  crystaldba/postgres-mcp --access-mode=unrestricted
```

### Ejecutar con SSE transport (para múltiples clientes)
```bash
docker run -p 8000:8000 \
  -e DATABASE_URI="postgresql://user:pass@localhost:5432/mydb" \
  crystaldba/postgres-mcp --access-mode=unrestricted --transport=sse
```

### Configurar Claude Desktop (Docker)
```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "DATABASE_URI", "crystaldba/postgres-mcp", "--access-mode=unrestricted"],
      "env": {
        "DATABASE_URI": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

### Configurar Claude Desktop (pipx)
```json
{
  "mcpServers": {
    "postgres": {
      "command": "postgres-mcp",
      "args": ["--access-mode=unrestricted"],
      "env": {
        "DATABASE_URI": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

### Configurar SSE en cliente MCP (Cursor/Cline)
```json
{
  "mcpServers": {
    "postgres": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Instalar extensiones requeridas
```sql
-- Para index tuning y análisis completo de queries
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS hypopg;
```

### Instalar desde fuente (desarrollo)
```bash
git clone https://github.com/crystaldba/postgres-mcp.git
cd postgres-mcp
uv pip install -e .
uv sync
uv run postgres-mcp "postgres://user:pass@localhost:5432/mydb"
```

## Cómo integrarlo en proyectos

### 1. Instalación mínima (5 minutos)
```bash
# Instalar el paquete
pipx install postgres-mcp

# Configurar en tu IDE (Cursor, Claude Desktop, etc.)
# Usar la configuración JSON de arriba con tu DATABASE_URI
```

### 2. Integración en producción (modo seguro)
```bash
# Ejecutar en modo restricted (solo lectura) con timeout de 30s por query
docker run -d --name postgres-mcp-pro \
  -e DATABASE_URI="postgresql://readonly_user:pass@prod-db:5432/appdb" \
  crystaldba/postgres-mcp \
  --access-mode=restricted \
  --transport=sse \
  --sse-port=8000
```

### 3. Integración con LLM Index Tuning (experimental)
```bash
# Requiere OPENAI_API_KEY para el modo LLM de tuning
docker run -d \
  -e DATABASE_URI="postgresql://user:pass@localhost:5432/mydb" \
  -e OPENAI_API_KEY="sk-..." \
  crystaldba/postgres-mcp \
  --access-mode=restricted \
  --transport=sse
```

Luego usar la herramienta `analyze_workload_indexes` con `method="llm"` o `analyze_query_indexes` con `method="llm"`.

### 4. Arquitectura recomendada para múltiples clientes

```
+---------------------------------------------+
|           MCP Clientes (Cursor, Claude,      |
|         Windsurf, Cline, etc.)               |
|         +----------+ +----------+           |
|         | Cursor   | | Claude   |           |
|         +----+-----+ +----+-----+           |
|              |            |                  |
|         +----v------------v-----+           |
|         |    SSE Server         |           |
|         |  localhost:8000/sse   |           |
|         +---------+-------------+           |
|                   |                         |
|         +---------v-------------+           |
|         |  Postgres MCP Pro     |           |
|         |  (restricted mode)    |           |
|         +---------+-------------+           |
|                   |                         |
|         +---------v-------------+           |
|         |   PostgreSQL DB       |           |
|         |  + pg_stat_statements |           |
|         |  + hypopg             |           |
|         +-----------------------+           |
+---------------------------------------------+
```

### 5. Flujo de trabajo típico con un agente IA
1. **Explorar schema**: `list_schemas` -> `list_objects(schema)` -> `get_object_details(schema, table)`
2. **Identificar problemas**: `analyze_db_health(health_type="all")`
3. **Encontrar queries lentas**: `get_top_queries(sort_by="resources", limit=10)`
4. **Optimizar queries**: `explain_query(sql="...", hypothetical_indexes=[...])`
5. **Tuning automático**: `analyze_workload_indexes()` o `analyze_query_indexes(queries=[...])`
6. **Ejecutar queries seguras**: `execute_sql("SELECT ...")`

### Dependencias clave
- `mcp>=1.25.0` — Framework MCP (FastMCP)
- `psycopg[binary]>=3.3.2` — Driver PostgreSQL async
- `pglast==7.11` — Parser SQL para validación de queries seguras
- `humanize>=4.15.0` — Formateo de números legibles
- `instructor>=1.14.4` — Para integración con LLM (tuning experimental)
- `psycopg-pool>=3.3.0` — Pool de conexiones

### Requisitos de la base de datos
- PostgreSQL 13-17 (testing enfocado en 15, 16, 17)
- Python 3.12+
- Extensiones opcionales pero recomendadas: `pg_stat_statements`, `hypopg`
- En cloud providers (AWS RDS, Azure, GCP) las extensiones ya están disponibles

## Fecha de aprendizaje: 2026-05-27
