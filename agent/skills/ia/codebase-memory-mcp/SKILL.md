---
name: codebase-memory-mcp
description: "Usa al indexar código en un grafo MCP para agentes IA."
version: "1.0.0"
author: Mastermind (stars-explorer)
license: MIT
metadata:
  hermes:
    tags: [mcp, knowledge-graph, tree-sitter, code-analysis, sqlite, cypher, code-intelligence, agent-tools]
    related_skills: [graphify-codebase-graph, native-mcp, mcp-servers-modelcontextprotocol, codebase-inspection]
---

# codebase-memory-mcp (CBM) — Servidor MCP de Inteligencia de Código

**Cuándo usarlo:** cuando un agente de código (Hermes, Claude Code, Codex, opencode…) necesite explorar o auditar un repositorio grande por estructura (quién llama a qué, impacto de un diff, código muerto, routes cross-service) en vez de leer ficheros uno a uno con grep.

**Repo:** https://github.com/DeusData/codebase-memory-mcp (43.406⭐, C puro, MIT, activo — verificado 2026-09-16 contra README real; arXiv:2603.27277)

Motor de inteligencia de código en un único binario nativo: indexa repositorios a un **grafo de conocimiento persistente en SQLite** (tree-sitter, 162 lenguajes + resolución de tipos **Hybrid LSP** en 12) y lo expone por MCP con 15 herramientas. Sin LLM embebido, sin API key, sin runtime de lenguaje: el agente que ya habla con el servidor ES la capa de inteligencia (NL→consulta lo traduce el cliente MCP).

Cifras del README (M3 Pro): kernel Linux (28M LOC, 75K ficheros) indexado en 3 min; consultas estructurales <1 ms; 5 consultas estructurales ~3.400 tokens vs ~412.000 vía grep fichero a fichero (−99% tokens).

## Instalación (verificada del README)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

```powershell
# Windows: descargar install.ps1, revisarlo, quitar Mark-of-the-Web y ejecutar
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1 -OutFile install.ps1
Unblock-File .\install.ps1
.\install.ps1   # si hay error de política: powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Opciones: `--skip-config` (solo binario), `--dir=<ruta>`. También disponible en npm, PyPI, Homebrew, Scoop, Winget, Chocolatey, AUR y `go install`. El comando `install` autodetecta agentes (45 superficies) y configura sus entradas MCP; **nunca toca flags experimentales ni permisos**. Actualizar: `codebase-memory-mcp update` imprime el comando del script de instalación a ejecutar (no se auto-actualiza desde el binario).

### Registro en Hermes (patrón propio)

Añadir al `config.yaml` de Hermes (stdio):

```yaml
mcp_servers:
  cbm:
    command: "C:/Users/d_ant/.local/bin/codebase-memory-mcp.exe"   # ruta absoluta del binario
    args: []
```

Hermes registra las herramientas como `mcp_cbm_*` (guiones → guiones bajos). Verificar reiniciando el agente y comprobando que aparecen las ~15 herramientas.

## Modelo de uso: 15 herramientas MCP

| Grupo | Herramientas |
|-------|-------------|
| Indexado | `index_repository` (ruta ABSOLUTA), `list_projects`, `delete_project`, `index_status` |
| Consulta | `get_graph_schema` (**ejecutarla primero**), `search_graph` (estructural/BM25/semántica con paginación `offset`/`limit` + `semantic_offset`), `trace_path` (BFS profundidad 1-5, inbound/outbound), `query_graph` (Cypher), `get_code_snippet` (por nombre cualificado), `search_code` (grep sobre indexado), `get_architecture` (idiomas, paquetes, routes, hotspots, clusters, ADR), `detect_changes` (git diff → símbolos afectados + blast radius con riesgo), `manage_adr` (CRUD ADR), `ingest_traces` (valida aristas HTTP_CALLS con trazas reales) |

**Datos del grafo:** nodos `Project, Package, Folder, File, Module, Class, Function, Method, Interface, Enum, Type, Route, Resource`; aristas `CONTAINS_*, DEFINES(_METHOD), IMPORTS, CALLS, CALL_REFERENCE, USAGE, IMPLEMENTS, HANDLES, HTTP_CALLS, ASYNC_CALLS, EMITS/LISTENS_ON, DATA_FLOWS, SIMILAR_TO, SEMANTICALLY_RELATED, TESTS, FILE_CHANGES_WITH`. Nombres cualificados: `<project>.<path_parts>.<name>` — descubrirlos con `search_graph` antes de `get_code_snippet`.

**Cypher:** subset openCypher SOLO lectura (`MATCH/OPTIONAL MATCH/WHERE/WITH/RETURN/ORDER BY/SKIP/LIMIT/DISTINCT/UNWIND/UNION/CASE`, `[*1..3]`, `EXISTS { (f)<-[:CALLS]-() }` para código muerto, agregados `count/sum/avg/min/max/collect`). Todo lo demás (MERGE, CALL, parameters, comprehensions) falla con error explícito — nunca devuelve vacío silencioso. Ejemplo: `MATCH (f:Function)-[:CALLS]->(g) WHERE f.name = 'main' RETURN g.name`.

## Modos de operación

```bash
# CLI one-shot (sin daemon, ideal para scripts/crons):
codebase-memory-mcp cli search_graph '{"project": "my-project", "name_pattern": ".*Handler.*"}'
# --format json para payload machine-readable; stdout = resultado, stderr = progreso/logs

