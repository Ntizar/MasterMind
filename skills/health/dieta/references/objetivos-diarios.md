# Objetivos de Hoy — Comparativa de Progreso Diario

**Fecha:** 2026-06-14
**Versión:** v4.0.3

## Patrón

Añadir una sección de "Objetivos de Hoy" en el dashboard que muestra el % de cumplimiento de todas las métricas clave del día en un grid visual de tarjetas.

## Estructura

### Grid de 6 tarjetas
Cada tarjeta muestra:
- Icono emoji + nombre de la métrica
- Valor actual vs objetivo (ej: "2.100 / 2.600 kcal")
- Porcentaje de cumplimiento con color dinámico
- Indicador de cantidad restante o exceso
- Barra de progreso

### Colores dinámicos
- ✅ Verde (`#22c55e`) → >=100% cumplimiento
- 🔵 Azul (`#2563eb`) → >=60% cumplimiento
- 🟠 Naranja (`#f97316`) → <60% cumplimiento

### Métricas incluidas
1. 🔥 Calorías — % vs TDEE calculado
2. 🥩 Proteínas — % vs objetivo (40% de TDEE)
3. 💧 Agua — % vs 2000ml
4. 🍞 Hidratos — % vs objetivo (35% de TDEE)
5. 🥑 Grasas — % vs objetivo (25% de TDEE)
6. 🚶 Pasos — % vs 10.000

## Implementación

### 1. HTML — Grid de tarjetas

```javascript
// En renderResumen(), antes de las barras de macros:
var html = '<div class="nz-section-header"><h2>🎯 Objetivos de Hoy</h2></div>';
html += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px">';

// Para cada métrica:
html += '<div class="nz-card--glass-liquid nz-hover-lift" style="padding:12px;text-align:center">';
html += '<div style="font-size:1.8rem;margin-bottom:4px">' + icono + '</div>';
html += '<div style="font-size:.85rem;color:var(--nz-text-secondary);margin-bottom:4px">' + nombre + '</div>';
html += '<div style="font-size:1.4rem;font-weight:700">' + porcentaje + '%</div>';
html += '<div style="font-size:.75rem;color:var(--nz-text-secondary);margin-top:2px">' + detalle + '</div>';
html += '<div style="margin-top:8px;height:6px;background:var(--nz-bg-tertiary);border-radius:3px;overflow:hidden">';
html += '<div style="height:100%;width:' + porcentaje + '%;background:' + color + ';border-radius:3px;transition:width .5s"></div>';
html += '</div></div>';

html += '</div>';
```

### 2. Cálculo de porcentajes

```javascript
function calcularProgreso(actual, objetivo) {
  if (!objetivo || objetivo <= 0) return { pct: 0, color: '#f97316', detalle: 'Sin objetivo' };
  var pct = Math.min(100, Math.round(actual / objetivo * 100));
  var color = pct >= 100 ? '#22c55e' : pct >= 60 ? '#2563eb' : '#f97316';
  var detalle = actual >= objetivo 
    ? '✅ Completado' 
    : (objetivo - actual).toFixed(actual > 100 ? 0 : 1) + ' restantes';
  return { pct, color, detalle };
}
```

### 3. Integración con datos existentes

- Leer datos del día actual desde las APIs existentes (`/api/datos`)
- Calcular TDEE con Mifflin-St Jeor (ya implementado en server.js)
- Leer macros del día actual desde `comidas` del día
- Leer agua desde `agua` del día
- Leer pasos desde `pasos` del día

## Reglas

- **NUNCA inventar datos** — si no hay datos del día, mostrar "0" con color naranja
- **NUNCA hardcodear objetivos** — leer de `meta` o `perfil`
- **TDEE dinámico** — recalcular si cambia el peso
- **Responsive** — grid `auto-fit, minmax(160px, 1fr)` para móvil/desktop

## TDEE Mifflin-St Jeor

```
TMB = 10 × peso(kg) + 6.25 × altura(cm) - 5 × edad(años) + 5  // hombre
TMB = 10 × peso(kg) + 6.25 × altura(cm) - 5 × edad(años) - 161 // mujer
TDEE = TMB × factor_actividad
  - Sedentario: × 1.2
  - Ligero: × 1.375
  - Moderado: × 1.55
  - Muy activo: × 1.725
```

## Pitfalls

- **No duplicar código de TDEE** — usar la función `calcularTDEE()` que ya existe en dashboard.html
- **No olvidar el dark mode** — añadir reglas CSS `body.mf-dark` para las nuevas tarjetas
- **No romper el orden del DOM** — insertar la sección ANTES de las barras de macros existentes
- **No usar `const charts`** — seguir patrón `var charts = window.charts = {}`
