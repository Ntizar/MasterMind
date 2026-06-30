---
name: math-intermediate
description: Funciones (lineal, cuadrática, exponencial, logarítmica, trigonométrica), identidades trigonométricas, logaritmos, matrices básicas, vectores en R2/R3, sucesiones.
tags: [stem, math, intermediate]
---

# Matemáticas Intermedias

## Referencias de autoridad

- Khan Academy — Precalculus (khanacademy.org/math/precalculus)
- Stewart, J. — *Precalculus: Mathematics for Calculus*, Cengage Learning
- Stewart, J. — *Calculus* (8th ed.), Cengage Learning (capítulos previos)
- Lay, D. — *Linear Algebra and Its Applications*, Pearson

## Contenido clave

### Funciones elementales
- **Función lineal**: f(x) = mx + b. Pendiente m = (y₂ - y₁)/(x₂ - x₁). Recta horizontal si m = 0, vertical si x = constante (no es función).
- **Función cuadrática**: f(x) = ax² + bx + c. Parábola. Si a > 0, abre arriba. Si a < 0, abre abajo. Vértice: xᵥ = -b/(2a).
- **Función exponencial**: f(x) = a · bˣ (b > 0, b ≠ 1). Creciente si b > 1, decreciente si 0 < b < 1. Dominio: ℝ, Imagen: (0, ∞) si a > 0.
- **Función logarítmica**: f(x) = log_b(x) (b > 0, b ≠ 1, x > 0). Inversa de la exponencial. Dominio: (0, ∞), Imagen: ℝ.
- **Función logaritmo natural**: ln(x) = logₑ(x), e ≈ 2.71828. Base del logaritmo natural.
- **Función trigonométrica**: sin(x), cos(x), tan(x) = sin(x)/cos(x). Periodo de sin y cos: 2π. Periodo de tan: π.

### Identidades trigonométricas fundamentales
- Pitagórica: sin²(θ) + cos²(θ) = 1
- Tangente: tan(θ) = sin(θ)/cos(θ)
- Secante: sec²(θ) = 1 + tan²(θ)
- Cosecante: csc²(θ) = 1 + cot²(θ)
- Suma de ángulos: sin(α ± β) = sin α cos β ± cos α sin β
- cos(α ± β) = cos α cos β ∓ sin α sin β
- tan(α ± β) = (tan α ± tan β)/(1 ∓ tan α tan β)
- Ángulo doble: sin(2θ) = 2 sin θ cos θ
- cos(2θ) = cos²θ - sin²θ = 2cos²θ - 1 = 1 - 2sin²θ
- Semiángulo: sin²(θ/2) = (1 - cos θ)/2, cos²(θ/2) = (1 + cos θ)/2
- Linealización: sin²θ = (1 - cos 2θ)/2, cos²θ = (1 + cos 2θ)/2

### Propiedades de logaritmos
- log_b(MN) = log_b(M) + log_b(N)
- log_b(M/N) = log_b(M) - log_b(N)
- log_b(Mⁿ) = n · log_b(M)
- Cambio de base: log_b(x) = ln(x)/ln(b) = log₁₀(x)/log₁₀(b)
- log_b(1) = 0, log_b(b) = 1
- ln(e) = 1, log₁₀(10) = 1
- e^(ln x) = x (x > 0), ln(eˣ) = x (x ∈ ℝ)

### Matrices básicas
- Matriz m × n: m filas, n columnas. A = [aᵢⱼ]
- **Suma**: (A + B)ᵢⱼ = aᵢⱼ + bᵢⱼ. Misma dimensión.
- **Multiplicación escalar**: (kA)ᵢⱼ = k · aᵢⱼ
- **Producto de matrices**: (AB)ᵢⱼ = Σₖ aᵢₖ · bₖⱼ. A es m×n, B es n×p, resultado m×p.
- NO conmutativo: AB ≠ BA en general.
- **Matriz identidad** Iₙ: 1 en diagonal, 0 fuera. AI = IA = A.
- **Determinante 2×2**: det([a b; c d]) = ad - bc
- **Determinante 3×3** (regla de Sarrus): det([a b c; d e f; g h i]) = aei + bfg + cdh - ceg - bdi - ahf
- **Transpuesta**: (Aᵀ)ᵢⱼ = aⱼᵢ. (AB)ᵀ = BᵀAᵀ

