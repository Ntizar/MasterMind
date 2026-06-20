---
name: skill-math-statistics
version: 1.0.0
category: STEM/Mathematics
description: "Estadística y Probabilidad — Estadística descriptiva, probabilidad, distribuciones de probabilidad e inferencia estadística básica. Skill especializado para el ecosistema STEM de Mastermind."
tags: [estadistica, probabilidad, distribuciones, inferencia, media, varianza, binomial, normal, poisson, hipotesis]
author: Mastermind STEM
---

# skill-math-statistics — Estadística y Probabilidad

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas de **Estadística Descriptiva**, **Probabilidad**, **Distribuciones de Probabilidad** e **Inferencia Estadística Básica**. Es el skill especializado del ecosistema STEM de Mastermind para el área de estadística y probabilidad.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Estadística Descriptiva
- **Medidas de tendencia central**: media aritmética, mediana, moda, cuartiles, deciles, percentiles.
- **Medidas de dispersión**: rango, varianza poblacional y muestral, desviación estándar, coeficiente de variación, rango intercuartílico (IQR).
- **Medidas de forma**: asimetría (skewness), curtosis, coeficiente de Pearson.
- **Tablas de frecuencia**: tablas de distribución de frecuencias, histogramas, polígonos de frecuencia, ojivas.
- **Diagramas estadísticos**: diagrama de caja (boxplot), diagrama de tallo y hojas, diagrama de dispersión.
- **Covarianza y correlación**: coeficiente de correlación de Pearson, coeficiente de Spearman, interpretación.
- **Regresión lineal**: método de mínimos cuadrados, ecuación de la recta de regresión, coeficiente de determinación R².

### 2. Probabilidad
- **Conceptos fundamentales**: espacio muestral, evento, evento complementario, eventos mutuamente excluyentes, eventos independientes.
- **Reglas de probabilidad**: regla de la suma, regla de la multiplicación, probabilidad total, teorema de Bayes.
- **Conteo combinatorio**: principio de multiplicación, permutaciones (con y sin repetición), combinaciones, variaciones.
- **Probabilidad condicional**: P(A|B) = P(A∩B) / P(B), independencia estadística.
- **Teorema de Bayes**: P(Aᵢ|B) = P(B|Aᵢ)·P(Aᵢ) / Σ P(B|Aⱼ)·P(Aⱼ).
- **Diagramas de árbol**: representación gráfica de problemas de probabilidad secuencial.

### 3. Distribuciones de Probabilidad
- **Distribución binomial**: B(n, p), PMF P(X=k) = C(n,k)·pᵏ·(1-p)ⁿ⁻ᵏ, media = np, varianza = np(1-p), aplicaciones.
- **Distribución normal**: N(μ, σ²), función de densidad, estandarización Z = (X - μ) / σ, tabla de la normal estándar, regla empírica (68-95-99.7).
- **Distribución de Poisson**: P(X=k) = (λᵏ · e⁻λ) / k!, media = λ, varianza = λ, aplicaciones a eventos raros.
- **Distribución uniforme**: continua U(a,b) y discreta, densidad constante en el intervalo.
- **Distribución t de Student**: propiedades, grados de libertad, aplicaciones en inferencia con muestras pequeñas.
- **Distribución χ² (Chi-cuadrado)**: propiedades, aplicaciones en pruebas de bondad de ajuste e independencia.
- **Distribución F**: relación de dos varianzas, aplicaciones en ANOVA.
- **Convergencia de distribuciones**: Teorema Central del Límite, aproximación binomial a la normal.

### 4. Inferencia Estadística Básica
- **Estimación puntual**: estimadores de la media, varianza, proporción.
- **Intervalos de confianza**: para la media (σ conocida y desconocida), para la proporción, para la varianza.
  - Media con σ conocida: x̄ ± z_(α/2) · σ/√n
  - Media con σ desconocida: x̄ ± t_(α/2, n-1) · s/√n
  - Proporción: p̂ ± z_(α/2) · √(p̂(1-p̂)/n)
- **Pruebas de hipótesis**:
  - Planteamiento: H₀ (hipótesis nula) vs H₁ (hipótesis alternativa).
  - Errores tipo I (α) y tipo II (β).
  - Valor p y nivel de significancia.
  - Pruebas de una cola y dos colas.
  - Prueba z para la media (σ conocida).
  - Prueba t para la media (σ desconocida).
  - Prueba z para proporciones.
  - Prueba χ² para bondad de ajuste e independencia.

