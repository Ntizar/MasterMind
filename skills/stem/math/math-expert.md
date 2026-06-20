---
name: math-expert
description: Ecuaciones diferenciales ordinarias, análisis complejo básico, álgebra lineal avanzada (autovalores, diagonalización, SVD), topología básica.
tags: [stem, math, expert]
---

# Matemáticas Expertas

## Referencias de autoridad

- Boyce, W. & DiPrima, R. — *Elementary Differential Equations and Boundary Value Problems*, Wiley
- Axler, S. — *Linear Algebra Done Right*, Springer (3rd ed.)
- Rudin, W. — *Principles of Mathematical Analysis* (3rd ed.), McGraw-Hill ("Red Book")
- Kreyszig, E. — *Advanced Engineering Mathematics*, Wiley
- Nagle, S., Saff, E. & Snider, A. — *Fundamentals of Differential Equations*, Pearson

## Contenido clave

### Ecuaciones diferenciales ordinarias (EDO)

**Clasificación**:
- Orden: mayor derivada presente. 1º, 2º, etc.
- Lineal: y y sus derivadas aparecen con grado 1 y sin productos entre ellas.
- Homogénea: término independiente = 0.

**EDO separable** (1º orden): dy/dx = g(x)h(y)
- Método: dy/h(y) = g(x)dx → ∫dy/h(y) = ∫g(x)dx + C
- Ejemplo: dy/dx = ky → ln|y| = kx + C → y = Ce^(kx)

**EDO lineal** (1º orden): dy/dx + P(x)y = Q(x)
- Factor integrante: μ(x) = e^(∫P(x)dx)
- Solución: y · μ(x) = ∫Q(x)μ(x)dx + C
- y = (1/μ(x)) · [∫Q(x)μ(x)dx + C]

**EDO lineal** (2º orden, coeficientes constantes): ay'' + by' + cy = 0
- Ecuación característica: ar² + br + c = 0
- Raíces reales distintas r₁ ≠ r₂: y = C₁e^(r₁x) + C₂e^(r₂x)
- Raíces repetidas r₁ = r₂ = r: y = C₁e^(rx) + C₂xe^(rx)
- Raíces complejas α ± βi: y = e^(αx)(C₁cos βx + C₂sen βx)

**EDO no homogénea**: ay'' + by' + cy = g(x)
- Solución general: y = yₕ + yₚ (homogénea + particular)
- **Coeficientes indeterminados**: suponer forma de yₚ según g(x)
  - g(x) = Pₙ(x) → yₚ = xˢQₙ(x)
  - g(x) = e^(αx) → yₚ = xˢAe^(αx)
  - g(x) = sen(βx) o cos(βx) → yₚ = xˢ(A sen βx + B cos βx)
  - s = 0, 1 o 2 según si la forma propuesta es o no solución de la homogénea
- **Variación de parámetros**: yₚ = u₁(x)y₁ + u₂(x)y₂
  - u₁' = -y₂g/W, u₂' = y₁g/W
  - W = Wronskiano = y₁y₂' - y₂y₁'

**Condiciones de existencia y unicidad** (Teorema de Picard-Lindelöf):
- dy/dx = f(x, y), y(x₀) = y₀
- Si f y ∂f/∂y son continuas en un rectángulo que contiene (x₀, y₀), existe única solución local.

### Álgebra lineal avanzada

**Autovalores y autovectores**:
- Av: λv = Av, donde v ≠ 0
- Ecuación característica: det(A - λI) = 0
- Trace(A) = Σλᵢ (suma de autovalores = traza)
- det(A) = Πλᵢ (producto de autovalores = determinante)
- Espacio propio Eλ = {v : Av = λv} = nul(A - λI)

**Diagonalización**:
- A es diagonalizable ⟺ tiene n autovalores linealmente independientes (n = dimensión)
- A = PDP⁻¹, donde D = diag(λ₁, ..., λₙ), P = [v₁ | v₂ | ... | vₙ]
- Si A es simétrica (A = Aᵀ), entonces es diagonalizable ortogonalmente: A = QDQᵀ con Q ortogonal.

**Valores singulares (SVD)**:
- A = UΣVᵀ donde U, V son ortogonales y Σ es diagonal con σᵢ ≥ 0
- σᵢ = √(λᵢ(AᵀA)) — valores singulares son raíces cuadradas de autovalores de AᵀA
- rank(A) = número de valores singulares no nulos
- Aplicaciones: compresión de datos, pseudo-inversa de Moore-Penrose, mínimos cuadrados

**Teorema espectral** (matrices simétricas reales):
- A simétrica real ⟺ existe base ortonormal de autovectores
- Todos los autovalores son reales
- A = QDQᵀ con Q ortogonal

**Forma canónica de Jordan**:
- Toda matriz A ∈ ℂⁿˣⁿ es similar a una matriz Jordan J: A = PJP⁻¹
- Bloques de Jordan: Jλ = λ en diagonal, 1 sobre diagonal
- Dimensión del espacio propio geométrico ≤ multiplicidad algebraica

### Análisis complejo básico

**Funciones holomorfas**:
- f(z) = u(x,y) + iv(x,y) es holomorfa en z₀ si es diferenciable en un entorno de z₀
- Ecuaciones de Cauchy-Riemann: ∂u/∂x = ∂v/∂y, ∂u/∂y = -∂v/∂x
- Si f es holomorfa, entonces es infinitamente diferenciable (teorema de Goursat).

