# Gráficos Plotly — Verificación y Patrones

## Problema Común

Los scripts generadores de HTML educativo crean:
1. CDN de Plotly: `<script src="https://cdn.plot.ly/plotly-latest.min.js">`
2. Contenedor: `<div id="plot-xxx" class="chart-plot">`
3. CSS: `.chart-plot { width: 100%; height: 350px; }`

Pero NO añaden la llamada `Plotly.newPlot()` → el gráfico queda vacío.

## Patrón de Verificación

```python
import re

def audit_plotly_charts(html_files, base_path):
    """Verify all Plotly chart containers have initialization code"""
    results = {}
    
    for fname in html_files:
        with open(f'{base_path}/{fname}') as f:
            content = f.read()
        
        containers = re.findall(r'<div\s+id="(plot-[^"]+)"', content)
        plots_init = re.findall(r'Plotly\.(newPlot|react)\(', content)
        has_cdn = 'plotly' in content.lower()
        
        issues = []
        
        # CDN present but no containers → waste
        if has_cdn and not containers:
            issues.append(f'⚠️ CDN Plotly cargado pero sin contenedores')
        
        # Containers but no init → empty charts (CRITICAL)
        if containers and not plots_init:
            issues.append(f'❌ {len(containers)} contenedores Plotly sin Plotly.newPlot(): {containers}')
        
        # More containers than inits → partial init
        if containers and plots_init and len(containers) > len(plots_init):
            missing = containers[len(plots_init):]
            issues.append(f'⚠️ {len(missing)} contenedores sin inicializar: {missing}')
        
        # No CDN and no containers → no charts (fine for non-visual content)
        if not has_cdn and not containers:
            pass  # OK — no charts expected
        
        # No CDN but containers exist → will render empty
        if not has_cdn and containers:
            issues.append(f'❌ Contenedores Plotly sin CDN: {containers}')
        
        results[fname] = issues
    
    return results
```

## Formato de Inicialización

Cada contenedor `plot-*` necesita un bloque `<script>` con `Plotly.newPlot()`:

```javascript
// Mínimo viable
Plotly.newPlot('plot-nombre', [{
    x: [1, 2, 3, 4, 5],
    y: [2, 4, 1, 5, 3],
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Serie 1',
    line: {color: '#2563eb', width: 2}
}], {
    title: 'Título del Gráfico',
    xaxis: {title: 'Eje X'},
    yaxis: {title: 'Eje Y'},
    margin: {t: 40, b: 40, l: 50, r: 20}
}, {responsive: true});
```

```javascript
// Múltiples series
Plotly.newPlot('plot-nombre', [
    {x: [...], y: [...], type: 'scatter', name: 'Serie 1'},
    {x: [...], y: [...], type: 'bar', name: 'Serie 2'}
], {
    title: 'Comparativa',
    xaxis: {title: 'X'},
    yaxis: {title: 'Y'}
}, {responsive: true});
```

## Estilos CSS Requeridos

```css
.chart-plot {
    width: 100%;
    min-height: 300px;
    max-height: 400px;
    margin: 1rem 0;
    border-radius: 8px;
}
```

**Pitfall:** Si no hay `min-height`, el contenedor puede colapsar a 0px y el gráfico no se ve aunque esté inicializado.

## Patrones de Gráficos Educativos

### Funciones matemáticas
```javascript
// f(x) = x²
const x = [];
const y = [];
for (let i = -5; i <= 5; i += 0.1) {
    x.push(i);
    y.push(i * i);
}
Plotly.newPlot('plot-parabola', [{x, y, type: 'scatter', mode: 'lines'}], {...});
```

