---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 0: Pre-Implementation Audit

**BEFORE any changes, run automated checks to validate the current state.** This prevents introducing new bugs and identifies real issues vs. perceived ones.

### 1. Syntax Validation

Check all modified files for syntax errors before making changes:

```bash
# Node.js
node -c server.js

# Python
python3 -m py_compile module.py

# JS/HTML (basic brace check)
python3 -c "c=open('dashboard.html').read(); print('OK' if c.count('{')==c.count('}') else 'MISMATCH')"
```

### 2. Variable Scope Analysis

For JavaScript/TypeScript files, check for:
- Undefined variables used in expressions (e.g., `perfil && perfil.altura_cm` when `perfil` is never declared in scope)
- `const charts` vs `var charts = window.charts = {}` (must use `var` for Chart.js instances)
- Mismatched function parameter names (e.g., function takes `objHidr` but caller passes `objetivoHidr`)
- Missing variable declarations in closures/lambdas

```python
# Check for undefined variable usage in a function scope
import re
with open('file.js', 'r') as f:
    content = f.read()

# Find function scope and check for used-but-undefined vars
# Look for patterns like `var && var.` where `var` is not declared with `var` in scope
```

### 3. Field Name Consistency

Check that frontend field names match backend expectations:

```bash
# Find all references to a field name
grep -rn "objetivo_peso_kg" dashboard.html server.js
grep -rn "peso_objetivo_kg" dashboard.html server.js
# If frontend uses X and backend expects Y → BUG
```

### 4. API Endpoint Verification

Verify all API endpoints called from frontend exist in backend:

```bash
# Extract all API calls from frontend
grep -oP "api\(['\"](/api/\S+)" dashboard.html | sort -u
# Compare with backend routes
grep -oP "app\.(get|post|put|delete)\(['\"](/api/\S+)" server.js | sort -u
```

### 5. Chart.js Memory Management

Check that charts are properly destroyed before recreation:

```bash
# Count chart destroy calls vs. new Chart calls
grep -c "\.destroy()" dashboard.html
grep -c "new Chart(" dashboard.html
# Should be equal or destroy > new (for safety)
```

### 6. XSS Risk Assessment

For files using `innerHTML`, check that user input is escaped:

```bash
# Count innerHTML assignments
grep -c "innerHTML =" dashboard.html
# Verify escape functions exist and are used
grep -c "escapeHtml" dashboard.html
grep -c "formatMarkdown" dashboard.html
```

### Phase 0 Completion Checklist

- [ ] Syntax validation passed for all files
- [ ] Variable scope checked (no undefined vars in scope)
- [ ] Field names match between frontend and backend
- [ ] All API endpoints verified
- [ ] Chart.js memory management checked
- [ ] XSS risk assessed (user input escaped)
- [ ] Known bugs documented before fixing

**STOP:** Do not proceed to Phase 1 until Phase 0 is complete. This phase takes 2-5 minutes but prevents 80% of "fixes that introduce new bugs."

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, not fix again. |

## Async-Specific Pitfalls

### Async infinite recursion ≠ stack overflow (harder to catch)

Async recursion doesn't stack overflow the same way sync does — the event loop unwinds between awaits. This makes it INVISIBLE in local testing yet deadly in production:

- **Symptom**: Container restarts silently (OOM kill), "no available server", not reproducible locally
- **Root cause**: Function A calls A internally with a shifted parameter (e.g., `buildSummary(today)` → `buildSummary(yesterday)` → `buildSummary(tomorrow)`...) without a base case. Each "recursive" call leaks memory (pending HTTP requests, unresolved promises, response buffers) until the process hits the RAM limit.
- **Why local testing misses it**: Local dev has abundant RAM + open file handles. The recursion eventually hits a date with no API data (returns null → error → terminates). On production with cached data, every date succeeds → infinite chain.
- **Fix**: Never let function A call function A (directly or indirectly) unless you have a hard depth limit. Replace with targeted single-call fetches.

