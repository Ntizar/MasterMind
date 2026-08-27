# CSS-only Dropdown con :has() — Patrón Checkbox Hack

Patrón implementado en Ntizar-Aurora mejora #15 (2026-06-01) para hacer dropdowns completamente CSS sin JavaScript.

## Estructura HTML

```html
<div class="nz-dropdown">
  <input type="checkbox" class="nz-dropdown__toggle" id="dd-toggle-1">
  <label class="nz-btn nz-btn--secondary" for="dd-toggle-1">Acciones ▾</label>
  <div class="nz-dropdown__menu">
    <button class="nz-dropdown__item">Editar</button>
    <button class="nz-dropdown__item">Duplicar</button>
    <div class="nz-dropdown__sep"></div>
    <button class="nz-dropdown__item nz-dropdown__item--danger">Eliminar</button>
  </div>
</div>
```

## CSS clave

```css
/* Checkbox oculto — estado del dropdown */
.nz-dropdown__toggle {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}

/* :has() — checkbox checked = menú abierto */
.nz-dropdown:has(> .nz-dropdown__toggle:checked) > .nz-dropdown__menu {
  display: flex;
}

/* :has() — hover abre como alternativa */
.nz-dropdown:hover > .nz-dropdown__menu { display: flex; }

/* :has() — hover en menú lo mantiene abierto */
.nz-dropdown:has(> .nz-dropdown__menu:hover) > .nz-dropdown__menu { display: flex; }

/* Compatibilidad JS: .is-open y [open] siguen funcionando */
.nz-dropdown__menu.is-open,
.nz-dropdown[open] > .nz-dropdown__menu { display: flex; }
```

## Limitaciones

- **Escape key:** No se puede detectar en CSS puro. El usuario debe hacer clic fuera o usar hover.
- **Click fuera:** No se cierra automáticamente (limitación CSS). El hover es la alternativa.
- **Submenús anidados:** No soportados con este patrón simple.

## Compatibilidad

- `:has()` — Chrome 105+, Firefox 121+, Safari 15.4+
- Aurora v5+ ya requiere navegadores modernos, así que no hay problema de compatibilidad.

## Referencias

- Implementación real: `/root/workspace/Ntizar-Aurora/ntizar.ui.css` líneas 472-570
- Demo en: `/root/workspace/Ntizar-Aurora/gallery.html`
- Plan 9009: `/root/workspace/Mastermind/notes/9009-ntizar-aurora-plan.md` mejora #15
