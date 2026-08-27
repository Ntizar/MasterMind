# Resultado 0 como concepto pedagógico

## Cuándo usarlo

En temas de **restar hasta 10** (1º Primaria), el resultado 0 es un concepto que NO se enseña naturalmente. Los alumnos tienden a pensar que restar siempre da un número positivo. Hay que enseñar explícitamente que `x - x = 0` es normal y no es un error.

## Ejemplo de vida real

```html
<div class="box box-ejemplo">
<strong>🔍 Ejemplo — La hucha vacía</strong>
Tenías 4 monedas en tu hucha 🐷 y gastaste 4 en un chicle. ¿Cuántas monedas te quedan?
<br>4 − 4 = <b>0</b> (¡la hucha está vacía! Pero no pasa nada, es normal que quede 0)
</div>
```

## Ejercicio de práctica

```html
<div class="exercise">
<p>🎈 Tienes 7 globos en una fiesta 🎉. Se van volando 7 globos. ¿Cuántos te quedan?</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, false)">7</button>
<button class="quiz-btn" onclick="checkExercise(this, true)">0</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">14</button>
</div>
<div class="result" id="e8result"></div>
</div>
```

## Resumen a añadir

```html
<li><b>Resultado 0:</b> cuando quitas todo lo que tienes, queda 0 (es normal, no es error)</li>
```

## Reglas

- El ejercicio debe ser **contextualizado** (no `7 - 7 = ?` abstracto)
- El feedback debe **normalizar** el resultado 0: "quedar 0 es normal"
- Incluir en el resumen final un punto sobre resultado 0
- No confundir con "no queda nada" — es un número válido

## Referencias

- Implementado en: `s01-5-restar-hasta-10.html` mejora 2026-06-10