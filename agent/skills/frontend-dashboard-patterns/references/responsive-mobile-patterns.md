# Responsive Mobile Patterns — Dashboards Leaflet + Sidebar

## Tab Navbar Wrapping (15+ pestañas)

Cuando un dashboard tiene 15+ pestañas en barra horizontal, el usuario NO quiere scroll horizontal — quiere verlas todas en filas.

**Patrón probado en DataHub España (35 tabs):**

```css
.tabs-row {
    display: flex;
    flex-wrap: wrap;      /* ← CLAVE: permite salto de línea */
    gap: 4px;
}
.tab-btn {
    font-size: 10px;
    padding: 3px 8px;
    /* NO poner flex-shrink: 0 — eso fuerza scroll horizontal */
    white-space: nowrap;
    flex-shrink: 0;       /* ← ELIMINAR esto si se quiere wrapping */
}

/* Desktop: mapa a la derecha, sidebar a la izquierda */
#main-area {
    display: flex;
    flex-direction: row;
}
#sidebar { width: 50%; min-width: 50%; }
#map-container { flex: 1; }

/* Tablet (768-1024px): sidebar más estrecho, mapa visible */
@media (max-width: 1024px) {
    #main-area { flex-direction: row; }  /* mantener lado a lado */
    #sidebar { width: 45% !important; min-width: 45% !important; }
    #map-container { flex: 1; }
}

/* Mobile (<768px): layout vertical */
@media (max-width: 768px) {
    #main-area { flex-direction: column; }
    #sidebar { width: 100%; min-width: 100%; }
}
```

**Pitfall:** `overflow-x: auto` en `.tabs-row` causa scroll horizontal invisible — el usuario no ve que hay más tabs. `flex-wrap: wrap` es mejor UX.

**Pitfall:** En tablet (768-1024px), si `#main-area` usa `flex-direction: column`, el mapa queda debajo del sidebar y el usuario pierde el mapa de vista. Mantener `row` en tablet.

## Map Container Fix (CRITICAL)

**El error más común**: el mapa no se ve en móvil porque `#map-container` y `#map` no tienen altura explícita. `height: 100%` falla si el padre no propaga altura.

### Patrón correcto (probado en DataHub España)
```css
@media (max-width: 768px) {
    /* Parent: absoluto cubre todo el viewport */
    #map-container {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
    }
    /* Map: fill el container */
    #map {
        width: 100%;
        height: 100%;
    }
}
```

### ❌ Patrón que FALLA
```css
/* NO hacer esto — height: 100% hereda 0 si padre no tiene altura */
#map { height: 100%; }
/* NO hacer esto — vh fijo no se adapta al sidebar */
#map { height: 35vh; }
```

**Por qué falla**: La cadena `100vh → #app → #main-area → #map-container → #map` se rompe en móvil si algún intermediate no tiene altura explícita. La solución es `position: absolute` con `top/left/right/bottom: 0` que no depende de la cadena de alturas.

## Sidebar Auto-Collapse en Móvil

```css
@media (max-width: 768px) {
    #sidebar {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        height: 42vh;
        border-radius: 16px 16px 0 0;
        transition: height 0.3s ease;
    }
    #sidebar.collapsed {
        height: 0;
        min-height: 0;
        border-top: none;
    }
}
```

```javascript
// Auto-collapse al cargar en móvil
function initMobile() {
    if (window.innerWidth <= 768) {
        document.getElementById('sidebar').classList.add('collapsed');
        document.getElementById('mobile-map-toggle').classList.add('visible');
    }
    // MutationObserver para sincronizar FAB con estado del sidebar
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

## FAB Button (Floating Action Button)

```css
#mobile-map-toggle {
    display: none;
    position: fixed;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 950;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 24px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(37,99,235,0.3);
}
@media (max-width: 768px) {
    #mobile-map-toggle { display: none; }
    #mobile-map-toggle.visible { display: block; }
}
```

## Touch Swipe Gestures

```javascript
// Swipe up → cerrar sidebar, swipe down → abrir
let touchStartY = 0, touchStartX = 0;
document.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
    touchStartX = e.touches[0].clientX;
}, { passive: true });
document.addEventListener('touchend', (e) => {
    const deltaY = e.changedTouches[0].clientY - touchStartY;
    const deltaX = Math.abs(e.changedTouches[0].clientX - touchStartX);
    if (Math.abs(deltaY) < 50 || deltaX > Math.abs(deltaY)) return;
    if (window.innerWidth > 768) return;
    const sb = document.getElementById('sidebar');
    if (deltaY < -60 && !sb.classList.contains('collapsed')) toggleSidebar();
    else if (deltaY > 60 && sb.classList.contains('collapsed')) toggleSidebar();
}, { passive: true });
```

**Pitfall**: Siempre `{ passive: true }` para touch events en mobile —否则 el scroll se bloquea.

## Orientation Change Handler

```javascript
if (screen.orientation) {
    screen.orientation.addEventListener('change', () => {
        setTimeout(() => {
            if (map) map.invalidateSize();
            Object.values(charts).forEach(c => { if (c?.resize) c.resize(); });
        }, 400); // 400ms para esperar al repaint
    });
}
```

**Pitfall**: `invalidateSize()` sin delay no funciona — el browser necesita tiempo para repaint después del rotation.

## Cross-Tab Province Filter

Patrón para filtrar datos por provincia en todas las pestañas de un dashboard:

```html
<div id="province-filter-bar">
    <label for="province-filter">📍 Filtrar por provincia</label>
    <select id="province-filter">
        <option value="">— Todas las provincias —</option>
    </select>
</div>
```

```javascript
function populateProvinceFilter() {
    const select = document.getElementById('province-filter');
    const sorted = Object.entries(provinceData)
        .sort((a, b) => (a[1].nombre || '').localeCompare(b[1].nombre || ''));
    sorted.forEach(([cod, d]) => {
        const opt = document.createElement('option');
        opt.value = cod;
        opt.textContent = `${d.nombre} (${d.capital || cod})`;
        select.appendChild(opt);
    });
}

function onProvinceFilterChange(cod) {
    if (cod) {
        updateFilteredData(cod);   // Panel: KPIs
        fetchWeatherFiltered(cod);  // Clima: weather
        renderParksFiltered(cod);   // Ambiente: parques by CCAA
        fillCatastro(cod);          // Catastro: auto-fill
    } else {
        resetAllTabs();
    }
}
```

**Pitfall**: Al cerrar el detalle de provincia, también resetear el select del filtro.

## Footer + Zoom + Detail en Móvil

```css
@media (max-width: 768px) {
    #footer { display: none; }
    .leaflet-control-zoom a {
        width: 36px !important; height: 36px !important;
        line-height: 36px !important; font-size: 18px !important;
    }
    #province-detail {
        width: 100%; border-left: none;
        border-radius: 16px 16px 0 0;
        overflow-y: auto;
    }
}
```

## Pitfalls Críticos

1. **`#map { height: 100% }` sin absolute en el container** → altura 0 en móvil
2. **Sidebar sin `transition`** → cambio brusco sin animación
3. **Sin FAB button** → usuario no sabe cómo volver al mapa
4. **`screen.orientation` sin setTimeout** → `invalidateSize()` no surte efecto
5. **Touch events sin `passive: true`** → scroll bloqueado en mobile
6. **`#province-detail` sin `overflow-y: auto`** → contenido desbordado en móvil
7. **Footer visible en móvil** → roba espacio al mapa