**Detection trick**: If you see `const data = await buildSummary(ayer, token)` inside function `buildSummary(...)` — that's the bug. The call chain is `buildSummary(d)` → `buildSummary(d-1)` → `buildSummary(d-2)` → ... with no termination.

### Event loop starvation por concurrencia HTTP en servidores de 1 vCPU

Cuando un servidor tiene 1 vCPU (NaN free, contenedores pequeños, VPS baratos), **múltiples llamadas HTTP simultáneas pueden colapsar el event loop de Node.js**:

- **Síntoma**: El servidor responde a `/healthz` (es síncrono) pero un endpoint que hace fetch a APIs externas devuelve 502 o se queda colgado eternamente. En el frontend, el spinner de carga nunca se libera.
- **Causa**: `Promise.all()` con N llamadas HTTP simultáneas bloquea el event loop de Node.js (single-threaded). Cada petición HTTP requiere parsing de headers, parsing de JSON, escritura de cache en disco — todo compite por el único CPU.
- **Por qué falla en producción pero no local**: Localmente hay más RAM/CPU y el cache en disco es rápido. En producción con 1 vCPU, el event loop se satura y ni siquiera los `setTimeout` del timeout se disparan (porque `setTimeout` también necesita el event loop).
- **Por qué el timeout de 30s no funciona**: Si el event loop está bloqueado, el timer de 30s nunca se ejecuta. El `Promise.race` queda colgado eternamente.
- **Diagnóstico**: Si `/healthz` funciona pero `/api/endpoint-que-hace-fetch` devuelve 502 → el servidor está vivo pero el event loop está colapsado.
- **Fix**: Reducir concurrencia. En vez de `Promise.all(batches.map(fetch))`, usar un bucle con batches de tamaño limitado:

```javascript
// ❌ MALO — 4 batches en paralelo = 32 llamadas simultáneas
const results = await Promise.all(batches.map(batch => fetchBatch(batch)));

// ✅ BUENO — max 2 batches simultáneos
const CONCURRENCY = 2;
for (let i = 0; i < batches.length; i += CONCURRENCY) {
  const slice = batches.slice(i, i + CONCURRENCY);
  const results = await Promise.all(slice.map(batch => fetchBatch(batch)));
  Object.assign(allData, ...results);
}
```

- **Prevención**: En servidores de 1 vCPU, NUNCA hacer más de 2-3 llamadas HTTP simultáneas. Usar batching (múltiples indicadores en 1 request) + concurrencia limitada.

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

## Algorithmic Pitfalls — Bugs que no son bugs de lógica

### Levenshtein swap optimization bug (O(min(m,n)) space)

**Síntoma:** Distancia de Levenshtein incorrecta cuando las dos cadenas tienen longitudes diferentes. Ejemplo: `levenshtein('adla', 'adela')` devuelve 3 en vez de 1.

**Causa raíz:** En la optimización de dos filas, cuando `m < n` se hace swap de `fuente` y `objetivo`, pero el loop exterior itera hasta `lenA` (longitud mayor) mientras que `fuente` tiene longitud `lenB` (menor). Esto causa acceso fuera de límites en `fuente[i-1]` cuando `i > lenB`.

**Patrón incorrecto:**
```typescript
const swap = m < n
const fuente = swap ? b : a        // fuente = más corto si m < n
const objetivo = swap ? a : b       // objetivo = más largo si m < n

for (let i = 1; i <= lenA; i++) {  // lenA = max(m,n) = longitud del más largo
  for (let j = 1; j <= lenB; j++) {
    const costo = objetivo[i - 1] === fuente[j - 1] ? 0 : 1
    // ❌ objetivo[i-1] out-of-bounds cuando i > lenB
    // ❌ fuente[j-1] out-of-bounds cuando j > lenA (imposible por loop)
  }
}
```

