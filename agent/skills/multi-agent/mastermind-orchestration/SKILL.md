---
name: mastermind-orchestration
version: "1.2.0"
description: "Orquestación multi-agente unificada para Mastermind en Hermes+GitHub. Reemplaza mastermind, orca y canvas-workflow. Usa delegate_task nativo de Hermes."
tags: [multi-agent, orchestration, mastermind, hermes, delegation]
---

# Mastermind Orchestration — Sistema Unificado

## Resumen

Sistema de orquestación multi-agente para Mastermind ejecutándose en Hermes con repos en GitHub. Reemplaza el antiguo sistema mastermind (Obsidian+OpenCode), orca y canvas-workflow. Simple, rápido, Hermes-native.

## Principios

1. **Un orquestador, muchos especialistas** — Mastermind clasifica y delega. Los 143 skills especializados ejecutan con conocimiento profundo de su dominio.
2. **Hermes-native** — Todo usa `delegate_task`, sin herramientas externas
3. **GitHub-centric** — El repo es la fuente de verdad, no Obsidian
4. **Skills sobre agentes** — Cada skill es un especialista en un dominio, no un rol genérico
5. **Delegar, no comprimir** — Paralelizar cuando sea posible
6. **Human loop obligatorio** — En cambios críticos (>5 archivos, decisiones de arquitectura), Mastermind presenta el plan y espera ✅ antes de ejecutar

## Carga de skills — Búsqueda semántica con ChromaDB (PRIMARIO)

Desde 2026-06-10, la carga de skills usa ChromaDB local como mecanismo principal:

1. **Mastermind recibe una petición** → extrae palabras clave / intención
2. **Consulta ChromaDB** (`localhost:8000`, colección `mastermind-skills`) con `consultar-skills.py`
3. **ChromaDB devuelve top-5 skills** con scores de similitud (0.0 - 1.0) usando vectores 4096-dim de `qwen3-embedding`
4. **Filtro por score > 0.5** → carga solo esos skills con `skill_view()`
5. **Fallback:** si ChromaDB no responde o no encuentra nada, usar el sistema de prioridad por dominio (abajo)

**Scripts:**
- `scripts/consultar-skills.py` — consulta semántica (modo `--json` para Mastermind)
- `scripts/indexar-skills.py` — re-indexación manual
- `scripts/delegation-flows.py` — clasificación de complejidad con `classify_task()` y heurísticas

**Cron:** `chromadb-reindex-semanal` (domingo 04:00 UTC)

**Skill de referencia:** `chromadb-skills-vector-search`

### Sistema de Prioridad por Dominio (FALLBACK)

Si ChromaDB no está disponible, se usa este sistema tradicional:

### Antes (v3.1) — Agentes genéricos
```
Implementer genérico → hace frontend, backend, infra, todo mal
```

### Después (v4.0) — Skills especializados
```
Mastermind clasifica dominio → Carga skills del dominio → delegate_task con contexto especializado
```

| Dominio | Skills | Especialización |
|---------|--------|----------------|
| **Software** (HIGH) | 17 skills | TDD, debug, code review, refactor, iteración |
| **GitHub** (MEDIUM) | 7 skills | PR workflow, code review, issues, repo mgmt |
| **Frontend** (MEDIUM) | 3 skills | Aurora Design System, patrones dashboard |
| **Backend** (MEDIUM) | 6 skills | APIs REST, ESM interop, fetch paralelo |
| **Infra** (MEDIUM) | 6 skills | HTTP robusto, Docker, seguridad, cache |
| **DevOps** (MEDIUM) | 10 skills | Deploy NaN, Aurora Nightly, cron jobs |
| **Data Science** (MEDIUM) | 8 skills | Simuladores, Monte Carlo, análisis |
| **Creative** (MEDIUM) | 22 skills | Diagramas, ASCII, diseño, video |

**Carga de skills:**
- **HIGH (Core)** → Se cargan automáticamente: `subagent-driven-development`, `delegar-no-comprimir`, `mastermind-orchestration`, `github-workflow`, `systematic-debugging`
- **MEDIUM (Dominio)** → Se cargan con `skill_view()` cuando toca ese tema
- **LOW (Archivo)** → Solo si el usuario los pide

