---
name: stem-estatica
description: Estática de estructuras: vigas, armaduras (método nodos/secciones), cables, estructuras 2D/3D, métodos matriciales, energía de deformación y teoremas de Castigliano.
tags: [stem, engineering, statics]
---

# Estática de Estructuras

## Referencias de autoridad

- **Hibbeler**: Structural Analysis, 9ª edición, Pearson
- **Bedford & Fowler**: Engineering Mechanics: Statics, 5ª edición, Prentice Hall
- **Timoshenko**: Theory of Structures, McGraw-Hill
- **Serrano**: Estática de Estructuras, UPC

## Equilibrio de cuerpos rígidos

### Ecuaciones de equilibrio (2D)
- ΣF_x = 0
- ΣF_y = 0
- ΣM_O = 0 (momento respecto a cualquier punto O)

### Ecuaciones de equilibrio (3D)
- ΣF_x = 0, ΣF_y = 0, ΣF_z = 0
- ΣM_x = 0, ΣM_y = 0, ΣM_z = 0

### Tipos de apoyos y reacciones
- **Rodillo**: 1 reacción (perpendicular al apoyo)
- **Articulación (pivote)**: 2 reacciones (Fx, Fy)
- **Empotramiento**: 3 reacciones (Fx, Fy, M)
- **Bola**: 3 reacciones (Fx, Fy, Fz)
- **Bola-cónica**: 2 reacciones

## Estructuras reticulares (armaduras)

### Suposiciones
- Todas las cargas en nudos
- Barras biseladas en ambos extremos
- Las barras solo soportan esfuerzos axiales (tracción o compresión)

### Método de los nudos
- ΣFx = 0 y ΣFy = 0 en cada nudo
- **Barras cero**: identificar antes de calcular
  - Dos barras no colineales en nudo sin carga externa → ambas son cero
  - Tres barras, dos colineales, sin carga externa → la tercera es cero

### Método de las secciones
- Cortar la estructura en una sección que pase por máximo 3 barras
- ΣFx = 0, ΣFy = 0, ΣM = 0
- Ideal para encontrar barras específicas sin resolver toda la estructura

### Estabilidad e indeterminación
- **2D**: m + r = 2j → isostática; m + r > 2j → hiperestática; m + r < 2j → inestable
  - m = barras, r = reacciones, j = nudos
- **3D**: m + r = 3j → isostática

## Vigas y marcos

### Esfuerzos internos
- **Cortante (V)**: ΣF_y en la sección
- **Momento flector (M)**: ΣM en la sección
- **Esfuerzo normal (N)**: ΣF_x en la sección

### Relación carga-cortante-momento
- dV/dx = -w(x)
- dM/dx = V(x)
- ΔV = -∫w(x)dx
- ΔM = ∫V(x)dx

### Diagramas de V y M
- **Carga puntual**: salto en V, quiebro en M
- **Carga distribuida uniforme**: V lineal, M parabólica
- **Carga triangular**: V parabólica, M cúbica
- **Momento aplicado**: salto en M

### Vigas hiperestáticas
- **Grado de hiperestaticidad**: r - 3 (2D) o r + m - 3j (armadura)
- **Métodos**:
  - **Ecuaciones de compatibilidad**: deflexiones conocidas
  - **Método de fuerzas**: eliminar apoyos, aplicar cargas ficticias
  - **Método de rigidez**: desplazamientos nodales como incógnitas
  - **Método de Cross (momentos)**: distribución de momentos

## Cables y arcos

### Cables
- **Cable con carga puntual**: forma poligonal
- **Cable con carga distribuida uniforme**: parábola
  - y = (w/2T₀)·x²
- **Cable con carga distribuida a lo largo del arco**: catenaria
  - y = a·cosh(x/a) = a·(e^(x/a) + e^(-x/a))/2
  - a = T₀/w

