# Formulario Inteligente — Validación en Vivo + Auto-cálculo

**Aprendido en:** Sesión 7, ContrataPúblico (2026-06-16)
**Reutilizable en:** Cualquier módulo con formulario en SPA single-file

## Patrón

Un formulario con validación visual en tiempo real y auto-cálculo de campos derivados.

### 1. CSS (en index.html)

```css
.cp-field-error {
  border-color: var(--nz-color-accent) !important;
  box-shadow: 0 0 0 3px rgba(192,57,43,0.15) !important;
}
.cp-field-success {
  border-color: #27ae60 !important;
  box-shadow: 0 0 0 3px rgba(39,174,96,0.1) !important;
}
.cp-validation-summary {
  padding: 12px 16px;
  border-radius: 10px;
  margin-bottom: 16px;
  font-size: 0.85rem;
}
.cp-validation-summary.error {
  background: rgba(192,57,43,0.08);
  border: 1px solid rgba(192,57,43,0.2);
  color: #c0392b;
}
.cp-validation-summary.success {
  background: rgba(39,174,96,0.08);
  border: 1px solid rgba(39,174,96,0.2);
  color: #27ae60;
}
.cp-auto-calc {
  font-size: 0.75rem;
  color: var(--nz-color-brand);
  margin-top: 4px;
  font-style: italic;
}
```

### 2. HTML del formulario

```html
<form id="actaForm" onsubmit="return false;">
  <div id="cpValidationSummary"></div>
  <div class="cp-acta-fields">
    <!-- campos generados por JS -->
  </div>
  <!-- botones -->
</form>
```

### 3. JS — Live validation listeners (al final de renderActaForm)

```javascript
// Live validation: highlight fields as user types
var campos = acta.campos;
for (var i = 0; i < campos.length; i++) {
  (function(campo) {
    var el = document.getElementById('acta_' + campo.id);
    if (!el) return;
    el.addEventListener('input', function() {
      var val = el.value.trim();
      if (campo.obligatorio && val) {
        el.classList.remove('cp-field-error');
        el.classList.add('cp-field-success');
      } else if (!campo.obligatorio && val) {
        el.classList.remove('cp-field-error');
        el.classList.remove('cp-field-success');
      } else if (campo.obligatorio && !val) {
        el.classList.remove('cp-field-success');
      }
      // Auto-calculate percentage for modificacion
      if (campo.id === 'porcentajeVariacion') {
        var impIni = document.getElementById('acta_importeInicial');
        var impMod = document.getElementById('acta_importeModificado');
        if (impIni && impMod && impIni.value && impMod.value) {
          var pct = ((parseFloat(impMod.value) - parseFloat(impIni.value)) / parseFloat(impIni.value) * 100).toFixed(2);
          el.value = pct;
        }
      }
    });
  })(campos[i]);
}
```

### 4. JS — Validación al generar

```javascript
// Validate and collect
var camposObligatorias = [];
for (var i = 0; i < acta.campos.length; i++) {
  var campo = acta.campos[i];
  var el = document.getElementById('acta_' + campo.id);
  if (!el) continue;
  datos[campo.id] = el.value.trim();
  if (campo.obligatorio && !datos[campo.id]) {
    camposObligatorias.push(campo.label);
    el.classList.add('cp-field-error');
  }
}

if (camposObligatorias.length > 0) {
  var summary = document.getElementById('cpValidationSummary');
  if (summary) {
    summary.innerHTML = '<div class="cp-validation-summary error">⚠️ Faltan ' +
      camposObligatorias.length + ' campo(s): ' +
      camposObligatorias.join(', ') + '</div>';
  }
  return;
}

// Clear validation summary on success
var summary = document.getElementById('cpValidationSummary');
if (summary) {
  summary.innerHTML = '<div class="cp-validation-summary success">✅ Todos los campos obligatorios completados</div>';
}
```

## Reglas

- Usar `var` no `const` para variables DOM (window scope)
- Los listeners se crean en `renderActaForm`, no en `DOMContentLoaded`
- El auto-cálculo es opcional: solo para campos derivados
- El resumen de validación es opcional: útil cuando hay muchos campos
