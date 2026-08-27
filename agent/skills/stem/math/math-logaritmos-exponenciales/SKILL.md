---
name: math-logaritmos-exponenciales
description: Funciones exponenciales y logarítmicas, propiedades de logaritmos, ecuaciones exponenciales y logarítmicas, crecimiento y decaimiento.
tags: [stem, math, intermediate]
---

# Logaritmos y Exponenciales

## Función exponencial

- f(x) = aˣ (a > 0, a ≠ 1)
- f(x) = eˣ (exponencial natural, base e ≈ 2,718281828...)
- Propiedades:
  - e^(x+y) = eˣ · eʸ
  - e^(xy) = (eˣ)ʸ
  - e⁰ = 1
  - eˣ > 0 para todo x ∈ R
  - Creciente si a > 1, decreciente si 0 < a < 1
  - Asíntota horizontal: y = 0 (cuando x → -∞ si a > 1)

## Función logarítmica

- f(x) = logₐ(x) (a > 0, a ≠ 1)
- f(x) = ln(x) = logₑ(x) (logaritmo natural)
- f(x) = log(x) = log₁₀(x) (logaritmo decimal)
- Propiedades:
  - Dom = (0, +∞)
  - Im = R
  - log(ab) = log(a) + log(b)
  - log(a/b) = log(a) - log(b)
  - log(aⁿ) = n · log(a)
  - logₐ(x) = ln(x) / ln(a) (cambio de base)
  - logₐ(a) = 1, logₐ(1) = 0
  - logₐ(x) = 1/logₓ(a)

## Derivadas e integrales

- d/dx(eˣ) = eˣ
- d/dx(aˣ) = aˣ · ln(a)
- d/dx(ln(x)) = 1/x
- d/dx(logₐ(x)) = 1/(x · ln(a))
- ∫eˣ dx = eˣ + C
- ∫(1/x) dx = ln|x| + C

## Ecuaciones exponenciales

- a^(f(x)) = a^(g(x)) → f(x) = g(x) (misma base)
- a^(f(x)) = b → f(x) = logₐ(b)
- x² = a → x = ±√a (cuidado con signos)

## Ecuaciones logarítmicas

- logₐ(f(x)) = logₐ(g(x)) → f(x) = g(x) (y f(x) > 0, g(x) > 0)
- logₐ(f(x)) = b → f(x) = aᵇ
- log(f(x)) + log(g(x)) = log(f(x)·g(x)) (solo si f > 0 y g > 0)

## Crecimiento y decaimiento exponencial

### Crecimiento exponencial
- P(t) = P₀ · e^(kt) donde k > 0
- P₀ = cantidad inicial, k = tasa de crecimiento

### Decaimiento exponencial
- P(t) = P₀ · e^(-kt) donde k > 0
- Vida media: t₁/₂ = ln(2)/k ≈ 0,693/k

### Interés compuesto
- A = P(1 + r/n)^(nt) (n veces al año)
- A = Pe^(rt) (capitalización continua)

## Función logística

- P(t) = M / (1 + Ae^(-kt))
- M = capacidad de carga, A = (M - P₀)/P₀
- Usada en epidemiología, crecimiento poblacional

## Desigualdades con exponenciales y logaritmos

- aˣ > aʸ: si a > 1, x > y; si 0 < a < 1, x < y (se invierte)
- logₐ(f(x)) > logₐ(g(x)): si a > 1, f(x) > g(x); si 0 < a < 1, f(x) < g(x)
- Siempre verificar dominio: argumento del log > 0

## Errores comunes / Pitfalls

- **log(a + b) ≠ log(a) + log(b)**. Solo log(ab) = log(a) + log(b)
- **ln(x²) = 2ln|x|**, no 2ln(x) (el dominio de ln(x²) es x ≠ 0, no x > 0)
- **e^(x+y) ≠ eˣ + eʸ**. La correcta: e^(x+y) = eˣ · eʸ
- **Resolver aˣ = b**: si a < 0 o a = 0, no tiene sentido para exponentes reales
- **Decaimiento vs crecimiento**: signo de k en e^(kt). k > 0 → crecimiento, k < 0 → decaimiento
- **Vida media**: t₁/₂ = ln(2)/k, NO 1/k

## Verificación

- [ ] Verificar dominio: argumentos de log > 0
- [ ] Comprobar propiedades con valores numéricos simples
- [ ] En ecuaciones logarítmicas: verificar que soluciones estén en el dominio
- [ ] En decaimiento: ¿la cantidad disminuye con el tiempo?
- [ ] ln(eˣ) = x, e^(ln(x)) = x (solo si x > 0)
