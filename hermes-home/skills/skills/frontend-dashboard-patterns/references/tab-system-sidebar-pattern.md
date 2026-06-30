# Tab System con Sidebar — Patrón ContrataPúblico

**Fecha:** 2026-06-16
**Proyecto:** ContrataPúblico (Ley 9/2017)
**Stack:** HTML vanilla + Aurora CDN + Plotly CDN

## Estructura

Sistema de tabs con sidebar de navegación, hero section, lazy-loading, y persistencia de estado.

### HTML

```html
<!-- Sidebar con tabs -->
<aside class="nz-sidebar" id="sidebar">
  <div class="nz-sidebar__header">
    <div class="nz-sidebar__logo">⚖️</div>
    <div class="nz-sidebar__title">ContrataPúblico</div>
    <div class="nz-sidebar__subtitle">Ley 9/2017</div>
  </div>
  <nav class="nz-sidebar__nav">
    <a class="nz-sidebar__link" onclick="switchTab('mapa')" data-tab="mapa">
      <span class="nz-sidebar__icon">🗺️</span>
      <span class="nz-sidebar__label">Mapa de la Ley</span>
    </a>
    <!-- ... más tabs ... -->
  </nav>
</aside>

<!-- Main con tabs -->
<main class="nz-main">
  <!-- Hero -->
  <section class="nz-hero nz-hero--centered">
    <div class="nz-hero__inner">
      <div class="nz-hero__eyebrow">Herramienta de comprensión</div>
      <h1 class="nz-hero__title nz-gradient-text">⚖️ ContrataPúblico</h1>
      <!-- Stats + acciones -->
    </div>
  </section>
  
  <!-- Tab containers -->
  <div id="tab-mapa" class="tab-content" style="display:none">...</div>
  <div id="tab-tipos" class="tab-content" style="display:none">...</div>
  <!-- ... más tabs ... -->
</main>
```

### JS — switchTab con lazy-loading y persistencia

```javascript
var _loadedTabs = {};

function switchTab(tabName) {
  // Ocultar todas las tabs
  document.querySelectorAll('.tab-content').forEach(function(t) {
    t.style.display = 'none';
  });
  
  // Mostrar tab activa
  var target = document.getElementById('tab-' + tabName);
  if (target) target.style.display = 'block';
  
  // Actualizar sidebar highlight
  document.querySelectorAll('.nz-sidebar__link').forEach(function(link) {
    link.classList.remove('nz-sidebar__link--active');
    if (link.getAttribute('data-tab') === tabName) {
      link.classList.add('nz-sidebar__link--active');
    }
  });
  
  // Lazy load
  if (!_loadedTabs[tabName]) {
    _loadedTabs[tabName] = true;
    switch(tabName) {
      case 'mapa': renderMapa(); break;
      case 'texto': renderTextoCompleto(); break;
      case 'tipos': renderTiposContrato(); break;
    }
  }
  
  // Persistir última tab
  try { localStorage.setItem('cp_lastTab', tabName); } catch(e) {}
  
  window.scrollTo(0, 0);
}

// Init: restaurar última tab
document.addEventListener('DOMContentLoaded', function() {
  try {
    var lastTab = localStorage.getItem('cp_lastTab');
    if (lastTab) { switchTab(lastTab); return; }
  } catch(e) {}
  switchTab('texto'); // default
});
```

### JS — Toast notifications

```javascript
var _toastQueue = [];
var _toastActive = false;

function showToast(title, message, type, duration) {
  type = type || 'success';
  duration = duration || 4000;
  var icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  var icon = icons[type] || icons.info;
  var container = document.getElementById('cpToastContainer');
  if (!container) return;
  _toastQueue.push({ title: title, message: message, type: type, icon: icon, duration: duration });
  if (_toastActive) return;
  _showNextToast();
}

function _showNextToast() {
  if (_toastQueue.length === 0) { _toastActive = false; return; }
  _toastActive = true;
  var toastData = _toastQueue.shift();
  var container = document.getElementById('cpToastContainer');
  if (!container) return;
  var toast = document.createElement('div');
  toast.className = 'mf-toast mf-toast--' + toastData.type;
  toast.innerHTML = /* ... */;
  container.appendChild(toast);
  setTimeout(function() {
    if (toast.parentElement) {
      toast.style.animation = 'mfToastOut 0.3s forwards';
      setTimeout(function() {
        if (toast.parentElement) toast.remove();
        _showNextToast();
      }, 300);
    }
  }, toastData.duration);
}
```

## Reglas

1. **Cada tab container** debe tener `id="tab-NOMBRE"` y `class="tab-content"` con `display:none`
2. **Cada sidebar link** debe tener `data-tab="NOMBRE"` que coincida con el container
3. **Lazy loading** con `_loadedTabs` flag — cada tab se renderiza una sola vez
4. **Persistencia** en localStorage — restaurar última tab al cargar
5. **Toast container** debe existir fuera del contenido dinámico
6. **No usar `const`/`let`** si el proyecto usa `var` consistentemente

## HTML validation checklist

Antes de deploy, verificar:
1. Parens balanceados en `<script>`: `(` count === `)` count
2. Braces balanceados: `{` count === `}` count
3. `</html>` y `</body>` presentes
4. Todos los `data-tab` tienen su `tab-NOMBRE` correspondiente
5. `switchTab` existe como función (no solo event listener)
