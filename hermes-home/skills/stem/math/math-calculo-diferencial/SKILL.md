---
name: math-calculo-diferencial
description: Límites, continuidad, derivadas (reglas de derivación, regla de cadena, optimización), teoremas del cálculo diferencial y series de Taylor/Maclaurin.
tags: [stem, math, advanced]
---

# Cálculo Diferencial

## Límites

- **Definición formal (ε-δ)**: lim(x→a) f(x) = L ↔ ∀ε > 0, ∃δ > 0: 0 < |x-a| < δ → |f(x) - L| < ε
- **Límite lateral**: lim(x→a⁺) f(x) y lim(x→a⁻) f(x)
- **Existencia**: lim(x→a) f(x) existe ↔ lim(x→a⁺) = lim(x→a⁻)
- **Indeterminaciones**: 0/0, ∞/∞, 0·∞, ∞-∞, 1^∞, 0⁰, ∞⁰

### Reglas de cálculo de límites
- lim(f ± g) = lim(f) ± lim(g)
- lim(f · g) = lim(f) · lim(g)
- lim(f/g) = lim(f) / lim(g) (denominador ≠ 0)
- lim(fⁿ) = (lim(f))ⁿ

### Límites notables
- lim(x→0) sen(x)/x = 1
- lim(x→0) (eˣ - 1)/x = 1
- lim(x→∞) (1 + 1/x)ˣ = e
- lim(x→0) (1 + x)^(1/x) = e

### Regla de L'Hôpital
Si lim(f/g) es 0/0 o ∞/∞: lim(f/g) = lim(f'/g') (si existe)

## Continuidad

- f es continua en x = a si:
  1. f(a) está definida
  2. lim(x→a) f(x) existe
  3. lim(x→a) f(x) = f(a)
- **Teorema del valor intermedio**: si f continua en [a,b] y k entre f(a) y f(b), ∃c ∈ (a,b) tal que f(c) = k
- **Teorema de Bolzano**: si f continua en [a,b] y f(a)·f(b) < 0, ∃c ∈ (a,b) tal que f(c) = 0
- **Teorema de Weierstrass**: f continua en [a,b] alcanza máximo y mínimo

## Derivadas

- **Definición**: f'(x) = lim(h→0) [f(x+h) - f(x)] / h
- **Interpretación**: pendiente de la recta tangente, razón de cambio instantánea

### Derivadas básicas
- d/dx(c) = 0
- d/dx(xⁿ) = nxⁿ⁻¹
- d/dx(eˣ) = eˣ
- d/dx(ln(x)) = 1/x
- d/dx(sen(x)) = cos(x)
- d/dx(cos(x)) = -sen(x)
- d/dx(tan(x)) = sec²(x)
- d/dx(arcsen(x)) = 1/√(1-x²)
- d/dx(arccos(x)) = -1/√(1-x²)
- d/dx(arctan(x)) = 1/(1+x²)

### Reglas de derivación
- **Suma**: (f + g)' = f' + g'
- **Producto**: (fg)' = f'g + fg'
- **Cociente**: (f/g)' = (f'g - fg')/g²
- **Regla de la cadena**: d/dx[f(g(x))] = f'(g(x)) · g'(x)
- **Derivada implícita**: diferenciar ambos lados y despejar dy/dx
- **Logarítmica**: d/dx[ln(f(x))] = f'(x)/f(x)

### Regla de la cadena (casos comunes)
- d/dx[f(g(x))] = f'(g(x)) · g'(x)
- d/dx[e^(g(x))] = e^(g(x)) · g'(x)
- d/dx[ln(g(x))] = g'(x)/g(x)
- d/dx[sen(g(x))] = cos(g(x)) · g'(x)

## Teoremas fundamentales

- **Rolle**: f continua en [a,b], diferenciable en (a,b), f(a) = f(b) → ∃c ∈ (a,b): f'(c) = 0
- **Lagrange (MVT)**: f continua en [a,b], diferenciable en (a,b) → ∃c ∈ (a,b): f'(c) = (f(b)-f(a))/(b-a)
- **Cauchy**: generalización de Lagrange para dos funciones

## Optimización

- **Máximos y mínimos relativos**: f'(c) = 0 y:
  - f''(c) < 0 → máximo
  - f''(c) > 0 → mínimo
  - f''(c) = 0 → indeterminado (usar primera derivada)
- **Máximos y mínimos absolutos** en [a,b]: evaluar f en puntos críticos y extremos
- **Optimización con restricciones**: multiplicadores de Lagrange

## Series de Taylor y Maclaurin

- **Taylor** (centro a): f(x) = Σₙ₌₀^∞ [f⁽ⁿ⁾(a)/n!] · (x-a)ⁿ
- **Maclaurin** (a = 0): f(x) = Σₙ₌₀^∞ [f⁽ⁿ⁾(0)/n!] · xⁿ

### expansiones notables
- eˣ = 1 + x + x²/2! + x³/3! + ... (toda x)
- sen(x) = x - x³/3! + x⁵/5! - ... (toda x)
- cos(x) = 1 - x²/2! + x⁴/4! - ... (toda x)
- ln(1+x) = x - x²/2 + x³/3 - ... (-1 < x ≤ 1)
- (1+x)ⁿ = 1 + nx + n(n-1)x²/2! + ... (|x| < 1)

## Errores comunes / Pitfalls

- **Regla de L'Hôpital**: solo aplica a 0/0 o ∞/∞. No es 1/0, 0/1, etc.
- **Regla de la cadena**: derivar la función exterior y MULTIPLICAR por la derivada de la interior. Error típico: olvidar multiplicar por g'(x)
- **f''(c) = 0**: no concluye nada. Usar prueba de la primera derivada
- **Taylor**: verificar que la función sea diferenciable n veces en el punto
- **Continuidad vs diferenciabilidad**: diferenciable → continua, pero continua NO → diferenciable (ej: |x| en 0)

## Verificación

- [ ] Derivadas: comprobar con definición numérica (h pequeño)
- [ ] Límites: aplicar L'Hôpital solo si es 0/0 o ∞/∞
- [ ] Optimización: verificar que es máximo/mínimo con f''
- [ ] Taylor: comparar con valores numéricos
- [ ] Continuidad: verificar las 3 condiciones
