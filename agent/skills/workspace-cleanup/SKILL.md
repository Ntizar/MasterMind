---
name: workspace-cleanup
version: "1.0.0"
description: "Procedimiento sistemático para auditar y limpiar el workspace de un agente AI — identificar espacio ocupado, clasificar por utilidad, eliminar lo innecesario."
tags: [cleanup, audit, disk-space, workspace, maintenance]
---

# Workspace Cleanup — Auditoría y Limpieza de Entorno

## Resumen

Procedimiento para auditar un entorno de agente (Hermes, Claude Code, etc.): medir espacio por componente, identificar dead weight, clasificar por utilidad real, y ejecutar limpieza ordenada por impacto.

## Cuándo usar

- Usuario pide "limpiar", "qué ocupa", "haz un resumen del estado", "qué borrar"
- El entorno crece descontroladamente y necesita mantenimiento
- Antes de un deploy o migración, para reducir superficie
- Cuando el usuario nota que algo ocupa demasiado

## Flujo de Auditoría (7 pasos)

### Paso 1: Mapear estructura

Medir todo en capas:

```bash
# Raíz del entorno
du -sh /hermes-home/* | sort -rh

# Workspace de proyectos
du -sh /root/workspace/*/ 2>/dev/null | sort -rh

# Subcomponentes de los grandes
du -sh /root/workspace/GRANDE/*/ 2>/dev/null | sort -rh
```

**Objetivo:** Ver qué componentes son los gordos y dónde está el espacio.

### Paso 2: Clasificar por categoría

Cada componente se clasifica en una de estas categorías:

| Categoría | Qué incluye | Ejemplo |
|-----------|-------------|---------|
| **Código fuente** | Archivos de código, configs, docs | `src/`, `README.md`, `package.json` |
| **Dependencias** | `node_modules/`, `.venv/`, `vendor/` | `node_modules/`, `chromadb-venv/` |
| **Datos cache** | Sesiones, logs, audio, modelos | `sessions/`, `audio_cache/`, `logs/` |
| **Modelos/ML** | ONNX, PyTorch, embeddings | `PINTO_model_zoo/`, `presidio/` |
| **Bases de datos** | SQLite, ChromaDB, state | `state.db`, `chromadb-data/` |
| **Output cron** | Resultados de jobs programados | `cron/output/` |
| **Proyectos activos** | Repos que se usan actualmente | `TimeIneco/`, `GTFSSpain/` |
| **Proyectos muertos** | Reos abandonados o de prueba | `AdelaTest01/` |

### Paso 3: Evaluar utilidad real

Para cada componente grande, verificar:

1. **¿Se referencia en código actual?** `grep -rl "nombre" /root/workspace/ProyectoActual/`
2. **¿Tiene cron asociado?** `cat /hermes-home/cron/jobs.json | grep nombre`
3. **¿Es un proyecto propio o de terceros?**
4. **¿Los datos se pueden regenerar?** (node_modules → `npm install`, modelos → descargar de nuevo)
5. **¿Hay un plan de mantenimiento?** (cron de limpieza, rotación)

### Paso 4: Priorizar por impacto

| Impacto | Criterio | Acción |
|---------|----------|--------|
| **🔴 Alto** | >100 MB y no esencial | Borrar o comprimir |
| **🟠 Medio** | 50-100 MB y regenerable | Borrar deps, regenerar después |
| **🟡 Bajo** | 10-50 MB y útil | Mantener, revisar periódicamente |
| **🟢 Mínimo** | <10 MB | No tocar |

### Paso 5: Presentar informe al usuario

Formato del informe:

```
## 🧹 Estado del Workspace

### Componentes principales
| Componente | Tamaño | Categoría | Utilidad |
|---|---|---|---|
| state.db | 1.3 GB | Base de datos | 🔴 CRÍTICO - investigar |
| sessions/ | 960 MB | Cache | 3,154 archivos >7 días |
| Adela/ | 1.79 GB | Código + deps | node_modules regenerables |
| repos/ | 592 MB | Modelos terceros | PINTO y presidio no referenciados |

### Propuesta de limpieza
1. 🔴 Adela node_modules → 1.79 GB → 104 MB (código intacto)
2. 🟠 repos/ PINTO + presidio → 592 MB → 25 MB (no referenciados)
3. 🟠 Sesiones >7 días → 960 MB → 232 MB (3,308 archivos)
4. 🟡 Audio cache duplicados → 11 MB → 1.4 MB
5. 🟡 Cron output antiguos → 7.6 MB → 2.5 MB

Total ahorrado: ~2.5 GB
```

### Paso 6: Ejecutar limpieza

Orden de ejecución:

1. **Dependencias regenerables primero** (`node_modules`, `.venv`)
2. **Modelos/ML no referenciados** (buscar referencias antes de borrar)
3. **Sesiones caché antiguas** (>7 días para JSONL, >14 días para audio)
4. **Output cron antiguos** (>7 días)
5. **Datos duplicados** (.ogg + .mp3 del mismo timestamp)

**Regla:** NUNCA borrar state.db sin investigar primero. Es la base de datos interna del agente.

### Paso 6.5: Verificar post-limpieza

```bash
# Medir delta
du -sh /hermes-home/
du -sh /root/workspace/
du -sh /root/workspace/*/ | sort -rh | head -10
```

### Paso 7: Configurar mantenimiento preventivo

Para evitar que el problema se repita:

| Componente | Frecuencia | Acción |
|------------|------------|--------|
| Sesiones JSONL | Semanal | Borrar >7 días |
| Audio cache | Mensual | Borrar >14 días |
| Cron output | Mensual | Borrar >7 días |
| node_modules | Al cambiar código | Regenerar con `npm install` |
| state.db | Trimestral | Investigar crecimiento anómalo |

## Ejemplos reales

### Caso: Workspace de Hermes (23 junio 2026)

- **Antes:** 3.69 GB workspace + 3.0 GB /hermes-home
- **Después:** 1.5 GB workspace + 3.0 GB /hermes-home
- **Ahorro:** 2.19 GB workspace
- **Método:** Borrar node_modules de Adela (1.69 GB), repos no referenciados (567 MB), sesiones antiguas (728 MB)
- **state.db:** 1.3 GB sin tocar (investigar en otra sesión)

## Pitfalls

- **No borrar state.db sin investigar** — Es la base de datos interna del agente. Si creció a 1.3 GB, puede ser normal (muchas sesiones) o puede indicar un problema. Investigar las tablas antes de tocar.
- **Verificar referencias antes de borrar** — Un modelo o repo puede parecer inútil pero estar referenciado en un cron o script. Siempre `grep -rl` antes de borrar.
- **Los node_modules son regenerables** — Si un proyecto tiene código fuente intacto, borrar node_modules es siempre seguro. El usuario puede reinstalar con `npm install` o `pip install`.
- **Sesiones JSONL vs JSON** — Los archivos `.jsonl` son el formato compacto de sesiones. Los `.json` grandes (2+ MB) son duplicados o formatos antiguos. Priorizar borrar los `.json`.
- **Audio cache duplicado** — El TTS genera tanto `.ogg` como `.mp3` del mismo contenido. Borrar uno de los dos (el más pesado) es seguro.
- **Cron output son directorios** — La estructura de `/hermes-home/cron/output/` usa directorios con hash como nombre, no archivos sueltos. Contar directorios, no archivos.
- **Metadata de proyectos** — Archivos como `metadata/conjuntos-datos.json` en GTFSSpain pueden ser usados por crons. Verificar el cron antes de borrar.
