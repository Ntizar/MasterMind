---
name: skill-math-linear-algebra
version: 1.0.0
category: STEM/Mathematics
description: "Álgebra Lineal — Vectores, matrices, espacios vectoriales, autovalores/autovectores y sistemas de ecuaciones lineales. Skill especializado para el ecosistema STEM de Mastermind."
tags: [algebra-lineal, vectores, matrices, determinantes, espacios-vectoriales, autovalores, Gauss, Cramer]
author: Mastermind STEM
---

# skill-math-linear-algebra — Álgebra Lineal

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas de **Vectores**, **Matrices**, **Espacios Vectoriales**, **Autovalores y Autovectores** y **Sistemas de Ecuaciones Lineales**. Es el skill especializado del ecosistema STEM de Mastermind para el área de álgebra lineal.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Vectores en R² y R³
- **Representación y operaciones básicas**: suma de vectores, producto por escalar, vector nulo, vector opuesto.
- **Módulo (norma) de un vector**: ||v|| = √(v₁² + v₂² + v₃²), vector unitario u = v / ||v||.
- **Producto escalar (producto punto)**: u · v = ||u|| · ||v|| · cos(θ) = u₁v₁ + u₂v₂ + u₃v₃.
  - Propiedades: conmutativa, distributiva, homogénea.
  - Vectores ortogonales: u · v = 0 ⟺ u ⊥ v.
  - Proyección ortogonal: proj_v(u) = (u · v / ||v||²) · v.
  - Ángulo entre vectores: cos(θ) = (u · v) / (||u|| · ||v||).
- **Producto vectorial** (solo en R³): u × v = (u₂v₃ - u₃v₂, u₃v₁ - u₁v₃, u₁v₂ - u₂v₁).
  - Propiedades: anticonmutativa, distributiva, ||u × v|| = ||u|| · ||v|| · sen(θ).
  - El resultado es ortogonal a ambos vectores.
  - Área del paralelogramo: A = ||u × v||.
  - Área del triángulo: A = ½ · ||u × v||.
- **Producto mixto**: u · (v × w) = det[u v w] (determinante de la matriz con columnas u, v, w).
  - Volumen del paralelepípedo: V = |u · (v × w)|.
  - Vectores coplanarios: u · (v × w) = 0.
- **Vectores colineales y coplanarios**: criterios de dependencia lineal.
- **Rectas y planos en el espacio**: ecuación paramétrica, continua, general de una recta; ecuación del plano.

### 2. Matrices
- **Tipos de matrices**: cuadrada, diagonal, identidad, simétrica, antisimétrica, triangular, transpuesta, nula, inversa.
- **Operaciones con matrices**:
  - Suma y resta: elemento a elemento.
  - Producto por escalar.
  - Producto de matrices: C = A · B, donde cᵢⱼ = Σ aᵢₖ · bₖⱼ.
  - Propiedades: asociativa, distributiva, NO conmutativa en general.
  - Transpuesta: (Aᵀ)ᵢⱼ = aⱼᵢ, (Aᵀ)ᵀ = A, (AB)ᵀ = BᵀAᵀ.
- **Determinantes**:
  - Matriz 2×2: det([[a,b],[c,d]]) = ad - bc.
  - Matriz 3×3: regla de Sarrus o desarrollo por cofactores.
  - Propiedades: det(Aᵀ) = det(A), det(AB) = det(A)·det(B), det(A⁻¹) = 1/det(A), det(kA) = kⁿ·det(A).
  - Desarrollo por cofactores (Laplace).
  - Regla de Cramer.
- **Matriz inversa**:
  - A⁻¹ = (1/det(A)) · adj(A) para matriz 2×2 y 3×3.
  - Método de Gauss-Jordan para matrices de cualquier tamaño.
  - Condiciones de existencia: det(A) ≠ 0 (matriz no singular).
  - Propiedades: (A⁻¹)⁻¹ = A, (AB)⁻¹ = B⁻¹A⁻¹, (Aᵀ)⁻¹ = (A⁻¹)ᵀ.