**Serie de Fourier** (funciones periódicas de periodo 2L):
- f(x) = a₀/2 + Σₙ₌₁^∞ [aₙ cos(nπx/L) + bₙ sen(nπx/L)]
- a₀ = (1/L)∫₋ₗˡ f(x)dx
- aₙ = (1/L)∫₋ₗˡ f(x)cos(nπx/L)dx
- bₙ = (1/L)∫₋ₗˡ f(x)sen(nπx/L)dx
- Si f es par: bₙ = 0 (serie de cosenos)
- Si f es impar: aₙ = 0 (serie de senos)
- Teorema de convergencia de Dirichlet: si f es por tramos suave, la serie converge a f(x) en puntos de continuidad y a [f(x⁺) + f(x⁻)]/2 en discontinuidades.

### Topología básica

**Espacio métrico** (X, d):
- d: X × X → ℝ tal que: d(x,y) ≥ 0, d(x,y) = 0 ⟺ x = y, d(x,y) = d(y,x), d(x,z) ≤ d(x,y) + d(y,z)

**Abiertos y cerrados** (en ℝⁿ con métrica euclídea):
- Bola abierta: Bᵣ(x₀) = {x ∈ X : d(x, x₀) < r}
- Abierto: U ⊆ X es abierto si ∀x ∈ U, ∃r > 0 tal que Bᵣ(x) ⊆ U
- Cerrado: F ⊆ X es cerrado si X \ F es abierto
- La bola abierta NO es cerrada (y viceversa) en ℝⁿ
- ∅ y X son abiertos y cerrados a la vez (conexos)

**Compacidad** (en ℝⁿ):
- Teorema de Heine-Borel: F ⊆ ℝⁿ es compacto ⟺ F es cerrado y acotado
- Propiedad: imagen de compacto por función continua es compacta
- Toda sucesión en compacto tiene subsucesión convergente (secuencialmente compacto)

**Conexidad**:
- Conexo por caminos: ∀x,y ∈ X, ∃γ: [0,1] → X continuo con γ(0) = x, γ(1) = y
- En ℝ: los únicos subconjuntos conexos son los intervalos

## Unidades y sistema SI

- EDOs: las unidades dependen del problema físico. Verificar dimensionalidad de cada término.
- Autovalores: mismas unidades que la traza de A (suma de elementos diagonales).
- SVD: valores singulares tienen mismas unidades que A.
- Series de Fourier: coeficientes tienen mismas unidades que f(x).
- Topología: abstracto, sin unidades físicas inherentes.

## Errores comunes / Pitfalls

- **Condiciones de existencia en EDOs**: el teorema de Picard requiere continuidad de f Y de ∂f/∂y. Si ∂f/∂y es discontinua, puede haber no unicidad (ej: y' = y^(2/3), y(0) = 0 tiene infinitas soluciones).
- **Interpretación geométrica de autovalores**: |λ| = factor de escala en dirección del autovector. λ < 0 = reflexión. λ = 0 = colapso a dimensión inferior.
- **Hipótesis del teorema espectral**: solo aplica a matrices SIMÉTRICAS reales (A = Aᵀ). No a matrices normales ni generales.
- **Diagonalización**: una matriz con autovalores repetidos puede NO ser diagonalizable si el espacio propio geométrico tiene dimensión < multiplicidad algebraica.
- **SVD vs diagonalización**: SVD existe PARA TODA MATRIZ (rectangular o no). La diagonalización solo para cuadradas y con n autovectores independientes.
- **Serie de Fourier en discontinuidad**: la serie converge al promedio de límites laterales, NO al valor de la función. Fenómeno de Gibbs: overshoot ~9% cerca de discontinuidad.
- **Ecuaciones de Cauchy-Riemann**: son NECESARIAS pero NO SUFICIENTES por sí solas. Se requiere continuidad de las derivadas parciales.
- **Compacidad en ℝⁿ**: en espacios generales, cerrado y acotado NO implica compacto. Solo en ℝⁿ con métrica euclídea (Heine-Borel).

## Verificación

- [ ] EDO separable: sustituir solución y verificar que satisface la ecuación original
- [ ] EDO lineal 2º orden: verificar que yₕ satisface la homogénea y yₚ la no homogénea
- [ ] EDO lineal 2º orden: verificar ecuación característica y tipos de raíces
- [ ] Coeficientes indeterminados: verificar que la forma propuesta de yₚ no es solución de la homogénea (ajustar s)
- [ ] Wronskiano: W ≠ 0 ⟺ soluciones linealmente independientes
- [ ] Autovalores: verificar det(A - λI) = 0 para cada λ encontrado
- [ ] Autovectores: verificar Av = λv para cada par (λ, v)
- [ ] Diagonalización: verificar AP = PD
- [ ] SVD: verificar AAᵀ = UΣ²Uᵀ y AᵀA = VΣ²Vᵀ
- [ ] Serie de Fourier: verificar coeficientes aₙ, bₙ calculando las integrales
- [ ] Compacidad: verificar que el conjunto es cerrado (contiene sus puntos de acumulación) y acotado (contenido en una bola)