# UI 3D del grafo en http://localhost:9749 (la posee el daemon compartido):
codebase-memory-mcp --ui=true --port=9749

# Configuración:
codebase-memory-mcp config list
codebase-memory-mcp config set auto_index true        # indexar al arrancar sesión MCP
codebase-memory-mcp config set auto_index_limit 50000
codebase-memory-mcp config set auto_watch false       # no registrar watcher por sesión
codebase-memory-mcp config set watcher_enabled false  # apagar hilo watcher (leelo abajo)
```

Persistencia: SQLite WAL en `~/.cache/codebase-memory-mcp/` (override `CBM_CACHE_DIR`); reset = borrar el directorio. Env vars útiles: `CBM_ALLOWED_ROOT` (confinar qué rutas se pueden indexar — clave si lo maneja un caller no confiado), `CBM_WORKERS`, `CBM_MEM_BUDGET_MB`, `CBM_LOG_LEVEL`, `CBM_DIAGNOSTICS`.

## Patrones reutilizables (lo que hay que aprender del repo)

1. **Backend estructural sin LLM + MCP como capa de inteligencia**: en vez de embeber un modelo NL→Cypher, el servidor solo ejecuta consultas y el agente cliente traduce → cero API keys, cero coste extra (arXiv: 83% calidad de respuesta, 10× menos tokens, 2.1× menos tool-calls vs exploración fichero a fichero).
2. **Pipeline RAM-first**: LZ4 + SQLite en memoria + volcado único al final, liberando RAM después — patrón para indexadores masivos.
3. **Confianza graduada en aristas**: `CALLS` (resuelto), `CALL_REFERENCE` (referencia a objetivo único), `USAGE` (usado sin objetivo probado) — modelar la incertidumbre en el grafo en vez de binarizar.
4. **Tiering de subagentes** (Scout/Verify/Auditor): descubrimiento rápido provisional → evidencia dirigida con cobertura → auditoría con límites explícitos; y `check_index_coverage` como evidencia negativa honesta ("sin hueco registrado" ≠ "completo").
5. **Exact-build admission barrier**: todos los procesos de la herramienta comparten versión/ABI/cache-root con barrera a prueba de crashes — patrón para CLI con daemon compartido.
6. **IaC como grafo**: Dockerfiles/K8s/Kustomize indexados como nodos `Resource`/`Module` con aristas `IMPORTS` — el grafo cruza código e infraestructura; y **cross-repo**: aristas `CROSS_*` entre repos bajo el mismo store.

## Pitfalls

- **Defender marca el binario** como `Trojan:Script/Wacatac.B!ml` — falso positivo conocido (misma familia que `gh`, llama.cpp, Godot); los releases se escanean en VirusTotal con SHA-256 publicado.
- **`watcher_enabled` se lee UNA vez al arrancar el daemon**: tras cambiarlo hay que `codebase-memory-mcp daemon stop`; reconectar el cliente MCP no reinicia el daemon (a diferencia de `auto_watch`, que se consulta por sesión).
- `trace_path` devuelve 0 si el nombre no es exacto → `search_graph(name_pattern=".*Parcial.*")` primero.
- Consultas sin `project="..."` pueden mezclar proyectos → `list_projects` para ver nombres.
- `index_repository` exige **ruta absoluta**.
- Un solo cache-root canónico por cuenta: cerrar sesiones CBM activas antes de cambiar `CBM_CACHE_DIR`.
- `manage_adr(mode='set_sections')` reescribe solo las secciones nombradas (matching exacto, case-sensitive); `update` reemplaza el documento ENTERO.
- `uninstall` NO borra el install.sh/ps1 lateral (no puede probar que es suyo) — solo imprime la ruta y el `rm`.
- El `skill_angles` del scout lo marcaba como "ai-cv-pipeline/ci-cd" — FALSO: no tiene nada que ver con CV; es inteligencia de código (pitfall conocido del heurístico por topics).

## Comparativa con graphify (ia/graphify-codebase-graph)

| | CBM | graphify |
|---|---|---|
| Forma | binario nativo C, MCP-first, SQLite + UI 3D + daemon | paquete Python CLI, salida graph.json/HTML/wiki |
| Alcance grafo | 162 lenguajes código + IaC + cross-repo | código (~40 lenguajes) + docs/PDF/media al mismo grafo |
| Consultas | Cypher subset + trace/BM25/semántica | `query`/`path`/`explain` sobre graph.json + MCP serve |
| Cuándo usar | en el bucle del agente de código (Claude Code/Codex/opencode/Hermes vía MCP), impacto de diffs, cross-service | investigación offline, compartir wiki/markdown, mezclar docs y media con código |

## Verificación

1. `echo '{}' | <ruta-binario>` imprime JSON → el binario responde.
2. `codebase-memory-mcp cli list_projects '{}'` tras indexar → el proyecto con conteo de nodos/aristas.
3. `get_graph_schema` → etiquetas y patrones de relación del indexado; `query_graph` con un `MATCH` simple devuelve filas <1 ms.
4. En Claude Code, `/mcp` muestra el servidor con 15 herramientas.