- **Rango de una matriz**: número de filas (o columnas) linealmente independientes. Método de Gauss para determinar el rango.
- **Matrices elementales y operaciones elementales por filas**.

### 3. Espacios Vectoriales
- **Definición y axiomas**: conjunto V con operaciones de suma y producto por escalar satisfaciendo 8 axiomas.
- **Subespacios**: subconjunto W ⊆ V que es cerrado bajo suma y producto por escalar. Criterio: 0 ∈ W, u,v ∈ W ⟹ u+v ∈ W, α ∈ R, v ∈ W ⟹ αv ∈ W.
- **Combinación lineal**: v = α₁v₁ + α₂v₂ + ... + αₙvₙ.
- **Generación**: Span(S) = conjunto de todas las combinaciones lineales de los vectores en S.
- **Dependencia e independencia lineal**: vectores linealmente independientes si α₁v₁ + ... + αₙvₙ = 0 ⟹ α₁ = α₂ = ... = αₙ = 0.
- **Base**: conjunto de vectores linealmente independientes que generan el espacio.
- **Dimensión**: número de vectores en una base. dim(Rⁿ) = n, dim(Mₘₓₙ) = m·n.
- **Cambio de base**: matriz de cambio de base P, coordenadas en nueva base: [v]B' = P⁻¹[v]B.
- **Producto interior**: definición general, norma inducida, ángulo, ortogonalidad, proceso de Gram-Schmidt.
- **Subespacios notables**: kernel (núcleo) y imagen (rango) de una transformación lineal.

### 4. Autovalores y Autovectores
- **Definición**: Av = λv, donde λ es el autovalor y v ≠ 0 es el autovector.
- **Polinomio característico**: p(λ) = det(A - λI) = 0.
- **Cálculo de autovalores**: resolver el polinomio característico.
- **Cálculo de autovectores**: para cada λ, resolver (A - λI)v = 0.
- **Autovalores multiplicidad algebraica y geométrica**.
- **Matriz diagonalizable**: A es diagonalizable si existe P invertible tal que D = P⁻¹AP es diagonal.
- **Propiedades**:
  - La traza de A = suma de autovalores.
  - El determinante de A = producto de autovalores.
  - Autovalores de Aᵀ son los mismos que los de A.
  - Si A es simétrica, sus autovalores son reales y sus autovectores son ortogonales.
- **Teorema espectral**: toda matriz simétrica real es diagonalizable mediante una matriz ortogonal.

### 5. Sistemas de Ecuaciones Lineales
- **Forma general**: a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ = b₁, etc.
- **Representación matricial**: Ax = b.
- **Sistemas compatibles**:
  - Determinado: única solución (det(A) ≠ 0 o rango(A) = rango(A|b) = n).
  - Indeterminado: infinitas soluciones (rango(A) = rango(A|b) < n).
- **Sistemas incompatibles**: sin solución (rango(A) ≠ rango(A|b)).
- **Método de Gauss (eliminación gaussiana)**:
  - Formar la matriz ampliada [A|b].
  - Aplicar operaciones elementales por filas para obtener forma escalonada.
  - Back-substitution para encontrar la solución.
- **Método de Gauss-Jordan**: reducción a forma escalonada reducida (identidad a la izquierda).
- **Regla de Cramer**: xᵢ = det(Aᵢ) / det(A), donde Aᵢ es A con la columna i reemplazada por b.
- **Uso de la inversa**: x = A⁻¹b (cuando A es invertible).
- **Sistemas homogéneos**: Ax = 0, siempre tienen al menos la solución trivial.

## Instrucciones Paso a Paso para el Agente

### Procedimiento General de Resolución

1. **Identificar el tipo de problema**: Clasificar en vectores, matrices, espacios vectoriales, autovalores/autovectores o sistemas de ecuaciones.
2. **Extraer los datos**: Identificar vectores, matrices, dimensiones y parámetros.
3. **Seleccionar el método** apropiado según la categoría.
4. **Realizar los cálculos** paso a paso, mostrando cada transformación.
5. **Verificar** la solución sustituyendo o comprobando propiedades.
6. **Interpretar** el resultado en el contexto del problema.

