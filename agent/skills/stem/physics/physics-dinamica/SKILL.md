---
name: physics-dinamica
description: Dinámica del punto: 3 leyes de Newton, fuerzas, rozamiento, tensión, planos inclinados, fuerza elástica, centro de masas y cantidad de movimiento.
tags: [stem, physics, basics]
---

# Dinámica

## Leyes de Newton

### 1ª Ley (Inercia)
Un cuerpo permanece en reposo o MRU si la fuerza neta sobre él es cero.
- Masa = medida de inercia (kg)
- Sistema inercial: donde se cumplen las leyes de Newton

### 2ª Ley (Fundamental de la Dinámica)
ΣF⃗ = m·a⃗
- F⃗ en Newtons (N = kg·m/s²)
- Dirección de a⃗ = dirección de ΣF⃗
- Si ΣF⃗ = 0 → a⃗ = 0 → v⃗ = constante

### 3ª Ley (Acción y Reacción)
Si A ejerce F⃗_AB sobre B, entonces B ejerce F⃗_BA = -F⃗_AB sobre A.
- Actúan sobre cuerpos DIFERENTES (no se anulan)
- Son del mismo tipo (ambas gravitatorias, ambas de contacto, etc.)

## Fuerzas comunes

### Peso
- P⃗ = m·g⃗ (hacia abajo)
- g ≈ 9,81 m/s² en la superficie terrestre
- P = mg (módulo)

### Normal
- N⃗: fuerza de contacto perpendicular a la superficie
- NO siempre es igual al peso (depende de la geometría)

### Fricción / Rozamiento
- **Estática**: f_s ≤ μ_s · N (fuerza que impide el inicio del movimiento)
- **Cinética**: f_k = μ_k · N (fuerza que se opone al movimiento)
- μ_s ≥ μ_k (más difícil iniciar que mantener el movimiento)
- f⃗ siempre paralela a la superficie, opuesta al movimiento o tendencia a moverse

### Tensión
- T⃗: fuerza a lo largo de una cuerda/cable
- Cuerda ideal: masa despreciable, tensión uniforme a lo largo
- Polea ideal: sin fricción, tensión igual en ambos lados

### Fuerza elástica (Hooke)
- F = -k·x
- k = constante elástica (N/m)
- x = deformación desde la posición de equilibrio (m)
- El signo negativo indica que la fuerza es restauradora

### Fuerza centrípeta
- F_c = m·v²/r = m·ω²·r
- NO es una fuerza "extra": es la resultante de otras fuerzas (tensión, gravedad, fricción, normal)

## Plano inclinado

- Ejes: x paralela al plano, y perpendicular
- mg_x = mg·sen(θ) (hacia abajo del plano)
- mg_y = mg·cos(θ) (perpendicular al plano)
- N = mg·cos(θ) (si no hay otras fuerzas en y)
- Si desliza: ΣF_x = mg·sen(θ) - f_k = ma
- a = g·(sen(θ) - μ_k·cos(θ))

## Centro de masas

- x_cm = Σmᵢxᵢ / Σmᵢ
- v_cm = Σmᵢvᵢ / Σmᵢ
- a_cm = ΣF⃗_ext / M_total
- ΣF⃗_ext = M·a_cm (las fuerzas internas no afectan al centro de masas)

## Diagrama de cuerpo libre (DCL)

1. Aislar el cuerpo
2. Dibujar TODAS las fuerzas que actúan SOBRE él
3. Elegir sistema de ejes
4. Descomponer fuerzas en componentes
5. Aplicar ΣF = ma en cada eje

## Errores comunes / Pitfalls

- **3ª Ley**: las fuerzas de acción-reacción actúan sobre cuerpos distintos, NO se anulan
- **Normal ≠ peso**: en plano inclinado N = mg·cos(θ), no mg
- **Fuerza centrípeta**: no es una fuerza adicional. Es la resultante. No se dibuja en el DCL como fuerza aparte
- **Rozamiento**: f_s ≤ μ_s·N (no f_s = μ_s·N, solo cuando está a punto de deslizar)
- **Unidades**: masa en kg, fuerza en N, distancia en m. SIEMPRE SI
- **Poleas**: la tensión es la misma en ambos lados SOLO si la polea es ideal (sin masa ni fricción)

## Verificación

- [ ] DCL: ¿todas las fuerzas tienen una fuente física identificable?
- [ ] Dimensiones: [F] = M·L/T²
- [ ] 3ª Ley: ¿las fuerzas actúan sobre cuerpos diferentes?
- [ ] Plano inclinado: si θ = 0, a = 0. Si θ = 90°, a = g
- [ ] Centro de masas: ¿está entre las masas?
