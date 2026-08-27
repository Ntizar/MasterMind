---
name: safe-refactoring-checklist
description: >
  Procedimiento seguro para auditar y refactorizar proyectos existentes sin romperlos.
  Capturado del incidente MasterFit v3 donde la extracción de JS a archivo separado
  eliminó los CDN de Chart.js y Three.js, rompiendo todo el dashboard.
trigger: When user asks to audit, refactor, or modernize an existing working project.
version: 1.0.0
---

# Safe Refactoring Checklist

## Contexto

Proyectos que **ya funcionan** y el usuario no quiere romper. La regla de oro:
**Primero no romper, luego mejorar.**

## El Incidente MasterFit (lección vivida)

Se extrajo JS inline a archivo separado (`dashboard.js`). El JS usaba `Chart` y `THREE`
pero los `<script src="cdn...">` de Chart.js y Three.js se quedaron en el HTML original
y **no se copiaron** al reestructurar. Resultado: el dashboard mostraba "Error cargando
datos" porque `new Chart()` fallaba silenciosamente y el `.catch()` lo capturaba.

**Causa raíz:** Dependencias externas olvidadas durante la reestructuración.

## Flujo obligatorio (5 fases)

### Fase 0: Snapshot del estado actual
```bash
# Verificar que funciona ANTES de tocar nada
curl -s URL | head -20        # Verificar HTML
curl -s URL/data/database.json | python3 -m json.tool | head -5  # API OK
# Tomar screenshot del dashboard funcional (browser_vision)
```

### Fase 1: Inventario de dependencias
**ANTES de mover cualquier código**, identificar TODAS las dependencias:

```bash
# CDN scripts en HTML
grep -i 'script.*src.*cdn' dashboard.html

# Librerías globales usadas en JS
grep -oP '\bnew\s+(Chart|THREE|Map|Set|Promise)\b' dashboard.js | sort -u
grep -oP '\b(Chart|THREE|axios|fetch|d3)\.' dashboard.js | sort -u

# CSS externos
grep -i 'link.*href.*cdn' dashboard.html

# Imports si es ES modules
grep -oP "from ['\"]([^'\"]+)['\"]" dashboard.js
```

**Crear lista explícita de dependencias:**
```
Dependencias del proyecto:
- chart.js@4.4.7 (CDN) → usado en: renderPesoChart, renderKcalChart, etc.
- three@0.160.0 (CDN) → usado en: initScene, renderHuman3D
- Ntizar-Aurora@latest (CDN CSS) → 8 archivos CSS
```

### Fase 2: Cambio最小 y verificado
Hacer UN solo tipo de cambio a la vez:

1. **Extraer JS a archivo separado** → commit → verificar
2. **var→const/let** → commit → verificar
3. **Arrow functions** → commit → verificar
4. **Element caching** → commit → verificar

**NUNCA** hacer múltiples cambios en un solo commit.

### Fase 3: Verificación post-cambio
```bash
# Syntax check
node --check extracted.js

# Verificar que las dependencias siguen accesibles
# Si el JS está en archivo separado, ¿siguen los CDN en el HTML?
grep 'chart.js' index.html  # ← DEBE aparecer
grep 'three' index.html     # ← DEBE aparecer

# Deploy + curl verify
curl -s URL | grep -c 'chart.js'  # debe ser > 0
curl -s URL | grep -c 'getElementById'  # debe coincidir con el JS

# Browser test
# browser_navigate → browser_vision → verificar que todo carga
```

### Fase 4: Rollback si falla
```bash
# Si algo roto, volver al último commit funcional
git log --oneline -5  # identificar el último OK
git revert HEAD       # revert del último commit
git push              # NaN redeploy automático
```

## Pitfalls conocidos

### 1. CDN olvidados (el incidente real)
**Síntoma:** "Error cargando datos" o gráficos vacíos
**Causa:** `<script src="cdn...">` en el HTML original no se migra al reestructurar
**Prevención:** Inventario de dependencias en Fase 1

### 2. Cloudflare cache en NaN
**Síntoma:** curl muestra el HTML nuevo pero el navegador ejecuta el viejo
**Causa:** `cache-control: public, max-age=14400` (4 horas)
**Solución:** Inline JS (cero cache) o `?v=timestamp` (parcial)
**NaN usa Cloudflare:** Siempre verificar con curl PRIMERO, luego browser

### 3. const→let para acumuladores
**Síntoma:** `TypeError: Assignment to constant variable`
**Causa:** Variables con `+=` dentro de loops declaradas como `const`
**Pattern de búsqueda:**
```bash
# Buscar const + += en el mismo scope
grep -n 'const.*=' dashboard.js | head -20
# Luego verificar si alguna usa += dentro de un loop
```
**Regla:** Si una variable usa `+=`, `-=`, `*=`, `/=`, `|=`, `^=` → debe ser `let`

### 4. Script en <head> sin DOM
**Síntoma:** `getElementById` retorna `null`, todo es `undefined`
**Causa:** Script ejecuta antes de que el navegador parsee el DOM
**Solución:** `<script>` al final de `</body>`, o `DOMContentLoaded`

### 5. .catch() engañoso
**Síntoma:** Muestra "error" pero la API funciona
**Causa:** `.catch()` captura errores de RENDERIZADO, no solo de red
```javascript
// MAL: catch captura errores de renderDashboard()
fetch('/api').then(r => r.json()).then(db => renderDashboard(db))
  .catch(() => showError())  // ← catchea TODO

// BIEN: separar errores de red y render
fetch('/api').then(r => r.json())
  .then(db => renderDashboard(db))
  .catch(err => {
    console.error('Render error:', err);  // ← log específico
    showError();
  });
```

### 6. Múltiples llamadas a loadData()
**Síntoma:** Error aparece y desaparece, datos parciales
**Causa:** `loadData()` en script bottom + `setTimeout(loadData, 500)` + `setHoraMadrid()`
**Solución:** Debounce o flag `let loading = false`

## Checklist rápido (pegar en PR)

```
- [ ] Inventario de dependencias externas (CDN, imports)
- [ ] Verificar que los CDN siguen en el HTML tras reestructurar
- [ ] node --check JS sin errores de syntax
- [ ] const→let para todas las variables con += o -=
- [ ] Script al final de </body> o en DOMContentLoaded
- [ ] Deploy a NaN + curl verify (no solo browser por cache)
- [ ] browser_vision: todos los charts/KPIs muestran datos
- [ ] Sin mensajes de error en consola del navegador
```
