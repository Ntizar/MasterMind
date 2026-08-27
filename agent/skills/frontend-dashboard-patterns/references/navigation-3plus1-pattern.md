# 3+1 Navigation Pattern (Mobile-First)

Para apps con muchas funcionalidades (7+ tabs), reorganizar en **3 tabs principales** + menú overflow "☰ Más".

## Por qué funciona

- **Cognitiva:** 3 tabs es el máximo que un usuario puede retener sin pensar
- **Mobile:** Los tabs principales caben en pantalla sin scroll horizontal
- **Acción:** Los 3 tabs representan las acciones más frecuentes

## Estructura recomendada

```
┌─────────────────────────────────────┐
│  [Logo]                 [Iconos ↑]  │  ← Header
├─────────────────────────────────────┤
│                                     │
│         CONTENIDO DEL TAB           │
│                                     │
├─────────────────────────────────────┤
│  [Registrar]  [Coach]  [Proy]  [☰] │  ← Bottom nav
└─────────────────────────────────────┘
```

### Los 3 tabs principales
1. **Registrar/Acción** — La acción más frecuente (registrar peso, comida, ejercicio)
2. **Interacción/IA** — Chat con asistente o coach
3. **Visualización** — Dashboard, gráficas, proyecciones

### El overflow "☰ Más"
Contiene las funciones secundarias:
- Historial completo
- Configuración/Perfil
- Exportar datos
- Progreso detallado
- Cualquier cosa que no sea diaria

## Implementación HTML

```html
<nav class="bottom-nav">
  <button class="nav-tab active" onclick="switchTab('registrar')">✏️ Registrar</button>
  <button class="nav-tab" onclick="switchTab('coach')">🤖 Coach</button>
  <button class="nav-tab" onclick="switchTab('proyecciones')">📊 Proyecciones</button>
  <button class="nav-tab" onclick="showOverflowMenu()">☰ Más</button>
</nav>

<!-- Overflow menu (modal) -->
<div id="overflowMenu" class="overflow-menu" style="display:none">
  <button onclick="switchTab('resumen')">📋 Resumen</button>
  <button onclick="switchTab('historial')">📜 Historial</button>
  <button onclick="switchTab('exportar')">📥 Exportar</button>
  <button onclick="switchTab('config')">⚙️ Configuración</button>
</div>
```

## Lazy Loading

Los tabs overflow solo cargan datos cuando se activan por primera vez:

```javascript
var loadedTabs = new Set();

function switchTab(tabId) {
  // ... render tab ...
  if (!loadedTabs.has(tabId)) {
    loadTabData(tabId);
    loadedTabs.add(tabId);
  }
}
```

## Persistencia de Sesión

Almacenar `sessionId` en `localStorage` y añadirlo a todas las llamadas fetch:

```javascript
function apiFetch(url, options) {
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-Session-Id': localStorage.getItem('session_id'),
      'Content-Type': 'application/json'
    }
  });
}
```
