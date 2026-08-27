---
name: csp-modelado-resolucion
description: Modelado y resolución de Problemas de Satisfacción de Restricciones (CSP): variables, dominios, restricciones unarias/binarias/globales, propagación de restricciones, consistencia de arco, backtracking con heurísticas y búsqueda local. Incluye mapeo SAT vs CSP, estrategias de poda y ejemplos prácticos.
---

# CSP: Modelado y Resolución

## Identidad

- **Fuente:** IA para gente curiosa — Fascículo 02, caps. 5-7 (SAT y CSP, variables/dominios, propagación/backtracking)
- **Autor:** 686f6c61 (CC BY 4.0)
- **Cuaderno Colab:** [Sudoku como CSP: fuerza bruta frente a propagación](https://colab.research.google.com/github/686f6c61/iaparagentecuriosa-notebooks/blob/main/Facs%C3%ADmil%2002/02-sudoku-como-csp.ipynb)

## Qué es un CSP

Un **Problema de Satisfacción de Restricciones** (CSP) busca una asignación de valores a variables que cumpla todas las reglas. No genera texto plausible: encuentra una asignación válida.

Un CSP tiene tres piezas:
- **Variables** `X = {X₁, X₂, …, Xₙ}` — los huecos que hay que rellenar
- **Dominios** `Dᵢ` — valores permitidos para cada variable
- **Restricciones** `C` — reglas que descartan combinaciones inválidas

## Paso 1 — Modelar: variables, dominios y restricciones

### Variables: qué huecos rellenar

Una variable puede ser cualquier cosa que nos convenga para modelar:
- En horarios: `reunión`, `persona-día`, `aula-hora`
- En planificación: `tarea-máquina`, `paquete-versión`
- En sudoku: `casilla (fila, columna)`

**Regla de oro:** la variable correcta es la que permite expresar reglas con menos esfuerzo.

### Dominios: qué valores permitidos

`Dᵢ` es el conjunto de valores que puede tomar `Xᵢ`. El espacio de búsqueda completo es:

```
|A| = ∏ᵢ |Dᵢ|
```

Ejemplo: 3 cursos × 2 horas × 2 salas = 4⁴³ = 64 combinaciones candidatas antes de filtrar.

### Restricciones: qué combinaciones prohibidas

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Unaria** | Restricción sobre una sola variable | `Python ≠ 9:00` |
| **Binaria** | Restricción entre dos variables | `Ana no puede estar en dos reuniones` |
| **Global** | Restricción sobre tres o más variables | `AllDifferent(casillas de la misma fila)` |

## Paso 2 — Propagación: borrar antes de buscar

La propagación usa restricciones para reducir dominios antes de explorar.

### Consistencia de arco (AC-3)

Un arco `(Xᵢ, Xⱼ)` es consistente si:

```
∀x ∈ Dᵢ, ∃y ∈ Dⱼ : Cᵢⱼ(x, y) = verdadero
```

**Algoritmo AC-3:**
```python
def ac3(csp):
    queue = deque()
    for xi, xj in csp.arcs:
        queue.append((xi, xj))
    
    while queue:
        xi, xj = queue.popleft()
        if revise(xi, xj):
            if csp.domains[xi]:  # dominio vacío
                return False  # no hay solución
            for xk in csp.neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(xi, xj):
    removed = False
    for x_val in csp.domains[xi]:
        if not any(csp.constraint(xi, x_val, xj, y_val)
                   for y_val in csp.domains[xj]):
            csp.domains[xi].remove(x_val)
            removed = True
    return removed
```

Efecto: con dos reglas unarias simples, pasamos de 4×4×4 = 64 combinaciones a 4×2×2 = 16 sin hacer búsqueda.

## Paso 3 — Backtracking con heurísticas

### Backtracking básico
```python
def backtracking(csp, asignacion={}):
    if len(asignacion) == len(csp.variables):
        return asignacion
    
    # Elegir variable sin asignar
    var = seleccionar_variable(csp, asignacion)
    
    # Probar valores en orden
    for valor in ordenar_valores(csp, var, asignacion):
        if consistente(var, valor, csp, asignacion):
            asignacion[var] = valor
            csp.reducir_dominios(var, valor)
            
            forward_checking(csp, var, valor, asignacion)
            if csp.sin_conflictos():
                resultado = backtracking(csp, asignacion)
                if resultado is not None:
                    return resultado
            
            # Retroceder
            del asignacion[var]
            csp.restaurar_dominios()
    
    return None
```

### Heurísticas clave

| Heurística | Qué hace | Cuándo usar |
|------------|----------|-------------|
| **MRV (Minimum Remaining Values)** | Elige la variable con menos valores posibles | Siempre como política principal |
| **Grado (Degree)** | Elige la variable que afecta a más restricciones | Como desempate del MRV |
| **Ordenamiento de valores (LCV)** | Prueba primero los valores que restringen menos vecinos | Para reducir backtracking |

**MRV:** "Empieza por quien tiene menos disponibilidad". Si una casilla de sudoku solo puede ser un 7, lo escribes directamente.

**Grado:** De dos variables con MRV igual, elige la que esté conectada a más variables no asignadas.

**LCV (Least Constraining Value):** Elige el valor que deje más opciones abiertas a los vecinos.

### Búsqueda local: min-conflicts

Alternativa al backtracking cuando ya tienes una asignación completa pero con conflictos:

```python
def min_conflicts(csp, max_steps=10000):
    asignacion = asignacion_inicial(csp)
    
    for _ in range(max_steps):
        if csp.sin_conflictos():
            return asignacion
        
        # Variable con más conflictos
        var = variable_en_conflicto(csp)
        
        # Valor que minimiza conflictos
        mejor_valor = min(csp.domains[var],
                         key=lambda v: contar_conflictos(var, v, csp, asignacion))
        
        asignacion[var] = mejor_valor
    
    return None  # no se encontró en max_steps
```

## SAT vs CSP: cuándo usar cada uno

| Característica | SAT | CSP |
|----------------|-----|-----|
| Variables | Booleanas (true/false) | Dominios arbitrarios |
| Pregunta | ¿Existe asignación que haga la fórmula verdadera? | ¿Existe asignación que cumpla todas las reglas? |
| Ejemplo | `∃x₁,x₂,x₃ : (x₁ ∨ ¬x₂) ∧ (x₂ ∨ x₃)` | Colocar reuniones sin solapes |
| Usar cuando | Problemas de sí/no, interruptores | Problemas con múltiples valores, horarios, asignaciones |
| Solver | DPLL, MiniSAT | AC-3, backtracking, solvers comerciales |

**Ambos comparten una filosofía:** separar el modelo de la resolución. La capa de verificación es ejecutable, no depende de un LLM.

## Pitfalls

1. **Demasiadas variables** — cada variable que sobra multiplica el espacio. Agrupar es mejor que fragmentar.
2. **Dominios sin filtrar** — si aplicas AC-3 antes de buscar, reduces exponencialmente el espacio.
3. **Sin MRV** — backtracking sin heurísticas es fuerza bruta disfrazada.
4. **Confundir validez con optimización** — un CSP dice sí/no, no optimiza. Para optimización, añade funciones objetivo.
5. **Modelado incorrecto de variables** — decidir "qué cuenta como variable" es la parte más difícil. Piensa en la forma de expresar reglas, no en objetos del mundo.

## Referencias

- **Capítulos de referencia:** F02-C5 (SAT y CSP), C6 (Variables, dominios, restricciones), C7 (Propagación, backtracking, heurísticas)
- **Cuaderno:** [Sudoku como CSP](https://colab.research.google.com/github/686f6c61/iaparagentecuriosa-notebooks/blob/main/Facs%C3%ADmil%2002/02-sudoku-como-csp.ipynb)
- **Referencia teórica:** Dechter, "Constraint Processing"; Russell & Norvig, Chapter 6
- **Libro original:** Ghallab, Nau y Traverso, "Automated Planning"
