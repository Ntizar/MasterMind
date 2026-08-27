# Mobile Responsive Audit — Static SPAs

Procedimiento para auditar la responsividad móvil de SPAs estáticas (sin backend): dashboards, visores de mapa, herramientas de datos desplegadas en GitHub Pages.

Extraído de DataHub España audit (2026-06-30).

## 1. Trazar la cadena de alturas (Flex Height Chain)

El error #1 en SPAs móviles es un mapa con 0px de altura. La causa: la cadena de alturas CSS se rompe en algún punto.

```
html { height: 100% }
  body { height: 100% }
    #app { height: 100vh; display: flex; flex-direction: column }
      #topbar { height: 52px; min-height: 52px }
      #main-area { flex: 1 }  ← DEBE tener altura computada
        #sidebar { width: 380px }  desktop / position:fixed en móvil
        #map-container { flex: 1; position: relative }
          #map { width: 100%; height: 100% }  ← DEPENDEN de todos los padres
      #footer { height: 32px }
```

**Regla:** Si algún eslabón no tiene altura computada (flex-basis:0 sin grow, sin height explícito, sin padre con height), los hijos con `height:100%` quedan en 0px.

**Cómo verificar:**
```javascript
// En browser console
document.querySelectorAll('#app, #main-area, #map-container, #map').forEach(el => {
    console.log(el.id, el.offsetWidth + 'x' + el.offsetHeight);
});
```

## 2. position:fixed rompe Flex Flow

Cuando un hijo flex pasa a `position:fixed` en un @media query, **se saca del flujo normal**. Los hijos restantes deben llenar el espacio.

**Patrón típico de dashboard:**
```css
/* Desktop: sidebar es flex child normal */
#sidebar { width: 380px; min-width: 380px; }

/* Mobile: sidebar se fija al fondo */
@media (max-width: 768px) {
    #sidebar {
        position: fixed;
        bottom: 0;
        height: 45vh;
        width: 100% !important;
        z-index: 900;
    }
}
```

**Consecuencia:** En móvil, `#main-area` (flex row) solo tiene `#map-container` como hijo in-flow. Con `flex:1`, debería llenar todo el espacio. PERO si el contenedor padre no tiene altura computada, el hijo queda en 0px.

**Verificación:**
```javascript
// En móvil (o simulando con DevTools)
const ma = document.getElementById('main-area');
const mc = document.getElementById('map-container');
console.log('main-area:', ma.offsetHeight);
console.log('map-container:', mc.offsetHeight);
console.log('map:', document.getElementById('map').offsetHeight);
```

## 3. @media Coverage Audit

Verificar que TODO contenedor crítico tiene reglas explícitas en @media:

```python
import re

media_blocks = re.findall(r'@media[^{]*\{(.+?)\n\s*\}', content, re.DOTALL)
media_selectors = set()
for block in media_blocks:
    selectors = re.findall(r'(#\w[\w-]*)\s*\{', block)
    media_selectors.update(selectors)

critical = {'#map-container', '#map', '#sidebar', '#main-area'}
missing = critical - media_selectors
if missing:
    print(f'Sin reglas mobile: {missing}')
```

**Fallo tipico:** `#map-container` y `#map` no tienen reglas en @media. Solo `#sidebar` tiene. El mapa depende del layout flex por defecto.

## 4. Panel Fijo que Tapa Contenido

**Patron:** Sidebar/panel con `position:fixed; bottom:0; height:45vh` tapa el contenido principal.

**Analisis de cobertura (iPhone SE 375x667):**
```
Topbar: 52px
Mapa visible: 667 - 52 - 32(footer) - 300(45vh sidebar) = 283px
Sidebar tapando: 300px (45vh)
```

**Fix patterns:**
1. Auto-collapse sidebar en movil
2. Sidebar como overlay: `position:fixed; bottom:0; height:auto; max-height:50vh`
3. Drawer pattern: sidebar se desliza desde la izquierda

## 5. invalidateSize en Orientacion

Leaflet necesita `map.invalidateSize()` cuando cambia el tamano del contenedor. En moviles, el cambio de orientacion a veces no dispara `resize` inmediatamente.

```javascript
if (screen.orientation) {
    screen.orientation.addEventListener('change', () => {
        setTimeout(() => map && map.invalidateSize(), 300);
    });
}
```

## 6. Map Legend Mobile Positioning

En desktop: `bottom: 40px; right: 12px;`  
En mobile: `bottom: 12px; right: 8px;` — puede quedar detras del sidebar fijo.

**Fix:** En movil, mover legend arriba:
```css
@media (max-width: 768px) {
    #map-legend { bottom: auto; top: 8px; right: 8px; }
}
```

## 7. Province/Detail Panel Full-Width en Movil

`#province-detail { position: absolute; width: 100%; }` en movil tapa TODO el mapa.

**Fix patterns:**
1. Slide-up panel: `position: fixed; bottom: 0; height: 60vh;`
2. Full-screen con back button: `position: fixed; inset: 0; z-index: 950;`
3. Mini-panel: `height: 200px; bottom: 45vh;` (encima del sidebar)

