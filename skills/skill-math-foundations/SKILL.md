---
name: skill-math-foundations
version: 1.0.0
category: STEM/Mathematics
description: "Fundamentos de Matemáticas — Álgebra, Geometría euclidiana, Trigonometría y Cálculo diferencial básico. Skill principal que consolida las bases matemáticas para el ecosistema STEM de Mastermind."
tags: [algebra, geometria, trigonometria, calculo, fundamentos, polinomios, triángulos, limites, derivadas]
author: Mastermind STEM
---

# skill-math-foundations — Fundamentos de Matemáticas

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas de **Álgebra**, **Geometría euclidiana**, **Trigonometría** y **Cálculo diferencial básico**. Es el skill fundamental que consolida las bases matemáticas del ecosistema STEM de Mastermind, sirviendo como punto de partida para los skills avanzados de cálculo, álgebra lineal, estadística y más.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Álgebra
- **Ecuaciones lineales y cuadráticas**: resolución de ecuaciones de primer y segundo grado, ecuaciones con parámetros.
- **Sistemas de ecuaciones**: sustitución, igualación, reducción, graficación.
- **Polinomios**: operaciones (suma, resta, multiplicación, división), teorema del resto, teorema fundamental del álgebra.
- **Factorización**: factor común, trinomios, diferencia de cuadrados, suma/diferencia de cubos, factorización por agrupación.
- **Fracciones algebraicas**: simplificación, suma, resta, multiplicación, división.
- **Desigualdades e inecuaciones**: lineales, cuadráticas, con valor absoluto, intervalos.
- **Números complejos**: operaciones básicas, forma polar, fórmula de De Moivre.

### 2. Geometría Euclidiana
- **Triángulos**: clasificación, teorema de Pitágoras, semejanza, congruencia, teorema de Thales, puntos notables (ortocentro, baricentro, circuncentro, incentro).
- **Círculos**: elementos, ángulos inscritos y centrales, tangentes, secantes, arcos, sectores y segmentos circulares.
- **Polígonos**: clasificación, ángulos interiores y exteriores, diagonales, polígonos regulares.
- **Áreas y perímetros**: triángulos, cuadriláteros, polígonos regulares, círculos.
- **Volúmenes y áreas superficiales**: prismas, pirámides, cilindros, conos, esferas.
- **Transformaciones geométricas**: traslación, rotación, reflexión, homotecia.

### 3. Trigonometría
- **Funciones trigonométricas**: seno, coseno, tangente, cotangente, secante, cosecante — definición, dominio, rango, gráficos.
- **Identidades trigonométricas**: fundamentales, pitagóricas, ángulo doble, ángulo mitad, suma y diferencia, producto a suma.
- **Ecuaciones trigonométricas**: resolución general, soluciones en intervalos dados.
- **Ley de senos y cosenos**: resolución de triángulos oblicuángulos.
- **Funciones inversas**: arcsen, arcosen, arcotangente — dominio, rango, propiedades.
- **Ecuaciones trigonométricas avanzadas**: sustitución, factorización, uso de identidades.

### 4. Cálculo Diferencial Básico
- **Límites**: definición intuitiva y formal (ε-δ), límites laterales, límites al infinito, indeterminaciones (0/0, ∞/∞, 0·∞, ∞−∞, 0⁰, 1^∞, ∞⁰).
- **Continuidad**: definición, tipos de discontinuidad, teorema del valor intermedio, teorema de Bolzano.
- **Derivadas**: definición como límite de la razón incremental, interpretación geométrica (pendiente de la recta tangente).
- **Reglas de derivación**: potencia, producto, cociente, cadena, derivadas de funciones elementales (polinomios, exponenciales, logarítmicas, trigonométricas, inversas trigonométricas).
- **Aplicaciones de derivadas**: funciones crecientes/decrecientes, extremos relativos y absolutos, concavidad, puntos de inflexión, regla de L'Hôpital.

## Instrucciones Paso a Paso para el Agente

### Procedimiento General de Resolución

1. **Identificar el tipo de problema**: Clasificar el problema en una de las cuatro categorías principales (Álgebra, Geometría, Trigonometría, Cálculo).
2. **Determinar el nivel de complejidad**: Decidir si se necesita el skill actual o si se debe derivar a un skill más especializado.
3. **Aplicar la metodología específica** de la categoría correspondiente (ver secciones detalladas abajo).
4. **Verificar la solución**: Comprobar resultados mediante sustitución, análisis dimensional o razonamiento alternativo.
5. **Presentar la respuesta** de forma clara, con pasos intermedios y justificación.

### Procedimiento para Álgebra

1. Leer y comprender el enunciado del problema algebraico.
2. Identificar las variables, coeficientes y operaciones involucradas.
3. Seleccionar la técnica de resolución apropiada:
   - Para ecuaciones: aislar la variable aplicando operaciones inversas.
   - Para polinomios: identificar el tipo de factorización aplicable.
   - Para sistemas: elegir el método más eficiente (sustitución, reducción, igualación).
