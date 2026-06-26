---
name: delegar-no-comprimir
version: "1.0.0"
description: Patrón para delegar tareas en subagentes en paralelo en vez de hacer compresiones de contexto con secuencias largas de herramientas
tags: [software-development, delegation, subagents, context]

---

# Delegar, no comprimir

## Cuándo delegar
Cuando la tarea implica **3+ archivos independientes** o **3+ cambios en paralelo**:
- Optimización frontend (JS + CSS + HTML)
- Backend + frontend + tests
- Múltiples endpoints de API
- Refactor de módulo con dependencias separadas
- **Creación de ecosistema de módulos** (3+ módulos independientes con mismo patrón)

## Cuándo NO delegar
- Cambios en 1-2 archivos relacionados
- Tareas cortas (< 5 min de ejecución)
- Depuración interactiva (requiere feedback en tiempo real)
- El usuario pide cambios directos
- Tareas con dependencias que requieren contexto compartido entre subagentes

## Patrón general
1. **Explorar** (yo) → identificar archivos afectados
2. **Planificar** (yo) → dividir en subtareas independientes
3. **Delegar** (`delegate_task` con `tasks: [...]`) → 2-3 subagentes en paralelo
4. **Integrar** (yo) → unificar, verificar, commit

---

## Patrón: Creación de ecosistema de módulos

**Cuándo usar:** 3+ módulos independientes (ej: paquetes npm, skills, microservicios) que comparten el mismo patrón estructural y de calidad.

**Estructura del prompt para cada subagente:**

Cada prompt debe incluir SIEMPRE:

1. **Estructura exacta de archivos** — Lista completa de archivos a crear (package.json, tsconfig, src/, tests/, README.md, dist/)
2. **Código fuente de referencia** — Qué archivos leer como fuente (ruta exacta)
3. **API/Interfaz a exponer** — Types, funciones, clases con firma completa
4. **Requisitos de calidad:** TypeScript strict, zero deps (si aplica), TODO en castellano
5. **Comandos de verificación:** npm test y npm run build al final

**Estructura típica de cada módulo:**
```
modulo/
├── README.md           # Quick start + API + "Integración con otros módulos"
├── package.json        # name: "adela-modulo", version: "1.0.0", type: "module"
├── tsconfig.json       # strict mode, ES2022, declarations + sourceMap
├── .gitignore          # node_modules/ y dist/
├── src/
│   ├── index.ts        # Barrel export (NO default exports)
│   ├── modulo.ts       # Implementación principal
│   └── types.ts        # Interfaces públicas
├── tests/
│   └── modulo.test.ts  # Tests con node:test+tsx o vitest
└── dist/               # Build output (generado)
```

**Pitfalls específicos de módulos TypeScript:**

- **tsconfig rootDir:** Si `rootDir: "."` con `include: ["src/**/*.ts", "tests/**/*.ts"]`, el build genera `dist/src/` y `dist/tests/`. Solución: `rootDir: "src"` y solo incluir `"src/**/*.ts"`.
- **package.json main/types paths:** Si `main: "dist/src/index.js"` pero el build genera `dist/index.js`, fallan los imports. Usar `main: "dist/index.js"`.
- **Test runner choice:** Si los tests usan `node:test` (describe/it de node), NO usar vitest. Usar `tsx --test tests/*.test.ts`. Vitest espera su propia API de test.
- **Timeout en subagentes con dependencias:** Módulos con dependencias reales (bcryptjs jsonwebtoken sql.js) pueden timeout (~10 min) porque npm install + compilación + tests toma más. Para estos módulos: o aumentar timeout, o hacer directo sin delegar.

**Flujo completo:**

```
1. MASTERMIND: Define estructura común (template de cada módulo)
2. MASTERMIND: Divide en N módulos independientes (sin dependencias entre sí)
3. MASTERMIND: Crea prompts autocontenidos para cada uno
4. DELEGAR: delegate_task con tasks: [modulo1, modulo2, modulo3] en paralelo
5. SUBAGENTES: Cada uno lee código fuente, escribe módulo, build, test
6. MASTERMIND: Verifica resultados (npm test + npm run build en cada uno)
7. MASTERMIND: Fix errores comunes (tsconfig, package.json paths, etc.)
8. MASTERMIND: Push a GitHub (o commit)
```

---

## Patrón: Push a GitHub

Cuando hay que crear repos y pushear código vía API:

1. Crear `.gitignore` con `node_modules/` y `dist/`
2. Crear repo vía API REST:
   ```
   curl -s -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     -d '{"name":"RepoName","description":"...","private":false}' \
     https://api.github.com/user/repos
   ```
3. git init → add → commit → branch -M main
4. git remote add + push (usar token en URL: `https://user:token@github.com/user/repo.git`)
5. Verificar con curl GET al repo

---

## Patrón: Batch Analysis de items independientes

**Cuándo usar:** Hay 10+ items (repos de GitHub, etc.) que necesitan análisis/clasificación (no ejecución) y cada uno produce un veredicto independiente.

**NUNCA usar:** para construcción de código, creación de módulos o features — para eso está el Ecosystem Module Factory.

**Solo para:** análisis, clasificación, decisiones de skill.

**Flujo:**
1. Registro rápido (solo GET /repos/{name} sin README/tree) — ~0.3s/repo
2. Clasificación por valor: High (>3000⭐) → batch AHORA; Medium (500-3000) → cron; Low (<500) → skip
3. 3 subagentes × 6 items = 18 en ~5 min (vs 1h en serie)
4. Agregar outputs, actualizar registry, crear skills si aplica

**Pitfalls:**
- Los subagentes no tienen memoria del chat → dar contexto COMPLETO de cada item
- ChromaDB dedup: cada subagente debe checkear antes de crear skill (score > 0.25 = skip)
- No `--all` en scripts con 100+ items (timeout). Mejor registro rápido + procesar en batches
- Awesome lists / Clone-Wars → skip siempre sin análisis

## Errores a evitar generales
- ❌ Compresión de contexto como sustituto de paralelismo
- ❌ Hacer 30+ llamadas de tool en secuencia cuando podrían ser 3 en paralelo
- ❌ Delegar tareas que requieren contexto compartido (el subagente no lo tiene)
- ❌ No delegar cuando los cambios son independientes
- ❌ Delegar tareas con dependencias npm pesadas (bcrypt, sql.js) sin aumentar timeout
- ❌ No verificar npm test + npm run build post-delegación
- ❌ No fijar rootDir en tsconfig de módulos → dist/src/ en vez de dist/
- ❌ Sibling file conflicts entre subagentes — Cuando 2+ subagentes trabajan en módulos con responsabilidades solapadas (ej: dos implementaciones de DB adapter en el mismo directorio), pueden crear archivos duplicados que rompen tests y compilación. **Siempre verificar que NO hay archivos extra** (`src/*.ts`, `tests/*.test.ts`) de otros subagentes antes de dar por terminado.
- ❌ No limpiar archivos huérfanos post-delegación — Tras paralelizar, revisar que cada módulo tenga EXACTAMENTE los archivos esperados. Eliminar sobrantes de otros subagentes.

## Linked Files

- `references/ecosystem-module-creation.md` — Caso real: creación del ecosistema Adela (6 módulos en paralelo) con prompts exactos, errores encontrados y soluciones
