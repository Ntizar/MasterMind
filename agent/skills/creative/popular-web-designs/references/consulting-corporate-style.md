# Estilo Corporativo / Consulting (McKinsey, BCG, Ineco)

> Patrón de diseño para presentaciones HTML de caso de negocio, propuestas comerciales y informes ejecutivos.
> Fondo BLANCO SIEMPRE. Sin glass, sin mesh, sin gradientes, sin dark mode.

## Cuándo usar
- Presentaciones internas de empresa (Kaizen, propuestas, roadmap)
- Informes ejecutivos con datos y tablas
- Casos de negocio / ROI analysis
- El usuario pide "fondo blanco", "corporativo", "elegante", "no parezca IA"

## Cuándo NO usar
- Dashboards interactivos → usar `aurora-design-system`
- Landing pages creativas → usar `claude-design`
- El usuario pide glass, mesh, dark, aurora → seguir sus instrucciones

## Paleta de colores

```css
:root {
  --blue: #2563eb;
  --blue-light: #eff6ff;
  --green: #059669;
  --green-light: #ecfdf5;
  --red: #dc2626;
  --red-light: #fef2f2;
  --amber: #d97706;
  --amber-light: #fffbeb;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
}
```

## Tipografía
- **Fuente:** Inter (Google Fonts)
- **Pesos:** 300-900, usar 400-700 para cuerpo, 700-800 para títulos
- **Títulos:** `clamp(1.8rem, 3.5vw, 2.6rem)`, font-weight 800, letter-spacing -0.02em
- **Cuerpo:** 0.88-1.05rem, color gray-500 o gray-600
- **Labels:** 0.68-0.75rem, uppercase, letter-spacing 0.06-0.12em, font-weight 600-700

## Estructura de secciones

```
Section (padding: 5rem 2rem)
  Container (max-width: 1060px, margin: 0 auto)
    Section Label → "01 · Nombre"
    Section Title → h2
    Section Sub → p (max-width: 600px)
    Grid content
```

## Componentes

### KPI Tiles
```html
<div class="kpi">
  <div class="kpi-value green">47,50€</div>
  <div class="kpi-label">Coste real con TimeIneco</div>
</div>
```

### Tablas
```html
<div class="table-wrap">
  <table>
    <thead><tr><th>Columna</th></tr></thead>
    <tbody><tr><td>Dato</td></tr></tbody>
  </table>
</div>
```
- Bordes: 1px solid gray-200
- Border-radius: 12px en el wrapper
- Hover: background gray-50

### Cards
```html
<div class="card card-accent">  <!-- borde izquierdo azul -->
<div class="card card-green">   <!-- fondo green-light -->
<div class="card card-red">     <!-- fondo red-light -->
<div class="card card-blue">    <!-- fondo blue-light -->
```

### Steps / Proceso
```html
<div class="step">
  <div class="step-num">1</div>
  <div class="step-content">
    <h4>Título</h4>
    <p>Descripción</p>
    <div class="step-time">⏱ Tiempo</div>
  </div>
</div>
```

### Callouts
```html
<div class="callout callout-blue">Dato importante</div>
<div class="callout callout-green">Resultado positivo</div>
<div class="callout callout-amber">Advertencia</div>
```

### Tags
```html
<span class="tag tag-blue">Etiqueta</span>
<span class="tag tag-green">Resultado</span>
```

### Investment Rows
```html
<div class="invest-row">
  <div class="invest-pct">5%</div>
  <div class="invest-info">
    <h4>Título</h4>
    <p>Descripción</p>
  </div>
</div>
```

## Estructura típica de presentación corporativa

1. **Hero** → Título + KPI tiles (4 columnas)
2. **Problema** → Comparación lado a lado (card-red vs card-green)
3. **Ejemplo Real** → Informe embebido con tablas de datos reales
4. **Modelo de Negocio** → % inversión + ejemplo numérico + proyección 3 años
5. **Por Qué** → Bloques con número grande (01, 02, 03...) a la izquierda + título y texto a la derecha. **NO usar cards con iconito+titulo+texto** (patrón IA clásico)
6. **Inversión** → Desglose costes + retorno + roadmap 3 fases
7. **Cierre** → KPI tiles + frase potente

### ❌ Patrón RECHAZADO — "Cards IA" (icon + título + texto)

David rechazó explícitamente el patrón de cards con icono arriba + título + párrafo debajo. Lo describió como "la línea esa típica de la IA". Es el patrón más recognizable de HTML generado por IA y David lo asocia directamente con falta de originalidad.

```html
<!-- ❌ ESTO NO — patrón IA clásico -->
<div class="grid-3">
  <div class="card">
    <div style="font-size:1.8rem">🎯</div>
    <h3>Los clientes exigen velocidad</h3>
    <p>Un ayuntamiento no puede esperar...</p>
  </div>
</div>
```

### ✅ Patrón ACEPTADO — "Bloques numerados"

Número grande gris a la izquierda, título bold + texto a la derecha. Sin iconos, sin cards separadas, sin bordes decorativos. Fluye como una lista editorial.