4. Ejecutar los pasos algebraicos con precisión, justificando cada transformación.
5. Verificar la solución sustituyendo en la ecuación original.
6. Expresar la respuesta en el formato solicitado (conjunto solución, intervalo, etc.).

### Procedimiento para Geometría

1. Dibujar o visualizar la figura geométrica descrita.
2. Identificar los datos conocidos y lo que se busca determinar.
3. Seleccionar los teoremas, fórmulas o propiedades relevantes.
4. Aplicar las relaciones geométricas apropiadas.
5. Realizar los cálculos con precisión, manteniendo unidades consistentes.
6. Verificar que la respuesta sea razonable (positiva, del orden correcto, etc.).

### Procedimiento para Trigonometría

1. Identificar si el problema involucra funciones, identidades o ecuaciones trigonométricas.
2. Para identidades: transformar el lado más complejo hasta igualar el otro.
3. Para ecuaciones: aislar la función trigonométrica, encontrar el ángulo principal y considerar todas las soluciones en el intervalo dado.
4. Para resolución de triángulos: aplicar Ley de Senos o Ley de Cosenos según corresponda.
5. Verificar que todas las soluciones estén en el dominio de la función.

### Procedimiento para Cálculo Diferencial Básico

1. Para límites:
   - Evaluar directamente primero.
   - Si hay indeterminación, aplicar factorización, racionalización, conjugado o L'Hôpital.
   - Para límites al infinito, comparar grados de polinomios o dividir por la mayor potencia.
2. Para derivadas:
   - Identificar la estructura de la función (suma, producto, cociente, composición).
   - Aplicar la regla correspondiente.
   - Simplificar el resultado.
