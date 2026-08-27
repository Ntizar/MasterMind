# CSS Grid de Tarjetas para Tablas de Resultados (Primaria)

Patrón para reemplazar Plotly en primaria cuando se necesita mostrar una tabla completa de resultados (ej: todas las restas de 10, tabla del 3, etc.).

## Patrón

```javascript
// Ejemplo: tabla de restas de 10
const container = document.getElementById('subTable');
for(let i = 0; i <= 10; i++){
  const result = 10 - i;
  const card = document.createElement('div');
  card.style.cssText = `background:${result > 5 ? 'var(--verde-claro)' : result > 2 ? 'var(--naranja-claro)' : 'var(--rojo-claro)'};border-radius:8px;padding:.6rem .4rem;text-align:center;border:2px solid ${result > 5 ? 'var(--verde)' : result > 2 ? 'var(--naranja)' : 'var(--rojo)'};`;
  card.innerHTML = `<div style="font-size:.75rem;color:#64748b">10−${i}</div><div style="font-size:1.4rem;font-weight:800;color:var(--texto)">${result}</div>`;
  container.appendChild(card);
}
```

## Contenedor HTML

```html
<div id="subTable" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:.5rem;margin:1rem 0"></div>
```

## Cuándo usarlo

- **Tabla completa de resultados** (ej: 10−0=10, 10−1=9, ..., 10−10=0)
- **Comparación visual de magnitudes** (colores verde/naranja/rojo según resultado)
- **Primaria** — más ligero que Plotly, más claro que emoji bars
- **Bachiller/Uni** — cuando se necesita una tabla compacta sin interactividad

## Cuándo NO usarlo

- Cuando necesitas interactividad (zoom, hover, botones) → usar Plotly
- Cuando necesitas gráfico de barras con grupos → usar `css-bar-chart-primaria.md`
- Cuando los datos son grandes (>20 items) → usar tabla HTML tradicional

## Ventajas sobre Plotly en primaria

1. **Sin CDN** — no hay dependencia externa
2. **Sin JS pesado** — solo DOM manipulation simple
3. **Responsive automático** — CSS grid con `auto-fill`
4. **Colores semánticos** — verde (>5), naranja (3-5), rojo (0-2)
5. **Carga instantánea** — sin async loading de librerías

## Sesión de ejemplo

Aplicado en `s01-5-restar-hasta-10.html` (2026-06-10): reemplazó Plotly de barras con 11 barras por tabla de 11 tarjetas coloreadas. Eliminado `<script src="plotly">` del HTML.
