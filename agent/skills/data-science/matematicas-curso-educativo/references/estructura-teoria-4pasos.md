# Patrón: Teoría Estructurada 4 Pasos — DeSumarIntegrar

## Problema detectado

Algunos temas tienen teoría dispersa en múltiples cajas `box-teoria` con analogías confusas que no ayudan al aprendizaje:
- "Vampiro matemático" (números con miedo) → no explica el concepto
- "La resta en el supermercado" → caso real bueno pero mezclado con teoría
- Analogías "divertidas" que no aportan comprensión

## Solución: Estructura 4 pasos

Reemplazar teoría dispersa con UNA sola caja estructurada:

```html
<div class="box box-teoria">
<strong>📖 ¿Qué es restar?</strong>
<b>1. ¿Qué es?</b> Restar es quitar algo de un grupo y ver cuántos quedan.<br>
<b>2. ¿Para qué sirve?</b> Para saber cuánto te queda después de gastar, comer o perder algo (como cuando gastas monedas de tu hucha 🐷).<br>
<b>3. ¿Cómo se hace?</b> Empiezas con un número, quitas otro y miras cuántos quedan. Ejemplo: 8 − 3 = 5.<br>
<b>4. ¿Qué error comete la gente?</b> Confundir restar con sumar: si tienes 8 y quitas 3, NO sumes (8+3=11), ¡quita! (8−3=5).
</div>
```

## Regla de decisión: ¿mantiene o elimina analogía?

| Tipo de analogía | Mantener | Eliminar |
|-----------------|----------|----------|
| Ayuda a entender el concepto | ✅ | ❌ |
| Solo es "divertida" | ❌ | ✅ |
| Se aplica a otros contextos | ✅ | ❌ |
| Confunde al alumno | ❌ | ✅ |
| No se puede generalizar | ❌ | ✅ |

## Ejemplo de eliminación

**Antes (confuso):**
```html
<div class="box box-teoria">
<strong>📖 Teoría — Restar es como un vampiro</strong>
Imagina que los números vampiro tienen miedo de los números grandes. Cuando ves 7 − 3, el 7 le tiene miedo al 3, así que el 3 se esconde y al 7 le quedan 4. ¡El vampiro matemático! 🧛
</div>
```

**Después (claro):**
```html
<div class="box box-teoria">
<strong>📖 ¿Qué es restar?</strong>
<b>1. ¿Qué es?</b> Restar es quitar algo de un grupo y ver cuántos quedan.<br>
<b>2. ¿Para qué sirve?</b> Para saber cuánto te queda después de gastar, comer o perder algo (como cuando gastas monedas de tu hucha 🐷).<br>
<b>3. ¿Cómo se hace?</b> Empiezas con un número, quitas otro y miras cuántos quedan. Ejemplo: 8 − 3 = 5.<br>
<b>4. ¿Qué error comete la gente?</b> Confundir restar con sumar: si tienes 8 y quitas 3, NO sumes (8+3=11), ¡quita! (8−3=5).
</div>
```

## Casos donde SÍ mantener analogía

- "La X echa brazos para llevar grupos" (división) → visual y aplicable
- "El signo × es como una X que cruza grupos" (multiplicación) → conecta con símbolo
- "Las fracciones son como pizzas cortadas" → intuitivo y universal

## Aplicación

Este patrón se aplica a cualquier tema de primaria donde la teoría tenga:
1. Múltiples cajas `box-teoria` con contenido disperso
2. Analogías que no explican directamente el concepto
3. Falta de estructura clara (qué es / para qué / cómo / error)

**Fecha de descubrimiento:** 2026-06-10, tema `s01-5-restar-hasta-10.html`
