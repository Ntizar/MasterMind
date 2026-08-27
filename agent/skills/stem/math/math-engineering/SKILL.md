---
name: stem-math-engineering
description: Matemáticas para ingeniería: series de Fourier, transformada de Laplace, ecuaciones diferenciales de segundo orden, cálculo multivariable, integrales múltiples, campos vectoriales y teoremas de Green/Stokes/Gauss.
tags: [stem, math, engineering]
---

# Matemáticas para Ingeniería

## Referencias de autoridad

- **Stewart**: Cálculo, 8ª edición, Cengage
- **Kreyszig**: Advanced Engineering Mathematics, 10ª edición, Wiley
- **Boyce & DiPrima**: Elementary Differential Equations, 11ª edición, Wiley
- **Gradshteyn & Ryzhik**: Table of Integrals, Series, and Products

## Series de Fourier

### Serie de Fourier
- f(x) = a₀/2 + Σ[aₙcos(nx) + bₙsen(nx)]
- **a₀** = (1/π) ∫₋π^π f(x)dx
- **aₙ** = (1/π) ∫₋π^π f(x)cos(nx)dx
- **bₙ** = (1/π) ∫₋π^π f(x)sen(nx)dx
- **Período 2L**: cambiar nx → nxπ/L y el factor 1/π → 1/L

### Serie de Fourier en intervalos diferentes
- Período T = 2L: ω₀ = π/L
- f(x) = a₀/2 + Σ[aₙcos(nω₀x) + bₙsen(nω₀x)]

### Serie de cosenos y senos
- **Par extensión par**: solo cosenos (bₙ = 0)
- **Par extensión impar**: solo senos (aₙ = 0)

### Teorema de convergencia de Dirichlet
- Si f es continua a trozos y f' es continua a trozos en [-L, L]:
  - La serie converge a f(x) en puntos de continuidad
  - Converge a [f(x⁺) + f(x⁻)]/2 en puntos de discontinuidad

### Coeficientes de Fourier complejos
- cₙ = (1/2L) ∫₋ᴸᴸ f(x)e^(-inxπ/L)dx
- f(x) = Σ cₙe^(inxπ/L)
- c₋ₙ = c̄ₙ (para f real)

### Identidad de Parseval
- (1/2L) ∫₋ᴸᴸ |f(x)|²dx = |a₀|²/4 + ½Σ(|aₙ|² + |bₙ|²)

## Transformada de Laplace

### Definición
- F(s) = L{f(t)} = ∫₀^∞ e^(-st)f(t)dt
- f(t) = L⁻¹{F(s)}

### Transformadas notables
- L{1} = 1/s
- L{tⁿ} = n!/s^(n+1)
- L{e^(at)} = 1/(s-a)
- L{sen(at)} = a/(s² + a²)
- L{cos(at)} = s/(s² + a²)
- L{senh(at)} = a/(s² - a²)
- L{cosh(at)} = s/(s² - a²)
- L{tⁿe^(at)} = n!/(s-a)^(n+1)

