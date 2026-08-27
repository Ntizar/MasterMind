---
name: math-basics
description: Aritmética, álgebra elemental, proporcionalidad, porcentajes, ecuaciones de 1º y 2º grado, notación científica, fracciones, potencias, raíces, MCD/MCM, desigualdades simples.
tags: [stem, math, basics]
---

# Fundamentos de Matemáticas

## Referencias de autoridad

- Khan Academy — Algebra 1 (khanacademy.org/math/algebra)
- Larson, R. & Edwards, B. — *Algebra and Trigonometry*, Cengage Learning
- Stewart, J. — *Precalculus*, Cengage Learning (capítulos introductorios)
- NCTM — *Principles and Standards for School Mathematics*

## Contenido clave

### Aritmética y números
- Operaciones fundamentales: suma, resta, multiplicación, división
- Jerarquía de operaciones (PEMDAS): paréntesis, exponentes, multiplicación/división (izquierda a derecha), suma/resta (izquierda a derecha)
- Números enteros, racionales, irracionales, reales
- Propiedades: conmutativa, asociativa, distributiva, elemento neutro, inverso

### Fracciones
- Simplificación: dividir numerador y denominador por MCD
- Suma/Resta: denominador común = MCM de denominadores
- Multiplicación: numerador × numerador, denominador × denominador
- División: multiplicar por la inversa
- Fracción como operador: ¾ de 20 = (¾) × 20 = 15

### Potencias y raíces
- Propiedades: aᵐ · aⁿ = aᵐ⁺ⁿ, (aᵐ)ⁿ = aᵐⁿ, aᵐ / aⁿ = aᵐ⁻ⁿ, a⁻ⁿ = 1/aⁿ, a⁰ = 1 (a ≠ 0)
- Raíz n-ésima: ⁿ√a = a^(1/n)
- ⁿ√(a·b) = ⁿ√a · ⁿ√b, ⁿ√(a/b) = ⁿ√a / ⁿ√b
- Raíz de raíz: ⁱ√(ⁿ√a) = ⁱⁿ√a = ⁱⁿ√a

### Notación científica
- Formato: a × 10ⁿ donde 1 ≤ |a| < 10 y n es entero
- Conversión: mover decimal n posiciones; si se mueve a la derecha, n > 0; si a la izquierda, n < 0
- Operaciones: multiplicar coeficientes y sumar exponentes; dividir coeficientes y restar exponentes

### Porcentajes y proporcionalidad
- Porcentaje: p% = p/100. x es p% de y → x = (p/100) · y
- Incremento/disminución: nuevo valor = valor × (1 ± p/100)
- Proporcionalidad directa: y = kx, k = y/x constante
- Regla de tres simple: a/b = c/x → x = (b·c)/a

### Ecuaciones de primer grado
- Forma: ax + b = 0 → x = -b/a (a ≠ 0)
- Método: aislar x pasando términos por el otro lado CAMBIANDO de signo
- Verificación: sustituir la solución en la ecuación original

### Ecuaciones de segundo grado
- Forma: ax² + bx + c = 0 (a ≠ 0)
- Fórmula: x = (-b ± √(b² - 4ac)) / (2a)
- Discriminante: Δ = b² - 4ac
  - Δ > 0: dos soluciones reales distintas
  - Δ = 0: una solución real doble (raíz repetida)
  - Δ < 0: no hay soluciones reales (dos complejas conjugadas)
- Factorización: ax² + bx + c = a(x - x₁)(x - x₂)
- Relación de Vieta: x₁ + x₂ = -b/a, x₁ · x₂ = c/a
- Vértice de la parábola: xᵥ = -b/(2a), yᵥ = f(xᵥ)

### MCD y MCM
- MCD(m, n): máximo divisor común. Algoritmo de Euclides: MCD(a, b) = MCD(b, a mod b) hasta resto = 0
- MCM(m, n): mínimo común múltiplo. MCM(a, b) = |a·b| / MCD(a, b)
- Relación: MCD(a, b) · MCM(a, b) = |a·b|

### Desigualdades
- Propiedades: si a < b y c > 0, entonces ac < bc. Si c < 0, se INVIERTE el sentido: ac > bc
- Desigualdad triangular: |a + b| ≤ |a| + |b|
- Valor absoluto: |x| = x si x ≥ 0, -x si x < 0
- |x| < a (a > 0) → -a < x < a
- |x| > a (a > 0) → x > a ó x < -a

## Unidades y sistema SI

- No aplica directamente (matemáticas puras), pero las cantidades aplicadas usan unidades SI:
  - Longitud: metro (m)
  - Masa: kilogramo (kg)
  - Tiempo: segundo (s)
  - Verificar coherencia dimensional en ecuaciones físicas

## Errores comunes / Pitfalls

- **Signo en ecuación cuadrática**: el término -b en la fórmula ya incluye el signo de b. Si b es negativo (-3), entonces -b = +3. No hacer doble cambio de signo.
- **Orden de operaciones**: 2 + 3 × 4 = 14, NO 20. La multiplicación va antes que la suma.
- **Simplificación de fracciones**: 6/8 = 3/4 (dividir por MCD = 2), NO 6/8 = 5/7.
- **Raíz de producto**: √(a + b) ≠ √a + √b. Solo se distribuye sobre multiplicación/división.
- **Potencias negativas**: a⁻ⁿ = 1/aⁿ, NO -aⁿ.
- **División por cero**: x = -b/a requiere a ≠ 0. Si a = 0, la ecuación no es de 1º grado.
- **Regla de tres inversa**: si y = k/x, entonces x₁y₁ = x₂y₂, NO x₁/y₁ = x₂/y₂.
- **Desigualdad con negativo**: al multiplicar/dividir por negativo, invertir el sentido. 2x < 6 → x < 3, pero -2x < 6 → x > -3.

## Verificación

- [ ] Ecuación de 1º grado: sustituir x = -b/a en ax + b = 0 y verificar que da 0
- [ ] Ecuación de 2º grado: verificar que ambas raíces satisfacen ax² + bx + c = 0
- [ ] Ecuación de 2º grado: verificar relación de Vieta (suma y producto de raíces)
- [ ] Fracciones: convertir resultado a decimal y comparar con cálculo directo
- [ ] Notación científica: verificar que el coeficiente está entre 1 y 10 (valor absoluto)
- [ ] MCD/MCM: verificar que MCD divide a ambos y MCM es múltiplo de ambos
- [ ] Porcentaje: verificar que (resultado / original) × 100 = porcentaje indicado
- [ ] Desigualdad: probar un valor en la solución y uno fuera para verificar sentido
