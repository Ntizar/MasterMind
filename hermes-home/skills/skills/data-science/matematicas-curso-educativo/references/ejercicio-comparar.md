# Patrón: Ejercicio de Comparar — DeSumarIntegrar

## Cuándo usarlo

Cuando el alumno necesita entrenar el **pensamiento relacional** — no calcular, sino comparar magnitudes. Ideal para:
- Restas: "quitar menos = queda más"
- Fracciones: "más partes = trozos más pequeños"
- Decimales: "0.5 > 0.3 aunque 3 > 5"
- Porcentajes: "25% de 100 > 10% de 200"

## HTML

```html
<div class="exercise">
<p>6. ¿Cuál resta da un resultado MAYOR?</p>
<p style="font-weight:400;font-size:.95rem">A) 9 − 2 &nbsp;|&nbsp; B) 9 − 7</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkE6(this, true)">A) 9 − 2</button>
<button class="quiz-btn" onclick="checkE6(this, false)">B) 9 − 7</button>
</div>
<div class="result" id="e6result"></div>
</div>
```

## JS

```javascript
function checkE6(btn, correct){
  const result = document.getElementById('e6result');
  btn.parentElement.querySelectorAll('.quiz-btn').forEach(b => {
    b.disabled = true;
    b.style.pointerEvents = 'none';
  });
  if(correct){
    btn.classList.add('correct');
    result.className = 'result ok';
    result.textContent = '✅ ¡Correcto! 9−2=7 es mayor que 9−7=2. Quitas menos, queda más.';
  } else {
    btn.classList.add('wrong');
    result.className = 'result fail';
    result.textContent = '❌ 9−7=2 es MENOR que 9−2=7. Cuando quitas menos, queda más.';
  }
}
```

## Pedagogía

- **No es cálculo:** el alumno no necesita calcular 9−2 y 9−7, necesita entender la relación.
- **Feedback conceptual:** la respuesta correcta debe explicar EL PRINCIPIO ("quitar menos = queda más"), no solo confirmar el resultado.
- **Diferente del quiz normal:** en un quiz normal, el foco es "¿cuánto es 9−2?". En comparar, el foco es "¿cuál da más?".

## Variantes

| Tema | Ejemplo | Concepto |
|------|---------|----------|
| Resta | ¿9−2 o 9−7 da más? | Quitar menos = queda más |
| Fracciones | ¿1/2 o 1/4 es mayor? | Más partes = trozos más pequeños |
| Decimales | ¿0.5 o 0.3 es mayor? | No confundir con dígitos |
| Multiplicación | ¿3×7 o 3×4 da más? | Mayor factor = mayor producto |

## Regla de feedback

El feedback debe explicar el **principio**, no el resultado:
- ✅ "Quitar menos, queda más" (principio)
- ❌ "9−2=7 y 9−7=2, así que 7>2" (solo resultado)

**Fecha de descubrimiento:** 2026-06-10, tema `s01-5-restar-hasta-10.html`
