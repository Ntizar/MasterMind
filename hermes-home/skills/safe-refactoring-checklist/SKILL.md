---
name: safe-refactoring-checklist
description: >
  Procedimiento seguro para auditar y refactorizar proyectos existentes sin romperlos.
  Capturado del incidente MasterFit v3 donde la extracción de JS a archivo separado
  eliminó los CDN de Chart.js y Three.js, rompiendo todo el dashboard.
trigger: When user asks to audit, refactor, or modernize an existing working project.
version: 1.1.0
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

### 7. Arrow function `this` roto (el incidente MasterFit #2)
**Síntoma:** Tab/función no carga, `undefined` en atributos, eventos que no disparan
**Causa:** `function` → arrow function `() => {}` en event listeners que usaban `this` para referenciar el elemento clicado
```javascript
// MAL — this es window, no el tab
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const name = this.getAttribute('data-tab'); // ← this = window
  });
});

// BIEN — usar la variable del closure
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const name = tab.getAttribute('data-tab'); // ← tab del closure
  });
});

// BIEN — o usar event parameter
tabs.forEach((tab) => {
  tab.addEventListener('click', (e) => {
    const name = e.currentTarget.getAttribute('data-tab');
  });
});
```
**Regla:** Si conviertes `function` a `() =>` en un event handler, busca `this.` dentro del body. Los arrow functions NO tienen `this` propio — heredan del scope exterior.
**Detección automática:**
```bash
# Buscar arrow functions que usen 'this'
grep -n '=> {' dashboard.js | head -20
# Para cada uno, verificar si el body usa 'this.'
```

### 8. DB sync entre dispositivos (localStorage ≠ servidor)
**Síntoma:** Datos registrados en un dispositivo no aparecen en otro
**Causa:** Estado guardado solo en `localStorage` (específico del navegador)
**Solución:** Migrar a API REST en servidor + persistencia en DB
```javascript
// MAL — solo funciona en este navegador
localStorage.setItem('mf_water_' + today, count);

// BIEN — sync entre dispositivos
fetch('/api/agua', { method: 'POST', body: JSON.stringify({ ml: 250 }) })
  .then(() => fetch('/api/agua?fecha=' + today))  // recargar desde servidor
  .then(r => r.json())
  .then(data => updateUI(data.registros));
```
**Checklist de migración localStorage → API:**
1. Crear endpoints GET/POST/DELETE en server.js
2. Añadir tipo a `allowedTypes` en endpoints genéricos de borrado
3. Reemplazar `localStorage.getItem/setItem` por `fetch` a API
4. Recargar datos desde servidor después de cada escritura
5. Añadir botón de borrado (el usuario lo pide siempre)

## Checklist rápido (pegar en PR)

```
- [ ] Inventario de dependencias externas (CDN, imports)
- [ ] Verificar que los CDN siguen en el HTML tras reestructurar
- [ ] node --check JS sin errores de syntax
- [ ] const→let para todas las variables con += o -=
- [ ] Arrow functions: buscar `this.` dentro de callbacks → reemplazar por variable del closure o e.currentTarget
- [ ] Script al final de </body> o en DOMContentLoaded
- [ ] Deploy a NaN + curl verify (no solo browser por cache)
- [ ] browser_vision: todos los charts/KPIs muestran datos
- [ ] Sin mensajes de error en consola del navegador
- [ ] Si se migró localStorage → API: verificar sync entre dispositivos
```

### 9. Regex ciego sobre HTML destruye estructura (MasterFit 2026-06-13)

**Síntoma:** Tabs sin `display:none` (todos visibles), funciones JS eliminadas, botones desaparecidos, `</div>` desbalanceados.

**Causa:** Usar `re.sub()` con regexs amplios sobre HTML inline (CSS + JS + HTML en un solo archivo) como `dashboard.html`. Los regexs que buscan patrones como `try { if(localStorage...` o bloques entre llaves `{...}` pueden coincidir accidentalmente con código dentro de strings JS, atributos HTML, o bloques CSS que contienen estructuras similares.