### Vectores / Espacios vectoriales
```javascript
// Representar vectores como flechas
Plotly.newPlot('plot-vectores', [
    {x: [0, 1], y: [0, 0], type: 'scatter', mode: 'lines+markers',
     marker: {size: 10, symbol: 'arrow'}, name: 'v₁ = (1,0)'},
    {x: [0, 0], y: [0, 1], type: 'scatter', mode: 'lines+markers',
     marker: {size: 10, symbol: 'arrow'}, name: 'v₂ = (0,1)'}
], {
    title: 'Base canónica en R²',
    xaxis: {range: [-1, 2], title: 'x₁'},
    yaxis: {range: [-1, 2], title: 'x₂'}
});
```

### Límites / asíntotas
```javascript
// f(x) = 1/x
const x = [];
const y = [];
for (let i = -5; i <= 5; i += 0.05) {
    if (Math.abs(i) < 0.01) continue; // saltar 0
    x.push(i);
    y.push(1 / i);
}
Plotly.newPlot('plot-inversa', [{x, y, type: 'scatter', mode: 'lines'}], {
    shapes: [{type: 'line', x0: 0, x1: 0, y0: -10, y1: 10,
              line: {color: 'red', dash: 'dash'}}] // asíntota
});
```

## 🔴 Plotly en Tag de Script Equivocado (NUEVO — v1.7)

**Problema:** El código `Plotly.newPlot()` puede terminar en ubicaciones que impiden su ejecución:

### Patrón 1: Código dentro de `<script src="...">`
```html
<!-- MAL: el navegador ignora el contenido inline de un tag src -->
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js">
// Gráfico de bases en R²
const trace1 = { x: [0,1], y: [0,0] };
Plotly.newPlot('plot-base', [trace1], {...});
</script>
```
**Consecuencia:** Ni KaTeX ni Plotly funcionan. El tag `src` dice al navegador que cargue el archivo remoto, el contenido inline se descarta.

### Patrón 2: Código flotante sin `<script>`
```html
<script src="katex.min.js"></script>
// Gráfico de bases en R²          ← esto es texto plano en HTML
const trace1 = { ... };
Plotly.newPlot('plot-trayectorias', [trace1], {...});
<script>window.addEventListener('scroll', ...)</script>
```
**Consecuencia:** El código JavaScript se renderiza como texto visible en la página. No se ejecuta.

### Patrón 3: Código en `<script>` separado antes de DOMContentLoaded
```html
<script>
// Se ejecuta INMEDIATAMENTE al cargar
Plotly.newPlot('plot-trayectorias', [...], {...});
</script>
<!-- ... todo el HTML body ... -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  renderMathInElement(document.body, {...});
});
</script>
```
**Consecuencia:** `Plotly.newPlot` se ejecuta cuando el `<div id="plot-trayectorias">` aún no existe en el DOM. Plotly no encuentra el contenedor → gráfico vacío.

### Detección

```python
def check_plotly_placement(content):
    """Detect Plotly code in wrong execution context"""
    issues = []
    
    # Check 1: Plotly inside a <script src="..."> tag
    for m in re.finditer(r'<script\s+src="[^"]*">\s*(.*?)\s*</script>', content, re.S):
        if 'Plotly.newPlot' in m.group(1):
            issues.append(f'❌ Plotly dentro de <script src=...> (navegador lo ignora)')
    
    # Check 2: Plotly outside any <script> tag
    # Find all script regions
    script_regions = []
    for m in re.finditer(r'<script[^>]*>.*?</script>', content, re.S):
        script_regions.append((m.start(), m.end()))
    
    for m in re.finditer(r'Plotly\.newPlot', content):
        in_script = any(s <= m.start() <= e for s, e in script_regions)
        if not in_script:
            issues.append(f'❌ Plotly.newPlot fuera de <script> en posición {m.start()}')
    
    # Check 3: Plotly before DOMContentLoaded (runs before DOM ready)
    plotly_pos = content.find('Plotly.newPlot')
    dom_pos = content.find("DOMContentLoaded")
    if plotly_pos > 0 and dom_pos > 0 and plotly_pos < dom_pos:
        # Check if it's in a separate script before DOMContentLoaded
        last_script_before = content.rfind('</script>', 0, dom_pos)
        if plotly_pos < last_script_before:
            issues.append(f'❌ Plotly ejecuta ANTES de DOMContentLoaded')
    
    return issues
```

