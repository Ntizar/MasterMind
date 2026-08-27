# Taxonomy Hierarchical Filters — Patrón de Filtros Jerárquicos

Filtros por checkboxes construidos desde una taxonomía **estática** (no desde los datos), con matching jerárquico: marcar un código padre incluye todos sus descendientes.

## Cuándo usar

- El dashboard tiene un sistema de clasificación jerárquica (taxonomía oficial, normativa, categorías anidadas)
- Quieres que el usuario pueda filtrar por categorías generales **y** subcategorías
- La taxonomía es fija y conocida de antemano (no depende de los datos cargados)
- Ejemplos: clasificación de accidentes (Anexo III), tipos de infraestructura, códigos NACE, jerarquías de producto

## Por qué no data-driven

El patrón típico es construir filtros desde los datos:

```js
const codes = [...new Set(data.map(d => d.codigo))];
codes.forEach(code => { /* crear checkbox */ });
```

**Problema:** si no hay datos para un código, ese código no aparece en el filtro. En dashboards normativos (donde la taxonomía es un estándar), esto es inaceptable — el usuario necesita ver toda la clasificación aunque no haya datos.

## Estructura

### 1. Taxonomía estática como objeto lookup

```js
const TAX = {
  suceso: {
    '1': 'Accidente',
    '1.1': 'Colisión con vehículo ferroviario',
    '1.1.1': 'Colisión frontal',
    '1.1.2': 'Colisión por alcance',
    '1.1.3': 'Colisión lateral',
    // ... todos los códigos, incluso los que no tienen datos
    '3.2': 'Intento de suicidio'
  },
  causa: {
    '1': 'Ferrocarril',
    '1.1': 'Factor humano',
    '1.1.1': 'FH - Señales',
    // ... completo
    '2.4': 'Sin identificar'
  }
};
```

### 2. Construir checkboxes desde el TAX, no desde los datos

```js
function buildCheckboxes(containerId, cat) {
  const c = document.getElementById(containerId);
  c.innerHTML = '';
  // Object.keys del TAX, no del dataset
  const codes = Object.keys(TAX[cat]).sort((a,b) =>
    a.localeCompare(b, undefined, {numeric: true})
  );
  codes.forEach(code => {
    const label = document.createElement('label');
    label.className = 'checkbox-item';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.value = code;
    cb.checked = true;
    cb.dataset.key = cat;
    cb.addEventListener('change', applyFilters);
    label.appendChild(cb);
    label.appendChild(document.createTextNode(
      TAX[cat][code] + ' (' + code + ')'
    ));
    c.appendChild(label);
  });
}
buildCheckboxes('sucesoCheckboxes', 'suceso');
buildCheckboxes('causaCheckboxes', 'causa');
```

### 3. Filtrado jerárquico (padre → descendientes)

El núcleo del patrón: un checkbox por código padre (ej. `'1.1'`) debe mostrar también los datos con códigos descendientes (ej. `'1.1.1'`, `'1.1.2'`).

```js
function applyFilters() {
  const sucesoChecked = [...document.querySelectorAll('#sucesoCheckboxes input:checked')]
    .map(i => i.value);
  const causaChecked = [...document.querySelectorAll('#causaCheckboxes input:checked')]
    .map(i => i.value);

  filtered = datos.filter(d => {
    // Jerárquico: si '1.1' está checked, '1.1.1' también pasa
    if (sucesoChecked.length && !sucesoChecked.some(c =>
      d.suceso_codigo === c ||
      d.suceso_codigo.startsWith(c + '.')
    )) return false;

    if (causaChecked.length && !causaChecked.some(c =>
      d.causa_codigo === c ||
      d.causa_codigo.startsWith(c + '.')
    )) return false;

    return true;
  });
}
```

**Clave:** `d.suceso_codigo.startsWith(c + '.')` — si el checkbox tiene `'1.1'`, cualquier data con `'1.1.1'` o `'1.1.2'` matchea porque empieza por `'1.1.'`.

## Consideraciones de UX

### Scroll en grupos grandes

Para taxonomías con 50+ checkboxes, ampliar el scroll:

```css
.checkbox-group {
  max-height: 300px;  /* en vez de 140px */
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 8px;
}
```

### Botones Seleccionar todo / Deseleccionar

Siempre incluir (especialmente importante con listas largas):

```html
<div class="filter-actions">
  <button id="sucesoSelectAll">Seleccionar todo</button>
  <button id="sucesoDeselect">Deseleccionar</button>
</div>
```

```js
document.getElementById('sucesoSelectAll').addEventListener('click', () => {
  document.querySelectorAll('#sucesoCheckboxes input').forEach(cb => cb.checked = true);
  applyFilters();
});
document.getElementById('sucesoDeselect').addEventListener('click', () => {
  document.querySelectorAll('#sucesoCheckboxes input').forEach(cb => cb.checked = false);
  applyFilters();
});
```

### Labels en gráficos

Los gráficos deben usar la etiqueta del TAX, no el código crudo:

```js
filtered.forEach(d => {
  const k = TAX.suceso[d.suceso_codigo] || d.suceso_codigo;
  tipos[k] = (tipos[k] || 0) + 1;
});
```

## Variantes

### Con función helper taxLabel()

Si prefieres un lookup más explícito:

```js
function taxLabel(cat, code) {
  const m = TAX[cat];
  return m && m[code] ? m[code] : code;
}
// Uso:
filtered.forEach(d => {
  const k = taxLabel('suceso', d.suceso_codigo);
  // ...
});
```

### Con tabla de códigos en datos (data-driven + taxonomía)

Si algunos datos usan códigos que no están en el TAX, el `taxLabel()` devuelve el código crudo como fallback — eso evita labels vacíos.

## Pitfalls

- **Confirmar con el usuario** si quiere ver TODOS los códigos (incluyendo los que nunca aparecen). A veces prefieren solo los que tienen datos para reducir ruido visual.
- **Ordenación natural de códigos:** `'1.10'` debe ir después de `'1.9'`, no después de `'1.1'`. Usar `localeCompare` con `{numeric: true}`.
- **Códigos de 4+ niveles** (ej. `'1.5.1.2.1'`): el `startsWith(c + '.')` funciona para cualquier profundidad. No hace falta recursión.
- **Checkbox de nivel 0** (ej. `'1'` = "Accidente"): matchea `'1'`, `'1.1'`, `'1.1.1'`, etc. por el `startsWith`. Si hay un código `'10'` en otra categoría, NO matchea porque `'1'.' != '10'` (el punto lo diferencia).
- **Rendimiento:** con 1000+ registros y 80 checkboxes, el filtro se ejecuta en <5ms. No necesita memoización.