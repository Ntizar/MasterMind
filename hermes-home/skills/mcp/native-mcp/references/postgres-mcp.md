# Postgres MCP Pro — MCP Server Pattern

**Repo:** [crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp) (~2.8k ⭐)  
**Version:** 0.3.0  
**License:** MIT

## Qué es

Postgres MCP Pro es un servidor MCP que expone 9 herramientas deterministas para que agentes IA interactúen con PostgreSQL de forma inteligente y segura. Va más allá de un simple wrapper de conexión: proporciona análisis de salud, optimización de índices, y ejecución segura de SQL.

## Arquitectura

- **Backend:** psycopg3 (async), pglast (SQL parsing/AST validation), hypopg (hypothetical indexes)
- **Transportes:** stdio, SSE, streamable-http
- **Modos de acceso:**
  - `unrestricted` (dev): lectura y escritura completa
  - `restricted` (producción): solo lectura, validación AST con pglast
- **Index tuning:** Anytime Algorithm de Microsoft SQL Server + hypopg
- **LLM optimizer:** Experimental, usa instructor + OpenAI para sugerencias de índices

## Las 9 Herramientas

| Herramienta | Descripción |
|---|---|
| `health_check` | Análisis de salud en 7 categorías (índices, conexiones, vacuum, secuencias, replicación, buffer, constraints) |
| `query_analysis` | Análisis de queries individuales con EXPLAIN + índices hipotéticos |
| `index_recommendation` | Recomendación de índices basada en carga de trabajo |
| `slow_query_analysis` | Identificación de queries lentas via pg_stat_statements |
| `table_stats` | Estadísticas de tablas (tamaño, filas, tuplas muertas) |
| `schema_analysis` | Análisis del esquema de la BD |
| `generate_sql` | Generación de SQL contextual basado en el esquema |
| `execute_sql` | Ejecución segura de SQL (con validación en modo restricted) |
| `index_optimizer` | Optimización de índices con LLM (experimental) |

## Configuración Claude Desktop (Docker)

```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "DATABASE_URI", "crystaldba/postgres-mcp", "--access-mode=unrestricted"],
      "env": {
        "DATABASE_URI": "postgresql://user:pass@localhost:5432/dbname"
      }
    }
  }
}
```

## Configuración Hermes Agent (config.yaml)

```yaml
mcp_servers:
  postgres:
    command: "docker"
    args: ["run", "-i", "--rm", "-e", "DATABASE_URI", "crystaldba/postgres-mcp"]
    env:
      DATABASE_URI: "postgresql://user:pass@localhost:5432/dbname"
    # O usar access-mode=restricted para producción
```

## Patrones de Uso

1. **Diagnóstico rápido:** `health_check` → identifica problemas antes de optimizar
2. **Tuning de índices:** `index_recommendation` → sugiere índices basados en queries reales
3. **Análisis de query lenta:** `slow_query_analysis` + `query_analysis` → plan EXPLAIN con hipótesis
4. **Generación de SQL segura:** `generate_sql` → SQL correcto basado en esquema real
5. **Producción:** Siempre usar `--access-mode=restricted` con validación AST

## Pitfalls

- **hypopg requerido:** La extensión `hypopg` debe estar instalada en PostgreSQL para índices hipotéticos
- **pg_stat_statements:** Necesaria para `slow_query_analysis` — activar en `postgresql.conf`
- **pglast:** Requiere compilación C — en Docker ya está incluida
- **Modo restricted:** No permite INSERT/UPDATE/DELETE — solo SELECT y DDL
- **Conexión:** El URI debe ser válido para psycopg3 (postgresql://user:pass@host:port/db)
