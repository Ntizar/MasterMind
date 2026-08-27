---
name: stem-probabilidad-estadistica-eng
description: Probabilidad y estadística para ingeniería: variables aleatorias, distribuciones, inferencia estadística, regresión, análisis de confiabilidad y teoría de colas.
tags: [stem, engineering, probability]
---

# Probabilidad y Estadística para Ingeniería

## Referencias de autoridades

- **Walpole, Myers, Myers & Ye**: Probability & Statistics for Engineers, 10ª edición, Pearson
- **Hines, Montgomery, Goldsman & Borovetz**: Probability & Statistics in Engineering, 5ª edición, Wiley
- **Devore**: Probability and Statistics for Engineering, 8ª edición, Cengage

## Variables aleatorias y distribuciones

### Función de distribución
- **CDF**: F(x) = P(X ≤ x)
- **PDF**: f(x) = dF/dx (continua)
- **PMF**: p(x) = P(X = x) (discreta)
- Propiedades: F(-∞) = 0, F(+∞) = 1, f(x) ≥ 0

### Esperanza y varianza
- **Esperanza**: E[X] = μ = ∫xf(x)dx (continua) o Σx·p(x) (discreta)
- **Varianza**: Var(X) = σ² = E[(X-μ)²] = E[X²] - μ²
- **Desviación típica**: σ = √σ²
- **Momentos**: E[Xⁿ] = momento n-ésimo
- **Función generatriz**: M_X(t) = E[e^(tX)]

### Distribuciones discretas

#### Bernoulli
- P(X = 1) = p, P(X = 0) = 1 - p
- E[X] = p, Var(X) = p(1-p)

#### Binomial
- X ~ B(n, p)
- P(X = k) = C(n,k)·pᵏ·(1-p)^(n-k)
- E[X] = np, Var(X) = np(1-p)
- Aproximación normal: si np > 5 y n(1-p) > 5

#### Poisson
- X ~ Pois(λ)
- P(X = k) = λᵏ·e^(-λ)/k!
- E[X] = λ, Var(X) = λ
- Aproximación de binomial: si n > 20 y p < 0,05 → Pois(np)

#### Geométrica
- X = número de ensayos hasta primer éxito
- P(X = k) = (1-p)^(k-1)·p
- E[X] = 1/p, Var(X) = (1-p)/p²

### Distribuciones continuas

#### Normal
- X ~ N(μ, σ²)
- f(x) = (1/(σ√(2π)))·e^(-(x-μ)²/(2σ²))
- **Estándar**: Z ~ N(0, 1)
- Regla empírica: 68-95-99,7
- **Suma de normales**: X+Y ~ N(μ_x+μ_y, σ_x²+σ_y²) (independientes)

#### Exponencial
- X ~ Exp(λ)
- f(x) = λe^(-λx), x ≥ 0
- F(x) = 1 - e^(-λx)
- E[X] = 1/λ, Var(X) = 1/λ²
- **Sin memoria**: P(X > s+t | X > s) = P(X > t)

#### Gamma
- X ~ Γ(α, β)
- f(x) = β^α·x^(α-1)·e^(-βx)/Γ(α)
- E[X] = α/β, Var(X) = α/β²
- **Caso especial**: Exp(λ) = Γ(1, λ)

#### Chi-cuadrado
- X ~ χ²(k) = suma de k variables normales estándar al cuadrado
- E[X] = k, Var(X) = 2k

#### t de Student
- X ~ t(k)
- Se usa cuando σ es desconocida y n es pequeña
- E[X] = 0 (k > 1), Var(X) = k/(k-2) (k > 2)

#### F de Fisher
- X ~ F(d₁, d₂)
- Se usa en ANOVA y comparación de varianzas
- E[X] = d₂/(d₂-2) (d₂ > 2)

## Teoremas fundamentales

### Ley de los grandes números
- X̄_n → μ cuando n → ∞ (convergencia en probabilidad)

### Teorema del límite central
- Z_n = (X̄_n - μ)/(σ/√n) → N(0, 1) cuando n → ∞
- Aplica para cualquier distribución con μ y σ finitos
- n ≥ 30 suele ser suficiente

### Desigualdad de Chebyshev
- P(|X - μ| ≥ kσ) ≤ 1/k² para k > 0
- P(|X - μ| < kσ) ≥ 1 - 1/k²

## Estimación de parámetros

### Estimadores puntuales
- **Media muestral**: X̄ = Σxᵢ/n
- **Varianza muestral**: S² = Σ(xᵢ - X̄)²/(n-1)
- **Propiedades**: sesgo, eficiencia, consistencia, suficiencia

### Intervalos de confianza

#### Media (σ conocida)
- IC = X̄ ± z_(α/2)·σ/√n

#### Media (σ desconocida)
- IC = X̄ ± t_(α/2, n-1)·S/√n

#### Proporción
- IC = p̂ ± z_(α/2)·√(p̂(1-p̂)/n)

#### Varianza
- IC = [(n-1)S²/χ²_(α/2, n-1), (n-1)S²/χ²_(1-α/2, n-1)]

#### Diferencia de medias
- IC = (X̄₁ - X̄₂) ± t_(α/2, ν)·S_p·√(1/n₁ + 1/n₂)
- S_p = √[((n₁-1)S₁² + (n₂-1)S₂²)/(n₁+n₂-2)]

### Tamaño de muestra
- **Para media**: n = (z_(α/2)·σ/E)²
- **Para proporción**: n = z_(α/2)²·p(1-p)/E²
- E = error máximo admisible

## Pruebas de hipótesis

