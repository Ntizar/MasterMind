---
name: math-advanced
description: Cálculo diferencial e integral (derivadas, integrales, series de Taylor), estadística descriptiva e inferencial básica.
tags: [stem, math, advanced]
---

# Matemáticas Avanzadas

## Referencias de autoridad

- Stewart, J. — *Calculus: Early Transcendentals* (9th ed.), Cengage Learning
- OpenStax — *Introductory Statistics* (openstax.org/details/introductory-statistics)
- Larson, R. & Edwards, B. — *Calculus*, Cengage Learning
- Ross, S. — *A First Course in Probability*, Pearson

## Contenido clave

### Cálculo diferencial — Derivadas

**Definición formal**: f'(x) = lim[h→0] (f(x+h) - f(x))/h

**Reglas básicas de derivación**:
- Constante: d/dx [c] = 0
- Potencia: d/dx [xⁿ] = n · xⁿ⁻¹
- Constante × función: d/dx [cf(x)] = c · f'(x)
- Suma: d/dx [f(x) + g(x)] = f'(x) + g'(x)
- Resta: d/dx [f(x) - g(x)] = f'(x) - g'(x)
- Producto: d/dx [f(x)g(x)] = f'(x)g(x) + f(x)g'(x)
- Cociente: d/dx [f(x)/g(x)] = (f'(x)g(x) - f(x)g'(x)) / g(x)²
- Regla de la cadena: d/dx [f(g(x))] = f'(g(x)) · g'(x)
- Potencia generalizada: d/dx [u(x)ⁿ] = n · u(x)ⁿ⁻¹ · u'(x)

**Derivadas de funciones elementales**:
- d/dx [sin x] = cos x
- d/dx [cos x] = -sin x
- d/dx [tan x] = sec²x = 1/cos²x
- d/dx [eˣ] = eˣ
- d/dx [ln x] = 1/x (x > 0)
- d/dx [aˣ] = aˣ · ln a
- d/dx [logₐ x] = 1/(x · ln a)
- d/dx [arcsin x] = 1/√(1 - x²)
- d/dx [arccos x] = -1/√(1 - x²)
- d/dx [arctan x] = 1/(1 + x²)

