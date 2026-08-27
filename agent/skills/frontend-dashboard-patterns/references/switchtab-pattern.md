# switchTab Pattern — onclick + event listener

**Fecha:** 2026-06-13
**Proyecto:** MasterFit (dieta-masterfit)

## Problema

Los botones del hero usaban `onclick="switchTab('registrar')"` pero `switchTab` no existía como función. Solo había un event listener en `.nz-nav-item` que manejaba los tabs de navegación. Los `<a>` del hero no son `.nz-nav-item`, así que el event listener no les aplicaba.

## Síntomas

- Botones visibles en el hero
- Al hacer clic, no pasa nada
- La navegación por la barra inferior funciona (event listener)
- La consola no muestra errores (onclick falla silenciosamente)

## Causa

El event listener `document.querySelectorAll('.nz-nav-item').forEach(...)` solo aplica a elementos con clase `.nz-nav-item`. Los botones del hero son `<a>` tags sin esa clase, así que el event listener no los alcanza.

## Solución

Crear la función `switchTab()` que hace lo mismo que el event listener:

```javascript
function switchTab(tabName) {
  // Desactivar todos los tabs
  document.querySelectorAll('.nz-nav-item').forEach((t) => {
    t.classList.remove('is-active');
  });
  // Ocultar todos los paneles
  document.querySelectorAll('[id^="tab-"]').forEach((p) => {
    p.style.display = 'none';
  });
  // Activar el tab seleccionado
  const targetTab = document.querySelector('[data-tab="' + tabName + '"]');
  if (targetTab) targetTab.classList.add('is-active');
  const targetDiv = document.getElementById('tab-' + tabName);
  if (targetDiv) targetDiv.style.display = '';
  
  // Lazy load progreso
  if (tabName === 'progreso') {
    const el = document.getElementById('tab-progreso');
    if (el && !el.getAttribute('data-loaded')) {
      loadProgreso();
      el.setAttribute('data-loaded', '1');
    }
  }
}
```

## Patrón de hero correcto

El hero debe ser **compacto** (solo título + objetivo). Los datos rápidos y acciones van en la tab donde tienen sentido:

```html
<!-- HERO: solo branding + objetivo -->
<section class="nz-hero nz-hero--centered">
  <div class="nz-hero__inner">
    <div class="nz-hero__eyebrow">Dashboard de seguimiento</div>
    <h1 class="nz-hero__title nz-gradient-text">🏋️ MasterFit</h1>
    <p class="nz-hero__sub">Objetivo: <strong id="headerObjetivo">78.5 kg</strong></p>
  </div>
</section>

<!-- TAB REGISTRAR: quick panel con datos + acciones -->
<div id="tab-registrar">
  <!-- Quick Panel con datos reales -->
  <div class="nz-card nz-card--glass-liquid">
    <div>📊 Tu progreso</div>
    <div style="display:flex;gap:var(--nz-space-2);">
      <div class="nz-surface">
        <div>⚖️ Peso</div>
        <div id="heroPeso">--</div>
      </div>
      <div class="nz-surface">
        <div>📉 Perdido</div>
        <div id="heroPerdido">--</div>
      </div>
      <div class="nz-surface">
        <div>🔥 Ritmo</div>
        <div id="heroRitmo">--</div>
      </div>
    </div>
    <!-- Acciones rápidas -->
    <a class="nz-btn nz-btn--glass-liquid-brand" onclick="switchTab('registrar')">➕ Registrar</a>
    <a class="nz-btn nz-btn--glass-liquid-accent" onclick="switchTab('ia')">🤖 Hablar con IA</a>
  </div>
</div>
```

## Reglas

1. **NUNCA confiar solo en event listeners** — si hay `onclick="switchTab(...)"` en el HTML, la función DEBE existir
2. **Hero compacto** — solo título + objetivo. No mostrar datos en el hero
3. **Quick panel en tab-registrar** — donde tiene sentido mostrar progreso + acciones
4. **switchTab() debe replicar el event listener** — no hacer algo diferente
5. **Poblar datos en renderDashboard()** — actualizar heroPeso, heroPerdido, heroRitmo después de calcular

## Verificación

```python
with open('dashboard.html', 'r') as f:
    content = f.read()
# switchTab como función
assert 'function switchTab' in content, "switchTab no existe como función"
# Los onclick usan switchTab
assert "switchTab('registrar')" in content, "Botón registrar no tiene switchTab"
assert "switchTab('ia')" in content, "Botón IA no tiene switchTab"
```