## 8. Checklist de Verificacion Rapida

```python
def mobile_responsive_audit(html_content):
    issues = []
    if 'viewport' not in html_content:
        issues.append(('CRITICO', 'Sin meta viewport'))
    media_count = html_content.count('@media')
    if media_count == 0:
        issues.append(('CRITICO', 'Sin @media queries'))
    for sel in ['#map-container', '#map', '#sidebar']:
        in_media = False
        for m in re.finditer(r'@media[^{]*\{', html_content):
            block_start = m.end()
            depth = 1
            for j in range(block_start, min(block_start + 5000, len(html_content))):
                if html_content[j] == '{': depth += 1
                elif html_content[j] == '}':
                    depth -= 1
                    if depth == 0:
                        if sel in html_content[block_start:j]:
                            in_media = True
                        break
        if not in_media:
            issues.append(('CRITICO', f'{sel} sin reglas en @media'))
    return issues
```

## Ejemplo Real: DataHub Espana (2026-06-30)

**Problema:** "El mapa no se ve desde el movil"

**Diagnostico:**
- `#map-container` y `#map` NO tenian reglas en @media
- `#sidebar` era `position:fixed; bottom:0; height:45vh` — tapaba 45% del mapa
- No habia auto-collapse del sidebar en movil
- `#map-legend` con `bottom:12px` quedaba detras del sidebar
- `#province-detail` con `width:100%` tapaba todo el mapa

**El mapa SI se renderizaba**, pero estaba tapado por el sidebar.

---

## Fix Patterns Concretos (DataHub España 2026-06-30)

### Fix 1: Map Container — Absolute Positioning

```css
@media (max-width: 768px) {
    #map-container {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
    }
    #map { width: 100%; height: 100%; }
}
```

**Por qué absolute en vez de height calc:** La cadena `100vh → #app → #main-area → #map-container → #map` se rompe si algún intermediate no propaga altura. `position: absolute` con inset 0 no depende de la cadena.

### Fix 2: Sidebar Auto-Collapse + FAB

```css
#mobile-map-toggle {
    display: none; position: fixed; bottom: 16px;
    left: 50%; transform: translateX(-50%);
    z-index: 950; background: #2563eb; color: white;
    border: none; border-radius: 24px; padding: 10px 20px;
}
@media (max-width: 768px) {
    #mobile-map-toggle.visible { display: block; }
}
```

```javascript
function initMobile() {
    if (window.innerWidth <= 768) {
        document.getElementById('sidebar').classList.add('collapsed');
        document.getElementById('mobile-map-toggle').classList.add('visible');
    }
    // MutationObserver para FAB ↔ sidebar sync
    const observer = new MutationObserver(() => {
        const sb = document.getElementById('sidebar');
        const fab = document.getElementById('mobile-map-toggle');
        if (window.innerWidth <= 768) {
            fab.classList.toggle('visible', sb.classList.contains('collapsed'));
        }
    });
    observer.observe(document.getElementById('sidebar'),
        { attributes: true, attributeFilter: ['class'] });
}
```

### Fix 3: Touch Swipe + Orientation

```javascript
// Swipe: up=close, down=open
let touchStartY = 0, touchStartX = 0;
document.addEventListener('touchstart', e => {
    touchStartY = e.touches[0].clientY;
    touchStartX = e.touches[0].clientX;
}, { passive: true });
document.addEventListener('touchend', e => {
    const dy = e.changedTouches[0].clientY - touchStartY;
    const dx = Math.abs(e.changedTouches[0].clientX - touchStartX);
    if (Math.abs(dy) < 50 || dx > Math.abs(dy)) return;
    if (window.innerWidth > 768) return;
    const sb = document.getElementById('sidebar');
    if (dy < -60 && !sb.classList.contains('collapsed')) toggleSidebar();
    else if (dy > 60 && sb.classList.contains('collapsed')) toggleSidebar();
}, { passive: true });

// Orientation: invalidateSize con delay
if (screen.orientation) {
    screen.orientation.addEventListener('change', () => {
        setTimeout(() => {
            if (map) map.invalidateSize();
            Object.values(charts).forEach(c => { if (c?.resize) c.resize(); });
        }, 400);
    });
}
```

**Pitfall:** `{ passive: true }` obligatorio en touch events — sin ello el scroll se bloquea en mobile.

### Fix 4: Footer + Zoom + Detail en Móvil

```css
@media (max-width: 768px) {
    #footer { display: none; }
    .leaflet-control-zoom a { width: 36px !important; height: 36px !important; }
    #province-detail { overflow-y: auto; border-radius: 16px 16px 0 0; }
}
```

### Fix 5: Cross-Tab Province Filter

Select global que filtra datos en todas las pestañas:
- Panel: KPIs de la provincia
- Clima: weather de Open-Meteo para la capital
- Ambiente: parques filtrados por CCAA
- Catastro: auto-fill

**Pitfall:** Al cerrar detalle de provincia, resetear también el select del filtro.