## Instrucciones Paso a Paso para el Agente

### Procedimiento General de Resolución

1. **Identificar el tipo de problema**: Clasificar en estadística descriptiva, probabilidad, distribución o inferencia.
2. **Extraer los datos**: Identificar variables, parámetros, tamaños de muestra y niveles de confianza/significancia.
3. **Seleccionar la fórmula o método** apropiado según la categoría.
4. **Realizar los cálculos** paso a paso, mostrando cada transformación.
5. **Interpretar el resultado** en el contexto del problema.
6. **Verificar** que la respuesta sea razonable y coherente.

### Procedimiento para Estadística Descriptiva

1. Organizar los datos en una tabla de frecuencias si es necesario.
2. Calcular la media: x̄ = Σxᵢ / n (o Σfᵢxᵢ / n para datos agrupados).
3. Calcular la mediana: ordenar datos, tomar el valor central (o promedio de los dos centrales si n es par).
4. Identificar la moda: valor con mayor frecuencia.
5. Calcular la varianza: σ² = Σ(xᵢ - x̄)² / n (poblacional) o s² = Σ(xᵢ - x̄)² / (n-1) (muestral).
6. Calcular la desviación estándar: σ = √σ² o s = √s².
7. Calcular coeficientes de asimetría y curtosis si se solicitan.
8. Interpretar las medidas en el contexto del problema.

### Procedimiento para Probabilidad

1. Definir el espacio muestral S y los eventos de interés.
2. Determinar si los eventos son mutuamente excluyentes, independientes o dependientes.
3. Aplicar la regla de probabilidad adecuada:
   - Eventos mutuamente excluyentes: P(A∪B) = P(A) + P(B)
   - Eventos generales: P(A∪B) = P(A) + P(B) - P(A∩B)
   - Eventos independientes: P(A∩B) = P(A) · P(B)
   - Probabilidad condicional: P(A|B) = P(A∩B) / P(B)
4. Para problemas de conteo: determinar si se trata de permutaciones, combinaciones o variaciones.
5. Aplicar el Teorema de Bayes cuando se requiera actualizar probabilidades con nueva información.

### Procedimiento para Distribuciones

1. Identificar la distribución apropiada según el contexto del problema.
2. Verificar las condiciones de aplicación:
   - Binomial: ensayos independientes, dos resultados, probabilidad constante.
   - Normal: variable continua, simétrica, definida por μ y σ.
   - Poisson: eventos raros, tasa constante, independencia entre eventos.
3. Estandarizar si es necesario (Z = (X - μ) / σ para la normal).
4. Consultar/tabular los valores correspondientes.
5. Interpretar la probabilidad calculada en el contexto del problema.

### Procedimiento para Inferencia Estadística

1. **Para intervalos de confianza**:
   - Identificar el parámetro de interés (media, proporción, varianza).
   - Determinar si σ es conocida o desconocida.
   - Seleccionar la distribución apropiada (Z o t).
   - Calcular el error estándar: SE = σ/√n o SE = s/√n.
   - Encontrar el valor crítico: z_(α/2) o t_(α/2, n-1).
   - Construir el intervalo: estimador ± valor crítico × SE.
   - Interpretar: "Con un [nivel]% de confianza, el parámetro está entre [límite inferior] y [límite superior]."

2. **Para pruebas de hipótesis**:
   - Plantear H₀ y H₁ claramente.
   - Determinar si la prueba es de una o dos colas.
   - Calcular la estadística de prueba (z, t, χ²).
   - Determinar el valor p o la región crítica.
   - Comparar el valor p con α (o la estadística con el valor crítico).
   - Tomar la decisión: rechazar o no rechazar H₀.
   - Interpretar el resultado en el contexto del problema.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Estadística Descriptiva
```
Dados los datos: 12, 15, 18, 22, 25, 28, 30, 35, 40. Calcula la media, mediana, moda, varianza muestral y desviación estándar.
```
**Respuesta esperada**: El agente calcula x̄ = 24, mediana = 25, no hay moda (todos los valores son únicos), s² = 84.25, s ≈ 9.18.

