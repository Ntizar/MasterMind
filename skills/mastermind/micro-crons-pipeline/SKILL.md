---
name: micro-crons-pipeline
version: "2.0.0"
description: "Sistema de producción iterativa con micro-crons: divide proyectos grandes en tareas atómicas y ejecuta automáticamente vía cron jobs en cadena"
tags: [pipeline, cron, automation, projects, iteration, assembly-line]
related_skills: [mastermind-orchestration, human-loop-control]
---

# 🏭 Micro-Crons Pipeline — Línea de Montaje de Proyectos

## Cuándo usar este skill

- Usuario quiere crear un proyecto grande y trabajar en él por iteraciones
- Hay múltiples tareas secuenciales que pueden automatizarse
- Se necesita un "pipeline" que avance solo con cron jobs
- Proyectos de 1+ día que受益 de ejecución incremental

## Concepto

Un **cron maestro** lee el estado del proyecto (archivos JSON), determina la siguiente tarea atómica, la ejecuta, y actualiza el estado. Cada iteración = 1 tarea completada. El proyecto crece gradualmente hasta completarse.

```
┌─────────────────────────────────────────────────┐
│           CRON MAESTRO (cada 2h)                │
│  1. Lee pipeline-status.json                    │
│  2. Lee backlog.json (tareas pendientes)        │
│  3. Ejecuta siguiente tarea atómica             │
│  4. Actualiza estado y métricas                 │
│  5. Entrega resumen                             │
└─────────────────────────────────────────────────┘
                    ↓
      Cada iteración = 1 tarea completada
                    ↓
      Proyecto crece hasta completarse
```

## Flujo de implementación

### Build Pipeline (original)
El flujo estándar descrito abajo: crear proyecto, poblar backlog, ejecutar crons.

### Audit Loop (variante — descubierta en sesión 2026-06-11)
Auditar cíclicamente un proyecto existente hasta que no queden issues.
No construye nada — solo encuentra problemas y reporta.

```
Build Pipeline → "haz cosas hasta que esté terminado"
Audit Loop    → "encuentra problemas hasta que no quede ninguno"
```

Características:
- **State file** trackea fases, issues encontrados, issues fijados
- **Script auditor** lee los docs, estructura el contexto para el agente
- **Cron diario** ejecuta la auditoría como agente LLM (con skills de contexto)
- **8+ fases secuenciales** — cada fase debe quedar 100% limpia antes de avanzar
- **Cada issue requiere solución concreta** — no vale "hay que mejorarlo"
- **Cuando todas las fases están limpias** → status=completed, cron se duerme

Ejemplo real: `terral-architecture` → `references/terran-audit-setup.md`

Para implementar un Audit Loop:
1. Definir las fases de auditoría (schema, permisos, rendimiento, negocio...)
2. Crear state file JSON con las fases y su estado
3. Crear script helper (Python) para leer estado + docs + loguear issues
4. Crear cron con prompt exhaustivo + skills de contexto + workdir del proyecto
5. El cron corre hasta que `state.completed = true`

### Paso 1: Crear el proyecto

```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh crear <nombre> [tipo] [descripcion]
```

Esto genera en `/root/workspace/proyectos/<nombre>/`:
- `pipeline-status.json` — estado actual del pipeline
- `backlog.json` — lista de tareas pendientes
- `README.md`, `src/`, `tests/`, `docs/`, `scripts/`

### Paso 2: Poblar el backlog

Agregar tareas atómicas al backlog.json. Cada tarea debe ser:
- **Atómica**: max 1-2 archivos principales
- **Autoconclusiva**: completable en ~15 min de ejecución del cron
- **Con dependencias claras**: qué necesita que esté hecho antes

```bash
bash pipeline-init.sh agregar <nombre> '{"id":"task-001","tipo":"feature","prioridad":"alta","descripcion":"...","criterios_aceptacion":[...],"dependencias":[],"archivos_afectados":["src/..."],"estado":"pending","intentos":0}'
```

### Paso 3: Generar el cron maestro

```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-generar-cron.sh <nombre> [deliver] [schedule]
```

Esto imprime el comando `hermes cron create` listo para copiar y pegar.

### Paso 4: Crear el cron en Hermes

```bash
hermes cron create \
  --name "<nombre>-pipeline" \
  --schedule "0 */2 * * *" \
  --deliver "telegram" \
  --prompt "<prompt auto-generado>"
```

### Paso 5: Gestionar el pipeline

| Acción | Comando |
|--------|---------|
| Ver estado | `bash pipeline-init.sh estado <nombre>` |
| Ejecutar iteración manual | `bash pipeline-init.sh iterar <nombre>` |
| Pausar | `hermes cron pause <nombre>-pipeline` |
| Reanudar | `hermes cron resume <nombre>-pipeline` |
| Ver cron jobs | `hermes cron list` |

## Schema del pipeline-status.json

