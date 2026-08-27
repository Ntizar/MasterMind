---
name: math-funciones
description: Dominio, rango, tipos de funciones (lineal, cuadrática, polinómica, racional, exponencial, logarítmica), composición, inversión, simetría y transformaciones.
tags: [stem, math, intermediate]
---

# Funciones

## Definición

- f: A → B asigna a cada x ∈ A un único y ∈ B
- **Dominio (Dom(f))**: conjunto de valores de x para los que f está definida
- **Rango (Im(f))**: conjunto de valores de y = f(x) que se obtienen
- **Función inyectiva**: f(a) = f(b) → a = b (un a uno)
- **Función suprayectiva**: Im(f) = B (llega a todo el codominio)
- **Función biyectiva**: inyectiva + suprayectiva → tiene inversa

## Tipos de funciones

### Función lineal
- y = mx + b
- m = pendiente (razón de cambio), b = ordenada en el origen
- Pendiente entre dos puntos: m = (y₂ - y₁) / (x₂ - x₁)
- Recta vertical: x = c (pendiente indefinida)

### Función cuadrática
- y = ax² + bx + c
- **Vértice**: xᵥ = -b/(2a), yᵥ = f(xᵥ)
- **Eje de simetría**: x = xᵥ
- Si a > 0: concava hacia arriba (mínimo). Si a < 0: concava hacia abajo (máximo)
- Raíces: x = (-b ± √(b²-4ac)) / 2a

### Función polinómica
- P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀
- Grado n → máximo n raíces reales
- Teorema fundamental del álgebra: n raíces (contando multiplicidad) en C

### Función racional
- f(x) = P(x) / Q(x)
- **Asíntotas verticales**: donde Q(x) = 0 (y P(x) ≠ 0)
- **Asíntota horizontal**: lim(x→±∞) f(x)
  - deg(P) < deg(Q): y = 0
  - deg(P) = deg(Q): y = coef. principal P / coef. principal Q
  - deg(P) = deg(Q) + 1: asíntota oblicua (división polinómica)

### Función exponencial
- f(x) = aˣ (a > 0, a ≠ 1)
- Dom = R, Im = (0, +∞)
- f(x) = eˣ (base e ≈ 2,71828)
- Creciente si a > 1, decreciente si 0 < a < 1

### Función logarítmica
- f(x) = logₐ(x) (a > 0, a ≠ 1)
- Dom = (0, +∞), Im = R
- Inversa de la exponencial: y = aˣ ↔ x = logₐ(y)
- logₐ(x) = ln(x) / ln(a) (cambio de base)
- ln(x) = logₑ(x), log(x) = log₁₀(x)

## Composición de funciones

- (f ∘ g)(x) = f(g(x))
- Dom(f ∘ g) = {x ∈ Dom(g) : g(x) ∈ Dom(f)}
- NO es conmutativa: f ∘ g ≠ g ∘ f en general

## Función inversa

- f⁻¹(f(x)) = x y f(f⁻¹(x)) = x
- Método para hallar f⁻¹:
  1. y = f(x)
  2. Despejar x en función de y
  3. Intercambiar x e y: x = f⁻¹(y)
- Solo existe si f es biyectiva
- Gráficamente: simétrica respecto a y = x

## Simetría

- **Función par**: f(-x) = f(x) → simétrica respecto al eje Y
  - Ej: f(x) = x², cos(x)
- **Función impar**: f(-x) = -f(x) → simétrica respecto al origen
  - Ej: f(x) = x³, sin(x), tan(x)
- La mayoría de funciones NO son ni pares ni impares

## Transformaciones

- f(x) + k → desplaza k unidades arriba (k > 0)
- f(x - h) → desplaza h unidades derecha (h > 0)
- -f(x) → refleja respecto al eje X
- f(-x) → refleja respecto al eje Y
- a·f(x) → estira/encoge verticalmente (a > 1: estira, 0 < a < 1: encoge)
- f(bx) → estira/encoge horizontalmente (b > 1: encoge, 0 < b < 1: estira)

## Errores comunes / Pitfalls

- **Dominio de log**: solo x > 0. log(x²) = 2log|x|, no 2log(x)
- **Dominio de raíz par**: radicando ≥ 0
- **Asíntota vertical**: verificar que el numerador NO se anule en ese punto (si se anula ambos, puede ser un agujero, no asíntota)
- **Inversa de cuadrática**: no es biyectiva en todo R. Restringir dominio a x ≥ -b/(2a) o x ≤ -b/(2a)
- **Composición**: f(g(x)) ≠ f(x) · g(x). Son cosas distintas
- **log(a + b) ≠ log(a) + log(b)**. La correcta: log(a·b) = log(a) + log(b)

## Verificación

- [ ] Dominio: ¿hay raíces pares? ¿logaritmos? ¿divisiones por cero?
- [ ] Rango: ¿tiene inversa? ¿es acotada?
- [ ] Simetría: comprobar f(-x)
- [ ] Asíntotas: calcular límites en ±∞ y en puntos singulares
- [ ] Inversa: verificar f(f⁻¹(x)) = x