### Ejemplo 2: Probabilidad — Combinaciones
```
En una lotería se eligen 6 números de un total de 49. ¿Cuál es la probabilidad de acertar los 6 números?
```
**Respuesta esperada**: P = 1 / C(49,6) = 1 / 13,983,816 ≈ 7.15 × 10⁻⁸.

### Ejemplo 3: Distribución Binomial
```
Si el 30% de los estudiantes de una universidad son de primer año, y se seleccionan 10 estudiantes al azar, ¿cuál es la probabilidad de que exactamente 3 sean de primer año?
```
**Respuesta esperada**: X ~ B(10, 0.3), P(X=3) = C(10,3) · 0.3³ · 0.7⁷ = 120 · 0.027 · 0.08235 ≈ 0.2668.

### Ejemplo 4: Distribución Normal
```
Las alturas de una población siguen N(170, 25). ¿Qué porcentaje de personas mide entre 165 y 175 cm?
```
**Respuesta esperada**: Z₁ = (165-170)/5 = -1, Z₂ = (175-170)/5 = 1. P(-1 < Z < 1) ≈ 0.6827 = 68.27%.

### Ejemplo 5: Inferencia — Intervalo de Confianza
```
Una muestra de 36 estudiantes tiene media de 72 y desviación estándar de 12. Construye un intervalo de confianza al 95% para la media poblacional.
```
**Respuesta esperada**: Como n ≥ 30, usamos Z. SE = 12/√36 = 2. z₀.₀₂₅ = 1.96. IC = 72 ± 1.96 × 2 = [68.08, 75.92].

### Ejemplo 6: Inferencia — Prueba de Hipótesis
```
Se afirma que la media de una población es 100. Una muestra de 25 observaciones da x̄ = 105 y s = 15. ¿Se rechaza H₀ al nivel α = 0.05 (prueba bilateral)?
```
**Respuesta esperada**: H₀: μ = 100, H₁: μ ≠ 100. t = (105-100)/(15/√25) = 5/3 ≈ 1.667. t₀.₀₂₅,₂₄ ≈ 2.064. Como |1.667| < 2.064, no se rechaza H₀.

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `math-estadistica-probabilidad` | `/hermes-home/skills/stem/math/math-estadistica-probabilidad` | Estadística y probabilidad completa — referencia principal del ecosistema |
| `math-estadistica-probabilidad-eng` | `/hermes-home/skills/stem/math/math-estadistica-probabilidad-eng` | Versión en inglés del skill de estadística y probabilidad |

### Cuándo derivar a otros skills

- Si el problema requiere **diseño experimental avanzado o ANOVA** → derivar a `math-estadistica-probabilidad`.
- Si el problema requiere **regresión múltiple o análisis de varianza** → derivar a `math-estadistica-probabilidad`.
- Si se necesita la versión en **inglés** del contenido → derivar a `math-estadistica-probabilidad-eng`.
- Si el problema involucra **procesos estocásticos o cadenas de Markov** → derivar a `math-estadistica-probabilidad`.

## Pitfalls — Errores Comunes

### Estadística Descriptiva
- **Confundir varianza poblacional con muestral**: la varianza poblacional divide por n, la muestral divide por n-1 (corrección de Bessel). Usar la correcta según el contexto.
- **Calcular la mediana sin ordenar datos**: siempre ordenar los datos de menor a mayor antes de encontrar la mediana.
- **Confundir correlación con causalidad**: un coeficiente de correlación alto no implica que una variable cause cambios en la otra.
- **Interpretar mal el coeficiente de variación**: CV = (s/x̄) × 100% es un porcentaje, no una cantidad absoluta.

### Probabilidad
- **Confundir eventos independientes con mutuamente excluyentes**: eventos mutuamente excluyentes NO pueden ser independientes (a menos que uno tenga probabilidad 0). Si A y B son mutuamente excluyentes, P(A∩B) = 0, pero P(A)·P(B) ≠ 0 en general.
- **Error del jugador**: creer que después de una secuencia de resultados, el siguiente "debe ser" diferente. En ensayos independientes, cada evento mantiene su probabilidad.
- **Aplicar Bayes incorrectamente**: recordar que P(A|B) ≠ P(B|A). El teorema de Bayes requiere el denominador completo (suma sobre todos los eventos Aᵢ).
- **Confundir permutaciones con combinaciones**: si el orden importa → permutación; si no importa → combinación.