### Arcos
- **Arco de tres articulaciones**: isostático
- **Arco biarticulado**: hiperestático 1º grado
- **Empotrado**: hiperestático 3º grado
- **Empuje horizontal**: H = M₀/L (arco parabólico con carga uniforme)

## Métodos matriciales

### Método de rigidez
- **Matriz de rigidez local** (barra 2D):
  - k = EA/L · [[1, 0, -1, 0], [0, 0, 0, 0], [-1, 0, 1, 0], [0, 0, 0, 0]]
- **Matriz de rigidez global**: k_global = Tᵀ·k_local·T
- **Ensamblaje**: K_global·D = F
- **Condición de contorno**: eliminar filas/columnas de desplazamientos conocidos

### Matriz de rigidez de barra 2D
- u = cos(θ), v = sen(θ)
- k = (EA/L) · [[u², uv, -u², -uv], [uv, v², -uv, -v²], [-u², -uv, u², uv], [-uv, -v², uv, v²]]

## Energía de deformación

### Energía elástica de deformación
- **Tracción/compresión**: U = N²L/(2EA)
- **Flexión**: U = ∫M²/(2EI)dx
- **Cortante**: U = ∫kV²/(2GA)dx (k = factor de forma)
- **Torsión**: U = T²L/(2GJ)

### Teorema de Castigliano

#### Primer teorema
- δ_i = ∂U/∂P_i (desplazamiento en el punto de aplicación de P_i)

#### Segundo teorema (para estructuras hiperestáticas)
- ∂U/∂R_i = 0 (para reacciones en apoyos fijos)
- Usar para resolver estructuras hiperestáticas

#### Método de la carga ficticia
- Añadir carga ficticia Q en el punto donde se busca el desplazamiento
- U = U(P, Q)
- δ = ∂U/∂Q |_(Q=0)

### Teorema de Maxwell-Betti
- δ_ij = δ_ji (reciprocidad de influencias)
- El desplazamiento en i debido a carga en j = desplazamiento en j debido a carga en i

### Teorema de Menabrea-Castigliano
- Para estructuras hiperestáticas: ∂U/∂X_i = 0 donde X_i son las incógnitas hiperestáticas

## Diagramas de influencia

### Concepto
- Representa el efecto de una carga unitaria móvil en una sección determinada
- **Ecuación de Müller-Breslau**: la forma de la deformada con la restricción eliminada = diagrama de influencia

### Aplicaciones
- **Cortante en una sección**: desplazamiento relativo en la sección
- **Momento en una sección**: giro relativo en la sección
- **Reacción en un apoyo**: desplazamiento vertical del apoyo

### Cargas móviles
- **Carga puntual móvil**: colocar en el pico del diagrama
- **Carga distribuida móvil**: colocar donde el diagrama tenga mayor área
- **Valor máximo**: P·y_pico + w·Área

## Errores comunes / Pitfalls

- **Barras cero**: no identificarlas antes de calcular → trabajo extra innecesario
- **Hiperestaticidad**: contar mal reacciones. En 2D: 3 ecuaciones de equilibrio
- **Signos en V y M**: convención: V positivo si rota en sentido horario, M positivo si comprime fibra superior
- **Müller-Breslau**: el diagrama de influencia es PROPORCIONAL a la deformada, no igual
- **Castigliano**: solo aplica a materiales lineales elásticos
- **Arco de tres articulaciones**: isostático. Verificar que las tres articulaciones no estén alineadas

## Verificación

- [ ] Equilibrio 2D: 3 ecuaciones, 3 incógnitas → isostático
- [ ] Armadura 2D: m + r = 2j → isostática
- [ ] Cortante: dV/dx = -w. Verificar con carga uniforme: V lineal
- [ ] Momento: dM/dx = V. Verificar con V lineal: M parabólica
- [ ] Castigliano: δ = ∂U/∂P. Verificar unidades: [J/N] = [m] ✓
- [ ] Diagrama de influencia: verificar en al menos dos puntos conocidos