Ver `skills_list` de Hermes para el índice completo (143 skills cargados dinámicamente).

## Roles de Agentes

### Mastermind (Orquestador Principal)
- Clasifica tareas por complejidad
- Decide: hacer directamente o delegar
- Integra resultados y verifica
- Define en SOUL.md

### Subagentes (vía `delegate_task`)

| Rol | Cuándo usarlo | Toolsets típicos |
|---|---|---|
| **Explorer** | Analizar código/contexto sin modificar | `file`, `terminal` |
| **Planner** | Diseñar estrategia y pasos | `file` |
| **Implementer** | Ejecutar código o cambios | `terminal`, `file` |
| **Reviewer** | Validar calidad contra spec | `file` |
| **Critic** | Revisión adversarial (cosas críticas) | `file` |

**Regla:** Tareas simples → Mastermind directo. Complejas (5+ pasos) → delegar.

## Niveles de Complejidad

### Nivel 1 — Directo (Mastermind solo)
- 1-3 tool calls
- Cambios en 1-2 archivos
- Respuestas simples
- **Ejemplo:** Buscar algo, leer archivo, hacer commit

### Nivel 2 — Delegación simple
- 4-8 tool calls
- Cambios en 3-5 archivos independientes
- **Ejemplo:** Refactor de módulo, implementar feature con tests
- **Patrón:** Mastermind planifica → 1 Implementer → Mastermind verifica

### Nivel 3 — Delegación paralela
- 8+ tool calls
- Múltiples features o módulos independientes
- **Ejemplo:** Optimizar frontend + backend + tests simultáneamente
- **Patrón:** Mastermind planifica → 2-3 Implementers en paralelo → Mastermind integra

### Nivel 4 — Orquestación completa
- Proyectos grandes, múltiples PRs
- **Ejemplo:** Feature completa con backend, frontend, docs, tests
- **Patrón:** Planner → Implementers paralelos → Reviewer → Critic → Mastermind integra y merge

## Flujo de Trabajo

### Tarea recibida
```
1. ¿Cuántos archivos toca?
   - 1-2 → Nivel 1 (directo)
   - 3-5 → Nivel 2 (delegación simple)
   - 5+ independientes → Nivel 3 (paralelo)
   - Proyecto completo → Nivel 4 (orquestación)

2. ¿Es código, análisis, o infra?
   - Código → subagentes de dev
   - Análisis → Mastermind directo o Explorer
   - Infra → Mastermind directo (conocimiento específico)

3. Ejecutar según nivel
```

### Delegación estándar (Nivel 2-3)
```python
delegate_task(
    tasks=[
        {
            "goal": "Tarea específica con contexto completo",
            "context": "Archivos, paths, errores, constraints",
            "toolsets": ["terminal", "file"]
        }
    ]
)
```

### Reglas de delegación
- ** SIEMPRE** dar contexto completo al subagente (no puede leer el chat)
- **NUNCA** delegar tareas que necesitan interacción con el usuario
- **NUNCA** delegar más de 3 tareas en paralelo (límite de Hermes)
- **SIEMPRE** verificar resultados del subagente antes de entregar

## Patrones de Uso

### Patrón: Fix paralelo
Cuando hay 3+ bugs independientes:
```
Mastermind identifica bugs → delega fixes en paralelo → integra y verifica
```

### Patrón: Feature completa
```
Mastermind planifica → Implementer(s) ejecutan → Reviewer valida → Mastermind merge
```

### Patrón: Investigación + implementación
```
Explorer analiza → Mastermind decide → Implementer ejecuta → Reviewer valida
```

### Patrón: Ecosystem Module Factory — Creación paralela de módulos TS

Cuando hay que crear un ecosistema de 3+ módulos TypeScript independientes (ej: Adela con 10 módulos), este patrón maximiza throughput mediante delegación paralela.

#### Estructura estándar de cada módulo

