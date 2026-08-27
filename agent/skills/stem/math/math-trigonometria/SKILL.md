---
name: math-trigonometria
description: Razones trigonométricas, identidades fundamentales, ecuaciones trigonométricas, funciones seno, coseno, tangente, teorema del seno y coseno.
tags: [stem, math, intermediate]
---

# Trigonometría

## Razones trigonométricas en triángulo rectángulo

- **sen(θ)** = cateto opuesto / cateto hipotenusa
- **cos(θ)** = cateto adyacente / cateto hipotenusa
- **tan(θ)** = sen(θ) / cos(θ) = cateto opuesto / cateto adyacente
- **csc(θ)** = 1/sen(θ), **sec(θ)** = 1/cos(θ), **cot(θ)** = 1/tan(θ)

## Triángulo notables

- 30°-60°-90°: lados 1, √3, 2
- 45°-45°-90°: lados 1, 1, √2

## Valores notables

| θ (grados) | 0° | 30° | 45° | 60° | 90° |
|---|---|---|---|---|---|
| sen(θ) | 0 | 1/2 | √2/2 | √3/2 | 1 |
| cos(θ) | 1 | √3/2 | √2/2 | 1/2 | 0 |
| tan(θ) | 0 | √3/3 | 1 | √3 | indefinido |

## Identidades fundamentales

### Pitagóricas
- sen²(θ) + cos²(θ) = 1
- 1 + tan²(θ) = sec²(θ)
- 1 + cot²(θ) = csc²(θ)

### Ángulo doble
- sen(2θ) = 2sen(θ)cos(θ)
- cos(2θ) = cos²(θ) - sen²(θ) = 2cos²(θ) - 1 = 1 - 2sen²(θ)
- tan(2θ) = 2tan(θ) / (1 - tan²(θ))

### Mitad
- sen(θ/2) = ±√((1 - cos(θ))/2)
- cos(θ/2) = ±√((1 + cos(θ))/2)
- tan(θ/2) = sen(θ)/(1 + cos(θ)) = (1 - cos(θ))/sen(θ)

### Suma y diferencia
- sen(α ± β) = sen(α)cos(β) ± cos(α)sen(β)
- cos(α ± β) = cos(α)cos(β) ∓ sen(α)sen(β)
- tan(α ± β) = (tan(α) ± tan(β)) / (1 ∓ tan(α)tan(β))

### Producto a suma
- sen(α)sen(β) = ½[cos(α-β) - cos(α+β)]
- cos(α)cos(β) = ½[cos(α-β) + cos(α+β)]
- sen(α)cos(β) = ½[sen(α+β) + sen(α-β)]

## Funciones trigonométricas

### Seno: y = sen(x)
- Período: 2π
- Dominio: R, Rango: [-1, 1]
- Impar: sen(-x) = -sen(x)

### Coseno: y = cos(x)
- Período: 2π
- Dominio: R, Rango: [-1, 1]
- Par: cos(-x) = cos(x)

### Tangente: y = tan(x)
- Período: π
- Dominio: R \ {π/2 + kπ}, Rango: R
- Impar: tan(-x) = -tan(x)
- Asíntotas en x = π/2 + kπ

## Teorema del seno y coseno

### Teorema del seno
a/sen(A) = b/sen(B) = c/sen(C) = 2R (R = circunradio)

### Teorema del coseno (Ley de cosenos)
c² = a² + b² - 2ab·cos(C)
a² = b² + c² - 2bc·cos(A)
b² = a² + c² - 2ac·cos(B)

Pitfall: El teorema del coseno generaliza Pitágoras. Si C = 90°, cos(C) = 0 y se reduce a c² = a² + b².

### Área de un triángulo
- Área = ½ab·sen(C) = ½bc·sen(A) = ½ac·sen(B)
- **Fórmula de Herón**: Área = √(s(s-a)(s-b)(s-c)), donde s = (a+b+c)/2

## Ecuaciones trigonométricas

- sen(x) = a → x = arcsen(a) + 2kπ o x = π - arcsen(a) + 2kπ (solo si |a| ≤ 1)
- cos(x) = a → x = arccos(a) + 2kπ o x = -arccos(a) + 2kπ (solo si |a| ≤ 1)
- tan(x) = a → x = arctan(a) + kπ

## Radianes

- 360° = 2π rad, 180° = π rad, 90° = π/2 rad
- θ(rad) = θ(°) · π/180
- Longitud de arco: s = r · θ (θ en radianes)
- Área de sector circular: A = ½r²θ (θ en radianes)

## Errores comunes / Pitfalls

- **Grados vs radianes**: las derivadas/integrales de trig solo funcionan con radianes
- **sen²(x)** = (sen(x))², NO sen(x²)
- **arcsen(sen(x)) ≠ x** en general. Solo es x si x ∈ [-π/2, π/2]
- **arccos(cos(x)) ≠ x** en general. Solo es x si x ∈ [0, π]
- **Identidad doble**: cos(2θ) tiene 3 formas equivalentes, usar la más conveniente
- **Ecuaciones**: siempre dar TODAS las soluciones en el intervalo dado

## Verificación

- [ ] Verificar identidades sustituyendo valores notables
- [ ] En ecuaciones: ¿todas las soluciones en el intervalo?
- [ ] sen² + cos² = 1 para cualquier ángulo
- [ ] Teorema del seno: verificar que lados mayores corresponden a ángulos mayores
- [ ] Conversión grados↔radianes: 180° = π
