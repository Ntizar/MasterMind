# Hero Redesign Pattern — Dashboard First Screen

**Fecha:** 2026-06-13
**Proyecto:** MasterFit (dieta-masterfit)
**Problema:** El hero del dashboard mostraba solo "Dashboard de seguimiento", "MasterFit", "Objetivo: 88 kg" y avatar DA. Cero datos reales, cero acciones rápidas. Desde el móvil se veía un espacio vacío sin información útil.

## Solución

Reemplazar el hero vacío con:
1. **Quick Status** (3 tarjetas horizontales): Peso actual, kg perdidos, ritmo semanal
2. **Acciones rápidas**: Botón "➕ Registrar" (azul brand) y "🤖 Hablar con IA" (naranja accent)

## Implementación

### HTML del hero nuevo
```html
<section class="nz-hero nz-hero--centered">
  <div class="nz-hero__inner">
    <div class="nz-hero__eyebrow">Dashboard de seguimiento</div>
    <h1 class="nz-hero__title nz-gradient-text">🏋️ MasterFit</h1>
    <p class="nz-hero__sub">Objetivo: <strong style="color:var(--nz-color-brand);" id="headerObjetivo">88 kg</strong></p>
    
    <!-- Quick Status -->
    <div id="heroQuickStatus" style="margin-top:var(--nz-space-3);display:flex;gap:var(--nz-space-2);justify-content:center;flex-wrap:wrap;">
      <div class="nz-surface nz-surface--glass-soft" style="padding:var(--nz-space-2) var(--nz-space-3);border-radius:var(--nz-radius-lg);text-align:center;min-width:100px;">
        <div style="font-size:var(--nz-size-xs);color:var(--nz-text-muted);">⚖️ Peso</div>
        <div style="font-size:var(--nz-size-xl);font-weight:700;color:var(--nz-color-brand);" id="heroPeso">--</div>
      </div>
      <div class="nz-surface nz-surface--glass-soft" style="padding:var(--nz-space-2) var(--nz-space-3);border-radius:var(--nz-radius-lg);text-align:center;min-width:100px;">
        <div style="font-size:var(--nz-size-xs);color:var(--nz-text-muted);">📉 Perdido</div>
        <div style="font-size:var(--nz-size-xl);font-weight:700;color:var(--nz-color-success);" id="heroPerdido">--</div>
      </div>
      <div class="nz-surface nz-surface--glass-soft" style="padding:var(--nz-space-2) var(--nz-space-3);border-radius:var(--nz-radius-lg);text-align:center;min-width:100px;">
        <div style="font-size:var(--nz-size-xs);color:var(--nz-text-muted);">🔥 Ritmo</div>
        <div style="font-size:var(--nz-size-xl);font-weight:700;color:var(--nz-color-accent);" id="heroRitmo">--</div>
      </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="nz-hero__cta nz-cluster nz-cluster--center" style="margin-top:var(--nz-space-3);">
      <a class="nz-btn nz-btn--glass-liquid-brand" onclick="switchTab('registrar');return false;" style="padding:12px 24px;font-size:var(--nz-size-sm);">
        ➕ Registrar
      </a>
      <a class="nz-btn nz-btn--glass-liquid-accent" onclick="switchTab('ia');return false;" style="padding:12px 24px;font-size:var(--nz-size-sm);">
        🤖 Hablar con IA
      </a>
    </div>
  </div>
</section>
```

### JS para poblar los datos
```javascript
// En renderDashboard(), después de actualizar headerObjetivo:
const hPeso = document.getElementById('heroPeso');
const hPerdido = document.getElementById('heroPerdido');
const hRitmo = document.getElementById('heroRitmo');
if (hPeso) hPeso.textContent = pesoActual + ' kg';
if (hPerdido) hPerdido.textContent = '+' + perdido.toFixed(1) + ' kg';
if (hRitmo) hRitmo.textContent = ritmoResult.icon + ' ' + ritmoResult.ritmo.toFixed(1) + '/sem';
```

### CSS móvil
```css
@media (max-width:768px) {
  #heroQuickStatus { flex-direction: column; gap: 6px; }
  #heroQuickStatus > * { min-width: auto; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 8px 12px !important; }
  #heroQuickStatus > * > div:first-child { font-size: var(--nz-size-2xs); }
  #heroQuickStatus > * > div:last-child { font-size: var(--nz-size-lg); }
  .nz-hero__cta .nz-btn { padding: 10px 16px !important; font-size: var(--nz-size-sm) !important; }
}
```

## Principio reutilizable

**Primera pantalla = valor inmediato.** Un dashboard en móvil debe mostrar en la primera pantalla:
1. **Datos reales** (no placeholders) — peso, progreso, ritmo
2. **Acciones directas** — registrar, consultar IA
3. **Sin scroll** — todo visible sin bajar

Si el hero no aporta nada, rediseñarlo para que muestre lo esencial.
