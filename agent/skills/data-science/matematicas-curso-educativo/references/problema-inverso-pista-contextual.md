# Problema Inverso con Pista Contextual

**Descubierto:** 2026-06-10  
**Uso:** Ejercicios donde se pide hallar un operando desconocido (minuendo, sustraendo, factor)

## Concepto

En vez de "2.5 + 1.3 = ?", pedir "___ − 2.4 = 3.6" — el alumno debe **invertir** la operación para encontrar el valor desconocido.

## HTML

```html
<div class="exercise">
  <p><strong>Ejercicio 3 — Completar hueco (resta):</strong></p>
  <p style="font-size:1.2rem;margin:.5rem 0">___ − 2.4 = 3.6</p>
  <div class="input-exercise">
    <input type="text" id="ej3" placeholder="?">
    <button onclick="checkEj3()">Comprobar</button>
  </div>
  <div class="result" id="ej3Result"></div>
</div>
```

## JS

```javascript
function checkEj3() {
  var val = document.getElementById('ej3').value.replace(',', '.').trim();
  var r = document.getElementById('ej3Result');
  if(val === '6' || val === '6.0') {
    r.className = 'result ok';
    r.textContent = '✅ ¡Correcto! Si ___ − 2.4 = 3.6, entonces ___ = 3.6 + 2.4 = 6.0. Para hallar el minuendo, sumas.';
  } else {
    r.className = 'result fail';
    r.textContent = '❌ Incorrecto. Pista: para encontrar el minuendo, suma: 3.6 + 2.4 = ?';
  }
}
```

## Reglas

1. **La pista en el feedback debe explicar el PORQUÉ**, no solo dar la respuesta.
   - ❌ "Incorrecto. La respuesta es 6.0"
   - ✅ "Pista: para encontrar el minuendo, suma: 3.6 + 2.4 = ?"
2. **Aceptar múltiples formatos:** `6`, `6.0`, `6,0` (para decimales)
3. **El feedback de éxito debe reforzar la regla inversa:**
   - Resta inversa → suma
   - División inversa → multiplicación
   - Multiplicación inversa → división

## Cuándo usar

- Temas de **operaciones inversas** (suma↔resta, multiplicación↔división)
- Temas de **decimales** (hallar minuendo, sustraendo, factor)
- Temas de **ecuaciones introductorias** (hallar x)

## Tipos de problema inverso

| Tipo | Ejemplo | Regla |
|------|---------|-------|
| Hallar minuendo | ___ − 2.4 = 3.6 | Sumar: 3.6 + 2.4 |
| Hallar sustraendo | 7.5 − ___ = 3.6 | Restar: 7.5 − 3.6 |
| Hallar factor | ___ × 3 = 12 | Dividir: 12 ÷ 3 |
| Hallar dividendo | ___ ÷ 4 = 3 | Multiplicar: 3 × 4 |
