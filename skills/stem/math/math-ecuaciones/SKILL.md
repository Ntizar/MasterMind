---
name: math-ecuaciones
description: Ecuaciones de primer y segundo grado, sistemas de ecuaciones, inecuaciones, ecuaciones con valor absoluto y ecuaciones irracionales.
tags: [stem, math, basics]
---

# Ecuaciones

## Ecuaciones de primer grado

- Forma: ax + b = 0 → x = -b/a (a ≠ 0)
- Método: despejar la incógnita operando inversamente
- Verificar siempre sustituyendo el resultado en la original

## Ecuaciones de segundo grado

- Forma: ax² + bx + c = 0 (a ≠ 0)
- **Fórmula general**: x = (-b ± √(b² - 4ac)) / 2a
- **Discriminante**: Δ = b² - 4ac
  - Δ > 0: dos soluciones reales distintas
  - Δ = 0: una solución real (raíz doble)
  - Δ < 0: dos soluciones complejas conjugadas
- **Teorema de Vieta**: x₁ + x₂ = -b/a, x₁ · x₂ = c/a

Pitfall: El signo de b es crucial. Si la ecuación es 2x² - 5x + 3 = 0, entonces b = -5, no 5.

## Ecuaciones bicuadradas

- Forma: ax⁴ + bx² + c = 0
- Sustitución: x² = t → at² + bt + c = 0
- Resolver para t y luego x = ±√t

## Ecuaciones con valor absoluto

- |x| = a (a > 0) → x = a o x = -a
- |x + b| < a → -a < x + b < a → -a - b < x < a - b
- |x + b| > a → x + b > a o x + b < -a

Pitfall: |x| = -3 no tiene solución (valor absoluto siempre ≥ 0).

## Sistemas de ecuaciones (2 incógnitas)

- **Sustitución**: despejar una de otra y sustituir
- **Igualación**: despejar la misma incógnita de ambas ecuaciones
- **Reducción (eliminación)**: sumar o restar ecuaciones para eliminar una
- **Matricial**: Ax = b → x = A⁻¹b (si A es invertible)

### Soluciones de un sistema 2×2:
- Sistema compatible determinado: una solución única
- Sistema compatible indeterminado: infinitas soluciones (rectas coincidentes)
- Sistema incompatible: ninguna solución (rectas paralelas)

## Inecuaciones

- Reglas:
  - Sumar/restar mismo valor: no cambia sentido
  - Multiplicar/dividir por positivo: no cambia sentido
  - Multiplicar/dividir por negativo: **INVERTIR** el sentido
- a < b → -a > -b (al multiplicar por -1)

## Ecuaciones irracionales (con radicales)

- Aislar el radical en un lado
- Elevar al cuadrado ambos miembros
- Verificar soluciones (pueden aparecer soluciones espurias)

Pitfall: Elevar al cuadrado introduce soluciones espurias. Siempre verificar en la ecuación original.

## Ecuaciones racionales

- Forma: P(x)/Q(x) = 0
- Condición: Q(x) ≠ 0 (verificar dominio antes de resolver)
- Solución: P(x) = 0, descartando valores que anulen denominadores

## Errores comunes / Pitfalls

- **Olvidar ± en raíz cuadrada**: x² = 9 → x = ±3, no x = 3
- **No verificar dominio**: en ecuaciones racionales, los valores que anulan denominadores no son soluciones
- **Invertir sentido de inecuación**: al multiplicar/dividir por negativo
- **Soluciones espurias**: al elevar al cuadrado, verificar siempre en la original
- **Discriminante negativo**: no confundir con "no tiene solución" — tiene soluciones complejas

## Verificación

- [ ] Sustituir la solución en la ecuación original
- [ ] Verificar Δ para segundo grado: ¿coincide con el número de soluciones?
- [ ] En sistemas, sustituir la solución en AMBAS ecuaciones
- [ ] En inecuaciones, probar un valor en la solución y uno fuera
- [ ] En ecuaciones con radicales, verificar que no haya soluciones espurias
