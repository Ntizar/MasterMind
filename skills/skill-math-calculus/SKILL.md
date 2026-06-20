---
name: skill-math-calculus
version: 1.0.0
category: STEM/Mathematics
description: "Cálculo Avanzado — Derivadas avanzadas, integrales, ecuaciones diferenciales, optimización y series. Skill especializado para el ecosistema STEM de Mastermind."
tags: [calculo, derivadas, integrales, edos, optimizacion, lagrange, series, taylor, maclaurin, convergencia]
author: Mastermind STEM
---

# skill-math-calculus — Cálculo Avanzado

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas de **Derivadas Avanzadas**, **Integrales**, **Ecuaciones Diferenciales Ordinarias (EDOs)**, **Optimización** y **Series y Sucesiones**. Es el skill avanzado de cálculo del ecosistema STEM de Mastermind, orientado a estudiantes de nivel universitario.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Derivadas Avanzadas
- **Regla de la cadena**: d/dx [f(g(x))] = f'(g(x)) · g'(x). Aplicación a funciones compuestas anidadas.
- **Derivación implícita**: diferenciar ecuaciones donde y no está explícitamente despejada. d/dx [f(x,y)] = ∂f/∂x + (∂f/∂y) · y'.
- **Derivación logarítmica**: aplicar ln a ambos lados para simplificar derivadas de productos, cocientes o potencias: d/dx [f(x)^g(x)] = f(x)^g(x) · d/dx [g(x) · ln(f(x))].
- **Derivadas de orden superior**: f''(x), f'''(x), ..., f⁽ⁿ⁾(x).
- **Derivadas de funciones definidas por integrales**: d/dx ∫ₐˣ f(t) dt = f(x) (Teorema Fundamental del Cálculo).
- **Derivadas parciales**: ∂f/∂x, ∂f/∂y, manteniendo las otras variables constantes.
- **Gradiente**: ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z). Dirección de máximo crecimiento.
- **Derivadas direccionales**: Dᵤf = ∇f · u, donde u es un vector unitario.
- **Funciones hiperbólicas**: senh(x), cosh(x), tanh(x) y sus derivadas.
- **Derivadas de funciones inversas**: d/dx [arcsen(x)] = 1/√(1-x²), d/dx [arcosen(x)] = 1/(x√(x²-1)), etc.

### 2. Integrales
- **Integrales indefinidas**: antiderivadas, reglas básicas (potencia, exponencial, logarítmica, trigonométricas).
  - ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
  - ∫ eˣ dx = eˣ + C
  - ∫ 1/x dx = ln|x| + C
  - ∫ cos(x) dx = sen(x) + C
  - ∫ sen(x) dx = -cos(x) + C
- **Integrales definidas**: ∫ₐᵇ f(x) dx = F(b) - F(a) (Teorema Fundamental del Cálculo).
  - Propiedades: linealidad, aditividad del intervalo, valor medio.
  - Desigualdades: si f(x) ≥ g(x) en [a,b], entonces ∫ₐᵇ f(x) dx ≥ ∫ₐᵇ g(x) dx.
- **Técnicas de integración**:
  - **Sustitución (cambio de variable)**: ∫ f(g(x)) · g'(x) dx = ∫ f(u) du, donde u = g(x).
  - **Integración por partes**: ∫ u dv = uv - ∫ v du (regla LIATE: Logarítmica, Inversa trigonométrica, Algebraica, Trigonométrica, Exponencial).
  - **Fracciones parciales**: descomponer R(x) = P(x)/Q(x) en fracciones más simples.
    - Factores lineales distintos: A/(x-a)
    - Factores lineales repetidos: A₁/(x-a) + A₂/(x-a)² + ...
    - Factores cuadráticos: (Ax+B)/(ax²+bx+c)
  - **Sustituciones trigonométricas**: x = a·sen(θ), x = a·tan(θ), x = a·sec(θ).
  - **Sustitución Euler**: para integrales con √(ax²+bx+c).
- **Integrales impropias**: límites infinitos o integrandos con singularidades.
  - ∫ₐ^∞ f(x) dx = lim(t→∞) ∫ₐᵗ f(x) dx
  - Criterios de convergencia: comparación, límite, integral.

### 3. Ecuaciones Diferenciales Ordinarias (EDOs)
- **EDOs de primer orden**:
  - **Separables**: dy/dx = f(x)·g(y) ⟹ dy/g(y) = f(x)dx ⟹ ∫ dy/g(y) = ∫ f(x)dx.
  - **Lineales**: dy/dx + P(x)y = Q(x). Factor integrante: μ(x) = e^(∫P(x)dx). Solución: y = (1/μ(x)) · ∫ μ(x)·Q(x) dx.
  - **Exactas**: M(x,y)dx + N(x,y)dy = 0, exacta si ∂M/∂y = ∂N/∂x. Solución: φ(x,y) = C donde ∂φ/∂x = M y ∂φ/∂y = N.
  - **Bernoulli**: dy/dx + P(x)y = Q(x)yⁿ. Sustitución: v = y^(1-n).
  - **Homogéneas**: dy/dx = F(y/x). Sustitución: y = vx.
- **EDOs de segundo orden lineales con coeficientes constantes**:
  - **Homogéneas**: ay'' + by' + cy = 0. Ecuación característica: ar² + br + c = 0.
    - Raíces reales distintas r₁, r₂: y = C₁e^(r₁x) + C₂e^(r₂x)
    - Raíces repetidas r: y = (C₁ + C₂x)e^(rx)
    - Raíces complejas α ± βi: y = e^(αx)(C₁cos(βx) + C₂sen(βx))
  - **No homogéneas**: ay'' + by' + cy = g(x). y = yₕ + yₚ (solución homogénea + particular).
    - Método de coeficientes indeterminados.
    - Método de variación de parámetros.
- **Sistemas de EDOs lineales**: representación matricial X' = AX.

### 4. Optimización
- **Máximos y mínimos de una variable**:
  - Puntos críticos: f'(x) = 0 o f'(x) no existe.
  - Primera derivada: analizar el signo de f'(x) alrededor del punto crítico.
  - Segunda derivada: f''(x) > 0 → mínimo, f''(x) < 0 → máximo, f''(x) = 0 → inconcluso.
  - Extremos absolutos en intervalos cerrados: evaluar en puntos críticos y extremos del intervalo.
- **Optimización con restricciones**:
  - **Multiplicadores de Lagrange**: maximizar/minimizar f(x,y) sujeto a g(x,y) = c.
    - ∇f = λ∇g ⟹ ∇f - λ∇g = 0
    - Resolver el sistema: ∂f/∂x = λ·∂g/∂x, ∂f/∂y = λ·∂g/∂y, g(x,y) = c.
  - Extensión a n variables: ∇f = λ₁∇g₁ + λ₂∇g₂ + ...
- **Problemas de optimización aplicada**:
  - Máximo volumen/minimizar superficie.
  - Minimizar costos/maximizar beneficios.
  - Problemas de distancia mínima.
  - Problemas de ingeniería y física.

### 5. Series y Sucesiones
- **Sucesiones numéricas**:
  - Definición: función f: N → R, aₙ = f(n).
  - Límite de una sucesión: lim(n→∞) aₙ = L.
  - Sucesiones monótonas y acotadas: teorema de convergencia monótona.
  - Sucesiones recurrentes: aₙ₊₁ = f(aₙ).
- **Series numéricas**:
  - Definición: Σ aₙ = a₁ + a₂ + a₃ + ...
  - Serie parcial: Sₙ = Σₖ₌₁ⁿ aₖ. La serie converge si lim(n→∞) Sₙ existe.
  - **Criterios de convergencia**:
    - Término nulo: si Σ aₙ converge, entonces lim(aₙ) = 0 (contrapositiva: si lim(aₙ) ≠ 0, la serie diverge).
    - Serie geométrica: Σ arⁿ converge si |r| < 1, suma = a/(1-r).
    - Serie telescópica: términos que se cancelan parcialmente.
    - Comparación directa: si 0 ≤ aₙ ≤ bₙ y Σ bₙ converge, entonces Σ aₙ converge.
    - Comparación por límite: lim(aₙ/bₙ) = L ∈ (0,∞) ⟹ ambas series convergen o divergen juntas.
    - Razón (d'Alembert): lim|aₙ₊₁/aₙ| = L < 1 → converge, L > 1 → diverge, L = 1 → inconcluso.
    - Raíz (Cauchy): lim|aₙ|^(1/n) = L < 1 → converge, L > 1 → diverge, L = 1 → inconcluso.
    - Integral: si f es positiva, continua y decreciente, Σ f(n) converge ⟺ ∫ f(x)dx converge.
    - Alternante (Leibniz): Σ (-1)ⁿbₙ converge si bₙ es decreciente y lim(bₙ) = 0.
    - Absoluta: si Σ |aₙ| converge, entonces Σ aₙ converge.
- **Series de potencias**:
  - Forma: Σ aₙ(x - c)ⁿ.
  - Radio de convergencia R: usar razón o raíz.
  - Intervalo de convergencia: (c-R, c+R), verificar extremos.
- **Series de Taylor y Maclaurin**:
  - Taylor: f(x) = Σₙ₌₀^∞ [f⁽ⁿ⁾(a)/n!] · (x-a)ⁿ
  - Maclaurin (a = 0): f(x) = Σₙ₌₀^∞ [f⁽ⁿ⁾(0)/n!] · xⁿ
  - Series notables:
    - eˣ = 1 + x + x²/2! + x³/3! + ...
    - sen(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
    - cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
    - ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ... (|x| < 1)
    - 1/(1-x) = 1 + x + x² + x³ + ... (|x| < 1)
    - (1+x)ᵐ = 1 + mx + m(m-1)x²/2! + ... (serie binomial generalizada)
  - **Cota del error (Lagrange)**: |Rₙ(x)| ≤ M · |x-a|ⁿ⁺¹ / (n+1)!, donde M = max|f⁽ⁿ⁺¹⁾(z)| en el intervalo.

## Instrucciones Paso a Paso para el Agente

### Procedimiento General de Resolución

1. **Identificar el tipo de problema**: Clasificar en derivadas, integrales, EDOs, optimización o series.
2. **Seleccionar la técnica** apropiada según la estructura del problema.
3. **Aplicar la técnica** paso a paso, justificando cada paso.
4. **Verificar** la solución derivando/integrando o sustituyendo.
5. **Interpretar** el resultado en el contexto del problema.

### Procedimiento para Derivadas Avanzadas

1. Para regla de la cadena: identificar la función exterior e interior, derivar la exterior evaluada en la interior, multiplicar por la derivada de la interior.
2. Para derivación implícita: diferenciar ambos lados de la ecuación respecto a x, tratar y como función de x (aplicar cadena), despejar y'.
3. Para derivación logarítmica: aplicar ln a ambos lados, usar propiedades del logaritmo para simplificar, diferenciar implícitamente, despejar y'.
4. Para derivadas parciales: derivar respecto a una variable manteniendo las demás constantes.
5. Para funciones hiperbólicas: recordar que d/dx[senh(x)] = cosh(x), d/dx[cosh(x)] = senh(x), d/dx[tanh(x)] = sech²(x).

### Procedimiento para Integrales

1. Para integrales indefinidas: identificar la forma de la integral y aplicar la técnica correspondiente.
2. Para sustitución: identificar u = g(x) tal que du = g'(x)dx, cambiar la integral a términos de u, integrar, volver a x.
3. Para integración por partes: seleccionar u y dv según la regla LIATE, calcular du y v, aplicar ∫u dv = uv - ∫v du.
4. Para fracciones parciales: factorizar el denominador, establecer la descomposición, resolver el sistema de ecuaciones para los coeficientes.
5. Para integrales definidas: encontrar la antiderivada, evaluar en los límites, restar F(b) - F(a).
6. Para integrales impropias: calcular el límite correspondiente y verificar convergencia.

### Procedimiento para EDOs

1. Identificar el tipo de EDO (separable, lineal, exacta, etc.).
2. Para separables: separar variables, integrar ambos lados, aplicar condición inicial si se da.
3. Para lineales de primer orden: identificar P(x) y Q(x), calcular el factor integrante μ(x) = e^(∫P(x)dx), multiplicar la EDO por μ(x), integrar.
4. Para exactas: verificar ∂M/∂y = ∂N/∂x, encontrar φ(x,y) integrando M respecto a x y N respecto a y, igualar a C.
5. Para EDOs de segundo orden homogéneas: resolver la ecuación característica, clasificar las raíces, escribir la solución general.
6. Para EDOs no homogéneas: encontrar yₕ (solución homogénea) y yₚ (solución particular), sumar: y = yₕ + yₚ.

### Procedimiento para Optimización

1. Definir la función objetivo f(x₁, x₂, ..., xₙ) y las restricciones gᵢ(x₁, x₂, ..., xₙ) = cᵢ.
2. Para optimización sin restricciones:
   - Encontrar puntos críticos: ∇f = 0.
   - Clasificar usando la matriz hessiana o la primera derivada.
3. Para optimización con restricciones (Lagrange):
   - Formar el Lagrangiano: L(x,y,λ) = f(x,y) - λ(g(x,y) - c).
   - Resolver ∇L = 0: ∂L/∂x = 0, ∂L/∂y = 0, ∂L/∂λ = 0.
   - Evaluar f en los puntos críticos encontrados.
4. Verificar que la solución sea un máximo o mínimo y que satisfaga las restricciones.

### Procedimiento para Series y Sucesiones

1. Para límites de sucesiones: aplicar propiedades de límites, regla de L'Hôpital si es necesario.
2. Para criterios de convergencia de series:
   - Verificar primero si lim(aₙ) = 0 (si no, diverge).
   - Identificar el tipo de serie (geométrica, telescópica, p-series, etc.).
   - Si no es reconocible, aplicar comparación, razón, raíz o integral.
   - Para series alternantes, aplicar Leibniz.
3. Para series de Taylor/Maclaurin:
   - Calcular las derivadas f⁽ⁿ⁾(a) o f⁽ⁿ⁾(0).
   - Evaluar en el punto a o 0.
   - Construir la serie usando la fórmula.
   - Determinar el radio de convergencia usando razón o raíz.
4. Para aproximar funciones: usar la serie de Taylor truncada y estimar el error con la cota de Lagrange.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Derivada — Regla de la Cadena Anidada
```
Encuentra la derivada de f(x) = sen³(2x² + 1).
```
**Respuesta esperada**: f'(x) = 3sen²(2x² + 1) · cos(2x² + 1) · 4x = 12x · sen²(2x² + 1) · cos(2x² + 1).

### Ejemplo 2: Derivada — Implícita
```
Encuentra y' si x² + y² = 25.
```
**Respuesta esperada**: 2x + 2y·y' = 0 ⟹ y' = -x/y.

### Ejemplo 3: Integral — Por Partes
```
Calcula ∫ x · eˣ dx.
```
**Respuesta esperada**: u = x, dv = eˣdx ⟹ du = dx, v = eˣ. ∫xeˣdx = xeˣ - ∫eˣdx = xeˣ - eˣ + C = eˣ(x-1) + C.

### Ejemplo 4: Integral — Fracciones Parciales
```
Calcula ∫ (3x+5)/(x²+x-2) dx.
```
**Respuesta esperada**: x²+x-2 = (x+2)(x-1). (3x+5)/((x+2)(x-1)) = A/(x+2) + B/(x-1). A = -1, B = 4. ∫ = -ln|x+2| + 4ln|x-1| + C.

### Ejemplo 5: EDO — Separable
```
Resuelve dy/dx = 2x · y, con y(0) = 3.
```
**Respuesta esperada**: dy/y = 2x dx ⟹ ln|y| = x² + C ⟹ y = Ce^(x²). y(0) = 3 ⟹ C = 3. y = 3e^(x²).

### Ejemplo 6: Optimización — Lagrange
```
Maximiza f(x,y) = xy sujeto a x + y = 10.
```
**Respuesta esperada**: L = xy - λ(x+y-10). ∂L/∂x = y - λ = 0, ∂L/∂y = x - λ = 0, x+y = 10. ⟹ x = y = 5, f(5,5) = 25 (máximo).

### Ejemplo 7: Serie de Maclaurin
```
Encuentra la serie de Maclaurin de f(x) = cos(x) hasta el término x⁶.
```
**Respuesta esperada**: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ... = 1 - x²/2 + x⁴/24 - x⁶/720 + ...

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `math-calculo-integral` | `/hermes-home/skills/stem/math/math-calculo-integral` | Integrales múltiples, integrales de línea y superficie, teoremas de Green, Stokes y Gauss |
| `math-calculo-diferencial` | `/hermes-home/skills/stem/math/math-calculo-diferencial` | Derivadas parciales, gradientes, optimización multivariable, teorema de la función implícita |
| `math-sucesiones-series` | `/hermes-home/skills/stem/math/math-sucesiones-series` | Sucesiones y series numéricas avanzadas, series de Fourier, convergencia uniforme |
| `math-ecuaciones` | `/hermes-home/skills/stem/math/math-ecuaciones` | Ecuaciones diferenciales avanzadas, ecuaciones en derivadas parciales, transformadas de Laplace |
| `math-funciones` | `/hermes-home/skills/stem/math/math-funciones` | Análisis profundo de funciones, asíntotas, composición, inversión |
| `math-logaritmos-exponenciales` | `/hermes-home/skills/stem/math/math-logaritmos-exponenciales` | Funciones logarítmicas y exponenciales en detalle, ecuaciones con ellas |

### Cuándo derivar a otros skills

- Si el problema requiere **integrales múltiples (dobles, triples)** → derivar a `math-calculo-integral`.
- Si el problema requiere **integrales de línea, superficie o teoremas de Green/Stokes/Gauss** → derivar a `math-calculo-integral`.
- Si el problema requiere **derivadas parciales, gradientes o optimización multivariable** → derivar a `math-calculo-diferencial`.
- Si el problema requiere **series de Fourier o convergencia uniforme** → derivar a `math-sucesiones-series`.
- Si el problema requiere **EDOs avanzadas, EDPs o transformadas de Laplace** → derivar a `math-ecuaciones`.
- Si el problema requiere **análisis profundo de funciones** → derivar a `math-funciones`.

## Pitfalls — Errores Comunes

### Derivadas Avanzadas
- **Olvidar la regla de la cadena**: al derivar f(g(x)), siempre multiplicar por g'(x). Es el error más frecuente.
- **Derivación implícita incorrecta**: al diferenciar términos con y, aplicar siempre la regla de la cadena: d/dx[f(y)] = f'(y) · y'.
- **Error en derivación logarítmica**: ln(f(x)^g(x)) = g(x) · ln(f(x)), no f(x) · ln(g(x)).
- **Confundir d/dx[e^(f(x))] con d/dx[ln(f(x))]**: el primero es e^(f(x)) · f'(x), el segundo es f'(x)/f(x).
- **Derivadas de funciones hiperbólicas**: d/dx[cosh(x)] = senh(x), NO cosh(x). Es fácil confundir con las trigonométricas.

### Integrales
- **Olvidar la constante +C** en integrales indefinidas: siempre agregar +C al resultado.
- **Sustitución incorrecta**: verificar que du = g'(x)dx esté presente o pueda obtenerse multiplicando/dividiendo.
- **Errores en integración por partes**: seleccionar u y dv incorrectamente (regla LIATE). Elegir u como la función que se simplifica al derivar.
- **Fracciones parciales mal descompuestas**: verificar que el grado del numerador sea menor que el del denominador antes de descomponer.
- **Confundir integrales impropias con definidas**: las impropias requieren límites, no se pueden evaluar directamente.
- **Error en el Teorema Fundamental del Cálculo**: ∫ₐᵇ f(x)dx = F(b) - F(a), NO F(b) + F(a).

### Ecuaciones Diferenciales
- **Confundir EDO separable con lineal**: una EDO es separable si se puede escribir como dy/g(y) = f(x)dx. Es lineal si tiene la forma dy/dx + P(x)y = Q(x).
- **Factor integrante incorrecto**: μ(x) = e^(∫P(x)dx), NO e^(P(x)).
- **Error en la ecuación característica**: para ay'' + by' + cy = 0, la ecuación es ar² + br + c = 0, no ar² + br - c = 0.
- **Raíces complejas**: para α ± βi, la solución es e^(αx)(C₁cos(βx) + C₂sen(βx)), NO C₁e^(αx) + C₂e^(βx).
- **Método de coeficientes indeterminados**: la forma de yₚ debe ser linealmente independiente de yₕ. Si hay solapamiento, multiplicar por x.

### Optimización
- **Olvidar verificar que los puntos críticos sean máximos o mínimos**: usar la segunda derivada o el criterio de la primera derivada.
- **No evaluar los extremos del intervalo**: para máximos/mínimos absolutos en un intervalo cerrado, evaluar también en los extremos.
- **Error en Lagrange**: el multiplicador λ NO es el valor de la función objetivo. Es un parámetro auxiliar.
- **Confundir máximo con mínimo en problemas de optimización**: verificar el contexto del problema.

### Series y Sucesiones
- **Confundir convergencia de sucesión con convergencia de serie**: una sucesión puede converger a L ≠ 0, pero la serie Σaₙ diverge (criterio del término nulo).
- **Aplicar el criterio de la razón incorrectamente**: L = 1 es inconcluso. No asumir convergencia o divergencia.
- **Radio de convergencia**: R = 1/L (razón) o R = 1/L (raíz). Si L = 0, R = ∞. Si L = ∞, R = 0.
- **Error en la serie de Taylor**: recordar que el coeficiente es f⁽ⁿ⁾(a)/n!, no f⁽ⁿ⁾(a) sin dividir por n!.
- **Confundir serie de Taylor con Maclaurin**: Maclaurin es un caso particular de Taylor con a = 0.
- **No verificar los extremos del intervalo de convergencia**: el radio de convergencia da el intervalo abierto, hay que verificar convergencia en los extremos por separado.

## Cuándo Usar Este Skill

Usa este skill cuando:

1. El problema requiere **derivadas avanzadas** (regla de la cadena, implícita, logarítmica, parciales, direccionales).
2. El problema requiere **calcular integrales** (indefinidas, definidas, por sustitución, partes, fracciones parciales).
3. El problema requiere **resolver ecuaciones diferenciales** (separables, lineales, exactas, de segundo orden).
4. El problema requiere **optimización** (máximos/mínimos, Lagrange, problemas de aplicación).
5. El problema requiere **analizar series y sucesiones** (convergencia, Taylor, Maclaurin, series de potencias).
6. El problema es de nivel **universitario de segundo/año o superior** en cálculo.
7. El problema involucra **integrales impropias** o técnicas avanzadas de integración.

**No** uses este skill cuando:
- El problema requiere **integrales múltiples o integrales de línea/superficie** → usar `math-calculo-integral`.
- El problema requiere **optimización multivariable con gradiente y Hessiana** → usar `math-calculo-diferencial`.
- El problema requiere **series de Fourier** → usar `math-sucesiones-series`.
- El problema requiere **transformadas de Laplace o EDPs** → usar `math-ecuaciones`.

## Formato de Salida Esperado

El agente debe presentar las soluciones en el siguiente formato:

```
### Problema
[Enunciado del problema]

### Tipo de Problema
[Derivada/Integral/EDO/Optimización/Serie]

### Solución
[Paso 1: Identificación de la técnica]
[Paso 2: Desarrollo paso a paso]
[Paso 3: Cálculo detallado]
[Paso 4: Resultado intermedio (si aplica)]
[Paso 5: Verificación]

### Resultado Final
[Respuesta clara y destacada]

### Notas
[Observaciones adicionales, alternativas de solución, dominio de validez, etc.]
```

## Notas Adicionales

- Este skill es el **pilar de cálculo avanzado** del ecosistema matemático de Mastermind.
- Todos los cálculos deben mostrarse con **pasos intermedios claros** para fines educativos.
- Se recomienda usar **notación LaTeX** para expresiones matemáticas cuando sea posible.
- En integrales, siempre **verificar la derivada del resultado** para confirmar la antiderivada.
- En EDOs, siempre **verificar la solución** sustituyendo en la ecuación original.
- En series, siempre **verificar los criterios de convergencia** antes de calcular la suma.
- En optimización con Lagrange, verificar que la solución satisfaga **todas las restricciones**.
- Para la cota del error de Taylor, usar el **máximo de la derivada (n+1)-ésima** en el intervalo.
- En integrales impropias, siempre **justificar la convergencia** antes de dar el resultado numérico.
