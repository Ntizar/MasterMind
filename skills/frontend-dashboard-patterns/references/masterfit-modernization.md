# MasterFit Modernization — Casos Reales y Métricas

**Fecha:** 2026-06-12  
**Proyecto:** dieta-masterfit (MasterFit v3)  
**URL:** https://dieta-ntizar-ntizar.apps.nan.builders/

## Métricas Antes/Después

| Métrica | Antes | Después | Cambio |
|---|---|---|---|
| Líneas HTML | 2042 | 558 | -73% |
| Líneas JS | 0 (inline) | 1513 (archivo) | Separado |
| `var` | 442 | 0 | -100% |
| `const` | 0 | 243 | +243 |
| `let` | 0 | 25 | +25 |
| `getElementById` | 142 | 68 | -52% |
| Arrow functions | 0 | 121 | +121 |
| Template literals | 0 | 0 | 0 (no aplicó) |
| innerHTML | 28 | 28 | 0 (seguro) |
| Tamaño total | 115,862 bytes | 115,524 bytes | -0.3% |

## Lecciones Aprendidas

### Template Literals — NO usar regex automático

El regex `'text' + var + 'text'` → `` `text ${var} text` `` **rompe strings con comillas escapadas**.

Caso real en MasterFit L306:
```javascript
// Original
'<button onclick="borrarRegistro(\'comidas\',' + realIdx + ')" ...>

// Regex lo convierte a (WRONG)
`<button onclick="borrarRegistro(\'comidas\`,${realIdx})" ...>`
// El backtick confunde con el cierre de string → SyntaxError
```

**Solución:** No usar template literals automáticos. Solo arrow functions automáticas.

### Arrow Functions — Regex específico, no genérico

Solo convertir `function(params) {` → `(params) => {`, NUNCA `() => {` que ya es arrow function.

Regex correcto:
```javascript
// function() { → () => {
re.sub(r'\bfunction\s*\(\s*\)\s*\{', '() => {', line)
// function(a) { → (a) => {
re.sub(r'\bfunction\s*\(\s*([a-zA-Z_]\w*)\s*\)\s*\{', r'(\1) => {', line)
// function(a,b) { → (a,b) => {
re.sub(r'\bfunction\s*\(\s*([a-zA-Z_]\w*,\s*[a-zA-Z_]\w*)\s*\)\s*\{', r'(\1) => {', line)
```

### var → const/let — Scope analysis por función

Las variables `var` en funciones diferentes con el mismo nombre son scope-local:
- `var labels` en `renderPesoChart()` ≠ `var labels` en `renderKcalChart()`
- Cada una es `const` dentro de su función si no se reasigna
- Solo `let` si se reasigna DENTRO de la misma función

### innerHTML en dashboards personales

En MasterFit, los 28 `innerHTML` inyectan HTML con clases Aurora (`ia-badge`, `nz-badge`, etc.). Los datos dinámicos son valores numéricos de la API (`d.kcal`, `d.kcal_estimadas`). **No hay riesgo XSS real.**

Regla: Si el `innerHTML` inyecta markup con clases CSS y los datos son números de API propia → seguro.

### Deploy NaN — Verificar con curl, no browser

Después de subir `dashboard.js` a GitHub, NaN puede tardar 15-30 segundos en servirlo. El browser tool puede servir versión cacheada. **Siempre verificar con `curl`**.

Caso real: dashboard.js dio 404 en NaN los primeros 2 intentos. Tras 30 segundos, `curl` devolvió 200 con 73KB de JS correcto.

### Git recovery — Siempre desde HEAD

Cuando se regenera el JS desde el HTML original, los cambios previos (var→const/let) se pierden. **Siempre recuperar el HTML desde `git show HEAD:dashboard.html`** antes de re-extraer el JS.