```html
<!-- ✅ ESTO SÍ — bloques numerados -->
<div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:1.5rem;">
  <div class="arg-block">
    <div class="arg-num">01</div>
    <div class="arg-body">
      <h4>Los clientes exigen velocidad</h4>
      <p>Un ayuntamiento no puede esperar 3 meses...</p>
    </div>
  </div>
  <!-- más argumentos -->
</div>
```

```css
.arg-block { display: flex; gap: 1.2rem; align-items: flex-start; padding: 1rem 0; border-bottom: 1px solid var(--gray-100); }
.arg-num { font-size: 1.6rem; font-weight: 900; color: var(--gray-200); min-width: 40px; text-align: right; }
.arg-body h4 { font-size: 0.92rem; font-weight: 700; }
.arg-body p { font-size: 0.84rem; color: var(--gray-500); }
```

### ✅ Patrón ACEPTADO — "Invest split" (mitad a mitad)

Para comparar inversión vs retorno, usar un grid de 2 columnas sin separar en cards independientes. Borde exterior único, división interna.

```html
<div class="invest-split">
  <div class="invest-left"><!-- inversión --></div>
  <div class="invest-right"><!-- retorno --></div>
</div>
```

```css
.invest-split { display: grid; grid-template-columns: 1fr 1fr; border: 1px solid var(--gray-200); border-radius: 12px; overflow: hidden; }
.invest-left { padding: 1.5rem; border-right: 1px solid var(--gray-200); }
.invest-right { padding: 1.5rem; background: var(--gray-50); }
```

## Reglas de David (críticas)
- **FONDO BLANCO SIEMPRE** para presentaciones corporativas
- **NUNCA** glass, mesh, gradientes, dark mode, neon
- **NUNCA** "look de IA" → Inter, colores sólidos, bordes limpios
- **NUNCA** cards con iconito+titulo+texto → usar bloques numerados
- **SÍ** tablas con datos reales embebidas en la presentación
- **SÍ** ejemplo de informe real (no screenshots, sino HTML embebido)
- **SÍ** números concretos: €/año, % sueldo, ROI, proyecciones
- **Footer:** "Hecho con ❤️ por David Antizar"

## ⚠️ Regla de presentación de datos (crítica)

**NUNCA usar "coste por minuto"** en tablas de costes de transporte. David corrigió esto explícitamente: "como va a perder un empleado en coche tanto al minuto… será a la hora".

**Patrón correcto para analizar costes de transporte laboral:**

```html
<table>
  <thead><tr>
    <th>Modo</th><th>€/mes</th><th>€/año</th>
    <th>Sueldo neto estimado</th><th>% sueldo en transporte</th>
    <th>Sueldo tras transporte</th>
  </tr></thead>
  <tbody>
    <tr><td>🚇 Metro</td><td>55€</td><td>655€</td><td>19.806€</td><td>3,3%</td><td>19.151€</td></tr>
    <tr><td>🚗 Coche</td><td>704€</td><td>8.448€</td><td>19.806€</td><td style="color:var(--red)">42,7%</td><td style="color:var(--red)">11.358€</td></tr>
  </tbody>
</table>
```

**Lógica:** Sueldo neto es FIJO para todos los modos. Lo que cambia es cuánto se gasta en transporte. El "% sueldo en transporte" = €/año transporte / sueldo neto. El "sueldo tras transporte" = sueldo neto - €/año transporte.

**Callout explicativo después de la tabla:**
> "Un empleado que va en coche gasta 8.448€ al año. De su sueldo neto de 19.806€, solo le quedan 11.358€ reales. Con metro serían 655€. Ahorro: 7.793€ al año."

**NUNCA:**
- ❌ "€/minuto" → confuso, no aporta
- ❌ Sueldo diferente por modo (el sueldo es el mismo, cambia el gasto)
- ❌ Formato "sueldo real" sin explicar que es sueldo-gasto

## CSS esencial (no incluir en cada presentación, usar las clases)

```css
section { padding: 5rem 2rem; }
.container { max-width: 1060px; margin: 0 auto; }
.kpi { background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: 12px; padding: 1.2rem; text-align: center; }
.kpi-value { font-size: 1.8rem; font-weight: 800; }
.kpi-label { font-size: 0.72rem; color: var(--gray-400); font-weight: 600; text-transform: uppercase; }
.card { background: white; border: 1px solid var(--gray-200); border-radius: 12px; padding: 1.5rem; }
.card-accent { border-left: 3px solid var(--blue); }
.card-green { border-left: 3px solid var(--green); background: var(--green-light); }
.table-wrap { overflow-x: auto; border: 1px solid var(--gray-200); border-radius: 12px; }
table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
thead { background: var(--gray-50); }
th { padding: 0.7rem 1rem; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; color: var(--gray-500); }
td { padding: 0.7rem 1rem; border-bottom: 1px solid var(--gray-100); }
```

## Referencia visual
- McKinsey & Company → fondo blanco, tipografía serif/sans-serif, datos prominentes
- BCG → mismo patrón, tabs numerados, grids de KPIs
- Ineco → este patrón exacto, colores azul #2563eb + verde #059669
