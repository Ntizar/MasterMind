# Patrón de canvas tachado (conteo visual con X roja)

## Cuándo usarlo

En temas de **restar** en 1º Primaria, cuando necesitas mostrar visualmente "quitar" algo. El canvas tachado muestra objetos (emojis) donde los "quitados" tienen una X roja encima y los restantes se colorean en verde.

## Estructura

```html
<div class="canvas-container">
  <canvas id="visualCount" width="500" height="100"></canvas>
</div>
```

## Implementación JS

```javascript
function drawVisualCount() {
  const vc = document.getElementById('visualCount');
  if (!vc) return;
  const vctx = vc.getContext('2d');
  vctx.clearRect(0, 0, vc.width, vc.height);
  vctx.fillStyle = '#f8faff';
  vctx.fillRect(0, 0, vc.width, vc.height);
  vctx.font = '28px sans-serif';
  vctx.textAlign = 'center';

  const total = 13;  // total de objetos
  const eaten = 5;   // cantidad que se "quita"
  let x = 30;

  for (let i = 0; i < total; i++) {
    if (i < eaten) {
      // TACHADOS: gris con X roja
      vctx.fillStyle = '#d1d5db';
      vctx.fillText('🍎', x, 50);
      vctx.strokeStyle = '#ef4444';
      vctx.lineWidth = 2;
      vctx.beginPath();
      vctx.moveTo(x - 10, 40);
      vctx.lineTo(x + 10, 60);
      vctx.moveTo(x + 10, 40);
      vctx.lineTo(x - 10, 60);
      vctx.stroke();
    } else {
      // RESTANTES: verde
      vctx.fillStyle = '#10b981';
      vctx.fillText('🍎', x, 50);
    }
    x += 36;
  }

  // Leyenda
  vctx.fillStyle = '#1e293b';
  vctx.font = 'bold 14px Inter, sans-serif';
  vctx.fillText(`🍎 ${eaten} tachadas (se comió)  |  🍎 ${total - eaten} restantes`, vc.width / 2, 90);
}
```

## Reglas

- Los tachados deben ser **grises** con **X roja** (diferenciación visual clara)
- Los restantes deben ser **verdes** (positivo, "quedan bien")
- Incluir **leyenda** que explique qué significa cada color
- El emoji debe ser relevante para el contexto (🍎 para manzanas, 🎈 para globos, etc.)
- El canvas debe ser responsive: usar `max-width: 100%` en CSS

## Diferencia con conteo visual normal

| Patrón | Uso | Visual |
|--------|-----|--------|
| Conteo visual normal | Sumar | Todos los emojis del mismo color |
| Canvas tachado | Restar | Tachados (gris+X) vs restantes (verde) |

## Implementado en

- `s01-6-restar-hasta-20.html` — 13 manzanas, 5 tachadas, 8 restantes (2026-06-10)