```
modulo/
├── README.md              # Quick start + API + "Integración con otros ..."
├── package.json           # name, version 1.0.0, type: module, scripts: build + test
├── tsconfig.json          # Strict, ES2022, Node16 moduleResolution
├── src/
│   ├── index.ts           # Barrel export
│   ├── ...ts              # Módulos funcionales
│   └── types.ts           # Interfaces
├── tests/
│   └── *.test.ts          # Tests con tsx --test (mínimo 15 tests)
└── dist/                  # outDir, rootDir: src
```

#### Flujo de ejecución

**FASE 1 — Preparación:**
1. Ver qué módulos extraer de código existente vs crear desde cero
2. Para cada módulo: leer código fuente con read_file si hay extracción
3. Para cada módulo desde cero: diseñar API completa (interfaces, funciones)

**FASE 2 — Delegación paralela:**
1. Lanzar 3-4 subagentes en paralelo, cada uno con:
   - Estructura exacta de archivos
   - API a exponer (copia-pega de interfaces)
   - Código fuente de referencia (si hay extracción)
   - Número mínimo de tests
   - Dependencias runtime necesarias
2. Asignar timeout=600s para módulos complejos (auth, db, export)
3. Cada subagente es autónomo: crea, testea, compila

**FASE 3 — Verificación post-ejecución:**
POR CADA módulo completado:
1. `cd /path/modulo && npm run build` → ¿Compila?
2. `npm test` → ¿Pasan tests?
3. Si falla: diagnóstico rápido y fix directo (tsconfig, imports, test config)
4. Si timeout (subagente no terminó): completar manualmente lo que falta

**FASE 4 — Push a GitHub (paralelo):**
1. Lanzar push en paralelo para N/2 grupos
2. Cada grupo: .gitignore → git init → add → commit → push

#### Pitfalls del patrón

- **Timeout en módulos complejos**: Adela_db (sql.js + migraciones) requirió 600s y aun así timeout. El subagente creó src/ pero no database.ts ni tests de migrations. Solución: para módulos con 3+ archivos src o dependencias nativas, hacer en 2 tandas o supervisar más cerca.
- **Build failure no siempre significa error real**: Adela_http compiló con tsc exit 0 pero tsconfig tenía rootDir="." en vez de "src", generando dist/src/. Fácil de arreglar, pero hay que revisar tsconfig de cada módulo.
- **TypeScript strict + tests de Jest**: los tests con jest+ts-jest hacen typecheck, y TS strict encuentra errores en tests (variables no usadas, imports raros). Arreglo: desactivar diagnostics en transform de jest.config, o configurar noUnusedLocals: false en tests.
- **Subagentes pueden modificar archivos que ya leíste**: Adela_auth/src/auth.ts fue modificado por un subagente después de leerlo → warning de "re-read antes de editar". Siempre re-read antes de parchear.

#### Ejemplo real: Ecosistema Adela (2026-06-14)

```
Sesión 1: 3 subagentes → Adela_time, Adela_env, Adela_http (P0)
          → 74 tests, push a 3 repos GitHub ✅

Sesión 2: 3 subagentes → Adela_cache, Adela_health (P1) + push P0
          + 1 subagente → Adela_auth (P1, timeout parcial, completado manual)
          → 106 tests, push a 5 repos ✅

Sesión 3: 3 subagentes → Adela_export, Adela_ai (P2) + Adela_i18n (P3)
          + 1 manual   → Adela_db (P2, timeout, completado por Mastermind)
          + 2 pushes   → push paralelo de 4 módulos
          → 114 tests, push a 10 repos ✅
```

### Patrón: Plan de mejora por fases (pipeline de crons)

Cuando hay múltiples mejoras pendientes que dependen unas de otras:

```
1. AUDIT → evaluar estado actual con métricas reales
2. PLAN → dividir en fases (cimientos → inteligencia → verificación)
3. EJECUTAR → cada fase como cron one-shot independiente
4. VERIFICAR → comprobar que todo funciona al final
```

**Reglas:**
- Cada fase debe ser **idempotente** (puede repetirse sin daño)
- Las fases se ejecutan en **serie** (cimientos antes que inteligencia)
- Cada cron entrega un resumen al final
- Si una fase falla, la siguiente no se ejecuta

