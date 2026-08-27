---
name: math-vectores-matrices
description: Vectores en R2 y R3 (producto escalar, vectorial, mixto), matrices, determinantes, autovalores, autovectores, diagonalización y SVD conceptual.
tags: [stem, math, intermediate]
---

# Vectores y Matrices

## Vectores en R2 y R3

- **Vector**: v = (v₁, v₂, ...) = v₁e₁ + v₂e₂ + ...
- **Norma (módulo)**: ||v|| = √(v₁² + v₂² + ... + vₙ²)
- **Vector unitario**: u = v / ||v||
- **Vector nulo**: 0 = (0, 0, ...)

### Producto escalar (dot product)
- u · v = u₁v₁ + u₂v₂ + u₃v₃ = ||u||·||v||·cos(θ)
- u · v = 0 ↔ u ⊥ v (ortogonales)
- Propiedades: conmutativo, distributivo, homogéneo

### Producto vectorial (cross product, R3)
- u × v = (u₂v₃ - u₃v₂, u₃v₁ - u₁v₃, u₁v₂ - u₂v₁)
- ||u × v|| = ||u||·||v||·|sen(θ)| = área del paralelogramo
- u × v ⊥ u y u × v ⊥ v
- Propiedades: anticonmutativo (u × v = -(v × u)), distributivo

### Producto mixto (R3)
- [u, v, w] = u · (v × w) = det(u, v, w)
- Volumen del paralelepípedo
- [u, v, w] = 0 ↔ u, v, w son coplanarios

## Matrices

### Operaciones
- A + B: suma elemento a elemento (mismas dimensiones)
- cA: cada elemento multiplicado por escalar
- AB: producto matricial (n filas de A × n columnas de B)
  - (AB)ᵢⱼ = Σₖ aᵢₖ · bₖⱼ
  - NO es conmutativo: AB ≠ BA en general

### Matrices especiales
- **Identidad** I: Iᵢⱼ = 1 si i = j, 0 si i ≠ j
- **Simétrica**: A = Aᵀ
- **Antisimétrica**: A = -Aᵀ
- **Ortogonal**: AᵀA = AAᵀ = I
- **Diagonal**: aᵢⱼ = 0 si i ≠ j

### Transpuesta
- (Aᵀ)ᵢⱼ = aⱼᵢ
- (AB)ᵀ = BᵀAᵀ
- (A⁻¹)ᵀ = (Aᵀ)⁻¹

## Determinantes

### 2×2
det([[a,b],[c,d]]) = ad - bc

### 3×3 (regla de Sarrus)
det([[a,b,c],[d,e,f],[g,h,i]]) = aei + bfg + cdh - ceg - bdi - afh

### Propiedades
- det(A) = det(Aᵀ)
- det(AB) = det(A) · det(B)
- det(A⁻¹) = 1/det(A)
- det(cA) = cⁿ · det(A) (A es n×n)
- A es invertible ↔ det(A) ≠ 0
- Si dos filas/columnas son iguales: det = 0

### Regla de Cramer
Para Ax = b con A invertible: xᵢ = det(Aᵢ) / det(A)
donde Aᵢ es A con la columna i reemplazada por b

## Sistema de ecuaciones lineales

### Método de Gauss (eliminación)
- Transformar en matriz triangular superior
- Sustitución hacia atrás
- Casos: compatible determinado (1 solución), indeterminado (infinitas), incompatible (ninguna)

### Rango y Teorema de Rouché-Frobenius
- Sistema Ax = b compatible ↔ rang(A) = rang(A|b)
- Compatible determinado ↔ rang(A) = rang(A|b) = n (n incógnitas)
- Compatible indeterminado ↔ rang(A) = rang(A|b) < n
- Incompatible ↔ rang(A) ≠ rang(A|b)

## Autovalores y autovectores

- Av = λv → λ es autovalor, v es autovector (v ≠ 0)
- Característica: det(A - λI) = 0
- **Traza(A)** = Σλᵢ = suma de diagonales
- **det(A)** = Πλᵢ = producto de autovalores

### Diagonalización
- A es diagonalizable ↔ A tiene n autovalores linealmente independientes
- A = PDP⁻¹ donde D = diag(λ₁, ..., λₙ) y P = [v₁ | v₂ | ... | vₙ]
- Aⁿ = PDⁿP⁻¹

## SVD (Descomposición en valores singulares)

- A = UΣVᵀ donde U, V son ortogonales y Σ es diagonal con σᵢ ≥ 0
- σᵢ = √(λᵢ(AᵀA)) = valores singulares
- Aplicaciones: compresión de datos, PCA, pseudoinversa

## Errores comunes / Pitfalls

- **Producto matricial**: verificar dimensiones. A(m×n) × B(n×p) = C(m×p)
- **Determinante 3×3**: cuidado con los signos en Sarrus (3 positivos, 3 negativos)
- **Autovalores complejos**: si el polinomio característico no tiene raíces reales, usar C
- **Diagonalización**: multiplicidad algebraica ≠ multiplicidad geométrica → no diagonalizable
- **Transpuesta del producto**: (AB)ᵀ = BᵀAᵀ, NO AᵀBᵀ
- **Producto vectorial**: ||u × v|| = área del paralelogramo, NO del triángulo (la mitad)

## Verificación

- [ ] Producto escalar: ¿es un escalar? ¿u · u = ||u||²?
- [ ] Producto vectorial: ¿u × v ⊥ u y ⊥ v?
- [ ] Det(AB) = det(A) · det(B)
- [ ] Autovalores: tr(A) = Σλᵢ y det(A) = Πλᵢ
- [ ] A · A⁻¹ = I
- [ ] Rang(A) ≤ min(m, n)
