# Verificación de consistencia HTML↔JS

**Descubierto:** 2026-06-10

## Problema

Cuando un HTML tiene un ejercicio con un enunciado, la función JS que lo valida puede:
1. Referenciar un `result` ID diferente al del ejercicio
2. Verificar una operación numérica distinta a la del enunciado
3. Usar parámetros booleanos invertidos (true↔false)

**Resultado:** el ejercicio muestra feedback incorrecto aunque el alumno acierte.

## Ejemplos reales

### Bug e2 V/F (s01-5-restar-hasta-10.html)
- **Enunciado:** "5 − 5 = 0"
- **Botones:** `onclick="checkVF(this, false)"` → dice Verdadero pero pasa `false`
- **Función checkVF:** verificaba "10 − 4 = 6, no 7" → ¡operación distinta!
- **Resultado:** el alumno que sabe que 5−5=0 ve un mensaje sobre 10−4

### Bug e6 Comparar (s01-5-restar-hasta-10.html)
- **Enunciado:** "8 − 3 vs 8 − 1 → cuál da mayor"
- **Respuesta correcta:** B (8−1=7 > 8−3=5)
- **Función checkE6:** verificaba "9−2=7 vs 9−7=2" → ¡números distintos!
- **Resultado:** el alumno ve explicación de 9−2/9−7 cuando el ejercicio es de 8−3/8−1

## Checklist manual (rápido)

Para cada ejercicio con función JS personalizada:

1. ¿El `id="eNresult"` referenced por `onclick` existe en el mismo bloque?
2. ¿Los números del enunciado coinciden con los de la función?
3. ¿Los parámetros booleanos de los botones son correctos? (`true` = correcto, `false` = incorrecto)
4. ¿El mensaje de feedback usa los mismos números que el enunciado?

## Fix

- Corregir el `id` referenced en la función JS
- Corregir los parámetros booleanos en los botones
- Asegurar que los mensajes de feedback coincidan con el enunciado
