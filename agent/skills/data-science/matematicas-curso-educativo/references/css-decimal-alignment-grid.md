# CSS Grid para Alineación Decimal (Primaria)

**Descubierto:** 2026-06-10  
**Uso:** Temas de decimales en primaria — visualizar alineación de comas sin canvas

## Patrón

Usar `display: inline-grid` con celdas individuales para cada dígito y la coma. La coma se colorea con `--naranja` para destacar visualmente.

## HTML

```html
<div class="decimal-grid">
  <div class="cell">2</div><div class="cell">.</div><div class="cell">5</div><div class="cell">0</div>
  <div class="cell">+</div><div class="cell">1</div><div class="cell">.</div><div class="cell">3</div><div class="cell">0</div>
  <div class="line"></div>
  <div class="cell">3</div><div class="cell">.</div><div class="cell">8</div><div class="cell">0</div>
</div>
```

## CSS

```css
.decimal-grid {
  display: inline-grid;
  grid-template-columns: repeat(4, 1.5rem);
  gap: 2px;
  font-family: monospace;
  font-size: 1.3rem;
  font-weight: 700;
  text-align: center;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  border: 2px solid var(--azul-claro);
}
.decimal-grid .cell { padding: 0.3rem; }
.decimal-grid .comma { color: var(--naranja); font-weight: 900; }
.decimal-grid .line {
  grid-column: 1 / -1;
  border-top: 3px solid var(--texto);
  margin-top: 0.3rem;
  padding-top: 0.3rem;
}
```

## Cuándo usarlo

- Temas de **sumar/restar decimales** (s05-1, s05-3)
- Mostrar **por qué importa alinear la coma**
- Reemplaza canvas cuando solo necesitas mostrar alineación (más ligero, accesible)

## Cuándo NO usarlo

- Temas de fracciones → usar canvas de barras divididas (`references/canvas-fracciones-equivalentes.md`)
- Temas de geometría → usar canvas para figuras
- Bachiller/Universidad → usar Plotly para gráficos de datos reales

## Variaciones

- Para **3 columnas** (un decimal + entero): `grid-template-columns: repeat(3, 1.5rem)`
- Para **restas**: cambiar `+` por `−` en la celda del operador
- Para **multiplicación**: añadir fila de resultado con línea separadora