**Patrón correcto:**
```typescript
const lenA = Math.max(m, n)  // longitud del más largo
const lenB = Math.min(m, n)  // longitud del más corto

// fuente = string más largo (iterado con i), objetivo = más corto (iterado con j)
const fuente = m >= n ? a : b
const objetivo = m >= n ? b : a

for (let i = 1; i <= lenA; i++) {  // recorre el string más largo
  for (let j = 1; j <= lenB; j++) {  // recorre el string más corto
    const costo = objetivo[j - 1] === fuente[i - 1] ? 0 : 1
    // ✅ i-1 < lenA = fuente.length, j-1 < lenB = objetivo.length
  }
}
```

**Regla mnemotécnica:** `fuente` es el string que se recorre en el loop exterior (más largo), `objetivo` es el string que se recorre en el loop interior (más corto). El costo se compara `objetivo[j-1]` vs `fuente[i-1]`.

**Verificación rápida:** Si `levenshtein('a', 'abc')` devuelve 3 en vez de 2, tienes este bug.

### Stemming agresivo y tests

**Síntoma:** Tests fallan porque el stemming produce raíces inesperadas. Ejemplo: `'hola'` stemmado a `'hol'` (se quita `-a`).

**Causa:** El stemming básico suele ser agresivo (strips `-a`, `-o`, `-es`, `-s`). Los tests que asumen "no stemming" fallan sistemáticamente.

**Solución:** Los tests de fuzzy matching deben verificar la raíz stemmed, no el token original. Siempre verificar con `console.log(stemmingBasico('palabra'))` antes de escribir assertions.

### Coincidencia parcial y distancia Levenshtein

**Síntoma:** `coincideParcial('catl', 'cataluña', 2)` devuelve false.

**Causa:** La distancia Levenshtein entre cadenas de longitudes muy diferentes es siempre grande. `catl` (4 chars) vs `cataluña` (8 chars) tiene distancia 4, no 2.

**Regla:** Para `coincideParcial`, la distancia máxima debe ser razonable respecto a la diferencia de longitudes. `distancia >= |a.length - b.length|` siempre. Si la distancia especificada es menor que la diferencia de longitudes, la coincidencia SIEMPRE fallará.

### extraerFragmento y ellipsis

**Síntoma:** Tests esperan que `extraerFragmento('Hola mundo', 0, 4)` devuelva `'Hola'` sin ellipsis.

**Causa:** La función añade ellipsis cuando `inicio > 0` (leading) O cuando `fin < texto.length` (trailing). Si el fragmento no llega al final del texto, SIEMPRE hay ellipsis trailing.

**Regla:** Verificar las condiciones exactas de la implementación antes de escribir tests. La intuición ("si empiezo en 0 no necesita ellipsis") no siempre coincide con la implementación.

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**

## Patch Safety — Pitfall Crítico con `skill_manage(action='patch')`

Cuando se parchea un archivo HTML/JS grande (>100KB) con `skill_manage(action='patch')` o `patch()`:

### El problema

La herramienta usa **fuzzy matching** por texto. Si el `old_string` coincide con un bloque similar pero equivocado, el patch se aplica al bloque incorrecto **sin error**. Esto corrompe funciones adyacentes silenciosamente.

### Caso real (2026-06-12, dieta-masterfit)

Un patch intentó reemplazar el cuerpo de `registrarDeporte` (función de ejercicio) pero el fuzzy match coincidió con el bloque de `registrarPasos` (función de pasos). Resultado:
- `registrarDeporte` ahora contenía código de pasos → el formulario de ejercicio enviaba datos incorrectos
- `registrarPasos` desapareció del archivo → el formulario de pasos fallaba al submit (onsubmit llamaba a función inexistente)
- **Ningún error de sintaxis** — el código era válido pero semánticamente roto

### Reglas de seguridad

