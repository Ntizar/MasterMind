---
name: math-calculo-integral
description: Integrales definidas e indefinidas, técnicas de integración (sustitución, partes, fracciones parciales), aplicaciones (áreas, volúmenes) y ecuaciones diferenciales elementales.
tags: [stem, math, advanced]
---

# Cálculo Integral

## Integrales indefinidas

- **Definición**: ∫f(x)dx = F(x) + C donde F'(x) = f(x)
- **Constante de integración**: siempre añadir + C
- **Linealidad**: ∫[af(x) + bg(x)]dx = a∫f(x)dx + b∫g(x)dx

### Integrales básicas
- ∫xⁿdx = xⁿ⁺¹/(n+1) + C (n ≠ -1)
- ∫(1/x)dx = ln|x| + C
- ∫eˣdx = eˣ + C
- ∫aˣdx = aˣ/ln(a) + C
- ∫sen(x)dx = -cos(x) + C
- ∫cos(x)dx = sen(x) + C
- ∫sec²(x)dx = tan(x) + C
- ∫(1/√(1-x²))dx = arcsen(x) + C
- ∫(1/(1+x²))dx = arctan(x) + C

## Integrales definidas

- **Definición**: ∫ₐᵇ f(x)dx = F(b) - F(a) (Teorema Fundamental del Cálculo)
- **Propiedades**:
  - ∫ₐᵃ f(x)dx = 0
  - ∫ₐᵇ f(x)dx = -∫ᵇₐ f(x)dx
  - ∫ₐᵇ f(x)dx + ∫ᵇᶜ f(x)dx = ∫ₐᶜ f(x)dx
  - Si f ≥ 0 en [a,b]: ∫ₐᵇ f(x)dx ≥ 0
  - **Desigualdad del valor medio**: ∃c ∈ [a,b]: ∫ₐᵇ f(x)dx = f(c) · (b-a)

## Técnicas de integración

### Sustitución (cambio de variable)
- ∫f(g(x)) · g'(x)dx = ∫f(u)du donde u = g(x)
- Cambiar límites si es definida
- Verificar derivando el resultado

### Integración por partes
- ∫u dv = uv - ∫v du
- Regla LIATE para elegir u:
  1. **L**ogarítmicas
  2. **I**nversas trigonométricas
  3. **A**lgébricas (polinómicas)
  4. **T**rigonométricas
  5. **E**xponenciales

### Fracciones parciales
- **Factores lineales distintos**: A/(x-a) + B/(x-b) + ...
- **Factores lineales repetidos**: A/(x-a) + B/(x-a)² + ...
- **Factores cuadráticos**: (Ax+B)/(x²+bx+c) + ...
- Siempre verificar que grado del numerador < grado del denominador

### Integrales trigonométricas
- ∫senᵐ(x)cosⁿ(x)dx:
  - n impar: sustituir u = sen(x)
  - m impar: sustituir u = cos(x)
  - Ambos pares: usar identidades de ángulo mitad
- ∫secⁿ(x)dx:
  - n par: u = tan(x)
  - n impar: u = sec(x)

## Aplicaciones

### Área entre curvas
- Área = ∫ₐᵇ |f(x) - g(x)|dx
- Si f ≥ g en [a,b]: Área = ∫ₐᵇ [f(x) - g(x)]dx

### Volúmenes de revolución
- **Discos**: V = π∫ₐᵇ [f(x)]²dx
- **Arcos (shell)**: V = 2π∫ₐᵇ x·f(x)dx
- **Anillos**: V = π∫ₐᵇ [R(x)² - r(x)²]dx

### Longitud de arco
- L = ∫ₐᵇ √(1 + [f'(x)]²)dx

### Superficie de revolución
- S = 2π∫ₐᵇ f(x)√(1 + [f'(x)]²)dx

## Ecuaciones diferenciales elementales

### EDO separable
- dy/dx = f(x)g(y) → dy/g(y) = f(x)dx → ∫dy/g(y) = ∫f(x)dx

### EDO lineal de primer orden
- dy/dx + P(x)y = Q(x)
- Factor integrante: μ(x) = e^(∫P(x)dx)
- Solución: y = (1/μ(x)) · ∫μ(x)Q(x)dx

### EDO lineal 2º orden coef. constantes
- ay'' + by' + cy = 0
- Ecuación característica: ar² + br + c = 0
- Raíces reales distintas r₁, r₂: y = C₁e^(r₁x) + C₂e^(r₂x)
- Raíces repetidas r: y = (C₁ + C₂x)e^(rx)
- Raíces complejas α ± βi: y = e^(αx)(C₁cos(βx) + C₂sen(βx))

## Errores comunes / Pitfalls

- **Olvidar + C** en integrales indefinidas
- **Sustitución**: cambiar límites SIEMPRE si es definida, o volver a la variable original
- **Fracciones parciales**: verificar grado numerador < denominador antes de descomponer
- **Integración por partes**: elegir u y dv correctamente (LIATE)
- **Área entre curvas**: usar valor absoluto si las curvas se cruzan (dividir en intervalos)
- **Volúmenes**: verificar si usar discos, arcos o anillos según el eje de rotación
- **EDO**: verificar la solución sustituyendo en la ecuación original

## Verificación

- [ ] Derivar el resultado de la integral indefinida: ¿se obtiene el integrando?
- [ ] En integrales definidas: ¿el resultado tiene sentido geométrico (signo)?
- [ ] En fracciones parciales: recomponer y verificar
- [ ] En volúmenes: unidades correctas (longitud³)
- [ ] En EDOs: sustituir la solución en la ecuación
