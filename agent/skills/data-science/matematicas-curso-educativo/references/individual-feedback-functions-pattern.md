# Patrón de Funciones Individuales con Feedback Rico - DeSumarIntegrar

## Cuando usarlo

Cuando cada ejercicio necesita feedback especific y explicativo que no se puede generalizar en una funcion unificada. Ideal para:

- Ejercicios conceptuales (VF, comparar, ordenar) donde la explicacion depende de la respuesta concreta
- Problemas contextualizados donde el feedback debe referenciar el contexto (chocolate, pizza, etc.)
- Ejercicios de ordenar/comparar donde la explicacion es diferente segun el error

## Cuando NO usarlo

- Ejercicios de calculo simple (usar checkE(num, correct) unificado)
- Cuando hay 10+ ejercicios del mismo tipo (unificar reduce codigo)
- Archivos pequenos donde el JS duplicado ocupa % significativo

## Patrón HTML

```html
<div class="exercise">
<p>6. Completa el hueco: 2/3 = ___/12</p>
<input type="number" class="input-answer" id="e6" min="0" max="99">
<button class="check-btn" onclick="checkE6()">Comprobar</button>
<div class="feedback" id="e6-fb"></div>
</div>
```

## Patrón JS

```javascript
function checkE6(){
  var a = parseInt(document.getElementById('e6').value);
  var fb = document.getElementById('e6-fb');
  if(a === 8){
    fb.className = 'feedback show ok';
    fb.textContent = 'Correcto! 2x4=8 y 3x4=12, asi que 2/3 = 8/12';
  } else {
    fb.className = 'feedback show fail';
    fb.textContent = 'No. Para pasar de 3 a 12 multiplicamos por 4: 2x4 = ___';
  }
}
```

## CSS necesario

```css
.quiz-options{display:flex;flex-wrap:wrap;gap:.5rem;margin:.8rem 0}
.quiz-options button{padding:.5rem 1rem;border:2px solid var(--azul);border-radius:8px;background:#fff;cursor:pointer;font-size:.95rem;font-weight:600;transition:all .15s}
.quiz-options button:hover{background:var(--azul-claro)}
.quiz-options button.correct{background:var(--verde);color:#fff;border-color:var(--verde)}
.quiz-options button.wrong{background:var(--rojo);color:#fff;border-color:var(--rojo)}
.quiz-options button:disabled{opacity:.6;cursor:not-allowed}
.input-answer{width:80px;padding:.4rem;border:2px solid var(--azul);border-radius:6px;text-align:center;font-size:1rem;font-weight:600}
.check-btn{background:var(--azul);color:#fff;border:none;padding:.5rem 1.2rem;border-radius:6px;cursor:pointer;font-size:.95rem;font-weight:600;margin-left:.5rem}
.check-btn:hover{background:#1d4ed8}
.feedback{margin-top:.5rem;padding:.6rem;border-radius:6px;font-weight:600;display:none}
.feedback.show{display:block}
.feedback.ok{background:var(--verde-claro);color:#065f46}
.feedback.fail{background:var(--rojo-claro);color:#991b1b}
```

## Comparacion: unificado vs individual

| | Unificado (checkE) | Individual (checkE6) |
|---|---|---|
| Lineas JS | 1 funcion para N ejercicios | N funciones (mas codigo) |
| Feedback | Genérico | Especifico y explicativo |
| Mantenimiento | Facil | Dificil |
| Uso ideal | Calculos | Conceptos, problemas contextualizados, V/F |
| Descubierto | 2026-06-09 | 2026-06-10 |

## Regla de decision

```
¿El ejercicio necesita feedback especifico con explicacion del por que?
  -> Si -> Individual (checkE6, checkE7, ...)
  -> No -> Unificado (checkE num, correct)
```

Ejemplos:
- "2/3 = ___/12" -> Unificado (solo verificar numero)
- "¿3/4 y 6/9 son equivalentes?" -> Individual (explicar multiplicacion en cruz)
- "Marta tiene 1/2, Pablo 2/4..." -> Individual (referenciar contexto chocolate)
- "¿Cual es mas pequena: 1/2, 1/3, 1/4?" -> Individual (explicar regla denominador)
