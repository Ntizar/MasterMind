# CSS-only Bar Chart for Primaria

When a primaria-level HTML file does NOT have Plotly.js loaded (most do not), use a pure CSS/JS bar chart instead of trying to load Plotly.

## Pattern

The `showDivBar(total, groups)` function renders a visual bar chart using inline styles and emoji, without any external library:

```javascript
function showDivBar(total, groups) {
  const result = total / groups;
  const container = document.getElementById('chart-div-table');
  const emojis = ['🍬','🍎','🌟','🎈','🍕','🧁','🎁','⭐','🌺','🐟'];
  const emoji = emojis[Math.floor(Math.random() * emojis.length)];
  
  let barsHTML = '';
  for (let i = 0; i < result; i++) {
    barsHTML += '<div style="display:inline-flex;flex-direction:column;align-items:center;margin:0 4px;">';
    barsHTML += '<div style="font-size:1.5rem;margin-bottom:2px;">' + emoji + '</div>';
    barsHTML += '<div style="width:36px;height:' + (result * 18) + 'px;background:linear-gradient(180deg,#3b82f6,#2563eb);border-radius:6px 6px 0 0;display:flex;align-items:flex-end;justify-content:center;">';
    barsHTML += '<span style="color:#fff;font-weight:bold;font-size:0.85rem;margin-bottom:4px;">' + result + '</span>';
    barsHTML += '</div></div>';
  }
  
  container.innerHTML = '<div style="display:flex;align-items:flex-end;justify-content:center;gap:4px;padding:1rem 0;"><div style="text-align:center;"><div style="font-size:0.8rem;color:#64748b;margin-bottom:4px;">' + groups + ' grupos</div>' + barsHTML + '</div></div><div style="text-align:center;font-size:1.1rem;font-weight:bold;color:#1e293b;margin-top:0.5rem;">' + total + ' ÷ ' + groups + ' = <span style="color:#2563eb;">' + result + '</span></div>';
}
```

## Container HTML

The container must have a placeholder with a default message:

```html
<div id="chart-div-table" style="min-height:120px;display:flex;align-items:center;justify-content:center;">
  <div style="text-align:center;color:#94a3b8;font-size:0.95rem;">👆 Pulsa un botón de arriba para ver la visualización</div>
</div>
```

## Why this matters

- **Plotly is only loaded in Bachiller/Universidad files** (s09, s10 series)
- **Primaria files (s01-s06) never load Plotly** — trying to use Plotly in these will silently fail
- This CSS-only approach uses the same chart-container CSS classes already defined in every file
- It's emoji-friendly, which matches the primaria aesthetic
- No external dependencies needed

## When to use

- Any primaria-level file (s01-s06) that needs a bar chart or visual representation
- Any file that doesn't already have a `<script src="...plotly...">` tag in its `<head>`
- When the result is a small integer (1-10) — perfect for emoji-based visualization

## Session example

Applied in `s01-4primaria.html` (2026-06-09) for a division visualization chart with 6 interactive buttons (12÷4, 20÷5, 18÷3, 24÷6, 30÷5, 36÷9).