### Corrección

**Dependiendo de dónde esté el `<script>`, hay dos estrategias correctas:**

#### Estrategia A: Script en `<head>` → usar DOMContentLoaded

```html
<head>
  <script src="katex.min.js"></script>
  <script src="plotly.min.js"></script>
</head>
<body>
  <!-- contenido HTML -->
  <div id="plot-chart"></div>
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      renderMathInElement(document.body, {...});
      Plotly.newPlot('plot-chart', [...], {...});
    });
  </script>
</body>
```

#### Estrategia B: Script al final de `</body>` → ejecución directa (NO DOMContentLoaded)

```html
<body>
  <!-- contenido HTML -->
  <div id="plot-chart"></div>
  <script src="katex.min.js"></script>
  <script src="plotly.min.js"></script>
  <script>
    // DOMContentLoaded YA se disparó — el wrapper NUNCA se ejecuta
    // Ejecutar directamente:
    renderMathInElement(document.body, {...});
    Plotly.newPlot('plot-chart', [...], {...});
  </script>
</body>
```

**🔴 PITFALL CRÍTICO: DOMContentLoaded YA SE DISPARÓ en scripts al final del body**

Cuando el `<script>` está justo antes de `</body>`, el navegador ya disparó `DOMContentLoaded` (el DOM está completo). El wrapper `document.addEventListener('DOMContentLoaded', () => { ... })` **NUNCA se ejecuta** porque el evento ya pasó.

**Síntoma:** Gráfico Plotly vacío (solo recuadro blanco), KaTeX no renderiza, ejercicios no funcionan. Pero NO hay errores en consola.

**Detección:**

```python
def check_domcontentloaded_position(content):
    """Detect if DOMContentLoaded wrapper is in a bottom-of-page script"""
    # Find position of the last </body> or </html>
    body_end = max(content.rfind('</body>'), content.rfind('</html>'))
    # Find position of DOMContentLoaded
    dom_pos = content.find("DOMContentLoaded")
    if dom_pos > 0 and body_end > 0:
        # Find which script tag contains DOMContentLoaded
        last_script_start = content.rfind('<script', 0, dom_pos)
        # Check if this script is after most HTML content
        last_div_close = content.rfind('</div>', 0, dom_pos)
        if last_div_close > last_script_start and last_script_start > 0:
            return '❌ DOMContentLoaded wrapper en script al final del body — nunca se ejecuta'
    return None
```

**Regla:** Si el `<script>` con Plotly.newPlot está al final del body (después de todo el HTML), NO usar DOMContentLoaded. Ejecutar directamente. Si está en `<head>`, sí usar DOMContentLoaded.

## Checklist de Verificación

- [ ] `<script src="katex.min.js">` separado de `<script src="auto-render.min.js">` (el core DEBE cargar antes)
- [ ] CDN Plotly cargado (`plotly-latest.min.js` o versión específica)
- [ ] CSS `.chart-plot` con `min-height` definido
- [ ] Cada `<div id="plot-*">` tiene `Plotly.newPlot('plot-*', ...)` correspondiente
- [ ] Títulos de gráficos descriptivos (no solo "Gráfico 1")
- [ ] Ejes etiquetados (`xaxis.title`, `yaxis.title`)
- [ ] Responsive: `{responsive: true}` en opciones de layout
- [ ] Datos coherentes con el contenido educativo de la sesión
- [ ] Colores consistentes con la paleta del proyecto (azul #2563eb, naranja #f97316)
- [ ] Funciones onclick (checkExercise, checkE, etc.) definidas en el mismo `<script>` inline
- [ ] Código Plotly fuera de `<script src="...">` (el navegador ignora contenido inline de tags src)