3. Para aplicaciones:
   - Encontrar puntos críticos (donde f'(x) = 0 o no existe).
   - Analizar el signo de f'(x) para determinar crec./decrec.
   - Evaluar f''(x) para concavidad y extremos.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Álgebra — Factorización de Polinomios
```
Factoriza completamente el polinomio P(x) = 2x³ - 5x² - 4x + 3.
```
**Respuesta esperada**: El agente identifica que x = 3 es raíz, aplica el teorema del factor, factoriza por agrupación y obtiene: P(x) = (x - 3)(2x + 1)(x - 1).

### Ejemplo 2: Geometría — Área de un Sector Circular
```
Calcula el área de un sector circular de radio 6 cm y ángulo central 60°.
```
**Respuesta esperada**: El agente aplica A = (θ/360°) · πr² = (60/360) · π · 36 = 6π cm² ≈ 18.85 cm².

### Ejemplo 3: Trigonometría — Identidad Trigonométrica
```
Demuestra que sen²(x) · cos²(x) = (1 - cos(4x)) / 8.
```
**Respuesta esperada**: El agente usa identidades de ángulo doble: sen(x)cos(x) = sen(2x)/2, luego eleva al cuadrado y aplica cos(2θ) = 1 - 2sen²(θ).

### Ejemplo 4: Cálculo — Límite con Indeterminación
```
Calcula el límite: lim(x→0) (sen(x) - x) / x³.
```
**Respuesta esperada**: El agente aplica L'Hôpital tres veces o usa la serie de Taylor de sen(x) = x - x³/6 + x⁵/120 - ..., obteniendo -1/6.

### Ejemplo 5: Cálculo — Derivada por Regla de la Cadena
```
Encuentra la derivada de f(x) = e^(sin(x²)).
```
**Respuesta esperada**: f'(x) = e^(sin(x²)) · cos(x²) · 2x.

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `math-calculo-diferencial` | `/hermes-home/skills/stem/math/math-calculo-diferencial` | Cálculo diferencial avanzado, derivadas parciales, optimización multivariable |
| `math-funciones` | `/hermes-home/skills/stem/math/math-funciones` | Estudio profundo de funciones: dominio, rango, composición, inversión, asíntotas |
| `math-ecuaciones` | `/hermes-home/skills/stem/math/math-ecuaciones` | Ecuaciones diferenciales, ecuaciones en diferencias, métodos numéricos |
| `math-logaritmos-exponenciales` | `/hermes-home/skills/stem/math/math-logaritmos-exponenciales` | Funciones logarítmicas y exponenciales, ecuaciones con ellas, aplicaciones |
| `math-numeros-algebra` | `/hermes-home/skills/stem/math/math-numeros-algebra` | Teoría de números, aritmética modular, divisibilidad, números primos |
| `math-sucesiones-series` | `/hermes-home/skills/stem/math/math-sucesiones-series` | Sucesiones numéricas, series de potencias, criterios de convergencia |
| `math-trigonometria` | `/hermes-home/skills/stem/math/math-trigonometria` | Trigonometría avanzada, funciones inversas, ecuaciones trigonométricas complejas |

### Cuándo derivar a otros skills

- Si el problema involucra **derivadas parciales, gradientes o optimización multivariable** → derivar a `math-calculo-diferencial`.
- Si el problema trata de **funciones logarítmicas o exponenciales en detalle** → derivar a `math-logaritmos-exponenciales`.
- Si el problema involucra **ecuaciones diferenciales** → derivar a `math-ecuaciones`.
- Si el problema requiere **series de potencias o criterios de convergencia avanzados** → derivar a `math-sucesiones-series`.
- Si el problema requiere **teoría de números o aritmética modular** → derivar a `math-numeros-algebra`.
- Si el problema requiere **trigonometría inversa compleja o funciones hiperbólicas** → derivar a `math-trigonometria`.
- Si el problema requiere **análisis profundo de funciones (asíntotas, composición, inversión)** → derivar a `math-funciones`.

## Pitfalls — Errores Comunes

### Álgebra
- **Olvidar verificar restricciones de dominio**: al resolver ecuaciones con fracciones algebraicas o raíces, siempre verificar que las soluciones no hagan cero el denominador ni generen raíces cuadradas de negativos.
- **Errores de signo al factorizar**: al aplicar diferencia de cuadrados a² - b² = (a+b)(a-b), verificar que el signo sea correcto en ambos factores.
- **Confundir inecuación con ecuación**: al multiplicar o dividir una inecuación por un número negativo, el sentido de la desigualdad se invierte.
- **Errores en la fórmula cuadrática**: recordar que x = (-b ± √(b² - 4ac)) / (2a), no confundir el signo de b ni dividir solo la raíz por 2a.

### Geometría
- **Confundir área con volumen**: verificar siempre las unidades (cm² vs cm³) y la fórmula adecuada.
- **Aplicar Pitágoras a triángulos no rectángulos**: el teorema de Pitágoras solo aplica a triángulos rectángulos. Para otros, usar Ley de Cosenos.
- **Olvidar que π es irracional**: en respuestas exactas, mantener π en el resultado; solo aproximar si se solicita explícitamente.
- **Confundir ángulo central con ángulo inscrito**: el ángulo inscrito es la mitad del ángulo central que subtende el mismo arco.

### Trigonometría
- **Confundir identidades pitagóricas**: recordar que sen²(x) + cos²(x) = 1, no sen²(x) - cos²(x).
- **Perder soluciones al dividir por funciones trigonométricas**: nunca dividir una ecuación trigonométrica por sen(x) o cos(x) sin considerar el caso en que sea cero.
- **Ángulos en grados vs radianes**: verificar siempre la unidad del calculadora y del problema.
- **Dominio de funciones inversas**: arcsen tiene dominio [-1, 1] y rango [-π/2, π/2]; arcosec tiene restricciones similares.

### Cálculo Diferencial
- **Aplicar L'Hôpital incorrectamente**: solo aplicar cuando hay indeterminación 0/0 o ∞/∞. No aplicar si el límite existe directamente.
- **Errores en la regla de la cadena**: al derivar f(g(x)), multiplicar por g'(x). No olvidar la derivada de la función interna.
- **Confundir concavidad con crecimiento**: f'(x) > 0 implica creciente, f''(x) > 0 implica cóncava hacia arriba. Son conceptos independientes.
- **Extremos absolutos sin evaluar extremos del intervalo**: al buscar máximos/mínimos absolutos en un intervalo cerrado, evaluar también los puntos finales.

## Cuándo Usar Este Skill

Usa este skill cuando:

1. El problema involucra **ecuaciones algebraicas** de primer o segundo grado, factorización de polinomios, o sistemas de ecuaciones simples.
2. El problema requiere **cálculo de áreas, perímetros, volúmenes** de figuras geométricas elementales.
3. El problema involucra **funciones trigonométricas**, identidades básicas o resolución de triángulos.
4. El problema requiere **calcular límites** simples o **derivadas de funciones elementales**.
5. El problema es de nivel **preuniversitario o de primer año universitario**.
6. El usuario necesita una **revisión completa de fundamentos matemáticos**.

**No** uses este skill cuando:
- El problema requiere cálculo multivariable (derivadas parciales, integrales múltiples) → usar `math-calculo-diferencial` o `math-calculo-integral`.
- El problema requiere álgebra lineal avanzada (espacios vectoriales, autovalores) → usar `skill-math-linear-algebra`.
- El problema requiere estadística avanzada o inferencia → usar `skill-math-statistics`.
- El problema requiere teoría de números profunda → usar `math-numeros-algebra`.

## Formato de Salida Esperado

El agente debe presentar las soluciones en el siguiente formato:

```
### Problema
[Enunciado del problema]

### Solución
[Paso 1: Identificación del tipo de problema]
[Paso 2: Metodología aplicada]
[Paso 3: Desarrollo paso a paso]
[Paso 4: Resultado intermedio (si aplica)]
[Paso 5: Verificación]

### Resultado Final
[Respuesta clara y destacada]

### Notas
[Observaciones adicionales, alternativas de solución, etc.]
```

## Notas Adicionales

- Este skill es el **pilar fundamental** del ecosistema matemático de Mastermind.
- Todos los cálculos deben mostrarse con **pasos intermedios claros** para fines educativos.
- Se recomienda usar **notación LaTeX** para expresiones matemáticas cuando sea posible.
- Siempre verificar que las respuestas sean **físicamente razonables** (positivas, del orden correcto, etc.).
- En problemas de geometría, sugerir un **diagrama** cuando sea útil para la comprensión.
