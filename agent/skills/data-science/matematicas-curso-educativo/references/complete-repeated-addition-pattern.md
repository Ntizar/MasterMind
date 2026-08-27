# Patrón "Completar Suma Repetida"

## Cuándo usarlo

Temas de introducción a multiplicación donde el alumno ya sabe sumar repetido pero no ha visto el signo x.

## Concepto

El alumno completa la suma repetida que representa una multiplicacion:
```
3 x 4 = __ + __ + __
```

## HTML

```html
<div class="exercise">
<p>Completa la suma repetida: 3 x 4 = __ + __ + __</p>
<p style="font-size:0.9rem;color:#64748b">3 grupos de 4 se escribe como 3 sumas de 4</p>
<input type="number" id="e3a" placeholder="?" style="width:50px;padding:0.4rem;font-size:1.1rem;text-align:center;border:2px solid var(--azul);border-radius:6px">
<input type="number" id="e3b" placeholder="?" style="width:50px;padding:0.4rem;font-size:1.1rem;text-align:center;border:2px solid var(--azul);border-radius:6px">
<input type="number" id="e3c" placeholder="?" style="width:50px;padding:0.4rem;font-size:1.1rem;text-align:center;border:2px solid var(--azul);border-radius:6px">
<button onclick="checkSumaRepetida()" style="background:var(--azul);color:#fff;border:none;padding:0.4rem 1rem;border-radius:6px;cursor:pointer;margin-left:0.5rem">Comprobar</button>
<div class="result" id="r3"></div>
</div>
```

## JS

```javascript
function checkSumaRepetida() {
  const a = parseInt(document.getElementById('e3a').value);
  const b = parseInt(document.getElementById('e3b').value);
  const c = parseInt(document.getElementById('e3c').value);
  const result = document.getElementById('r3');
  if(a === 4 && b === 4 && c === 4) {
    result.className = 'result ok';
    result.textContent = 'Correcto! 3 x 4 = 4 + 4 + 4 = 12. 3 sumas de 4!';
  } else {
    result.className = 'result fail';
    result.textContent = 'Error. 3 x 4 = 3 sumas de 4: 4 + 4 + 4 = 12';
  }
}
```

## Reglas

1. **N inputs numéricos** — uno por cada sumando (N = primer numero de la multiplicacion)
2. **Todos los inputs deben tener el mismo valor** — el segundo numero de la multiplicacion
3. **Feedback debe explicar por que** — no solo "correcto/incorrecto"
4. **Usar input type="number"** — para teclado numerico en movil

## Ejemplo real (2026-06-10)

Usado en s02-3-intro-multiplicacion.html:
- `3 x 4 = __ + __ + __` (3 inputs, todos deben ser 4)
- `2 x 7 = __ + __` (2 inputs, ambos deben ser 7)

## Variante: completar con resultado

Tambien se puede pedir el resultado:
```
3 x 4 = 4 + 4 + 4 = __
```
Aqui solo hay 1 input con el resultado final.