**Patrones de riesgo:**
- Regex que busca `{...}` o `try { ... }` — puede coincidir con strings JS que contienen `{...}`
- Regex que busca bloques entre llaves — puede eliminar código JS completo que está dentro de un bloque coincidente
- Regex que busca `id="X"` y reemplaza — puede eliminar atributos `style="display:none"` adyacentes
- Regexs que buscan "todo lo que contiene X" — puede eliminar más de lo esperado

**Prevención obligatoria:**

1. **NUNCA usar `re.sub()` con regexs amplios sobre HTML inline.** Si necesitas eliminar un bloque:
   - Primero: `grep -n` para encontrar la línea exacta
   - Segundo: `patch` con `old_string`/`new_string` de texto EXACTO y único
   - Tercero: Si el texto no es único, incluir contexto suficiente (líneas anteriores/siguientes)

2. **Después de cualquier edición con `patch`/`re.sub`:**
   ```python
   # Verificar balance de divs
   open_divs = content.count('<div')
   close_divs = content.count('</div')
   assert open_divs == close_divs, f"Desbalance: {open_divs} vs {close_divs}"
   
   # Verificar elementos críticos existen
   assert 'display:none' in content  # tabs ocultos
   assert 'function switchTab' in content  # funciones JS
   assert 'toggleDarkMode' not in content  # código eliminado
   ```

3. **Para eliminar bloques grandes:** Preferir `patch` con texto EXACTO del bloque a eliminar, NO regex.

4. **Si el bloque a eliminar es grande (>50 líneas):** Extraerlo con `grep -n` + `sed` o editar línea por línea con `patch`.

**Detectar si un patch rompió algo:**
```python
# Verificar que los elementos críticos siguen existiendo
for term in ['display:none', 'function loadData', 'function renderDashboard', 'tab-resumen']:
    assert term in content, f"¡{term} eliminado por el patch!"

# Verificar que el código eliminado ya no existe
for term in ['toggleDarkMode', 'data-nz-theme', 'mf-dark']:
    assert term not in content, f"¡{term} aún presente!"
```

**Lección:** `patch` es seguro porque usa fuzzy matching de texto EXACTO. `re.sub()` es peligroso porque usa patrones que pueden coincidir con contenido inesperado. **NUNCA usar `re.sub()` sobre HTML inline.**

### 10. Extracción CSS de HTML corrompe inline JS

**Síntoma:** Tras extraer `<style>` a `css/custom.css`, los inline `<script>` dejan de ejecutarse. `SyntaxError: Invalid or unexpected token` en datos de referencia JS.

**Causa:** El patrón `read_file` → regex para extraer CSS → `write_file` para reescribir el HTML puede corromper contenido JS complejo (arrays de objetos, strings con caracteres especiales, escape sequences). `write_file` dentro de `execute_code` no preserva fielmente todo el contenido.

**Prevención:**
1. Para extracción CSS, usar `terminal` con `python3` directamente, NO `read_file` → process → `write_file`
2. Si se usa `write_file`, verificar inmediatamente con `node --check` sobre el inline JS extraído
3. Restaurar desde git si hay corrupción: `git show COMMIT:index.html > index.html`

**Patrón seguro:**
```bash
# Extraer CSS usando python3 directamente en terminal
python3 -c "
import re
html = open('index.html').read()
style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    css = style_match.group(1).strip()
    open('css/custom.css', 'w').write(css)
    # Reemplazar <style>...</style> con <link>
    html = html.replace(style_match.group(0), '<link rel=\"stylesheet\" href=\"css/custom.css\">')
    open('index.html', 'w').write(html)
"
# Verificar
node --check inline-script.js  # syntax check
python3 -c "c=open('index.html').read(); assert c.count('<script')==c.count('</script>')"
```

## Referencias

Ver `references/incidente-masterfit-caso-completo.md` para el caso de estudio completo
con timeline, causa raíz, y lecciones aprendidas.

Ver `references/execute-code-readfile-limit.md` para el caso de estudio del truncamiento
silencioso de archivos por `read_file` en `execute_code` (incidente AdelaCRM 2026-06-15).
