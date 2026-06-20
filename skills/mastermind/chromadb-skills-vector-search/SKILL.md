---
name: chromadb-skills-vector-search
version: "2.2.0"
description: "Búsqueda semántica de skills usando ChromaDB local + qwen3-embedding (NaN API). Indexa 190+ skills como vectores 4096-dim y consulta por similitud para cargar solo los relevantes."
tags: [chromadb, embeddings, skills, vector-search, mastermind, qwen3, nan]
---

# ChromaDB Skills Vector Search

## Resumen

Sistema de búsqueda semántica de skills usando ChromaDB **local** (puerto 8000 en Hermes VM) y el modelo `qwen3-embedding` de NaN API. Indexa 190+ skills como vectores de 4096 dimensiones y permite consultarlos por similitud de contenido.

**Estado actual:** ✅ 229 skills indexados (2026-06-14), funcionando en localhost:8000

## Arquitectura

```
Petición del usuario
  ↓
Mastermind extrae palabras clave / intención
  ↓
Script consultar-skills.py → embedding (qwen3-embedding) → query ChromaDB local
  ↓
Top-5 skills más relevantes con scores de similitud (0.0 - 1.0)
  ↓
Mastermind carga SOLO esos skills con skill_view()
  ↓
Ejecuta la tarea con contexto preciso
```

## Componentes

### ChromaDB Server (local)
- **URL:** `http://localhost:8000`
- **Colección:** `mastermind-skills`
- **Datos persistentes:** `/hermes-home/chromadb-data/`
- **Versión:** 1.5.9
- **Venv:** `/hermes-home/chromadb-venv/`
- **Arranque:** `bash /hermes-home/scripts/start-chromadb.sh` (script con health check y reintentos)

### Scripts

| Script | Ruta | Función |
|---|---|---|
| `indexar-skills.py` | `/hermes-home/scripts/indexar-skills.py` | Indexar todos los skills en ChromaDB |
| `consultar-skills.py` | `/hermes-home/scripts/consultar-skills.py` | Consultar skills por similitud semántica |
| `start-chromadb.sh` | `/hermes-home/scripts/start-chromadb.sh` | Arrancar ChromaDB con health check |
| `verify-index.sh` | `scripts/verify-index.sh` | Verificar estado de indexación (disco vs ChromaDB) |

### Modelo de Embeddings
- **Modelo:** `qwen3-embedding` vía `api.nan.builders/v1/embeddings`
- **Dimensiones:** 4096
- **API Key:** `NAN_API` (variable de entorno del sistema)
- **Rate limit:** 60 req/min, 3 paralelo

## Uso

### Indexar skills
```bash
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python indexar-skills.py
```

### Re-indexar desde cero
```bash
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python indexar-skills.py --reset
```

### Consultar skills (modo humano)
```bash
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python consultar-skills.py "generar informe del mercado eléctrico"
```

### Consultar skills (modo JSON — para Mastermind)
```bash
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python consultar-skills.py "texto" --json
```

### Desde Mastermind (flujo integrado)
```python
import subprocess, json, os

# 1. Consultar ChromaDB
result = subprocess.run(
    ["python3", "/hermes-home/scripts/consultar-skills.py", query_text, "--json"],
    capture_output=True, text=True, timeout=30,
    env={**os.environ, "NAN_API": os.environ.get("NAN_API", "")}
)
skills = json.loads(result.stdout)["results"]

# 2. Filtrar por score mínimo
relevantes = [s for s in skills if s["score"] > 0.25]

# 3. Cargar top-3 skills
for s in relevantes[:3]:
    skill_view(name=s["name"])
```

## Formato de datos en ChromaDB

Cada skill se guarda con:
- **id:** path relativo del directorio del skill, con `/` → `--` (ej: `health--dieta`, `esios--esios-telegram-report`). Esto evita colisiones cuando dos directorios comparten el mismo `name:` en frontmatter.
- **metadata.name:** nombre del frontmatter (campo `name:`), que puede haber duplicados.
- **embedding:** vector 4096-dim desde qwen3-embedding
- **metadata:** name, category, tags, version, description
- **document:** texto combinado (nombre + descripción + tags + secciones relevantes)

## Mantenimiento

### Re-indexación automática
- **Cron semanal:** domingo 04:00 UTC
- **Trigger manual:** después de crear/actualizar un skill