**Ejemplo real (2026-06-10):** Pipeline de 14 crons para mejorar Mastermind: Fase 1 (8 crons, cimientos: ChromaDB, SOUL.md, limpieza skills) → Fase 2 (5 crons, inteligencia: Ebbinghaus, grafo, lifecycle, orquestación, dashboard) → Fase 3 (1 cron, verificación + mantenimiento semanal).

**Skill dedicado:** `micro-crons-pipeline` — para pipelines de proyectos grandes con backlog de tareas atómicas y cron maestro automático. Usar cuando el usuario quiera un proyector que avance solo con iteraciones programadas.

### Patrón: Parallel Batch Data Processing — Análisis masivo de items independientes

Cuando hay un **conjunto grande de items** (50-200) que necesitan **análisis/classificación independiente** (no construcción de código), y cada item produce un veredicto:

**Ejemplo real:** Analizar 117 repos de GitHub Stars → decidir CREATE_SKILL / SKIP / ALREADY_COVERED para cada uno.

```
FASE 1 — Registro masivo sin análisis profundo
  → Solo fetch básico (nombres, stars, lenguaje) — ~2 min para 117 items
  → NO fetch de README/tree/content (se timeout: 117 × 4 reqs ≈ 1h)

FASE 2 — Clasificación por valor
  → High (>3000⭐) → procesar AHORA con subagentes
  → Medium (500-3000⭐) → dejar para cron/siguiente
  → Low (<500⭐) o awesome lists → skip automático

FASE 3 — Batch en paralelo (3 subagentes × 6-8 items cada uno)
  ├── Subagente A: items 1-6
  ├── Subagente B: items 7-12
  └── Subagente C: items 13-18
  Toolsets: ["terminal", "file"] (necesitan acceso a archivos + shell)

FASE 4 — Cada subagente produce un veredicto por item:
  ├── CREATE_SKILL → nombre, categoría, razón
  ├── ALREADY_COVERED → qué skill existente lo cubre
  └── SKIP → razón (awesome list, irrelevante, <500⭐, C++ legacy, etc.)

FASE 5 — Mastermind agrega resultados:
  ├── Crea skills pendientes con skill_manage (acción real)
  ├── Actualiza registry con las decisiones
  └── Re-indexa ChromaDB si hubo cambios

FASE 6 — Pendientes para el cron:
  → Items que no se procesaron van al cron nocturno (3/noche)
```

**Características clave de este patrón:**
- Los items son **INDEPENDIENTES** (no comparten estado) — pueden ir en paralelo sin riesgo
- Cada subagente recibe **contexto completo** de sus 6 items (nombres, stars, descripciones)
- El output es **estructurado** (veredictos), no código
- **No hay riesgo de conflictos** entre subagentes (cada uno decide sobre items distintos)
- **Tiempo total:** 3 subagentes × ~3 min = ~5 min para 18 items (vs ~1h en serie)

