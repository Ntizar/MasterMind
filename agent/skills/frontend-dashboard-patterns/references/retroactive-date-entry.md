# Retroactive Date Entry — Registro en días pasados

Patrón completo para permitir al usuario registrar datos (peso, comidas, ejercicio, pasos) en **cualquier fecha**, no solo hoy.

## Cuándo aplicar

- Apps de seguimiento personal (dieta, fitness, hábitos) donde el usuario puede olvidar registrar un día
- Dashboards de logging donde los datos pueden llegar con retraso
- Cualquier formulario CRUD que actualmente usa `hoy()` hardcodeado

## Arquitectura

```
Formulario HTML:
  <input type="date"> pre-rellenado con today()
       ↓
  Frontend JS → lee la fecha + resto de campos
       ↓
  Backend → `fecha || hoy()` — usa la fecha del body o la actual como fallback
       ↓
  SQL: INSERT con la fecha recibida
```

## Frontend — HTML

### 1. Función helper `today()`

```javascript
function today() {
  return new Date().toLocaleDateString('sv-SE'); // → "2026-06-19"
}
```

### 2. Input date en cada tarjeta de registro

Cada tarjeta de registro (peso, comida, ejercicio, pasos) necesita su propio `<input type="date">`:

```javascript
// Peso
'<div style="display:flex;gap:6px;align-items:center">' +
  '<input type="date" id="peso-fecha" value="' + today() + '" style="width:auto;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
  '<input type="number" step="0.1" min="30" max="300" id="peso-input" placeholder="kg" style="flex:1">' +
  '<input type="time" id="peso-hora" style="width:auto;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
'</div>'

// Comida
'<div style="display:flex;gap:6px;align-items:center;margin-top:6px">' +
  '<input type="date" id="comida-fecha" value="' + today() + '" style="flex:1;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
  '<input type="time" id="comida-hora" style="flex:1;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
'</div>'

// Ejercicio
'<div style="display:flex;gap:6px;margin-top:6px">' +
  '<input type="date" id="ejercicio-fecha" value="' + today() + '" style="flex:1;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
  '<input type="number" id="ejercicio-dur" placeholder="min" style="flex:1">' +
  '<input type="time" id="ejercicio-hora" style="width:auto;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
'</div>'

// Pasos
'<div style="display:flex;gap:6px;margin-top:6px">' +
  '<input type="date" id="pasos-fecha" value="' + today() + '" style="flex:1;padding:10px;border:1.5px solid var(--bg2);border-radius:8px;font-size:.85rem">' +
  '<input type="number" id="pasos-input" placeholder="pasos" style="flex:1">' +
'</div>'
```

### 3. Orden de campos: fecha primero

UX: el **input date va primero** en el layout (antes del valor y del time). Así el usuario cambia primero el día, luego el valor. Es más intuitivo para registro retroactivo.

## Frontend — JS

### 4. Leer fecha y pasarla al body

```javascript
var fecha = document.getElementById('peso-fecha').value || '';
var data = await api('/api/peso', {
  method: 'POST',
  body: { fecha: fecha, hora: hora, peso_kg: peso, notas: notas }
});
```

### 5. En cajas de estimación editables (comida, ejercicio)

La fecha también debe ser editable en la caja de estimación previa a confirmar:

```javascript
comidaEstData = { fecha: fecha, descripcion: desc, hora: hora, ... };

document.getElementById('comida-est-box').innerHTML =
  '<div class="estimation-box">' +
    '<div class="eb-row"><span>📅 Fecha</span>' +
      '<input type="date" id="ed-comida-fecha" value="' + fecha + '" ...>' +
    '</div>' +
    // ... resto de campos editables
  '</div>';
```

Y al confirmar:

```javascript
var fechaEl = document.getElementById('ed-comida-fecha');
var body = {
  fecha: fechaEl ? fechaEl.value : (comidaEstData.fecha || ''),
  // ... resto de campos
};
```

## Backend — Server (Node.js/Express)

### 6. Aceptar `fecha` opcional con fallback

```javascript
// ANTES: fecha hardcodeada a hoy()
sql_run('INSERT INTO ... fecha VALUES ?', [req.userId, hoy(), ...]);

// DESPUÉS: aceptar fecha del body, fallback a hoy()
const { fecha, hora, ... } = req.body;
sql_run('INSERT INTO ... fecha VALUES ?', [req.userId, fecha || hoy(), ...]);
```

El patrón `fecha || hoy()` garantiza retrocompatibilidad — clientes viejos que no envían fecha siguen funcionando.

### 7. Para UPSERT (INSERT OR UPDATE basado en fecha)

Cuando hay lógica de `SELECT ... WHERE usuario_id = ? AND fecha = ?`:

```javascript
const { fecha, ... } = req.body;
const f = fecha || hoy();
const existing = sql_get('SELECT id FROM pasos WHERE usuario_id = ? AND fecha = ?', [req.userId, f]);
if (existing) {
  sql_run('UPDATE pasos SET ... WHERE id=?', [...valores, existing.id]);
} else {
  sql_run('INSERT INTO pasos (usuario_id, fecha, ...) VALUES (?, ?, ...)', [req.userId, f, ...]);
}
```

## Pitfalls

- **No olvidar `today()` helper** — el input date necesita un valor por defecto. Si no se rellena, el campo sale vacío y el usuario no sabe qué día es.
- **`sv-SE` locale** — es el locale ISO (`YYYY-MM-DD`) que entienden los inputs `date` nativos. `toISOString().slice(0,10)` también funciona pero puede tener offset UTC.
- **Backwards compatibility** — la clave del patrón es `fecha || hoy()` en servidor. Sin eso, los clientes viejos que no envían `fecha` rompen.
- **La fecha editable en estimación** — si el usuario estima una comida para hoy pero quiere registrarla para ayer, necesita poder cambiar la fecha en la caja de edición. Añadir `ed-comida-fecha` y `ed-ejer-fecha` en el HTML de la estimación.
- **Pasos es UPSERT** — al añadir fecha a pasos, asegurarse de que el lookup `WHERE fecha = ?` usa la fecha recibida, no `hoy()`. Sin esto, los pasos de ayer se actualizarían sobre los de hoy.