### Estructura
- **H₀**: hipótesis nula (la que se quiere refutar)
- **H₁**: hipótesis alternativa
- **α**: nivel de significación (típicamente 0,05)
- **p-value**: P(datos | H₀)

### Errores
- **Error tipo I (α)**: rechazar H₀ siendo cierta
- **Error tipo II (β)**: no rechazar H₀ siendo falsa
- **Potencia**: 1 - β = P(rechazar H₀ | H₁ es cierta)

### Test Z para la media
- H₀: μ = μ₀
- Z = (X̄ - μ₀)/(σ/√n)
- Rechazar si |Z| > z_(α/2)

### Test T para la media
- H₀: μ = μ₀
- t = (X̄ - μ₀)/(S/√n) con df = n-1
- Rechazar si |t| > t_(α/2, n-1)

### Test para la varianza
- H₀: σ² = σ₀²
- χ² = (n-1)S²/σ₀²
- Rechazar si χ² < χ²_(1-α/2, n-1) o χ² > χ²_(α/2, n-1)

### Test para proporciones
- H₀: p = p₀
- Z = (p̂ - p₀)/√(p₀(1-p₀)/n)

### ANOVA (una vía)
- H₀: μ₁ = μ₂ = ... = μ_k
- F = MS_between/MS_within
- Rechazar si F > F_(α, k-1, N-k)

## Regresión y correlación

### Regresión lineal simple
- Y = β₀ + β₁X + ε
- **Mínimos cuadrados**: β₁ = Σ(xᵢ - x̄)(yᵢ - ȳ)/Σ(xᵢ - x̄)²
- β₀ = ȳ - β₁·x̄
- **Coeficiente de determinación**: R² = 1 - SS_res/SS_tot
- **Error estándar**: s = √(SS_res/(n-2))

### Regresión múltiple
- Y = β₀ + β₁X₁ + ... + βₖXₖ + ε
- Y = Xβ + ε
- β̂ = (XᵀX)⁻¹XᵀY
- **R² ajustado**: R²_adj = 1 - (1-R²)(n-1)/(n-k-1)

### Diagnóstico de regresión
- **Residuos**: eᵢ = yᵢ - ŷᵢ
- **Normalidad de residuos**: test de Shapiro-Wilk o QQ-plot
- **Homocedasticidad**: varianza constante de residuos
- **Autocorrelación**: test de Durbin-Watson

## Confiabilidad

### Función de confiabilidad
- R(t) = P(T > t) = 1 - F(t)
- **Función de fallo**: f(t) = -dR/dt
- **Tasa de fallo**: λ(t) = f(t)/R(t)

### Distribución Weibull
- R(t) = e^(-(t/η)^β)
- β < 1: tasa de fallo decreciente (mortalidad temprana)
- β = 1: tasa constante (exponencial)
- β > 1: tasa de fallo creciente (desgaste)
- η = vida característica (R(η) = e^(-1) ≈ 0,368)

### Sistemas en serie y paralelo
- **Serie**: R_sistema = R₁·R₂·...·Rₙ
- **Paralelo**: R_sistema = 1 - (1-R₁)(1-R₂)...(1-Rₙ)
- **Sistema serie-paralelo**: combinar paso a paso

### MTBF y MTTF
- **MTBF** (Mean Time Between Failures): tiempo medio entre fallos
- **MTTF** (Mean Time To Failure): tiempo medio hasta el fallo
- Para exponencial: MTTF = 1/λ

## Teoría de colas

### Modelo M/M/1
- **Llegadas**: Poisson (λ)
- **Servicio**: exponencial (μ)
- **1 servidor**, cola infinita, población infinita
- **ρ = λ/μ < 1** (estabilidad)
- L = λ/(μ-λ) = ρ/(1-ρ) (nº medio en sistema)
- L_q = ρ²/(1-ρ) (nº medio en cola)
- W = 1/(μ-λ) (tiempo medio en sistema)
- W_q = ρ/(μ-λ) (tiempo medio en cola)

### Modelo M/M/c
- **c servidores**
- ρ = λ/(cμ) < 1
- P₀ = 1/[Σ(n=0,c-1)(cρ)ⁿ/n! + (cρ)ᶜ/(c!(1-ρ))]
- L_q = P₀·(cρ)ᶜ·ρ/(c!(1-ρ)²)

## Errores comunes / Pitfalls

- **Binomial vs Poisson**: binomial tiene n fijo, Poisson no. Poisson ≈ binomial si n > 20, p < 0,05
- **Normal**: la suma de normales es normal, pero la normal NO es la única distribución que converge a normal (TLC)
- **IC para varianza**: NO simétrico. Usar χ², no normal
- **R²**: un R² alto NO implica causalidad. Solo indica ajuste
- **Confiabilidad en serie**: el sistema es TAN FIABLE COMO el componente menos fiable
- **Weibull**: β = 1 → exponencial. No confundir η (vida característica) con MTTF

## Verificación

- [ ] Binomial: E[X] = np, Var(X) = np(1-p). Si p = 0, E = 0 ✓
- [ ] Normal: regla 68-95-99,7. Verificar Z = (x-μ)/σ
- [ ] TLC: n ≥ 30 suele ser suficiente para la mayoría de distribuciones
- [ ] IC media: X̄ ± t·S/√n. Verificar df = n-1
- [ ] Weibull: R(η) = e^(-1) ≈ 0,368. MTTF = η·Γ(1+1/β)
- [ ] M/M/1: L = ρ/(1-ρ). Si ρ → 1, L → ∞ (cola crece sin límite)
