---
name: math-estadistica-probabilidad
description: Estadística descriptiva e inferencial: media, varianza, desviación, distribución normal, intervalos de confianza, test de hipótesis, Bayes y regresión lineal.
tags: [stem, math, advanced]
---

# Estadística y Probabilidad

## Estadística descriptiva

### Medidas de tendencia central
- **Media**: x̄ = Σxᵢ/n
- **Mediana**: valor central (ordenar datos). Si n par: promedio de dos centrales
- **Moda**: valor más frecuente
- **Media ponderada**: x̄ = Σ(wᵢ · xᵢ) / Σwᵢ

### Medidas de dispersión
- **Rango**: máximo - mínimo
- **Varianza muestral**: s² = Σ(xᵢ - x̄)² / (n-1)
- **Varianza poblacional**: σ² = Σ(xᵢ - μ)² / N
- **Desviación típica**: s = √s², σ = √σ²
- **Coeficiente de variación**: CV = s/x̄ (sin unidades)

### Cuartiles y percentiles
- **Q1** (25° percentil), **Q2** = mediana, **Q3** (75° percentil)
- **Rango intercuartílico**: IQR = Q3 - Q1
- Valores atípicos: x < Q1 - 1,5·IQR o x > Q3 + 1,5·IQR

## Probabilidad

### Conceptos básicos
- P(A): probabilidad de A, 0 ≤ P(A) ≤ 1
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- Si A, B independientes: P(A ∩ B) = P(A) · P(B)
- P(A|B) = P(A ∩ B) / P(B) (probabilidad condicionada)
- P(A) + P(Aᶜ) = 1

### Teorema de Bayes
P(A|B) = P(B|A) · P(A) / P(B)
P(A|B) = P(B|A) · P(A) / [P(B|A) · P(A) + P(B|Aᶜ) · P(Aᶜ)]

### Conteo
- **Permutaciones**: P(n,r) = n! / (n-r)!
- **Combinaciones**: C(n,r) = n! / (r! · (n-r)!)
- **Principio multiplicativo**: si hay m opciones para A y n para B: m·n combinaciones

## Distribuciones de probabilidad

### Distribución binomial
- X ~ B(n, p)
- P(X = k) = C(n,k) · pᵏ · (1-p)^(n-k)
- E[X] = np, Var(X) = np(1-p)
- Usar cuando: n ensayos independientes, 2 resultados, p constante

### Distribución normal
- X ~ N(μ, σ²)
- f(x) = (1/(σ√(2π))) · e^(-(x-μ)²/(2σ²))
- **Normal estándar**: Z ~ N(0, 1)
- Regla empírica: 68% en [μ-σ, μ+σ], 95% en [μ-2σ, μ+2σ], 99,7% en [μ-3σ, μ+3σ]
- Estandarización: Z = (X - μ) / σ

### Distribución t de Student
- Similar a normal pero con colas más pesadas
- Grados de libertad: df = n - 1 (para una muestra)
- Usar cuando: σ desconocido, n pequeño (< 30)

### Distribución χ² (Chi-cuadrado)
- df = n - 1 (para varianza)
- Usar en test de varianza y bondad de ajuste

## Inferencia estadística

### Intervalo de confianza para la media
- **σ conocida**: x̄ ± z_(α/2) · σ/√n
- **σ desconocida**: x̄ ± t_(α/2, n-1) · s/√n
- **n grande (≥30)**: x̄ ± z_(α/2) · s/√n (aproximación)

### Intervalo de confianza para la proporción
- p̂ ± z_(α/2) · √(p̂(1-p̂)/n)

### Test de hipótesis
- **Hipótesis nula (H₀)**: la que se quiere refutar
- **Hipótesis alternativa (H₁)**: lo que se quiere demostrar
- **Error tipo I (α)**: rechazar H₀ siendo cierta
- **Error tipo II (β)**: no rechazar H₀ siendo falsa
- **p-value**: probabilidad de obtener un resultado tan extremo si H₀ es cierta
- Si p-value < α: rechazar H₀
- **Z-test**: σ conocida o n ≥ 30
- **T-test**: σ desconocida y n < 30

### Test Z para la media
- Z = (x̄ - μ₀) / (σ/√n)

### Test T para la media
- t = (x̄ - μ₀) / (s/√n) con df = n-1

## Regresión lineal

### Recta de regresión
- y = a + bx
- b = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²
- a = ȳ - b·x̄

### Coeficiente de correlación (Pearson)
- r = Σ(xᵢ - x̄)(yᵢ - ȳ) / √[Σ(xᵢ - x̄)² · Σ(yᵢ - ȳ)²]
- -1 ≤ r ≤ 1
- r = 1: correlación perfecta positiva
- r = -1: correlación perfecta negativa
- r = 0: sin correlación lineal

### Coeficiente de determinación
- R² = r²: proporción de varianza explicada

## Errores comunes / Pitfalls

- **Varianza muestral**: dividir por (n-1), NO por n (corrección de Bessel)
- **p-value**: NO es P(H₀ es cierta). Es P(datos | H₀)
- **Correlación ≠ causalidad**: r alto no implica que una variable cause la otra
- **Normalidad**: test Z solo si σ conocida o n grande. Si no, usar t
- **Bayes**: confundir P(A|B) con P(B|A). Son distintas
- **Binomial**: verificar independencia y p constante
- **Intervalo de confianza**: no interpretar como "P(μ está en el IC) = 95%". Interpretación correcta: si repitiéramos el experimento muchas veces, el 95% de los IC contendrían μ

## Verificación

- [ ] Probabilidades: ¿están entre 0 y 1? ¿P(A) + P(Aᶜ) = 1?
- [ ] Media muestral: ¿entre el mínimo y el máximo?
- [ ] Varianza: siempre ≥ 0
- [ ] Correlación: -1 ≤ r ≤ 1
- [ ] p-value: < 1 (si es > 1, algo va mal)
- [ ] Regresión: verificar y̅ = a + b·x̄