### Procedimiento para Vectores

1. Para operaciones básicas: aplicar la definición directamente.
2. Para producto escalar: u · v = u₁v₁ + u₂v₂ + u₃v₃. Para encontrar el ángulo: θ = arccos((u · v) / (||u|| · ||v||)).
3. Para producto vectorial (R³): usar la fórmula del determinante con i, j, k o la fórmula explícita.
4. Para producto mixto: calcular el determinante de la matriz con los tres vectores como filas o columnas.
5. Para proyección: proj_v(u) = (u · v / ||v||²) · v.

### Procedimiento para Matrices

1. Para suma/resta: operar elemento a elemento.
2. Para producto de matrices: verificar que el número de columnas de A sea igual al número de filas de B. Calcular cᵢⱼ = Σ aᵢₖ · bₖⱼ.
3. Para determinantes:
   - 2×2: ad - bc.
   - 3×3: regla de Sarrus o desarrollo por cofactores.
   - Mayor tamaño: reducir por filas o desarrollar por cofactores.
4. Para inversa:
   - 2×2: A⁻¹ = (1/(ad-bc)) · [[d,-b],[-c,a]].
   - 3×3: A⁻¹ = (1/det(A)) · adj(A).
   - Mayor tamaño: método de Gauss-Jordan.

### Procedimiento para Espacios Vectoriales

1. Para verificar si un subconjunto es subespacio: verificar los 3 criterios (0 ∈ W, cerrado bajo suma, cerrado bajo producto por escalar).
2. Para determinar dependencia lineal: formar la matriz con los vectores como columnas y calcular el rango. Si rango < número de vectores → dependientes.
3. Para encontrar una base: aplicar Gauss a la matriz con los vectores como filas/columnas y seleccionar las filas/columnas pivote.
4. Para dimensión: contar el número de vectores en la base encontrada.

### Procedimiento para Autovalores y Autovectores

1. Calcular el polinomio característico: p(λ) = det(A - λI).
2. Resolver p(λ) = 0 para encontrar los autovalores.
3. Para cada autovalor λᵢ, resolver (A - λᵢI)v = 0 para encontrar los autovectores.
4. Determinar la multiplicidad algebraica (grado del factor en el polinomio) y geométrica (dimensión del espacio propio).
5. Verificar diagonalizabilidad: A es diagonalizable si la suma de multiplicidades geométricas = n.

### Procedimiento para Sistemas de Ecuaciones Lineales

1. Escribir el sistema en forma matricial Ax = b.
2. Calcular det(A) para verificar si A es invertible.
3. Si det(A) ≠ 0:
   - Usar x = A⁻¹b o Regla de Cramer.
4. Si det(A) = 0:
   - Aplicar el método de Gauss a la matriz ampliada [A|b].
   - Determinar el rango de A y de [A|b].
   - Si rango(A) = rango(A|b) = n: único solución.
   - Si rango(A) = rango(A|b) < n: infinitas soluciones.
   - Si rango(A) ≠ rango(A|b): sin solución.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Vectores — Producto Vectorial
```
Calcula el producto vectorial de u = (1, 2, 3) y v = (4, 5, 6).
```
**Respuesta esperada**: u × v = (2·3 - 3·5, 3·4 - 1·6, 1·5 - 2·4) = (-9, 6, -3).

### Ejemplo 2: Matrices — Determinante 3×3
```
Calcula el determinante de A = [[2, 1, 3], [0, 4, -1], [1, -2, 5]].
```
**Respuesta esperada**: det(A) = 2(20 - 2) - 1(0 + 1) + 3(0 - 4) = 36 - 1 - 12 = 23.

### Ejemplo 3: Autovalores
```
Encuentra los autovalores y autovectores de A = [[3, 1], [0, 2]].
```
**Respuesta esperada**: p(λ) = (3-λ)(2-λ) = 0, λ₁ = 3, λ₂ = 2.
Para λ₁ = 3: (A - 3I)v = 0 → [[0,1],[0,-1]]v = 0 → v₁ = (1, 0).
Para λ₂ = 2: (A - 2I)v = 0 → [[1,1],[0,0]]v = 0 → v₂ = (1, -1).

