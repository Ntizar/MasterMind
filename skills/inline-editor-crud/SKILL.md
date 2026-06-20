---
name: inline-editor-crud
version: "1.0"
description: Patrón de modal overlay para editar registros in-situ en listas/grillas de frontend
---

# Inline Editor CRUD — Modal de edición en el lugar

## Cuándo usarlo

Tienes una lista/grilla de registros en un frontend y necesitas que el usuario pueda editarlos sin recargar la página ni navegar a un formulario aparte.

## Patrón

Cada registro tiene un botón `✏️` que abre un **modal overlay** creado en JS puro:

```js
var overlay = document.createElement('div');
overlay.className = 'edit-modal';
overlay.innerHTML = '<div class="edit-modal-card">...<button class="em-save">Guardar</button></div>';
document.body.appendChild(overlay);
```

### Estructura del modal

```html
<div class="edit-modal">          <!-- overlay fullscreen con backdrop-filter -->
  <div class="edit-modal-card">    <!-- tarjeta blanca centrada -->
    <h3>✏️ Editar [tipo]</h3>
    <label>📅 Fecha</label><input type="date">
    <label>🕐 Hora</label><input type="time">
    <!-- campos específicos del tipo de registro -->
    <div class="em-actions">
      <button class="em-cancel">Cancelar</button>
      <button class="em-save">Guardar</button>
    </div>
  </div>
</div>
```

### Funcionalidad

- **Abrir modal:** `editEntry(tipo, index)` — busca el registro en los datos cargados (`loadDatos()`), construye el HTML con los valores actuales
- **Cerrar:** Click en el fondo del overlay → `e.target === overlay` → `overlay.remove()`
- **Guardar:** `onclick` del botón → lee valores de los inputs → `await api('/api/' + tipo + '/' + index, { method: 'PUT', body: body })` → refresca la lista

### Servidor

El endpoint `PUT` debe aceptar dinámicamente los campos que llegan. En Node.js:

```js
const COLUMNS = {
  peso: ['fecha','hora','peso_kg','notas'],
  comidas: ['fecha','hora','tipo','descripcion','kcal','proteinas_g','...'],
  // ...
};
const allowed = Object.keys(req.body).filter(k => COLUMNS[tipo].includes(k));
```

### CSS clave

```css
.edit-modal{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.4);backdrop-filter:blur(4px)}
.edit-modal-card{background:#fff;border-radius:16px;padding:24px;max-width:420px;width:90%;max-height:85vh;overflow-y:auto}
```

### Pitfalls

- **No duplicar `id` de elementos** — cada modal se crea desde 0, no hay conflicto si se borra antes de abrir otro
- **Los inputs `date` necesitan `text-align:left`** o se ven centrados horriblemente en móvil
- **Refrescar la lista** después de guardar: `appState.tabRendered[X] = false` + volver a renderizar
- **El modal no debe tener `onclick` que cierre si clickas dentro** — el truco es `if (e.target === overlay)` en el overlay, no en el card