### Cuándo re-indexar
- Después de crear un skill nuevo
- Después de actualizar un skill existente
- Si se detectan skills con score bajo en consultas donde deberían aparecer

## Pitfalls

- **Python venv obligatorio:** El Python del sistema NO tiene `requests`. Usar `/hermes-home/chromadb-venv/bin/python` para ejecutar `indexar-skills.py` y `consultar-skills.py`. Ejemplo: `/hermes-home/chromadb-venv/bin/python /hermes-home/scripts/indexar-skills.py --reset`
- **Rate limit NaN (60 req/min, 3 paralelo):** Al indexar 190+ skills, se alcanza el límite de 60 requests por minuto de NaN. **Solución:** el script `indexar-skills.py` incluye delay de 1.5s entre embeddings (añadido 2026-06-10). Si falla con 429, esperar ~60s y re-ejecutar. Los skills que fallaron se saltan y se pueden re-indexar individualmente después.
- **Nombres de directorio vs frontmatter:** Los skills se indexan con el nombre del frontmatter (campo `name:`), que puede diferir del nombre del directorio. Ejemplo: directorio `creative-ideation/` → skill `ideation`. Al verificar skills faltantes, comparar con nombres reales del frontmatter, no nombres de directorio.
- **Conteo real:** 229/229 SKILL.md indexados (2026-06-14, tras fix de duplicados).
- **ChromaDB caído tras reinicio:** Si la VM se reinicia, ChromaDB no arranca solo. Solución: ejecutar `bash /hermes-home/scripts/start-chromadb.sh`.
- **Embedding fallido:** Si qwen3-embedding falla (429), reintentar con sleep(3). Si falla 3 veces, saltar ese skill
- **Memoria:** ChromaDB usa ~500MB RAM con 200 skills. En MicroVM de 2GB va justo pero funciona
- **No duplicar IDs:** Si un skill ya existe, se sobrescribe (add con mismo id = upsert). Pero cuidado con el siguiente punto.
- **IDs duplicados por nombre frontmatter (CRÍTICO):** El indexador usa el path relativo del directorio como ID de ChromaDB (ej: `health--dieta`), NO el nombre del frontmatter (`name:`). Esto es intencional porque hay skills con el mismo `name:` en directorios distintos:
  - `dieta` → `health/dieta/` y `health/dieta-tracking/`
  - `static-digest-pipeline` → `devops/` y `frontend-dashboard-patterns/`
  Si el indexador se modifica para volver a usar `name:` como ID, fallará con `DuplicateIDError`. **Siempre usar path relativo como ID.**
