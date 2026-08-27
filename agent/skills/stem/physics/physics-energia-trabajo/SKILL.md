---
name: physics-energia-trabajo
description: Trabajo, energía cinética, potencial, conservación de energía, potencia, fuerzas conservativas y no conservativas, energía mecánica.
tags: [stem, physics, basics]
---

# Energía y Trabajo

## Trabajo

- **Definición**: W = F⃗ · d⃗ = F·d·cos(θ) (J = N·m = J)
- θ = ángulo entre fuerza y desplazamiento
- W > 0: fuerza ayuda al movimiento (θ < 90°)
- W < 0: fuerza se opone (θ > 90°)
- W = 0: fuerza perpendicular al desplazamiento (θ = 90°)
- Trabajo de fuerza variable: W = ∫F⃗ · dr⃗

### Trabajo de fuerzas específicas
- **Peso**: W_p = -mg·Δh = mg(h_i - h_f)
- **Elástica**: W_e = -½k(x_f² - x_i²)
- **Fricción**: W_f = -f_k · d (siempre negativo)

## Energía cinética

- E_c = ½mv²
- **Teorema trabajo-energía**: W_total = ΔE_c = ½mv_f² - ½mv_i²

## Energía potencial

### Gravitatoria (cerca de la superficie)
- E_p = mgh
- h medido desde un nivel de referencia arbitrario

### Gravitatoria (universal)
- E_p = -G·M·m/r
- G = 6,674 × 10⁻¹¹ N·m²/kg²
- E_p → 0 cuando r → ∞

### Elástica (resorte)
- E_p = ½kx²
- x = deformación desde la posición de equilibrio

## Fuerzas conservativas vs no conservativas

- **Conservativas**: el trabajo no depende del camino (solo de los puntos inicial y final)
  - Gravedad, fuerza elástica, fuerza electrostática
  - W_circuito cerrado = 0
  - ΔE_p = -W_c
- **No conservativas**: dependen del camino
  - Fricción, resistencia del aire, tensión (en general)
  - W_nc = ΔE_mecánica = Δ(E_c + E_p)

## Conservación de la energía mecánica

- Si solo actúan fuerzas conservativas: E_mec = E_c + E_p = constante
- ½mv_i² + mgh_i + ½kx_i² = ½mv_f² + mgh_f + ½kx_f²
- Con fuerzas no conservativas: E_i + W_nc = E_f

## Potencia

- **Potencia media**: P̄ = W/Δt (W = J/s = Watio)
- **Potencia instantánea**: P = dW/dt = F⃗ · v⃗
- **1 CV (caballo de vapor)**: 736 W ≈ 75 kgf·m/s
- **1 kWh**: 3,6 × 10⁶ J

## Rendimiento

- η = W_útil / W_total = E_útil / E_total
- 0 ≤ η ≤ 1 (o 0% a 100%)
- η = 1: máquina ideal (no existe en la práctica)

## Energía en colisiones

- **Elástica**: se conserva E_c y cantidad de movimiento
- **Inelástica**: se conserva cantidad de movimiento, NO E_c
- **Perfectamente inelástica**: los cuerpos quedan unidos tras la colisión

## Errores comunes / Pitfalls

- **Trabajo del peso**: W = mg·Δh, NO mgh. Si subes, el peso hace trabajo negativo
- **Energía potencial gravitatoria universal**: siempre NEGATIVA (convenio: E_p = 0 en el infinito)
- **Fricción**: siempre hace trabajo negativo (se opone al movimiento)
- **Potencia**: P = F·v SOLO si F y v están en la misma dirección
- **Conservación de energía**: verificar SIEMPRE si hay fuerzas no conservativas
- **E_p = mgh**: solo cerca de la superficie. Para alturas grandes, usar -GMm/r

## Verificación

- [ ] Dimensiones: [W] = M·L²/T², [P] = M·L²/T³
- [ ] Energía: siempre ≥ 0 para E_c, puede ser negativa para E_p gravitatoria universal
- [ ] Trabajo: verificar el ángulo θ entre F⃗ y d⃗
- [ ] Conservación: ¿hay fricción o resistencia del aire? Si sí, W_nc ≠ 0
- [ ] Potencia: P = F·v, verificar unidades (N·m/s = W)
