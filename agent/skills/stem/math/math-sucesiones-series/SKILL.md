---
name: math-sucesiones-series
description: Sucesiones (aritméticas, geométricas), series, sumatorios, convergencia y test de convergencia.
tags: [stem, math, intermediate]
---

# Sucesiones y Series

## Sucesiones aritméticas

- **Definición**: aₙ = aₙ₋₁ + d, donde d es la diferencia común
- **Término general**: aₙ = a₁ + (n-1)·d
- **Suma de n términos**: Sₙ = n/2 · (a₁ + aₙ) = n/2 · [2a₁ + (n-1)d]
- **Propiedad**: aₙ = (aₙ₋₁ + aₙ₊₁) / 2 (término medio)

Ejemplo: 3, 7, 11, 15, ... → a₁ = 3, d = 4, a₁₀ = 3 + 9·4 = 39

## Sucesiones geométricas

- **Definición**: aₙ = aₙ₋₁ · r, donde r es la razón común
- **Término general**: aₙ = a₁ · r^(n-1)
- **Suma de n términos (r ≠ 1)**: Sₙ = a₁ · (rⁿ - 1) / (r - 1)
- **Suma infinita (|r| < 1)**: S∞ = a₁ / (1 - r)

Ejemplo: 2, 6, 18, 54, ... → a₁ = 2, r = 3, a₁₀ = 2 · 3⁹ = 39 366

## Series

- **Notación sumatorio**: Σᵢ₌₁ⁿ aᵢ = a₁ + a₂ + ... + aₙ
- **Series aritméticas infinitas**: divergen (salvo d = 0)
- **Series geométricas infinitas**: convergen si |r| < 1

## Test de convergencia

### Test de la n-ésima (terminación)
Si lim(n→∞) aₙ ≠ 0, la serie Σaₙ diverge.
Pitfall: Si lim = 0, NO se concluye nada (podría converger o divergir).

### Series geométricas
Σ arⁿ converge si |r| < 1, diverge si |r| ≥ 1.

### Serie telescópica
Σ (bₙ - bₙ₊₁) = b₁ - lim(n→∞) bₙ₊₁

### Test de comparación
Si 0 ≤ aₙ ≤ bₙ y Σbₙ converge, entonces Σaₙ converge.
Si 0 ≤ aₙ ≤ bₙ y Σaₙ diverge, entonces Σbₙ diverge.

### Test de comparación por límites
Si lim(aₙ/bₙ) = L donde 0 < L < ∞, ambas series convergen o ambas divergen.

### Test de la razón (d'Alembert)
L = lim|aₙ₊₁/aₙ|. Si L < 1: converge. Si L > 1: diverge. Si L = 1: indeterminado.

### Test de la raíz (Cauchy)
L = lim |aₙ|^(1/n). Si L < 1: converge. Si L > 1: diverge. Si L = 1: indeterminado.

### Test de la integral
Si f(x) es positiva, continua y decreciente para x ≥ 1, entonces Σaₙ y ∫₁^∞ f(x)dx convergen o divergen juntas, donde aₙ = f(n).

### Serie armónica
Σ 1/n diverge (aunque lim 1/n = 0).

### Serie p
Σ 1/nᵖ converge si p > 1, diverge si p ≤ 1.

## Series notables

- **Armónica**: Σ 1/n → diverge
- **p-series**: Σ 1/nᵖ → converge si p > 1
- **Geométrica**: Σ arⁿ → converge si |r| < 1

## Errores comunes / Pitfalls

- **Confundir d y r**: en aritmética se suma d, en geométrica se multiplica por r
- **Suma geométrica infinita**: solo aplica si |r| < 1. Si r ≥ 1, la serie diverge
- **Test de la n-ésima**: lim = 0 NO implica convergencia (ej: serie armónica)
- **Índices del sumatorio**: Σᵢ₌₀ⁿ ≠ Σᵢ₌₁ⁿ. Verificar el índice de inicio
- **Fórmula de suma geométrica**: Sₙ = a₁(rⁿ - 1)/(r - 1) = a₁(1 - rⁿ)/(1 - r). Son equivalentes pero cuidado con signos

## Verificación

- [ ] Verificar término general calculando los primeros 3-4 términos manualmente
- [ ] En series geométricas infinitas: ¿|r| < 1?
- [ ] Aplicar test de la n-ésima antes de tests más complejos
- [ ] Para series con factoriales: usar test de la razón
- [ ] Para series con potencias n-ésimas: usar test de la raíz