### Ejemplo 4: Sistema por Gauss
```
Resuelve el sistema: 2x + y - z = 8, -3x - y + 2z = -11, -2x + y + 2z = -3.
```
**Respuesta esperada**: El agente aplica Gauss a la matriz ampliada y obtiene x = 2, y = 3, z = -1.

### Ejemplo 5: Producto Mixto
```
Calcula el volumen del paralelepípedo formado por u = (1, 0, 0), v = (0, 2, 0), w = (0, 0, 3).
```
**Respuesta esperada**: V = |u · (v × w)| = |det([[1,0,0],[0,2,0],[0,0,3]])| = |6| = 6.

### Ejemplo 6: Espacios Vectoriales
```
Determina si W = {(x, y, z) ∈ R³ : x + y + z = 0} es un subespacio de R³.
```
**Respuesta esperada**: Sí, es un subespacio porque: (0,0,0) ∈ W (0+0+0=0), cerrado bajo suma: si x₁+y₁+z₁=0 y x₂+y₂+z₂=0, entonces (x₁+x₂)+(y₁+y₂)+(z₁+z₂)=0, y cerrado bajo producto por escalar: αx+αy+αz = α(x+y+z) = α·0 = 0.

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `math-vectores-matrices` | `/hermes-home/skills/stem/math/math-vectores-matrices` | Vectores y matrices — referencia principal del ecosistema |
| `math-ecuaciones` | `/hermes-home/skills/stem/math/math-ecuaciones` | Sistemas de ecuaciones y ecuaciones matriciales |
| `math-numeros-algebra` | `/hermes-home/skills/stem/math/math-numeros-algebra` | Teoría de números aplicada a álgebra lineal (rangos, divisibilidad) |
| `math-funciones` | `/hermes-home/skills/stem/math/math-funciones` | Transformaciones lineales como funciones especiales |

### Cuándo derivar a otros skills

- Si el problema requiere **transformaciones lineales avanzadas** (rotaciones, reflexiones en Rⁿ) → derivar a `math-vectores-matrices`.
- Si el problema requiere **sistemas de ecuaciones diferenciales lineales** → derivar a `math-ecuaciones`.
- Si el problema requiere **álgebra lineal sobre campos finitos** → derivar a `math-numeros-algebra`.
- Si el problema requiere **análisis de funciones vectoriales** → derivar a `math-funciones`.

## Pitfalls — Errores Comunes

### Vectores
- **Confundir producto escalar con producto vectorial**: el producto escalar da un número, el vectorial da un vector. Son operaciones completamente diferentes.
- **Orden en el producto vectorial**: u × v ≠ v × u (son opuestos). u × v = -(v × u).
- **Calcular mal la norma**: ||v|| = √(v₁² + v₂² + v₃²), no √(v₁ + v₂ + v₃).
- **Confundir producto por escalar con producto de vectores**: αv ≠ u · v. Uno es escalar × vector, el otro es producto punto.

### Matrices
- **Multiplicar matrices como si fueran números**: AB ≠ BA en general. El producto de matrices NO es conmutativo.
- **Verificar dimensiones antes de multiplicar**: Aₘₓₙ · Bₚₓq solo es posible si n = p. El resultado es mₓq.
- **Confundir transpuesta con inversa**: Aᵀ ≠ A⁻¹ en general. Solo son iguales para matrices ortogonales (Aᵀ = A⁻¹).
- **Error en la regla de Sarrus**: recordar repetir las dos primeras columnas a la derecha y sumar productos de diagonales hacia abajo, restar los de arriba.
- **Olvidar el signo en cofactores**: el cofactor Cᵢⱼ = (-1)ⁱ⁺ʲ · Mᵢⱼ, donde Mᵢⱼ es el menor complementario.

