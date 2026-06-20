---
name: physics-cinematica
description: Cinemática del punto material: MRU, MRUA, MCU, caída libre, tiro parabólico, composición de movimientos y movimiento relativo.
tags: [stem, physics, basics]
---

# Cinemática

## Magnitudes básicas

- **Posición** (x): m
- **Desplazamiento** (Δx): x_f - x_i (vector, m)
- **Distancia recorrida**: escalar, siempre ≥ 0 (m)
- **Velocidad** (v): Δx/Δt (m/s)
- **Velocidad media**: v̄ = Δx/Δt
- **Velocidad instantánea**: v = dx/dt
- **Aceleración** (a): Δv/Δt (m/s²)
- **Aceleración media**: ā = Δv/Δt
- **Aceleración instantánea**: a = dv/dt = d²x/dt²

## MRU (Movimiento Rectilíneo Uniforme)

- a = 0, v = constante
- x(t) = x₀ + v·t
- Gráfica x-t: recta de pendiente v
- Gráfica v-t: recta horizontal

## MRUA (Movimiento Rectilíneo Uniformemente Acelerado)

- a = constante ≠ 0
- v(t) = v₀ + a·t
- x(t) = x₀ + v₀·t + ½a·t²
- **Ecuación sin tiempo**: v² = v₀² + 2a·Δx
- Gráfica x-t: parábola
- Gráfica v-t: recta de pendiente a

## Caída libre

- v₀ = 0 (soltar, no lanzar)
- a = g = 9,81 m/s² (hacia abajo)
- Despreciando resistencia del aire: todos los cuerpos caen igual
- t_subida = t_bajada (si sube y baja al mismo nivel)
- h_max = v₀²/(2g)

## Tiro parabólico

- v₀x = v₀·cos(θ), v₀y = v₀·sen(θ)
- x(t) = v₀·cos(θ)·t
- y(t) = v₀·sen(θ)·t - ½g·t²
- **Alcance**: R = v₀²·sen(2θ)/g
- **Altura máxima**: H = v₀²·sen²(θ)/(2g)
- **Tiempo de vuelo**: T = 2·v₀·sen(θ)/g
- θ = 45° → alcance máximo (sin resistencia del aire)

## MCU (Movimiento Circular Uniforme)

- ω = constante (velocidad angular, rad/s)
- v = ω·r (velocidad lineal, m/s)
- a_c = v²/r = ω²·r (aceleración centrípeta, hacia el centro)
- T = 2π/ω (período, s)
- f = 1/T = ω/(2π) (frecuencia, Hz)
- f = ω/(2π)

## Movimiento relativo

- v⃗_A/C = v⃗_A/B + v⃗_B/C
- v⃗_AG = v⃗_AB + v⃗_BG (velocidad del avión respecto al suelo)

## Gráficas cinemáticas

- **x-t**: pendiente = v
- **v-t**: pendiente = a, área bajo la curva = Δx
- **a-t**: área bajo la curva = Δv

## Errores comunes / Pitfalls

- **Velocidad vs rapidez**: velocidad es vectorial (tiene dirección), rapidez es escalar
- **Desplazamiento vs distancia**: Δx puede ser 0 si vuelves al inicio; la distancia recorrida no
- **Signo de g**: si el eje y apunta hacia arriba, g = -9,81 m/s²
- **MCU**: la velocidad lineal es constante en módulo pero NO en dirección. Hay aceleración centrípeta
- **Tiro parabólico**: en la altura máxima, v_y = 0 pero v_x ≠ 0. La velocidad NO es cero

## Verificación

- [ ] Dimensiones: [v] = L/T, [a] = L/T²
- [ ] MRUA: verificar v² = v₀² + 2aΔx con valores numéricos
- [ ] MCU: a_c = v²/r. Si v = 0, a_c = 0
- [ ] Alcance máximo a 45°: verificar con θ = 30° y 60° (mismo alcance)
- [ ] Gráficas: pendiente de v-t = a
