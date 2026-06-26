# Patrón: Módulos JS lazy-load en SPA single-file

**Aprendido:** 2026-06-16, Sesión 6 de ContrataPúblico
**Contexto:** Proyecto con 10 tabs, cada tab es un módulo independiente. `index.html` es el orquestador.

## Problema

Un proyecto SPA con 10+ módulos en un solo `index.html` se vuelve inmanejable. Cada módulo nuevo requiere:
- Añadir HTML en el tab content
- Añadir CSS inline
- Añadir JS inline
- El archivo crece sin control

## Solución: Módulos en `js/modules/`

### Estructura

```
index.html                    ← Orquestador: tabs, navegación, lazy-load
js/
├── ley-data.js              ← Datos compartidos
└── modules/
    ├── generador-actas.js   ← Tab 4
    ├── procedimientos.js    ← Tab 3 (Sesión 7)
    └── ...
```

### Pasos para añadir un nuevo módulo

1. **Crear `js/modules/NOMBRE.js`** con IIFE:
   ```javascript
   (function() {
     'use strict';
     var _state = {};
     window.renderNombre = function() { ... };
     window.publicaFuncion = function() { ... };
   })();
   ```

2. **Añadir script tag en `<head>`** de index.html:
   ```html
   <script src="js/modules/NOMBRE.js"></script>
   ```

3. **Añadir lazy load en `switchTab()`**:
   ```javascript
   case 'nombre': renderNombre(); break;
   ```

4. **Añadir CSS inline** en `<style>` de index.html (no archivos externos)

5. **Añadir `<div id="tab-nombre">`** con placeholder en index.html

### Reglas

- **IIFE siempre** — no contaminar el scope global
- **`var` para state** — no `const` (window scope para que otros módulos accedan)
- **CSS inline** — no archivos externos (single-file deploy)
- **Lazy load** — renderizar solo al primer acceso
- **Máximo 50KB por módulo** — si es más, dividir

### Casos de uso

- Proyectos con 5+ tabs/módulos
- Dashboards con navegación por pestañas
- Herramientas web con funcionalidades independientes