### Propiedades
- **Linealidad**: L{af + bg} = aL{f} + bL{g}
- **Desplazamiento en s**: L{e^(at)f(t)} = F(s-a)
- **Desplazamiento en t**: L{u(t-a)f(t-a)} = e^(-as)F(s)
- **Derivada**: L{f'(t)} = sF(s) - f(0)
- **Segunda derivada**: L{f''(t)} = s²F(s) - sf(0) - f'(0)
- **Integral**: L{∫₀ᵗ f(τ)dτ} = F(s)/s
- **División por t**: L{f(t)/t} = ∫ₛ^∞ F(u)du
- **Convolución**: L{(f*g)(t)} = F(s)·G(s)

### Transformada inversa
- **Fracciones parciales**: descomponer F(s) y buscar en tabla
- **Desplazamiento**: usar L{e^(at)f(t)} = F(s-a)
- **Convolución**: L⁻¹{F(s)G(s)} = (f*g)(t)

### Ecuaciones diferenciales con Laplace
1. Aplicar L a ambos lados de la EDO
2. Usar condiciones iniciales
3. Despejar Y(s)
4. Aplicar L⁻¹ para obtener y(t)

## Ecuaciones diferenciales de segundo orden

### EDO lineal 2º orden con coeficientes constantes
- ay'' + by' + cy = g(t)

### Solución homogénea
- ay'' + by' + cy = 0
- Ecuación característica: ar² + br + c = 0

#### Casos:
- **Raíces reales distintas** r₁ ≠ r₂: y = C₁e^(r₁t) + C₂e^(r₂t)
- **Raíces repetidas** r: y = (C₁ + C₂t)e^(rt)
- **Raíces complejas** α ± βi: y = e^(αt)(C₁cos(βt) + C₂sen(βt))

### Solución particular

#### Coeficientes indeterminados
- g(t) = polinomio → probar polinomio del mismo grado
- g(t) = e^(at) → probar Ae^(at)
- g(t) = sen(at) o cos(at) → probar Acos(at) + Bsen(at)
- g(t) = polinomio·e^(at) → probar polinomio del mismo grado·e^(at)
- g(t) = sen(at)·e^(bt) → probar [Acos(at) + Bsen(at)]·e^(bt)

#### Variación de parámetros
- y₁, y₂ son soluciones fundamentales
- yₚ = u₁y₁ + u₂y₂
- u₁' = -y₂g/W, u₂' = y₁g/W
- W = W(y₁, y₂) = y₁y₂' - y₁'y₂ (Wronskiano)

### Sistema de segundo orden (oscilador amortiguado)
- my'' + cy' + ky = 0
- ω₀ = √(k/m) = frecuencia natural
- ζ = c/(2√(mk)) = factor de amortiguamiento
- **Subamortiguado** (ζ < 1): oscilaciones decrecientes
- **Críticamente amortiguado** (ζ = 1): retorno más rápido sin oscilar
- **Sobreamortiguado** (ζ > 1): retorno lento sin oscilar

## Cálculo multivariable

### Funciones de varias variables
- z = f(x, y): dominio en R², imagen en R
- **Derivadas parciales**: ∂f/∂x, ∂f/∂y
- **Gradiente**: ∇f = (∂f/∂x, ∂f/∂y)
- **Derivada direccional**: Dᵤf = ∇f · u⃗ (u⃗ unitario)
- **Vector normal**: ∇f es perpendicular al nivel f = c
- **Plano tangente**: z = f(a,b) + ∂f/∂x(a,b)(x-a) + ∂f/∂y(a,b)(y-b)

### Optimización multivariable
- **Puntos críticos**: ∇f = (0, 0)
- **Segunda derivada**: D = fₓₓ·fᵧᵧ - (fₓᵧ)²
  - D > 0, fₓₓ > 0 → mínimo
  - D > 0, fₓₓ < 0 → máximo
  - D < 0 → punto de silla
  - D = 0 → indeterminado
- **Multiplicadores de Lagrange**: ∇f = λ∇g para f(x,y) con g(x,y) = c

### Integrales dobles
- ∬_R f(x,y)dA = ∫ₐᵇ ∫ₐᵇ f(x,y)dydx
- **Cambio a polares**: dA = r·dr·dθ, x = rcos(θ), y = rsen(θ)

### Integrales triples
- ∭_V f(x,y,z)dV
- **Coordenadas cilíndricas**: dV = r·dr·dθ·dz
- **Coordenadas esféricas**: dV = ρ²sen(φ)·dρ·dθ·dφ

## Campos vectoriales y teoremas integrales

### Campos vectoriales
- F⃗(x,y) = P(x,y)i⃗ + Q(x,y)j⃗
- **Campo conservativo**: F⃗ = ∇f (f es potencial)
- **Condición**: ∂Q/∂x = ∂P/∂y (en R², simplemente conexo)
- **Integral de línea**: ∫_C F⃗ · dr⃗
- **Teorema fundamental**: si F⃗ = ∇f, ∫_C ∇f · dr⃗ = f(B) - f(A)

### Divergencia y rotacional
- **Divergencia** (R²): div F⃗ = ∂P/∂x + ∂Q/∂y
- **Rotacional** (R²): curl F⃗ = (∂Q/∂x - ∂P/∂y)k⃗
- **Divergencia** (R³): div F⃗ = ∂P/∂x + ∂Q/∂y + ∂R/∂z
- **Rotacional** (R³): ∇ × F⃗ = (∂R/∂y - ∂Q/∂z)i⃗ + (∂P/∂z - ∂R/∂x)j⃗ + (∂Q/∂x - ∂P/∂y)k⃗

### Teorema de Green
- ∮_C (Pdx + Qdy) = ∬_R (∂Q/∂x - ∂P/∂y)dA
- C: curva cerrada simple, positiva (anti-horaria)
- R: región interior a C

### Teorema de Stokes
- ∮_C F⃗ · dr⃗ = ∬_S (∇ × F⃗) · n⃗ dS
- S: superficie con borde C
- n⃗: normal unitaria (regla de la mano derecha)

### Teorema de la divergencia (Gauss)
- ∬_S F⃗ · n⃗ dS = ∭_V (∇ · F⃗)dV
- S: superficie cerrada, n⃗ hacia fuera
- V: volumen encerrado por S

## Errores comunes / Pitfalls

- **Fourier**: verificar el período. Si es 2L, los coeficientes cambian
- **Laplace**: verificar condiciones iniciales antes de aplicar L
- **EDO 2º orden**: si g(t) contiene términos de la solución homogénea, multiplicar por t
- **Lagrange**: verificar que el punto crítico satisface la restricción
- **Cambio de variable**: en polares, NO olvidar el factor r
- **Teorema de Green**: la curva debe ser cerrada y simple, orientada anti-horaria
- **Stokes**: la orientación de C y n⃗ deben ser consistentes (mano derecha)

## Verificación

- [ ] Fourier: verificar coeficientes con f(x) = 1 (a₀ = 2, resto = 0)
- [ ] Laplace: L{f'(t)} = sF(s) - f(0). Verificar con f(t) = t
- [ ] EDO: verificar que yₕ + yₚ satisface la ecuación completa
- [ ] Gradiente: ∇f es perpendicular a las curvas de nivel
- [ ] Green: verificar con P = -y, Q = x → ∮ xdy - ydx = 2·Área
