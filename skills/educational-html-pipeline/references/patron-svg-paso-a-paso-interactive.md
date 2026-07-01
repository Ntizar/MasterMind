# Patrón SVG Paso a Paso Interactivo — Dibujo Técnico

**Cuándo usar:** Cuando un tema necesita explicar un proceso o transformación visual (abatimiento, proyección, corte, etc.).

## Estructura

```
<div class="step-indicator">
  <div class="step-dot active" id="dot1" onclick="showPaso(1)"></div>
  <div class="step-dot" id="dot2" onclick="showPaso(2)"></div>
  <div class="step-dot" id="dot3" onclick="showPaso(3)"></div>
</div>
<div class="svg-container" style="cursor:pointer">
  <svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg">
    <!-- Panel 1: Paso inicial (visible) -->
    <g id="panel1" onclick="showPaso(1)">
      <rect ... />
      <text>PASO 1: Título</text>
      <!-- contenido SVG del paso 1 -->
      <text>Click para ver Paso 2 →</text>
    </g>
    <!-- Panel 2: Paso siguiente (oculto) -->
    <g id="panel2" style="display:none" onclick="showPaso(2)">
      <!-- contenido SVG del paso 2 -->
    </g>
    <!-- Panel 3: Comparación o cierre (oculto) -->
    <g id="panel3" style="display:none">
      <!-- lado izquierdo: ❌ incorrecto -->
      <!-- lado derecho: ✅ correcto -->
    </g>
  </svg>
</div>
```

## Función JS

```js
function showPaso(n) {
  document.getElementById('panel1').style.display = n===1 ? '' : 'none';
  document.getElementById('panel2').style.display = n===2 ? '' : 'none';
  document.getElementById('panel3').style.display = n===3 ? '' : 'none';
  for(var i=1;i<=3;i++){
    var d=document.getElementById('dot'+i);
    if(d) d.classList.toggle('active', i===n);
  }
}
```

## Variantes documentadas

| Sesión | Tema | Variantes |
|--------|------|-----------|
| 2026-06-10 (Sesión 3) | b02-04 correspondencia-vistas | 3 pasos: X/Z/Y transporte de dimensiones |
| 2026-06-10 (Sesión 3) | b02-08 vista-auxiliar-parcial | 3 pasos: auxiliar → parcial → comparación |
| 2026-06-10 (Sesión 3) | b03-01 isometrica-ejes | 4 pasos: Z → X → Y → verificación |
| 2026-06-10 (Sesión 3) | b05-01 cortes | 4 pasos: pieza → plano corte → rayado → resultado |
| 2026-06-10 (Sesión 3) | b08-01 abatimientos | 3 pasos: antes → abatir → comparación |
| 2026-06-10 (Sesión 3) | b09-01 planos-conjunto | 3 pasos: conjunto → lista → cotización |

## Reglas

- **Siempre 3 pasos mínimo** (inicio → proceso → resultado/comparación)
- **Cada panel debe ser clickeable** con `onclick="showPaso(N)"`
- **Step-dots animados** con `.active` class toggle
- **Panel 3 siempre comparativo** (❌ vs ✅) cuando aplica
- **Textos guía** dentro del SVG ("Click para ver Paso N →")
- **viewBox 600x280** como mínimo para que quepan 3 paneles
