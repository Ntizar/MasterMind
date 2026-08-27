# Flex Layout + Leaflet Patterns — Debugging y Best Practices

## 🔥 Flex Layout Debugging: SIEMPRE Verificar DOM Primero

**Señal de que esto aplica:** El layout no respeta `flex: 1`, `width: 50%`, o `flex-direction: row` aunque el CSS parece correcto.

### Paso 1: Verificar estructura DOM (NO CSS)

Cuando un layout flex no funciona, **el 90% de las veces el problema es estructural, no de CSS**. Antes de tocar CSS, verificar:

```javascript
// En browser console — verificar cadena de padres
(function() {
  const target = document.getElementById('map-container');
  let el = target;
  const ancestry = [];
  while (el && el !== document.body) {
    ancestry.push(el.id || el.tagName);
    el = el.parentElement;
  }
  console.log('Ancestry:', ancestry.join(' > '));
})()

// Verificar dimensiones y computed styles
(function() {
  const ma = document.getElementById('main-area');
  const sb = document.getElementById('sidebar');
  const mc = document.getElementById('map-container');
  return JSON.stringify({
    mainArea: ma ? { w: ma.offsetWidth, h: ma.offsetHeight, flexDir: getComputedStyle(ma).flexDirection } : 'NOT FOUND',
    sidebar: sb ? { w: sb.offsetWidth } : 'NOT FOUND',
    mapContainer: mc ? { w: mc.offsetWidth } : 'NOT FOUND',
    children: ma ? Array.from(ma.children).map(c => c.id || c.tagName) : [],
    viewport: { w: window.innerWidth, h: window.innerHeight }
  });
})()
```

**Si `children` NO incluye `map-container`:** El contenedor del mapa está fuera del flex parent. Buscar el `</div>` prematuro.

### Paso 2: Encontrar el `</div>` prematuro

```python
python3 -c "
with open('index.html') as f:
    lines = f.readlines()
depth = 0; in_area = False
for i, line in enumerate(lines):
    if 'id=\"main-area\"' in line:
        in_area = True; depth = 1; continue
    if in_area:
        depth += line.count('<div') - line.count('</div>')
        if depth == 0:
            print(f'main-area closes at line {i+1}')
            for j in range(i+1, min(i+4, len(lines))):
                print(f'  {j+1}: {lines[j].rstrip()[:100]}')
            break
"
```

## Leaflet en Flex Containers

Leaflet expansiona el mapa a 100% del viewport. Fix:

```css
#map-container {
    flex: 1 1 0%;    /* NO usar solo flex: 1 */
    min-width: 0;    /* CRÍTICO — permite shrink */
    overflow: hidden;
    position: relative;
}
```

Después de inicializar: `setTimeout(() => map.invalidateSize(), 300);`

## innerHTML vs textContent

`setTxt()` usa `textContent` que NO renderiza HTML. Para contenido con tags: usar `innerHTML`.

## ESIOS API Auth

Algunos indicadores requieren `x-api-key`. Verificar con curl antes de asumir que "la API no funciona".
Token: variable `ESIOS_API` o `/hermes-home/.env`.
