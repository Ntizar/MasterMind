# Multi-Proyecto Audit & Unificación con Aurora

## Procedimiento

1. **Auditar:** `python3 audit-aurora.py <archivo.html>` en cada proyecto
2. **Leer HTML en bloques:** 500 líneas por lectura (archivos grandes)
3. **Verificación visual:** `browser_vision` para confirmar diseño actual
4. **Patch incremental:** Reemplazar `<head>`, estructura HTML, CSS custom, clases sidebar. NO reescribir todo. Mantener JS intacto.
5. **Auditar post-patch:** CSS custom <70 líneas, packs Aurora >=7, body nz/theme/skin PASS
6. **Verificación visual post-rediseño:** Confirmar consistencia entre proyectos
7. **Commit:** Solo archivos relevantes. NO data/, node_modules/, ZIPs.

## Pitfalls

- Archivos >100KB: subagentes fallan. Hacer patches manuales con `patch` tool.
- Git push OOM: repo con datos grandes → commit solo código. ZIPs en .gitignore.
- ZIPs en staging aunque estén en .gitignore: `git reset HEAD` antes de commit.
- No romper JS: solo CSS/HTML layout.

## ⚠️ Layout Aurora: nz-app-shell correcto (2026-06-23)

Cuando se aplica Aurora a un proyecto existente, el layout `nz-app-shell` debe seguir ESTRICTAMENTE esta estructura:

```html
<body class="nz" data-nz-theme="light" data-nz-skin="aurora">
<div class="nz-app-shell">  <!-- flex column, flex:1, min-height:0 -->
  <header class="nz-app-shell__header">...</header>  <!-- flex-shrink:0 -->
  <div class="nz-app-shell__body">  <!-- flex row, flex:1, min-height:0 -->
    <div class="nz-app-shell__sidebar">  <!-- flex: 0 0 380px -->
      <div class="sidebar">  <!-- display: block !important (Aurora puede setear flex-direction: row) -->
        ...
      </div>
    </div>  <!-- CERRAR sidebar ANTES de main -->
    <div class="nz-app-shell__main">  <!-- flex: 1, min-width: 0 -->
      <div id="map"></div>  <!-- flex: 1, min-height: 0, width: 100% -->
    </div>
  </div>  <!-- CERRAR body -->
</div>  <!-- CERRAR shell -->
<footer class="nz-footer">...</footer>  <!-- FUERA del shell, height: 44px -->
```

**Errores comunes que rompen el mapa:**

1. **`nz-app-shell__main` DENTRO de `nz-app-shell__sidebar`**: El `</div>` que cierra el sidebar interno también cierra el body. El main queda anidado en el sidebar en vez de ser hermano. **Solución:** cerrar `.sidebar` y `.nz-app-shell__sidebar` ANTES de abrir `.nz-app-shell__main`.

2. **Footer dentro del shell**: El footer empuja el body y reduce la altura del mapa. **Solución:** footer FUERA del shell, con `height: 44px; min-height: 44px; max-height: 44px; overflow: hidden` para evitar que Aurora le dé altura enorme.

3. **Sidebar sin `flex: 0 0 380px`**: El sidebar se encoge cuando su contenido interno es alto. **Solución:** `flex: 0 0 380px` + `overflow-y: auto`.

4. **`.sidebar` interno con `flex-direction: row`**: Aurora puede setear `display: flex; flex-direction: row` en el contenedor interno del sidebar, rompiendo el layout vertical. **Solución:** `.sidebar { display: block !important; flex-direction: column !important }`.

5. **Mapa sin `flex: 1`**: Leaflet necesita que el contenedor tenga dimensiones conocidas. **Solución:** `#map { flex: 1; min-height: 0; width: 100% }` + `map.invalidateSize()` tras init.

6. **`nz-app-shell` sin `flex: 1`**: Si el shell tiene `height: 100vh` en vez de `flex: 1`, no se adapta al body flex. **Solución:** `body { display: flex; flex-direction: column; height: 100vh }` + `.nz-app-shell { flex: 1; min-height: 0 }`.

**Verificación post-layout:** Usar `browser_console` para verificar dimensiones:
```js
JSON.stringify({
  bodyW: getComputedStyle(document.querySelector('.nz-app-shell__body')).width,
  sbW: getComputedStyle(document.querySelector('.nz-app-shell__sidebar')).width,
  mnW: getComputedStyle(document.querySelector('.nz-app-shell__main')).width,
  mapW: getComputedStyle(document.getElementById('map')).width,
  footerH: getComputedStyle(document.querySelector('.nz-footer')).height
})
// mnW debe ser ~bodyW - sbW (ej: 1280 - 380 = 900px)
// footerH debe ser ~44px
```