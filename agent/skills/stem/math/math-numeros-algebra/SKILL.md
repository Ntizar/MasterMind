---
name: math-numeros-algebra
description: Números reales, potencias, raíces, radicales, notación científica, factorización, MCD/MCM, conjuntos numéricos y álgebra elemental básica.
tags: [stem, math, basics]
---

# Números y Álgebra Elemental

## Referencias de autoridad

- **Khan Academy** — Pre-Algebra & Algebra 1 (khanacademy.org)
- **OpenStax Algebra** — Elementary Algebra (openstax.org)
- **Barron's** — Schaum's Outline of Beginning Algebra

## Conjuntos numéricos

- **N** (naturales): {1, 2, 3, ...}
- **N₀** (naturales con cero): {0, 1, 2, 3, ...}
- **Z** (enteros): {..., -2, -1, 0, 1, 2, ...}
- **Q** (racionales): p/q donde p∈Z, q∈Z, q≠0
- **I** (irracional): √2, π, e — no se pueden expresar como fracción
- **R** (reales): Q ∪ I

Propiedad: N ⊂ Z ⊂ Q ⊂ R

## Propiedades de potencias

- a^m · a^n = a^(m+n)
- a^m / a^n = a^(m-n)
- (a^m)^n = a^(m·n)
- a^0 = 1 (a ≠ 0)
- a^(-n) = 1/a^n
- a^(1/n) = ⁿ√a
- a^(m/n) = ⁿ√(a^m) = (ⁿ√a)^m

Pitfall: (a + b)² ≠ a² + b². La correcta es a² + 2ab + b².

## Raíces y radicales

- ⁿ√(a·b) = ⁿ√a · ⁿ√b
- ⁿ√(a/b) = ⁿ√a / ⁿ√b
- ⁿ√(aᵐ) = a^(m/n)
- ⁿ√(ᵐ√a) = ⁿᵐ√a

Pitfall: √(a + b) ≠ √a + √b. No se distribuye la raíz sobre suma.

## Notación científica

- Formato: a × 10ⁿ donde 1 ≤ |a| < 10
- Ejemplo: 3 450 000 = 3,45 × 10⁶
- Ejemplo: 0,000 078 = 7,8 × 10⁻⁵

## Factorización

- **Factor común**: 6x² + 9x = 3x(2x + 3)
- **Trinomio cuadrado**: x² + 5x + 6 = (x + 2)(x + 3)
- **Diferencia de cuadrados**: a² - b² = (a+b)(a-b)
- **Diferencia de cubos**: a³ - b³ = (a-b)(a² + ab + b²)
- **Suma de cubos**: a³ + b³ = (a+b)(a² - ab + b²)

## MCD y MCM

- **MCD(a,b)**: mayor divisor común. Se calcula con Euclides o factorización prima.
- **MCM(a,b)**: menor múltiplo común. MCM(a,b) = |a·b| / MCD(a,b)

## Operaciones con fracciones

- a/b + c/d = (ad + bc) / bd
- a/b · c/d = ac / bd
- a/b ÷ c/d = a/b · d/c = ad / bc

Pitfall: No sumar denominadores. a/b + c/d ≠ (a+c)/(b+d).

## Orden de operaciones (PEMDAS)

1. Paréntesis
2. Exponentes
3. Multiplicación y división (izquierda a derecha)
4. Suma y resta (izquierda a derecha)

## Errores comunes / Pitfalls

- **Signos**: -(-x) = +x, -(a+b) = -a-b
- **Potencias con base negativa**: (-2)² = 4, pero -2² = -4
- **Dividir por cero**: indefinido, siempre verificar denominadores ≠ 0
- **Simplificar fracciones**: solo se puede simplificar factores, no términos sumados
- **Raíz cuadrada**: √(x²) = |x|, no x (solo si x ≥ 0)

## Verificación

- [ ] Verificar factorización multiplicando los factores
- [ ] Comprobar potencias con valores numéricos simples
- [ ] En notación científica, verificar que 1 ≤ |a| < 10
- [ ] En fracciones, comprobar con valores numéricos
- [ ] MCD × MCM = |a × b| (siempre)
