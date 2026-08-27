# MasterFit v3 — Full-Stack SPA Audit (2026-06-11)

Proyecto auditorado: `dieta-masterfit` (MasterFit v3)
Stack: Express + vanilla JS + Chart.js v4.4.7 + Three.js r160 + Aurora CSS + SQLite-less (JSON persistance)
Repo: github.com/Ntizar/dieta
Puerto: 5050

## Bugs encontrados

### 🔴 BUG 1: Borrar ejercicios siempre falla

**Causa raíz:** `renderDeporteList()` llama a `borrarRegistro('deporte', idx)` pero el servidor espera `'entrenamientos'` en `allowedTypes`.

**Archivo:** `dashboard.html` línea 627
```javascript
onclick="borrarRegistro('deporte', "+realIdx+")"
```

**Servidor** `server.js` línea 689:
```javascript
const allowedTypes = ['peso', 'comidas', 'entrenamientos', 'pasos'];
//                                              ^^^^^^^^^^^^^^^^
```

**Solución:** Cambiar `'deporte'` por `'entrenamientos'` en `renderDeporteList()`.

### 🔴 BUG 1b: indexOf con arrays invertidos

**Causa raíz:** `renderDeporteList()` itera sobre `deporte.slice().reverse()` pero usa `deporte.indexOf(d)` sobre el array ORIGINAL. Si hay descripciones duplicadas, `indexOf` devuelve la PRIMERA ocurrencia, no la actual.

**Archivo:** `dashboard.html` líneas 619-627

**Solución:** Almacenar el índice real como `data-idx` en el HTML generado, igual que se intenta en `renderComidasList()` con `indexMap`.

### 🔴 BUG 2: Tab Progreso no responsive

**Causa raíz:** El media query existente (`@media (max-width:768px)`) solo cubre los grids de Resumen y Registrar, pero NO los de la tab Progreso:

- Grid 3D + gráfico (línea 396): `grid-template-columns: 1fr 1fr` sin breakpoint
- KPIs Progreso (línea 361): `minmax(140px,1fr)` con 6 items → 840px mínimo
- Canvas 3D (línea 406): `height:500px` fijo → ocupa toda la pantalla en móvil
- Labels HTML absolutas del 3D (líneas 1334-1368): posicionadas con px fijos

**Solución:** Añadir media queries para la tab `progreso` con:
```css
@media (max-width:768px) {
  #tab-progreso .mf-kpi-grid { grid-template-columns: repeat(3,1fr) !important; }
  #tab-progreso div[style*="grid-template-columns:1fr 1fr"] { grid-template-columns:1fr !important; }
  #canvas3d { height: 350px !important; }
  /* Labels 3D más pequeñas */
  #canvas3d div[style*="position:absolute"] { font-size: 10px !important; padding: 3px 8px !important; }
}
```

### 🟡 Mejora: Tabs no scrollables en móvil

Las tabs caben 7 en desktop pero en <400px se salen del contenedor. Solución:
```css
.mf-tabs-row { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
.mf-tab { white-space: nowrap; flex-shrink: 0; }
```

## Aciertos del proyecto

- **Diseño visual:** Aurora CSS + Liquid Glass + orbes → muy atractivo, 10/10
- **3D InBody:** Three.js con datos reales → diferenciador brutal
- **IA Amadeo Llados:** Contexto real de DB, personalidad carismática, bien implementado
- **Sync GitHub automático:** Cada cambio se versiona → historial completo
- **Auto-estimación IA:** Comidas y ejercicios estimados con LLM → reduce fricción
- **Tabs con lazy loading:** Progreso solo carga al hacer click → rendimiento optimizado
- **KPIs informativos:** Métricas claras con deltas y tendencias

## Lecciones aprendidas

1. **Endpoint mismatch es el bug #1 en SPA con servidor**: el frontend llama a `/api/deporte`, el backend espera `/api/entrenamiento`. Siempre hacer `grep` de endpoints en ambos lados.
2. **indexOf con array invertido es bug #2**: la iteración con `.reverse()` o `.slice().reverse()` rompe el índice. Almacenar como `data-idx` en el HTML.
3. **Responsive no es monocapa**: las tabs lazy-loaded suelen quedar sin media queries. Verificar cada `tab-*` por separado.
4. **Todo fetch debe tener `.catch()` visible**: los errores silenciosos son el peor tipo de bug (el usuario no sabe que algo falló).