```json
{
  "proyecto": "nombre",
  "version": "1.0.0",
  "tipo": "web|backend|documento|generico",
  "estado": "planning|in-progress|review|done",
  "fase_actual": "nombre-fase",
  "tarea_actual": { "id": "task-001", "estado": "in-progress" },
  "metricas": {
    "tareas_totales": 15,
    "tareas_completadas": 3,
    "tareas_en_curso": 1,
    "tareas_pendientes": 11,
    "tasa_exito": 94,
    "ultima_ejecucion": "2026-06-11T14:30:00Z"
  },
  "historial": [],
  "configuracion": {
    "frecuencia_horas": 2,
    "max_intentos_por_tarea": 3,
    "timeout_minutos": 30
  }
}
```

## Schema del backlog.json

```json
{
  "proyecto": "nombre",
  "tareas": [
    {
      "id": "task-001",
      "tipo": "feature|fix|refactor|docs|test",
      "prioridad": "alta|media|baja",
      "descripcion": "Descripción clara de la tarea",
      "criterios_aceptacion": ["Criterio 1", "Criterio 2"],
      "dependencias": [],
      "archivos_afectados": ["src/..."],
      "estado": "pending|in-progress|review|done|failed|blocked",
      "intentos": 0
    }
  ]
}
```

## Templates de fases por tipo de proyecto

### Web (HTML/JS/CSS)
1. wireframe → estructura-html, css-basico, layout-responsive
2. desarrollo → componentes-core, interactividad, estado-global
3. optimizacion → accesibilidad, performance, seo-basico

### Backend (Node.js)
1. fundamentos → setup-proyecto, config-db, modelos-base
2. api → endpoints-core, validacion, autenticacion
3. integracion → tests-unit, tests-integracion, docs-api

### Documento/Artículo
1. estructura → outline, secciones-principales
2. contenido → desarrollo-seccion-1, desarrollo-seccion-2, ejemplos
3. pulido → edicion, formato, revision-final

## Configuración de frecuencia

| Tamaño proyecto | Frecuencia | Tareas | Validación |
|-----------------|------------|--------|------------|
| Pequeño (1-2 días) | Cada 1h | 5-10 | No |
| Mediano (1 semana) | Cada 2h | 10-30 | Después de cada feature |
| Grande (1+ mes) | Cada 4h o diaria | 30-100+ | + reporte semanal |

## Prompt del cron maestro (template)

```
Eres el orquestador del pipeline de producción del proyecto "[NOMBRE]".
Ubicación: /root/workspace/proyectos/[NOMBRE]/

INSTRUCCIONES:
1. Lee pipeline-status.json y backlog.json
2. Busca siguiente tarea pending sin dependencias bloqueadas
3. Si hay tarea:
   - Actualiza backlog.json → estado "in-progress"
   - Ejecuta la tarea (crea/modifica archivos)
   - Si éxito: marca "done", agrega al historial
   - Si falla: incrementa intentos, si >=3 marca "failed"
4. Actualiza métricas en pipeline-status.json
5. Entrega resumen: qué se hizo, progreso, siguiente tarea

REGLAS:
- Tareas atómicas (max 1-2 archivos)
- Máx 15 min por tarea
- NUNCA dejes archivos a mitad
- JSON siempre válido
- Si proyecto completo → marca estado "done"
```

## Pitfalls

- **Cron no tiene contexto entre sesiones**: todo el estado vive en archivos JSON. El cron SIEMPRE lee los archivos antes de actuar.
- **Tarea demasiado grande**: dividir en subtareas. Si toma >15 min, no es atómica.
- **Lock files**: usar `/root/workspace/proyectos/<nombre>/.pipeline.lock` para evitar ejecuciones paralelas.
- **NaN deploy tiene delay**: tras push a GitHub, NaN tarda 10-30s en reconstruir el contenedor. No asumir que es inmediato.
- **Express sirve index.html por defecto**: si el archivo principal se llama `dashboard.html`, Express no lo sirve en `/`. Renombrar a `index.html`.
- **Cron jobs anidados**: NUNCA programar más crons dentro de un cron pipeline. Mantener simple.
- **🔴 Crons paralelos NO deben modificar los mismos archivos**: Si dos crons se ejecutan a la vez y ambos modifican app.ts (o index.html, o crm.js), el segundo en escribir SOBRESCRIBE el trabajo del primero. Solución: consolidar en UN solo cron todo lo que modifique el mismo archivo (ej: un cron que cree pedidos.ts + cobros.ts + actualice app.ts de una vez). Si no es posible, staggerear secuencialmente (30 min de diferencia).
- **🔴 Frontend crons que modifican index.html + crm.js deben ir SECUENCIALES**: Aunque los cambios sean en diferentes secciones (diferentes tabs HTML, diferentes funciones JS), el riesgo de corrupción por escritura concurrente es real. Staggerear con mínimo 30 min de diferencia entre crons que toquen los mismos archivos. Alternativa: consolidar en un solo cron que añada todos los tabs pendientes.
- **🔴 NaN container aislado**: el contenedor NaN NO puede leer archivos de `/hermes-home/`. Si el pipeline necesita datos de Hermes, generarlos en la microVM primero (patrón "static data bake"). Ver `frontend-dashboard-patterns` sección 17.
- **🔴 Datos inventados = rechazados**: David rechaza explícitamente datos sintéticos en dashboards. Empty state honesto > lista de eventos falsos. "Aquí hacemos las cosas bien y no nos inventamos cosas."

