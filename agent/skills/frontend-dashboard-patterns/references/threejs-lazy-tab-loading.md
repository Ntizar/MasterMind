# Three.js Lazy-Loaded en Tab — MasterFit Case Study

## Contexto

**Proyecto:** MasterFit (dieta-masterfit) — dashboard de dieta con tab "Progreso" que usa Three.js para visualización 3D del cuerpo.
**Fecha:** 2026-06-11
**Problema:** Panel 3D en blanco, sin renderizar figura humana ni doughnut chart.

## Síntomas

1. Tab "Progreso" se muestra pero el área "Tu Cuerpo 3D" está vacía (fondo lila/azul)
2. El chart "Composición Corporal" está vacío
3. No hay errores en la consola de JavaScript
4. `typeof THREE` devuelve `"undefined"`
5. El HTML sirve correctamente el script `three.min.js` desde CDN (verificado con curl)

## Diagnóstico

El problema fue una combinación de:
1. **Browser tool cache agresivo** — el browser tool de Hermes no recargaba el HTML nuevo
2. **THREE no disponible al momento de init3DHuman()** — el CDN de Three.js podía no haberse ejecutado antes de que la función intentara crear `new THREE.Scene()`
3. **container3D no asignado correctamente** — se declaraba como `var` dentro de `buildHuman3D` pero se usaba antes de esa línea

## Solución Implementada

### Paso 1: Añadir CDN de Three.js al `<head>`

```html
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
```

### Paso 2: Declarar variables globales arriba del todo

```javascript
var _scene3D, _camera3D, _renderer3D, _humanGroup3D;
var _autoRotate3D = true;
var _mouseDown3D = false, _lastMouse3D = {x:0, y:0};
var _chartComposicion, _chartPesoEvo, _chartEntrenos;
var container3D; // global ref for labels
```

### Paso 3: Asignar container3D en loadProgreso()

```javascript
function loadProgreso() {
  _progLoaded = true;
  container3D = document.getElementById('canvas3d');
  fetch('/api/progreso')
    .then(function(r){return r.json();})
    .then(function(data) {
      renderProgresoKPIs(data.datos3D);
      init3DHuman(data.datos3D);
      renderComposicionChart(data.datos3D);
      renderPesoEvoChart(data.datos3D);
      renderEntrenos(data.historialEntrenos, data.resumenSemanal);
    })
    .catch(function(err) {
      console.error('Error cargando progreso', err);
      if (container3D) {
        container3D.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#ef4444;font-size:0.9rem;">Error cargando datos de progreso</div>';
      }
    });
}
```

### Paso 4: Verificar typeof THREE en init3DHuman()

```javascript
function init3DHuman(d) {
  var container = document.getElementById('canvas3d');
  if (!container) return;
  
  // Check Three.js is loaded
  if (typeof THREE === 'undefined') {
    container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#94a3b8;font-size:0.85rem;">Cargando motor 3D...</div>';
    setTimeout(function(){ init3DHuman(d); }, 1000);
    return;
  }
  
  // Clean up previous renderer
  if (_renderer3D) {
    container.removeChild(_renderer3D.domElement);
    _renderer3D.dispose();
  }
  
  // ... resto del init
}
```

### Paso 5: Eliminar declaración duplicada de container3D

Se eliminó `var container3D = document.getElementById('canvas3d');` que estaba después de `buildHuman3D` (hoisting conflict).

## Checklist de Debugging

```javascript
// 1. Verificar THREE está cargado
typeof THREE === 'object'  // → true

// 2. Verificar scripts cargados
document.querySelectorAll('script[src]').length  // → ≥ 2

// 3. Verificar canvas existe y tiene tamaño
document.getElementById('canvas3d')?.clientWidth  // → > 0

// 4. Forzar recarga si browser tool tiene cache
// Navegar con: https://dieta-ntizar-ntizar.apps.nan.builders/?t=<unix_timestamp>
```

## Deploy

- Commit y push a `main` → NaNBuilders detecta cambios en ~60-90s
- Si el browser tool sigue mostrando HTML viejo → navegar con timestamp query param
- Verificar con `curl` que el HTML sirve `three.min.js`
- Verificar `typeof THREE` en consola del browser tool