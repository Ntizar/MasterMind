# Patrón: Completar Hueco Multi-Pasos — DeSumarIntegrar

## Problema

Los ejercicios de "completar hueco" normales tienen un solo input. Pero para enseñar **procesos de varios pasos** (como la descomposición de multiplicaciones), un solo hueco no basta.

## Solución: Múltiples inputs inline en un solo ejercicio

```html
<div class="exercise">
<p><strong>Ejercicio 1 — Completar hueco:</strong> Completa los pasos de 23 × 4</p>
<p style="margin-top:.5rem">
23 × 4 = (20 × <span class="hueco-input" id="e1a" placeholder="?">4</span>) + (3 × <span class="hueco-input" id="e1b" placeholder="?">4</span>) = <span class="hueco-input" id="e1c" placeholder="?">80</span> + <span class="hueco-input" id="e1d" placeholder="?">12</span> = <span class="hueco-input" id="e1e" placeholder="?">92</span>
</p>
<div class="exercise-input">
<button onclick="checkHueco()" style="background:var(--naranja)">Comprobar</button>
</div>
<div class="feedback" id="hueco-fb"></div>
</div>
```

## CSS necesario

```css
.hueco-input{
  display:inline-block;
  width:80px;
  padding:.3rem .5rem;
  border:2px solid var(--azul);
  border-radius:6px;
  font-size:1.1rem;
  text-align:center;
  background:var(--azul-claro);
  font-weight:700;
}
.hueco-input:focus{
  outline:none;
  border-color:var(--naranja);
  background:var(--naranja-claro);
}
```

## JS de verificación

```javascript
function checkHueco() {
  const a = parseInt(document.getElementById('e1a').value);
  const b = parseInt(document.getElementById('e1b').value);
  const c = parseInt(document.getElementById('e1c').value);
  const d = parseInt(document.getElementById('e1d').value);
  const e = parseInt(document.getElementById('e1e').value);
  const fb = document.getElementById('hueco-fb');
  
  if ([a,b,c,d,e].some(x => isNaN(x))) {
    fb.textContent = 'Rellena todos los huecos';
    fb.className = 'feedback incorrect';
    return;
  }
  
  if (a === 4 && b === 4 && c === 80 && d === 12 && e === 92) {
    fb.textContent = '✅ ¡Perfecto! Has descompuesto bien la multiplicación.';
    fb.className = 'feedback correct';
  } else {
    let msg = 'Revisa: 23×4=(20×4)+(3×4)=80+12=92. ';
    if (a !== 4 || b !== 4) msg += 'Los factores son 4 y 4. ';
    if (c !== 80) msg += '20×4=80. ';
    if (d !== 12) msg += '3×4=12. ';
    if (e !== 92) msg += '80+12=92. ';
    fb.textContent = '❌ ' + msg;
    fb.className = 'feedback incorrect';
  }
}
```

## Cuándo usarlo

- Enseñar **descomposición de operaciones**: multiplicación distributiva, fracciones equivalentes
- Mostrar **pasos intermedios** de un procedimiento largo
- Conectar **operaciones inversas** (× → ÷)
- **NO usar** para cálculos simples de un paso (ahí un input basta)

## Reglas

1. **Máximo 5 inputs** por ejercicio multi-pasos — más de eso abruma
2. **Cada input tiene un propósito pedagógico** — no poner inputs decorativos
3. **El feedback debe indicar qué hueco está mal** — no solo "incorrecto"
4. **Pista opcional** — añadir un `<p style="font-size:.9rem;color:var(--gris)">Pista: ...</p>` antes del botón

## Diferencia con otros tipos

| Tipo | Inputs | Uso |
|------|--------|-----|
| Completar hueco simple | 1 | Fórmula o dato suelto |
| Completar hueco inverso | 1 | Hallar operando desconocido |
| **Multi-pasos** | 2-5 | **Procedimiento completo paso a paso** |

## Ejemplo alternativo: fracciones equivalentes

```html
<p>1/2 = <span class="hueco-input" id="f1">2</span>/4 = <span class="hueco-input" id="f2">4</span>/8 = <span class="hueco-input" id="f3">6</span>/12</p>
```

## Fecha de descubrimiento

2026-06-10, tema `s02-3primaria.html` (multiplicar 2 cifras)