### Espacios Vectoriales
- **Confundir dependencia lineal con colinealidad**: dos vectores son dependientes si uno es múltiplo del otro. Tres o más vectores son dependientes si uno es combinación lineal de los otros.
- **Olvidar que el conjunto vacío NO genera un subespacio**: el subespacio debe contener al menos el vector cero.
- **Error en el cambio de base**: la matriz de cambio de base P tiene como columnas los vectores de la nueva base expresados en la base original. Las coordenadas se transforman como [v]B' = P⁻¹[v]B.

### Autovalores y Autovectores
- **Olvidar que los autovectores deben ser no nulos**: v ≠ 0 por definición.
- **Confundir multiplicidad algebraica con geométrica**: la multiplicidad geométrica (dimensión del espacio propio) siempre es ≤ multiplicidad algebraica (grado del factor).
- **Asumir que toda matriz es diagonalizable**: solo lo es si la suma de multiplicidades geométricas = n.
- **Error en el polinomio característico**: det(A - λI), no det(A + λI) ni det(λI - A) con signos incorrectos.

### Sistemas de Ecuaciones Lineales
- **Aplicar Cramer cuando det(A) = 0**: la regla de Cramer solo aplica cuando det(A) ≠ 0.
- **Confundir rango de A con rango de [A|b]**: son diferentes cuando el sistema es incompatible.
- **Error en la back-substitution**: al resolver por Gauss, verificar cada paso sustituyendo en las ecuaciones originales.
- **Olvidar parámetros en sistemas indeterminados**: cuando hay infinitas soluciones, expresar las variables libres en términos de parámetros.

## Cuándo Usar Este Skill

Usa este skill cuando:

1. El problema involucra **operaciones con vectores** (suma, producto escalar, vectorial, mixto).
2. El problema requiere **operaciones con matrices** (suma, producto, determinante, inversa, transpuesta).
3. El problema requiere **analizar espacios vectoriales** (subespacios, bases, dimensión, independencia lineal).
4. El problema requiere **calcular autovalores y autovectores** de una matriz.
5. El problema requiere **resolver sistemas de ecuaciones lineales** (Gauss, Cramer, inversión).
6. El problema es de nivel **universitario de primer/segundo año** en álgebra lineal.
7. El problema involucra **transformaciones lineales** representadas por matrices.

**No** uses este skill cuando:
- El problema requiere **cálculo multivariable** (gradientes, divergencia, rotacional) → usar `math-calculo-diferencial`.
- El problema requiere **integrales de línea o superficie** → usar `math-calculo-integral`.
- El problema requiere **optimización con restricciones** → usar `math-calculo-diferencial` (Lagrange).

## Formato de Salida Esperado

El agente debe presentar las soluciones en el siguiente formato:

```
### Problema
[Enunciado del problema]

### Datos Identificados
- [Vector/Matrix/Parameter]: [valor]
- [Tipo de problema]: [descripción]

### Solución
[Paso 1: Fórmula/método seleccionado]
[Paso 2: Sustitución de valores]
[Paso 3: Cálculo paso a paso]
[Paso 4: Resultado intermedio (si aplica)]

### Resultado Final
[Respuesta clara y destacada]

### Verificación
[Sustitución o comprobación del resultado]

### Notas
[Observaciones adicionales, propiedades relevantes, etc.]
```

## Notas Adicionales

- Este skill es el **pilar de álgebra lineal** del ecosistema matemático de Mastermind.
- Todos los cálculos deben mostrarse con **pasos intermedios claros** para fines educativos.
- Se recomienda usar **notación LaTeX** para expresiones matemáticas cuando sea posible.
- En problemas de autovalores, siempre verificar que los autovectores calculados **satisfagan Av = λv**.
- En sistemas de ecuaciones, siempre **verificar la solución** sustituyendo en las ecuaciones originales.
- Para matrices simétricas, recordar que **siempre son diagonalizables** y sus autovalores son **reales**.
- El producto mixto u · (v × w) es igual al determinante de la matriz con u, v, w como filas o columnas.
- En el método de Gauss, las **operaciones elementales por filas** no alteran la solución del sistema.