### Vectores en R2 y R3
- Vector: v = (v₁, v₂) en R2, v = (v₁, v₂, v₃) en R3
- **Magnitud**: |v| = √(v₁² + v₂²) en R2, |v| = √(v₁² + v₂² + v₃²) en R3
- **Producto escalar** (dot product): u · v = |u||v|cos θ = u₁v₁ + u₂v₂ (+ u₃v₃ en R3)
  - u · v = 0 ⟺ u ⊥ v (ortogonales)
  - cos θ = (u · v) / (|u| · |v|)
- **Producto vectorial** (cross product, SOLO en R3): u × v = (u₂v₃ - u₃v₂, u₃v₁ - u₁v₃, u₁v₂ - u₂v₁)
  - |u × v| = |u||v|sin θ = área del paralelogramo
  - u × v es perpendicular a u y v
  - u × v = -(v × u) (anticomutativo)
- **Producto mixto** (R3): u · (v × w) = volumen del paralelepípedo
- **Proyección de u sobre v**: projᵥ(u) = (u · v/|v|²) · v
- **Distancia entre puntos**: d = √((x₂-x₁)² + (y₂-y₁)²) en R2, √((x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²) en R3

### Sucesiones
- **Sucesión aritmética**: aₙ = a₁ + (n-1)d, donde d = aₙ₊₁ - aₙ (diferencia constante)
  - Suma: Sₙ = n(a₁ + aₙ)/2 = n/2[2a₁ + (n-1)d]
- **Sucesión geométrica**: aₙ = a₁ · rⁿ⁻¹, donde r = aₙ₊₁/aₙ (razón constante)
  - Suma (r ≠ 1): Sₙ = a₁(rⁿ - 1)/(r - 1) = a₁(1 - rⁿ)/(1 - r)
  - Suma infinita (|r| < 1): S∞ = a₁/(1 - r)
- **Sumatoria**: Σₖ₌₁ⁿ k = n(n+1)/2, Σₖ₌₁ⁿ k² = n(n+1)(2n+1)/6, Σₖ₌₁ⁿ k³ = [n(n+1)/2]²

## Unidades y sistema SI

- Ángulos: radianes (rad) es la unidad SI. 360° = 2π rad. 180° = π rad. 90° = π/2 rad.
- Conversión: grados × π/180 = radianes; radianes × 180/π = grados
- Funciones trigonométricas en cálculo: argumento SIEMPRE en radianes
- Matrices: sin unidades (números puros)
- Vectores: heredan unidades de la magnitud física representada

## Errores comunes / Pitfalls

- **Confundir logaritmo natural con base 10**: ln(x) ≠ log₁₀(x). ln(10) ≈ 2.303, log₁₀(e) ≈ 0.434.
- **Identidad trig no cuadrada**: sin(α + β) ≠ sin α + sin β. La función seno NO es aditiva.
- **Producto escalar vs vectorial**: el escalar da un número (u · v), el vectorial da un vector (u × v). Solo existe el vectorial en R3.
- **Determinante 3×3**: recordar los 3 términos positivos (aei, bfg, cdh) y 3 negativos (ceg, bdi, ahf). Un error de signo cambia todo.
- **Producto de matrices**: verificar dimensiones. A(m×n) · B(n×p) = C(m×p). El número interno debe coincidir.
- **Suma infinita geométrica**: solo converge si |r| < 1. Si |r| ≥ 1, la suma diverge.
- **Período de funciones**: sin y cos tienen período 2π, tan tiene período π. sin(2x) tiene período π, no 2π.
- **Dominio de logaritmo**: log(x) solo definido para x > 0. log(-5) no existe en ℝ.
- **Producto vectorial dirección**: usar regla de la mano derecha. i × j = k, j × k = i, k × i = j.

## Verificación

- [ ] Identidad trigonométrica: probar con valores concretos (θ = π/6, π/4, π/3)
- [ ] Producto escalar: verificar que u · v = |u||v|cos θ calculando por ambos métodos
- [ ] Producto vectorial: verificar que u × v es perpendicular a u (producto escalar = 0) y a v
- [ ] Matriz producto: verificar dimensión del resultado y calcular un elemento concreto a mano
- [ ] Determinante 3×3: calcular por expansión de Laplace en una fila/columna y comparar con Sarrus
- [ ] Sucesión aritmética: verificar que aₙ₊₁ - aₙ = d constante para varios n
- [ ] Sucesión geométrica: verificar que aₙ₊₁/aₙ = r constante para varios n
- [ ] Logaritmos: verificar log_b(bˣ) = x para varios valores de b y x
- [ ] Función inversa: verificar f(f⁻¹(x)) = x y f⁻¹(f(x)) = x