- **Fallback:** Si ChromaDB no responde, Mastermind debe cargar skills por el método tradicional (snapshot completo)
- **Deployment ≠ Integración (CRÍTICO):** Tener ChromaDB corriendo con 190 skills indexados NO significa que Mastermind lo use. En auditoría se descubrió que el sistema estaba técnicamente operativo pero NUNCA se invocaba en sesiones reales — la integración era 100% documental. **Check obligatorio tras desplegar:** ¿hay algún trigger real que llame a `consultar-skills.py`? Si la respuesta es "no, pero está documentado que debería", ESTÁ ROTO. Solución: añadir la llamada al SOUL.md como paso OBLIGATORIO en el flujo de carga de skills.
- **Threshold demasiado alto (CRÍTICO):** El threshold de 0.5 es demasiado restrictivo. Skills relevantes como `mastermind-orchestration` (score 0.46) o `delegar-no-comprimir` (0.40) se quedan fuera. **Solución:** usar threshold de 0.25. Con qwen3-embedding, los scores rara vez superan 0.5 incluso para skills muy relevantes. Si el threshold está en 0.5, ChromaDB devuelve 0 resultados en la mayoría de consultas y se cae al fallback, anulando todo el sistema.
- **Calidad del embedding limitada por el documento indexado:** El `document` que se guarda en ChromaDB solo incluye frontmatter (nombre + descripción + tags). El cuerpo del SKILL.md no se indexa. **Solución:** modificar `indexar-skills.py` para que el documento incluya también las primeras secciones relevantes del cuerpo (Resumen, secciones principales). Más texto en el embedding = mejor similitud semántica. Ver `references/embedding-quality.md`.
- **pip install bloqueado por detector de servidores de Hermes:** El detector de procesos largos de Hermes confunde `pip install` con un servidor y lo rechaza en foreground. **Solución:** ejecutar `pip install` en background mode (`terminal(background=true)`) o usando `python -m pip install` dentro del venv. Ver `references/setup-from-scratch.md` para el procedimiento completo de instalación.
- **ChromaDB 1.5.9 necesita opentelemetry-instrumentation-fastapi:** No es una dependencia declarada en `pip install chromadb`, pero el servidor FastAPI de ChromDB la requiere en tiempo de importación. **Solución:** instalar `opentelemetry-instrumentation-fastapi` después de chromadb. Sin esto, el server falla con `ModuleNotFoundError: No module named 'opentelemetry.instrumentation'`.
- **ChromaDB 1.5.9 CLI cambió:** `python -m chromadb run` ya no funciona (error `chromadb is a package and cannot be directly executed`). El nuevo CLI es `chroma run`. El script `start-chromadb.sh` debe usar `chroma run --path ... --host ... --port ...`.
- **ChromaDB 1.5.9 API v1 deprecada:** El endpoint REST `/api/v1/collections` devuelve `{"error": "Unimplemented"}`. Los scripts de indexación/consulta deben usar el **cliente Python** (`chromadb.HttpClient(host="localhost", port=8000)`) en lugar de `requests` directo contra la API v1. El cliente Python usa API v2 internamente.
- **ChromaDB 1.5.9 tarda 60-120s en arrancar con datos persistentes:** Al cargar un dataset grande de vectores desde disco, el servidor Rust se queda "listening" pero no atiende peticiones HTTP hasta que termina de reconstruir el índice. **No usar `subprocess.run()` con timeout corto** — el proceso se queda pegado. **Solución:** lanzar con `nohup` en background y esperar con `curl` o `requests` en un loop de hasta 120s. El script `start-chromadb.sh` ya incluye este patrón. Si ChromaDB responde con 410 (v1 deprecated) pero el heartbeat funciona, el servidor está operativo — usar solo API v2.
- **ChromaDB no se desapeña con nohup + subprocess.run():** Si se lanza `chroma run` desde Python con `subprocess.run()`, el proceso NO se queda en background — se queda pegado en el padre. **Solución:** usar `Popen` con `stdout=PIPE` y esperar, o mejor aún, usar `nohup` + `&` desde shell (`bash -c "nohup ... &"`). El script `start-chromadb.sh` usa este patrón correctamente.
- **ChromaDB 1.5.9 HttpClient:** El constructor acepta `host` y `port` como parámetros separados, NO `url=`. Ejemplo correcto: `chromadb.HttpClient(host="localhost", port=8000)`. Pasar `url="http://localhost:8000"` da `TypeError: HttpClient() got an unexpected keyword argument 'url'`.
- **El indexador necesita logging a archivo para debug:** El script original imprimía a stdout sin buffer, pero cuando se ejecuta en background el output no se capturaba. **Solución:** el indexador v2 usa `logging.FileHandler` a `/tmp/indexar-skills.log` además de stdout. Siempre revisar ese log si el indexador parece no producir output.

## Referencias

- Scripts: `/hermes-home/scripts/indexar-skills.py`, `/hermes-home/scripts/consultar-skills.py`, `/hermes-home/skills/mastermind/chromadb-skills-vector-search/scripts/start-chromadb.sh`
- Datos: `/hermes-home/chromadb-data/`
- API NaN: `https://api.nan.builders/v1/embeddings`
- Modelo: `qwen3-embedding`
- Rate limit 429 recovery: `references/rate-limit-nan-429.md`
- Setup desde cero (instalación completa): `references/setup-from-scratch.md`
- Calidad del embedding: `references/embedding-quality.md`
- Skill relacionado: `mastermind-orchestration`
- Reranker status: `references/nan-reranker-status.md` — estado del endpoint `/rerank` de Nan (404, no activo)
- ChromaDB startup troubleshooting: `references/chromadb-startup-troubleshooting.md` — problemas de arranque con ChromaDB 1.5.5+ (tarda 60-120s, no se desapeña con nohup, API v1 vs v2)
- Duplicate names audit: `references/duplicate-names-audit.md` — skills con mismo nombre frontmatter en directorios distintos (`dieta`, `static-digest-pipeline`), por qué el indexador usa path relativo como ID