**Derivadas de orden superior**: f''(x), f'''(x), f⁽ⁿ⁾(x)

**Teorema de Rolle**: Si f es continua en [a,b], diferenciable en (a,b), y f(a) = f(b), entonces existe c ∈ (a,b) tal que f'(c) = 0.

**Teorema del valor medio (Lagrange)**: Si f es continua en [a,b] y diferenciable en (a,b), entonces existe c ∈ (a,b) tal que f'(c) = (f(b) - f(a))/(b - a).

**Regla de L'Hôpital**: Si lim f(x)/g(x) da forma 0/0 o ∞/∞, entonces lim f(x)/g(x) = lim f'(x)/g'(x) (si existe).

### Cálculo integral — Integrales

**Integral definida**: ∫ₐᵇ f(x) dx = F(b) - F(a), donde F' = f (Teorema Fundamental del Cálculo)

**Integrales básicas**:
- ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
- ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C
- ∫ aˣ dx = aˣ/ln a + C
- ∫ sin x dx = -cos x + C
- ∫ cos x dx = sin x + C
- ∫ sec²x dx = tan x + C
- ∫ 1/(1+x²) dx = arctan x + C
- ∫ 1/√(1-x²) dx = arcsin x + C
- ∫ 1/x dx = ln|x| + C

**Métodos de integración**:
- **Sustitución (cambio de variable)**: ∫ f(g(x)) · g'(x) dx = ∫ f(u) du, donde u = g(x)
- **Integración por partes**: ∫ u dv = uv - ∫ v du
  - Regla LIATE para elegir u: Logarítmica, Inversa trigonométrica, Algebraica, Trigonométrica, Exponencial
- **Fracciones parciales**: para racionales P(x)/Q(x) donde grado(P) < grado(Q)

**Propiedades**:
- ∫ₐᵇ f(x) dx = -∫ᵇₐ f(x) dx
- ∫ₐᵇ [f(x) + g(x)] dx = ∫ₐᵇ f(x) dx + ∫ₐᵇ g(x) dx
- ∫ₐᵃ f(x) dx = 0
- Si f es par: ∫₋ₐᵃ f(x) dx = 2∫₀ᵃ f(x) dx
- Si f es impar: ∫₋ₐᵃ f(x) dx = 0

### Series de Taylor y Maclaurin

**Serie de Taylor** (centrada en a):
f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(a)/n! · (x - a)ⁿ

**Serie de Maclaurin** (a = 0):
f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(0)/n! · xⁿ

**Series notables** (válidas en el dominio indicado):
- eˣ = 1 + x + x²/2! + x³/3! + ... = Σₙ₌₀^∞ xⁿ/n! (x ∈ ℝ)
- sin x = x - x³/3! + x⁵/5! - x⁷/7! + ... = Σₙ₌₀^∞ (-1)ⁿx²ⁿ⁺¹/(2n+1)! (x ∈ ℝ)
- cos x = 1 - x²/2! + x⁴/4! - x⁶/6! + ... = Σₙ₌₀^∞ (-1)ⁿx²ⁿ/(2n)! (x ∈ ℝ)
- ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ... = Σₙ₌₁^∞ (-1)ⁿ⁺¹xⁿ/n (-1 < x ≤ 1)
- 1/(1-x) = 1 + x + x² + x³ + ... = Σₙ₌₀^∞ xⁿ (|x| < 1)
- (1+x)ᵏ = 1 + kx + k(k-1)x²/2! + ... (serie binomial generalizada)

### Estadística descriptiva

**Medidas de tendencia central**:
- Media aritmética: x̄ = Σxᵢ/n
- Mediana: valor central al ordenar (impar n: posición (n+1)/2; par n: promedio de posiciones n/2 y n/2+1)
- Moda: valor más frecuente

**Medidas de dispersión**:
- Rango: máximo - mínimo
- Varianza muestral: s² = Σ(xᵢ - x̄)²/(n-1)
- Varianza poblacional: σ² = Σ(xᵢ - μ)²/N
- Desviación típica: s = √s², σ = √σ²
- Coeficiente de variación: CV = s/x̄ × 100%

**Covarianza y correlación**:
- Cov(x,y) = Σ(xᵢ - x̄)(yᵢ - ȳ)/(n-1)
- Coeficiente de Pearson: r = Cov(x,y)/(sₓ · sᵧ), -1 ≤ r ≤ 1

### Estadística inferencial básica

**Distribución normal N(μ, σ²)**:
- Densidad: f(x) = (1/σ√(2π)) · e^(-(x-μ)²/(2σ²))
- Regla empírica: ~68% en [μ-σ, μ+σ], ~95% en [μ-2σ, μ+2σ], ~99.7% en [μ-3σ, μ+3σ]
- Normal estándar Z ~ N(0, 1): Z = (X - μ)/σ

**Intervalo de confianza para la media** (σ conocida, n ≥ 30 o población normal):
IC = x̄ ± z_(α/2) · σ/√n

**Intervalo de confianza para la media** (σ desconocida):
IC = x̄ ± t_(α/2, n-1) · s/√n

**Prueba de hipótesis**:
- Hipótesis nula H₀ y alternativa H₁
- p-valor: probabilidad de obtener un resultado tan extremo o más, asumiendo H₀ verdadera
- Se rechaza H₀ si p-valor < α (nivel de significancia, típicamente 0.05)
- Error tipo I: rechazar H₀ siendo verdadera (probabilidad α)
- Error tipo II: no rechazar H₀ siendo falsa (probabilidad β)

## Unidades y sistema SI

- Derivadas: unidades de f por unidad de x (ej: m/s para velocidad)
- Integrales: unidades de f × unidades de x (ej: m × s = m·s para área bajo curva)
- Series de Taylor: cada término debe tener mismas unidades que f(x)
- Estadística: media y desviación en unidades originales; varianza en unidades²
- Coeficiente de correlación: adimensional (sin unidades)

## Errores comunes / Pitfalls

- **Regla de cadena mal aplicada**: d/dx [sin(3x²)] = cos(3x²) · 6x, NO solo cos(3x²). Derivar la función externa Y la interna.
- **Signos en integrales**: ∫ sin x dx = -cos x + C, NO cos x + C. El signo negativo es crucial.
- **Confusión varianza muestral vs poblacional**: dividir por (n-1) para muestra, por N para población. El (n-1) hace el estimador insesgado.
- **Interpretación de p-valor**: p-valor NO es la probabilidad de que H₀ sea verdadera. Es P(resultado ≥ observado | H₀ verdadera).
- **Integral de 1/x**: ∫ 1/x dx = ln|x| + C, NO ln(x) + C. El valor absoluto es necesario para x < 0.
- **Integración por partes elegir mal u**: seguir LIATE. Elegir u como la función que se simplifica al derivar.
- **Serie de Taylor convergencia**: verificar radio de convergencia. ln(1+x) solo converge para -1 < x ≤ 1.
- **Regla de L'Hôpital**: solo aplicar si la forma es indeterminada (0/0 o ∞/∞). No es una regla general de derivación.
- **Derivada de producto**: d/dx [f(x)g(x)] ≠ f'(x)g'(x). Es f'g + fg'.

## Verificación

- [ ] Derivada: aproximar numéricamente con h pequeño: f'(x) ≈ (f(x+h) - f(x-h))/(2h) y comparar
- [ ] Integral: derivar el resultado de la integral y verificar que da el integrando
- [ ] Regla de L'Hôpital: verificar que se cumple la condición de forma indeterminada antes de aplicar
- [ ] Serie de Taylor: calcular los primeros 3-4 términos a mano y verificar con la fórmula
- [ ] Varianza: verificar que s² = (Σxᵢ² - (Σxᵢ)²/n)/(n-1) da el mismo resultado
- [ ] IC: verificar que el intervalo contiene la media verdadera (si se conoce) en simulaciones
- [ ] p-valor: verificar con tabla de distribución normal estándar (Z-table)
- [ ] Teorema fundamental: ∫ₐᵇ f'(x) dx = f(b) - f(a)