1. **NUNCA parchear sin leer el contexto antes y después del old_string** — siempre verificar con `read_file` que el bloque a reemplazar es exactamente el correcto
2. **Incluir contexto suficiente en `old_string`** — al menos 3-5 líneas de código real, no solo el nombre de la función. Incluir el comentario anterior y las líneas de cierre del bloque
3. **Después de cada patch en HTML/JS grande, validar con `node -c` y `grep`/`search_files`** — verificar que las funciones clave siguen existiendo y que los braces están balanceados
4. **Si el fuzzy match podría coincidir con múltiples bloques, usar `replace_all=false` (default) y verificar que solo se modificó el bloque esperado**
5. **Para archivos >100KB, preferir `write_file` con el contenido completo** si el patch requiere cambios en múltiples bloques dispersos — es más seguro que múltiples patches individuales

### Verificación post-patch

```bash
# Validar JS
node -c server.js

# Verificar funciones clave existen
grep -c "function registrarPasos" dashboard.html
grep -c "function registrarDeporte" dashboard.html

# Verificar braces balanceados
python3 -c "c=open('dashboard.html').read(); print('OK' if c.count('{')==c.count('}') else 'MISMATCH')"

# Verificar que no hay duplicados de event listeners
grep -c "tab.addEventListener('click'" dashboard.html
```

## Deep Audit Pattern — NO PARES EN EL PRIMER FIX

**Pitfall crítico (2026-06-14, MasterFit v4):** El usuario dice "no funciona". Encuentras el brace faltante, lo parcheas, verificas que compila, y le dices "arreglado". El usuario prueba y sigue sin funcionar.

### Por qué pasa
Los bugs fáciles de encontrar (braces, syntax) son SÍNTOMAS de un código con deuda técnica. Si hay un brace roto, probablemente haya más bugs debajo. **El primer fix visible no es el fix completo.**

### Flujo correcto
```
1. Fix obvio (braces, syntax) → commit
2. NO decir "arreglado" todavía
3. Auditar todo el proyecto ANTES de declarar victoria:
   - Syntax check (node -c, brace balance)
   - Variable scope (undefined vars en funciones)
   - API mismatch (frontend vs backend routes)
   - Error handling (JSON.parse sin try-catch)
   - Security (XSS, SQL injection)
   - Delete/update flows (singular vs plural, column names)
4. delegate_task para deep audit si el proyecto tiene >500 líneas
5. FIX ALL bugs found, commit together
6. THEN say "arreglado"
```

### delegate_task para deep audit
Cuando el proyecto es complejo (>500 líneas, multi-archivo), delegar la auditoría completa a un subagente:

```python
delegate_task(
    goal="Full audit of [project] — find ALL bugs in frontend and backend",
    context="""
    Check for: syntax errors, brace balance, API mismatches (frontend calls vs backend routes),
    undefined variables in function scope, missing error handling, XSS, SQL injection,
    delete/update flow mismatches (singular vs plural), Chart.js memory management.
    Return structured list with line numbers and severity.
    """,
    toolsets=['terminal', 'file']
)
```

**Resultado real:** Auditoría manual encontró 2 bugs. delegate_task encontró 12 (3 críticos, 2 altos, 3 medios, 4 bajos).

## Referencias

- `references/es-module-silent-failure.md` — **NUEVO** Patrón de fallo silencioso de ES modules: una sola importación con nombre incorrecto (case mismatch, función renombrada) hace que **todo el árbol de módulos falle sin mensaje de error visible**. Síntoma: la página carga pero nada funciona. Diagnóstico: verificar cada import contra su export real.
- `references/levenshtein-swap-bug.md` — Caso de estudio: bug en la optimización de dos filas de Levenshtein
- `references/event-loop-starvation-nan.md` — caso de estudio: colapso de event loop por 32 llamadas HTTP simultáneas en servidor NaN de 1 vCPU
- `references/pre-implementation-audit-masterfit-v4.md` — caso real: Phase 0 audit que encontró 2 bugs (variable scope + field name mismatch) antes de implementar features
- `references/masterfit-v4-full-audit.md` — caso real: auditoría completa que encontró 12 bugs tras fix inicial insuficiente