### Distribuciones
- **Usar la normal para muestras pequeñas sin justificación**: la aproximación normal a la binomial solo es válida cuando np ≥ 5 y n(1-p) ≥ 5.
- **Confundir parámetros de la Poisson**: en la distribución de Poisson, media y varianza son iguales (ambas = λ).
- **Estandarizar incorrectamente**: Z = (X - μ) / σ, no (X + μ) / σ ni (X - σ) / μ.
- **Usar la distribución incorrecta**: verificar las condiciones de cada distribución antes de aplicarla.

### Inferencia Estadística
- **Confundir α con β**: α es la probabilidad de error tipo I (rechazar H₀ cuando es verdadera); β es la probabilidad de error tipo II (no rechazar H₀ cuando es falsa).
- **Interpretar mal el valor p**: el valor p NO es la probabilidad de que H₀ sea verdadera. Es la probabilidad de obtener un resultado tan extremo como el observado, asumiendo que H₀ es verdadera.
- **Confundir intervalo de confianza con probabilidad**: un IC al 95% no significa que hay 95% de probabilidad de que μ esté en el intervalo. Significa que el método produce intervalos que contienen μ en el 95% de los casos.
- **Usar Z cuando σ es desconocida y n es pequeño**: si σ es desconocida y n < 30, usar la distribución t de Student, no la normal estándar.
- **Olvidar verificar supuestos**: las pruebas paramétricas requieren normalidad, independencia y homocedasticidad. Verificar estos supuestos antes de aplicar la prueba.

## Cuándo Usar Este Skill

Usa este skill cuando:

1. El problema requiere **calcular medidas descriptivas** (media, mediana, moda, varianza, desviación estándar).
2. El problema involucra **cálculo de probabilidades** usando reglas de suma, multiplicación, condicional o Bayes.
3. El problema requiere **distribuciones de probabilidad** (binomial, normal, Poisson, etc.).
4. El problema requiere **construir intervalos de confianza** para medias, proporciones o varianzas.
5. El problema requiere **realizar pruebas de hipótesis** (z-test, t-test, χ²-test).
6. El problema involucra **regresión lineal simple** y correlación.
7. El problema es de nivel **preuniversitario o de primer/segundo año universitario**.

**No** uses este skill cuando:
- El problema requiere **diseño experimental avanzado, ANOVA o regresión múltiple** → usar `math-estadistica-probabilidad`.
- El problema requiere **procesos estocásticos, cadenas de Markov o teoría de colas** → usar `math-estadistica-probabilidad`.
- El problema requiere **estadística bayesiana avanzada** → usar `math-estadistica-probabilidad`.
- El problema requiere **muestreo estratificado o por conglomerados** → usar `math-estadistica-probabilidad`.

## Formato de Salida Esperado

El agente debe presentar las soluciones en el siguiente formato:

```
### Problema
[Enunciado del problema]

### Datos Identificados
- [Variable 1]: [valor]
- [Variable 2]: [valor]
- [Tipo de problema]: [descripción]

### Solución
[Paso 1: Fórmula/método seleccionado]
[Paso 2: Sustitución de valores]
[Paso 3: Cálculo]
[Paso 4: Resultado intermedio (si aplica)]

### Resultado Final
[Respuesta clara y destacada]

### Interpretación
[Interpretación del resultado en el contexto del problema]

### Notas
[Observaciones adicionales, verificación, etc.]
```

## Notas Adicionales

- Este skill es el **pilar estadístico** del ecosistema matemático de Mastermind.
- Todos los cálculos deben mostrarse con **pasos intermedios claros** para fines educativos.
- Se recomienda usar **notación LaTeX** para expresiones matemáticas cuando sea posible.
- En problemas de inferencia, siempre **interpretar el resultado en el contexto** del problema, no solo dar el número.
- Cuando se use la distribución normal estándar, indicar los valores de Z consultados en la tabla.
- En pruebas de hipótesis, siempre especificar claramente **H₀, H₁, estadística de prueba, valor p y decisión**.
- Para la distribución binomial, verificar siempre que **np ≥ 5 y n(1-p) ≥ 5** antes de usar la aproximación normal.