**Pitfalls:**
- **Contexto grande:** 6 repos × READMEs de 8K chars = 48K chars de input. Asegurar que el modelo tiene suficiente ventana de contexto (min 32K, recomendar 128K)
- **Timeout en --all:** No ejecutar `explorar-stars.py --all` con 100+ repos si el script hace fetch de README/tree. Se timeout. Mejor hacer registro masivo primero (solo 1 req/repo)
- **Deduplicación ChromaDB:** Antes de crear skill, cada subagente debe consultar ChromaDB local para evitar duplicados. Si score > 0.25, SKIP con razón "ya existe skill X"
- **Awesome lists:** `awesome-*`, `Clone-Wars`, `*-awesome-*` → **siempre SKIP** sin análisis
- **Repos personales del usuario (Ntizar/*):** siempre prioridad, crear skill aunque sea simple
- **Agregación post-batch:** Mastermind debe verificar que los skills se crearon realmente (no confiar ciegamente en el subagente). Leer el registry post-ejecución.

### Patrón: Greenfield project con cron pipeline

Cuando hay que construir un proyecto COMPLETO desde cero (no mejorar uno existente), usar crons one-shot secuenciales para cada fase del desarrollo. Cada cron construye una parte, hace commit+push, y el siguiente cron construye sobre lo anterior.

```
1. SCAFFOLD → repositorio, estructura, README, ARCHITECTURE.md, ADR inicial
2. HACER YO (Mastermind) → Fase 0 de investigación: fuentes, zona piloto, mapa de datos, backlog
3. CRONs ONE-SHOT → cada hora/fase del desarrollo, en orden de dependencia
4. CANCELAR crons que ya no aplican → si adelantas trabajo manualmente, quitas el cron
5. AUDITORÍA → cron final para bugs, CHANGELOG, calidad
```

**Reglas específicas de greenfield:**
- **Fase 0 la hace Mastermind** — investigación, documentación, decisiones de arquitectura. No delegar a cron las decisiones de diseño.
- **Cada cron es autocontenido** — el prompt debe incluir: contexto del proyecto, archivos a modificar, qué verificar, y que haga commit+push. No asume nada del contexto del chat.
- **Import paths en monorepos** — desde apps/web-viewer/src/main.js, el path relativo correcto a src/ocean/gerstner.js es ../../../src/ocean/gerstner.js (3 niveles), no ../../src/ (2 niveles). Esto es un pitfall común en monorepos Vite con estructura apps/web-viewer/src/ + src/ raíz.
- **GH Actions + GH Pages** — usar peaceiris/actions-gh-pages@v4 para deploy automático desde GH Actions. La branch destino es gh-pages. Para repos privados, GitHub Pages requiere plan de pago. Si el usuario tiene plan gratuito, hacer el repo público o servir desde NaN.builders.
- **Build local primero** — siempre verificar npm run build localmente antes del push. El GH Actions tarda ~2-3 min y si falla, hay que esperar otro ciclo.
- **Cancelar crons solapados** — si Mastermind adelanta trabajo manualmente (ej: mejora UI mientras espera un cron), cancelar ese cron con cronjob(action='remove', job_id=...) para evitar que sobrescriba.
- **Entregar resultados** — los crons deben tener deliver='origin' para que los resultados lleguen al chat actual.

**Pipeline típico para proyecto web 3D (Three.js + Vite, ejemplo WaveThree):**
```
Cron 1 (17:18): Fase 1.1 — MVP visual (shader, escena, UI base, GH Pages)
Cron 2 (18:18): Fase 1.2 — UI avanzada + selector escenarios
Cron 3 (19:18): Fase 1.3 — Pipeline datos reales (GEBCO, NetCDF)
Cron 4 (20:18): Fase 2.1 — Batimetría 3D en escena
Cron 5 (21:18): Fase 2.2 — Escenarios reales + selector funcional
Cron 6 (22:18): Fase 3 — Océano espectral (JONSWAP + iFFT)
Cron 7 (23:18): Fase 4 — Estructuras costeras + espuma
Cron 8 (00:18): Fase 5 — Producto técnico (comparador, exportación)
Cron 9 (01:18): Auditoría final (bugs, CHANGELOG)
```

**Pitfalls del patrón greenfield:**
- **WebGPU en Three.js r170** — WebGPURenderer no está disponible desde el bundle principal (three.module.js). Se necesita three/build/three.webgpu.js. Para el MVP inicial, usar WebGLRenderer con buena configuración y añadir WebGPU cuando se necesite compute shaders.
- **Three.js bundle size** — Three.js añade ~500KB al bundle. Esperable y normal en proyectos 3D.
- **package-lock.json obligatorio** — para GH Actions, subir siempre el package-lock.json al repo. Sin él, npm install puede fallar por versiones de paquetes que no existen (ej: netcdf@0.4.1 no existe, el correcto es netcdfjs).
- **npm package name vs actual** — netcdf (npm) tiene versiones 0.2.0, 1.0.0-1.1.1 (paquete cheminfo). netcdfjs (npm) llega hasta 4.0.0. No confundirlos.
- **Git user config** — los crons ejecutan en sesiones aisladas. Asegurar que el git user.name y user.email están configurados globalmente o en el prompt del cron. Si no, los commits salen con el usuario por defecto del runner.
- **Paths de import en estructura apps/src/** — desde un archivo en apps/web-viewer/src/main.js, para importar src/ocean/file.js se necesita ../../../src/ocean/file.js. Desde apps/web-viewer/vite.config.js, para apuntar a src/ se usa path.resolve(__dirname, '../../src').

### Patrón: Frontend SPA Extension — Sidebar + Tabs + JS en paralelo

Cuando hay que añadir 3+ módulos/tabs a un dashboard SPA (Express + vanilla JS), delegar HTML y JS en paralelo:

```
Subagente A: sidebar links + tab containers (HTML)
  → Añade <a onclick="switchTab('x')" data-tab="x"> y <div id="tab-x" class="tab-content">
Subagente B: load/crear/editar/eliminar functions (JS)
  → Añade function loadX(), crearX(), etc.
```

**Contexto a pasar a ambos subagentes:**
- Lista exacta de nombres de módulo (tiene que coincidir en ambos)
- Archivo HTML actual (para A) o JS actual (para B)
- Patrón de API: `apiFetch('/api/modulos')` → `{ modulos: [...] }`
- Patrón de respuesta: `res.json({ ok: true, data: ... })` o `res.json({ modulos: [...] })`
- Convenciones del proyecto: `var` vs `const`, español vs inglés, IDs de elementos

**Verificación post-delegación:**
```bash
# Verificar consistencia de nombres
grep -c 'data-tab=' public/index.html          # sidebar links
grep -c 'id="tab-' public/index.html           # tab containers
grep -c 'function load' public/js/app.js        # JS load functions

# La cuenta debería coincidir
```

**Reglas:**
- Los nombres de tab (`data-tab="x"` en sidebar) deben coincidir EXACTAMENTE con los contenedores (`id="tab-x"`)
- Las funciones JS `loadX()` deben usar exactamente el mismo nombre `'x'` en el lazy-load
- No olvidar `window._xLoaded` flag para evitar recargas múltiples
- Después: compilar → testear → commit → push

```

### Pitfalls

- **No delegar sin contexto completo** — el subagente no tiene memoria del chat
- **No delegar tareas dependientes en paralelo** — causan conflictos
- **No saltarse la verificación** — siempre checkear resultado del subagente
- **No crear sub-subagentes** — Hermes limita profundidad a 1
- **Timeout en subagentes** — tareas research usan timeout=600, código timeout=180
- **No usar gh CLI si no está instalado** — usar git + token HTTPS con GIT_ASKPASS
- **Migraciones de plataforma:** cuando migres un proyecto a otra plataforma (Obsidian→GitHub, OpenCode→Hermes, etc.), SIEMPRE hacer un escaneo post-migración con `search_files` buscando nombres de la plataforma antigua en TODOS los archivos activos (excluyendo `legacy/`). Ver skill `system-audit` sección "Post-Migration Cleanup Execution".
- **9009 multi-iteration en archivos grandes:** subagentes fallan con timeout en código extenso (>100KB, múltiples funciones). Hacer directo con `patch`/`write_file`. Ver skill `subagent-driven-development` sección "Pitfall: 9009 multi-iteration con subagentes".
- **Fuzzy matching en `skill_manage(action='patch')`:** el patch usa fuzzy matching por texto. Si `old_string` coincide con un bloque similar pero equivocado, el patch se aplica al bloque incorrecto sin error. Siempre verificar con `read_file` el contexto antes de parchear, incluir 3-5 líneas de contexto en `old_string`, y validar post-patch con `node -c` y `grep`. Ver `references/patch-safety-fuzzy-matching.md` en skill `dieta` y la sección "Patch Safety" en `systematic-debugging`.
- **Patch puede introducir caracteres de escape literales (`\\n`):** cuando el `old_string` contiene caracteres que el sistema interpreta como escapes, el resultado del patch puede tener `\\n` literales en vez de saltos de línea reales. Verificar siempre con `read_file` post-patch que las líneas están correctamente formateadas. Si ocurre, reemplazar con `patch` usando el string literal `\\\\n` como `old_string` y el texto formateado correctamente como `new_string`.
- **terran-auditor.py `max_issues_per_phase=20` es insuficiente:** la fase 06 (seguridad) acumuló 36 issues. El límite no previene acumulación, solo es informativo. Subir a **50+** en la config. Ver skill `terran-schema-fix` sección "Paso 0: Verificar configuración del auditor".

- **terran-auditor.py `log-issue` JSON encoding:** el script usa `sys.argv[3]` con `json.loads()` — no acepta comillas simples dentro del JSON. **Siempre usar `execute_code` con `subprocess.run()`** para construir el JSON en Python y pasarlo como string. Ver skill `terral-architecture` referencia `terran-audit-setup.md`.

## Human Loop — Sistema de Control

Cuando la tarea es crítica (cambios >5 archivos, decisiones de diseño/arquitectura, deploy a producción), Mastermind ejecuta este patrón:

```
1. PLANIFICAR → presentar plan al humano
2. ESPERAR → ✅ o feedback del humano
3. IMPLEMENTAR → ejecutar con diffs visibles
4. ESPERAR → ✅ o feedback del humano
5. SINTEZAR → presentar resultado final
6. ESPERAR → ✅ para archivar
```

**Reglas del Human Loop:**
- **Nunca silenciar** — terminar una fase, presentar resultado, empezar siguiente inmediatamente sin preguntar
- **Máximo 2 reintentos** por fase — si falla, escalar al humano
- **Cambios críticos** (>5 archivos o arquitectura) → mostrar diffs antes de commit
- **Decisión de diseño** → siempre preguntar, nunca decidir en silencio (ya existe regla en SOUL.md)
- **Archivado** → solo con ✅ humano (ya existe en SOUL.md)

**Cuándo aplicar Human Loop:**
- Cambios en >5 archivos
- Decisiones de arquitectura o diseño
- Deploy a producción (NaN, GitHub Pages, Vercel)
- Migraciones o reestructuraciones
- Cualquier cosa que el humano considere "crítica"

**Cuándo NO aplicar Human Loop:**
- Tareas simples (1-3 tool calls)
- Lectura/exploración sin modificación
- Commits de mantenimiento rutinario
- Tareas mecánicas sin impacto estructural

## Aprendizaje

Después de tarea compleja (5+ tool calls):
- ¿Merece skill? → `skill_manage`
- ¿Merece nota? → `notes/YYYY-MM-DD-titulo.md`
- ¿Merece memoria? → `memory` tool

## Pitfalls (ampliación)

### Branches y fusión selectiva

- **NUNCA eliminar branches sin preguntar al humano** — aunque parezcan obsoletos, pueden tener contenido/diseño que el usuario prefiere
- **Branch merge directo no sirve con archivos comunes diferentes** — ver `github-workflow` sección 11 "Branch Merge Selectivo" para el patrón de fusión manual
- **Después de push, verificar GitHub-side artifacts** — el description del repo se actualiza vía API REST, no está en el repo. Escanear con `search_files` nombres de plataforma antigua en TODOS los archivos activos (excluyendo `legacy/`)
- **Branches remotos huérfanos** — si eliminas un branch local, comprobar si sigue en remoto. Si el usuario dice "master está mejor" y resulta que el branch remoto existe, recuperarlo de `origin/master`
- **Branch rename + Pages:** al cambiar master→main, actualizar workflow YAML + activar Pages via API PUT + dispatch workflow manualmente
- **No copiar el patrón Mastermind (11 agentes)** — fue diseñado para OpenCode+Obsidian. En Hermes, `delegate_task` nativo reemplaza todo. 1 orquestador + subagentes = suficiente.
- **No omitir checkpoints humanos** — en cambios >5 archivos, decisiones de arquitectura o deploy, siempre presentar diffs/plan y esperar ✅ antes de ejecutar. Ver sección "Human Loop" abajo.
- **Migraciones de plataforma:** cuando migres un proyecto a otra plataforma (Obsidian→GitHub, OpenCode→Hermes, etc.), SIEMPRE hacer un escaneo post-migración con `search_files` buscando nombres de la plataforma antigua en TODOS los archivos activos (excluyendo `legacy/`). Ver skill `system-audit` sección "Post-Migration Cleanup Execution".

### Cleanup y poda de legacy

- **Analizar antes de eliminar** — clasificar archivos en personales, mixtos y genéricos. Siempre presentar análisis al humano con tablas
- **Human loop en cleanup** — cambios >5 archivos requieren presentar plan → esperar ✅ → ejecutar
- **Siempre mantener patrones genéricos** — los skills que son patrones universales (flujo adaptativo, critical adversarial, etc.) tienen valor más allá de tu infraestructura
- **GitHub description del repo puede tener ruido legacy** — si el repo tiene description que referencia la plataforma antigua, actualizarlo vía API REST: `PATCH /repos/{owner}/{repo}` con `{"description": "nuevo texto"}`

### Verificación post-cambio

- **Después de reescribir README o index.html** — verificar que no hay URLs rotas ni enlaces a archivos eliminados
- **CDN Aurora** → siempre `@latest`, NUNCA `@master`. Error común: dejar `@master` después de merge
- **Si el repo tiene learning-platform** — asegurar que `vercel.json` existe si se va a deployar en Vercel

## Estado de implementación (2026-06-10)

| Componente | Estado | Evidence |
|---|---|---|
| **ChromaDB search** | ✅ OPERATIVO | 192 skills indexados, consultar-skills.py funcional, integrado en SOUL.md como flujo obligatorio |
| **Complexity-based delegation** | ✅ OPERATIVO | Niveles 1-4 documentados, delegate_task nativo, patrones de uso comprobados |
| **Human loop** | ✅ OPERATIVO | Checkpoints en SOUL.md, implementado en flujos reales |
| **Memory decay (Ebbinghaus)** | ⚡ SCRIPT EXISTE, NO INTEGRADO | Script `ebinghaus-decay.py` en scripts/, genera informes JSON en learning/, pero Mastermind NO lo consulta antes de cargar skills. Pendiente de integrar en SOUL.md como paso obligatorio. |
| **Knowledge graph** | ⚡ SCRIPT EXISTE, NO INTEGRADO | Script `knowledge-graph.py` genera grafos de conexiones entre skills, pero Mastermind no lo consulta como herramienta. Pendiente de crear `consultar-grafo.py` e integrar en flujo. |
| **Skill lifecycle** | ⚡ SCRIPT EXISTE, NO INTEGRADO | Script `skill-lifecycle.py` re-prioriza skills por uso, pero no se ejecuta automáticamente. Pendiente de integrar en cron semanal. |
| **Delegation flows (scripts)** | ✅ OPERATIVO | Scripts de clasificación de complejidad: `scripts/delegation-flows.py` con heurísticas y `classify_task()` |
| **Mastermind dashboard** | ✅ OPERATIVO (estático) | HTML interactivo de estado del sistema en `dashboard/mastermind-status.html`. Pendiente de convertir en generación dinámica con datos reales. |

**Regla:** Los componentes en 📋 DISEÑO NO están implementados. No asumir que existen scripts o funcionalidad para ellos. Si un usuario pregunta por memory decay, explicar el diseño pero no buscar código que no existe.

## Referencias

- SOUL.md → Identidad de Mastermind y lista de subagentes
- `human-loop-control` → Sistema de control y human loop
- `subagent-driven-development` → Workflow detallado para dev con 2-stage review
- `delegar-no-comprimir` → Cuándo delegar vs comprimir
- `micro-crons-pipeline` → Pipeline de producción iterativa con cron jobs para proyectos grandes (backlog + cron maestro + scripts de inicialización)
- `system-audit` → Procedimiento para auditar repositorios de sistemas multi-agente (arquitectura, memoria, flujos, portabilidad, tokens, seguridad)
- Repo antiguo (legacy): https://github.com/Ntizar/NtizarBrainMasterMind (solo referencia histórica, no modificar)
- `github-workflow` → Flujo completo de GitHub: autenticación, PR lifecycle, deploy Pages, branch rename
- `scripts/delegation-flows.py` → Script de clasificación de complejidad (referencia ejecutable)