## Archivos de referencia

- `references/pipeline-status-template.json` — Template del archivo de estado del pipeline
- `references/cron-maestro-prompt-template.md` — Template del prompt autónomo para el cron maestro
- `references/mega-plan-pattern.md` — Patrón MEGA-PLAN.md (fuente de verdad multi-sesión)
- `references/contrata-publico-sesion-08.md` — Caso de estudio: Sesión 8 (checklist + pulido)
- `scripts/pipeline-init.sh` — Script de inicialización de proyectos y gestión del backlog
- `scripts/pipeline-generar-cron.sh` — Generador automático del prompt del cron maestro
- `examples/pipeline-ejemplo.md` — Tutorial paso a paso con ejemplo práctico
- `examples/pipeline-demo.html` — Demo visual interactiva del pipeline

**Ver también:** `esios-nan-deploy` para patrones de deploy NaN, `frontend-dashboard-patterns` para arquitectura de dashboards.

### MEGA-PLAN.md Pattern (alternativa ligera al JSON-based pipeline)

**Cuándo usar:** Proyectos grandes (8+ sesiones) donde el plan debe ser legible por humanos y ejecutable por crons. Es más simple que el patrón JSON-based: un solo archivo Markdown como fuente de verdad.

**Arquitectura:**
```
proyecto/
├── MEGA-PLAN.md          ← Estado + plan (fuente de verdad)
├── index.html            ← Frontend
├── scripts/
│   ├── sesion-01.py      ← Script de cada sesión
│   └── sesion-02.py
└── data/
    └── datos-generados/
```

**Reglas del MEGA-PLAN.md:**
1. **Contiene:** Visión, módulos, estructura de archivos, lista de sesiones con dependencias, estado actual
2. **Cada sesión lee el MEGA-PLAN.md** al inicio para saber dónde está el proyecto
3. **Cada sesión actualiza el MEGA-PLAN.md** marcando su estado como ✅ al terminar
4. **Nunca cambia el plan** — solo el estado (pendiente → completado)
5. **Un cron = una sesión** — el cron prompt incluye "lee MEGA-PLAN.md, ejecuta tu sesión, actualiza estado"

**Crear crons one-shot:**
```bash
hermes cron create \
  --name "proyecto-sesion-02" \
  --schedule "30m" \
  --repeat 1 \
  --workdir "/root/workspace/proyecto/" \
  --deliver "origin" \
  --prompt "1. Navega a /root/workspace/proyecto/
2. Lee MEGA-PLAN.md para contexto
3. Ejecuta: python3 scripts/sesion-02.py
4. Si OK, actualiza MEGA-PLAN.md marcando Sesión 2 como ✅
5. Commit + push
6. Resume resultado"
```

**Ventajas vs JSON-based:**
- ✅ Legible por humanos (Markdown)
- ✅ No necesita parser JSON
- ✅ El cron tiene todo el contexto en el prompt
- ❌ Menos estructurado para machine-reading
- ❌ No tiene métricas automáticas

**Pitfalls:**
- **Crons paralelos NO modifican mismos archivos** — si dos crons tocan index.html, staggerear 30+ min
- **MEGA-PLAN.md debe ser autocontenido** — cada cron lo lee, no depende de contexto de chat
- **Commit tras cada sesión** — si un cron falla, el MEGA-PLAN muestra exactamente dónde se quedó
- **Script placeholder ≠ implementación real** — los scripts `sesion-XX.py` creados inicialmente son placeholders (ej: `print('placeholder')`). Si la sesión se implementa manualmente (write_file/patch directo), el placeholder NO se ejecuta. No confiar en que el script "funcione" — verificar output directamente.

### Verificación post-sesión (checklist obligatorio)

Antes de marcar una sesión como ✅ en el MEGA-PLAN.md, verificar:

1. **Archivos creados/modificados** — `git status` o `ls` para confirmar
2. **Funcionalidad core** — la feature principal funciona (ej: Tab 6 renderiza, no muestra "próximamente")
3. **Integración** — no rompe tabs/existing features (verificar que `switchTab` no tiene errores)
4. **Responsive** — al menos breakpoint base (640px) presente
5. **Hero section** — presente con stats
6. **Footer** — atribución "David Antizar" presente
7. **Commit message** — formato `Sesión N: descripción corta`
8. **MEGA-PLAN.md actualizado** — sesión marcada como ✅ con output descriptivo

**Si alguna verificación falla** → documentar error, NO avanzar a la siguiente sesión.

## Referencias

- `mastermind-orchestration` — Orquestación multi-agente (patrón "pipeline de crons" en sección Patrones)
- `human-loop-control` — Sistema de control para cambios críticos
- Repo Mastermind: `mastermind/micro-crons-pipeline.md` (copia en repo)

---

**Autor:** David Antizar
**Versión:** 1.0.0
