---
name: postgres-mcp
description: "PostgreSQL MCP Pro — expone PostgreSQL como servidor MCP para que agentes de IA realicen health checks, tuning de índices, exploración de esquema y ejecución segura de SQL."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [postgres, mcp, database, sql, monitoring, performance]
    category: devops
---

# postgres-mcp — PostgreSQL como Servidor MCP

## Cuándo usar

- Un agente IA necesita interactuar con PostgreSQL de forma segura y programática
- Necesitas health checks, index tuning y query analysis sin acceso directo a la BD
- Quieres exponer PostgreSQL como herramientas MCP para agentes LLM
- Necesitas modo restricted (solo lectura) para entornos de producción

## Cuándo NO usar

- No usas PostgreSQL → este skill es específico de PostgreSQL
- El agente ya tiene acceso directo a la BD → MCP añade capa innecesaria
- Necesitas escritura arbitraria sin validación → el modo restricted lo impide

## Instalación

```bash
# Docker (recomendado)
docker pull crystaldba/postgres-mcp

# pipx
pipx install postgres-mcp

# uv
uv pip install postgres-mcp
```

## Configuración

```bash
# Variable obligatoria
DATABASE_URI=postgresql://user:pass@host:5432/dbname

# Opcional (para LLM optimization experimental)
OPENAI_API_KEY=tu_key
```

## Transportes MCP
- **stdio** (default) — clientes locales
- **SSE** — múltiples clientes compartidos
- **Streamable HTTP** — transporte moderno

## 9 Herramientas MCP

| Herramienta | Descripción | Modo |
|-------------|-------------|------|
| `list_schemas` | Lista schemas de la BD | Solo lectura |
| `list_objects` | Lista tablas, vistas, secuencias, extensiones | Solo lectura |
| `get_object_details` | Columnas, constraints, índices de un objeto | Solo lectura |
| `execute_sql` | Ejecuta SQL arbitrario | Depende del modo |
| `explain_query` | EXPLAIN con soporte hypopg y ANALYZE | Solo lectura |
| `get_top_queries` | Queries más lentos desde pg_stat_statements | Solo lectura |
| `analyze_workload_indexes` | Recomienda índices óptimos (DTA o LLM) | Solo lectura |
| `analyze_query_indexes` | Analiza hasta 10 queries y recomienda índices | Solo lectura |
| `analyze_db_health` | Health checks completos | Solo lectura |

## Modos de Acceso

```bash
# Desarrollo — lectura/escritura completa
postgres-mcp --access-mode=unrestricted

# Producción — solo lectura con protecciones
postgres-mcp --access-mode=restricted
```

## Seguridad en modo Restricted
- **SafeSqlDriver** con pglast para validación AST
- Whitelist de ~500+ funciones SQL permitidas
- Whitelist de ~70 extensiones PostgreSQL
- Timeout por defecto 30s
- `force_readonly=True` en conexiones
- Rechaza COMMIT, ROLLBACK, locking clauses

## Extensiones Requeridas (para tuning)
- **pg_stat_statements** — estadísticas de queries
- **hypopg** — simulación de índices hipotéticos

## Algoritmos de Indexación

### 1. DTA (Database Tuning Advisor)
Algoritmo greedy basado en el "Anytime Algorithm" de Microsoft SQL Server:
- Identifica queries candidatos para tuning
- Genera candidatos de índices (combinaciones de columnas)
- Búsqueda greedy con análisis Pareto (costo vs beneficio)
- Usa `hypopg` para simular impacto antes de crear índices
- Parámetros: `max_index_size_mb`, `max_runtime_seconds=30`, `max_index_width=3`, `pareto_alpha=2.0`

### 2. LLM Optimizer (experimental)
- Usa GPT-4o vía `instructor` para generar sugerencias de índices
- Iterativo: LLM sugiere → hypopg evalúa → feedback al LLM
- Requiere `OPENAI_API_KEY`
- Máximo 5 intentos sin progreso antes de parar

## Health Checks (adaptados de PgHero)

| Check | Qué verifica |
|-------|-------------|
| **index** | Índices inválidos, duplicados, bloated, no usados |
| **buffer** | Hit rate del buffer cache (tablas e índices) |
| **connection** | Número y utilización de conexiones |
| **vacuum** | Salud de VACUUM, riesgo de transaction ID wraparound |
| **sequence** | Secuencias cerca de exceder su valor máximo |
| **replication** | Lag entre primary/replicas, status, slots |
| **constraint** | Constraints inválidos |

## Casos de Uso para Mastermind
1. Exploración de esquema por agentes
2. Diagnóstico de rendimiento automático
3. Optimización de índices basada en carga real
4. Debugging de queries con EXPLAIN + índices hipotéticos
5. Monitoreo proactivo con health checks

## Recursos
- GitHub: https://github.com/crystaldba/postgres-mcp
- Licencia: MIT
- Docker: `crystaldba/postgres-mcp`
