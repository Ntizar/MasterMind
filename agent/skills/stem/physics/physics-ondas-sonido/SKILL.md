---
name: physics-ondas-sonido
description: Movimiento armónico simple, ondas mecánicas, sonido, efecto Doppler, interferencia y ondas estacionarias.
tags: [stem, physics, basics]
---

# Ondas y Sonido

## Movimiento Armónico Simple (MAS)

- **Posición**: x(t) = A·cos(ωt + φ₀)
- **Velocidad**: v(t) = -Aω·sen(ωt + φ₀)
- **Aceleración**: a(t) = -Aω²·cos(ωt + φ₀) = -ω²·x
- **A** = amplitud (m)
- **ω** = ω = 2πf = 2π/T = 2π/T (rad/s)
- **φ₀** = fase inicial (rad)

### Relación con movimiento circular
- x = A·cos(θ), θ = ωt + φ₀
- La proyección de un MCU es un MAS

### Energía del MAS
- E_c = ½mv² = ½mω²A²sen²(ωt + φ₀)
- E_p = ½kx² = ½kA²cos²(ωt + φ₀)
- E_total = ½kA² = ½mω²A² (constante)
- k = mω²

### Periodo de sistemas
- **Muelle-masa**: T = 2π√(m/k)
- **Péndulo simple** (θ pequeño): T = 2π√(L/g)
- **Péndulo físico**: T = 2π√(I/mgd)

## Ondas mecánicas

### Clasificación
- **Transversal**: vibración perpendicular a la dirección de propagación (cuerdas, electromagnéticas)
- **Longitudinal**: vibración paralela a la propagación (sonido)

### Ecuación de una onda viajera
- y(x,t) = A·sen(kx - ωt + φ)
- **k** = 2π/λ = número de ondas (rad/m)
- **ω** = 2πf = frecuencia angular (rad/s)
- **v** = λ·f = ω/k (velocidad de propagación, m/s)

### Energía de una onda
- Potencia ∝ A²
- Intensidad I = P/A (W/m²)

## Sonido

### Parámetros
- **Frecuencia** (f): Hz → tono (agudo/grave)
- **Intensidad** (I): W/m² → volumen
- **Nivel sonoro**: β = 10·log₁₀(I/I₀) dB, I₀ = 10⁻¹² W/m² (umbral de audición)

### Velocidad del sonido
- En aire: v ≈ 343 m/s (a 20°C)
- v = √(B/ρ) en fluidos (B = módulo de compresibilidad)
- v = √(T/μ) en cuerdas (T = tensión, μ = densidad lineal)
- En sólidos: v = √(E/ρ) (E = módulo de Young)

### Efecto Doppler
- f_obs = f_fuente · (v ± v_obs) / (v ∓ v_fuente)
  - Observador se acerca: +v_obs
  - Observador se aleja: -v_obs
  - Fuente se acerca: -v_fuente (denominador)
  - Fuente se aleja: +v_fuente (denominador)

### Ondas estacionarias
- Cuerda fija en ambos extremos: λ_n = 2L/n, f_n = nv/(2L) (n = 1, 2, 3, ...)
- f₁ = v/(2L) = frecuencia fundamental
- Armónicos: f_n = n·f₁

### Tubos sonoros
- **Abierto-abierto**: λ_n = 2L/n, f_n = nv/(2L)
- **Cerrado-abierto**: λ_n = 4L/(2n-1), f_n = (2n-1)v/(4L) (solo armónicos impares)

## Interferencia

- **Constructiva**: Δr = nλ (máximos)
- **Destructiva**: Δr = (n + ½)λ (mínimos)
- **Bands**: Δf = |f₁ - f₂| (pulsaciones)

## Errores comunes / Pitfalls

- **MAS**: a = -ω²x, no a = ω²x. El signo negativo es crucial (fuerza restauradora)
- **Ondas**: v = λf, NO v = λ/f
- **Doppler**: la fuente que se acerca AUMENTA la frecuencia percibida. Verificar con sentido común
- **Péndulo**: la fórmula T = 2π√(L/g) solo vale para ángulos pequeños (< 15°)
- **Intensidad sonora**: β = 10·log(I/I₀), NO 20·log (eso es para amplitudes, no intensidades)
- **Ondas estacionarias**: n = 1 es el fundamental, NO n = 0

## Verificación

- [ ] MAS: verificar a = -ω²x derivando x(t) dos veces
- [ ] Energía MAS: E_total = ½kA² (constante)
- [ ] Ondas: v = λf → [L/T] = [L]·[1/T] ✓
- [ ] Doppler: si la fuente se acerca, f_obs > f_fuente
- [ ] Ondas estacionarias: f_n = n·f₁ (armónicos múltiplos del fundamental)
- [ ] Decibelios: duplicar intensidad → +3 dB. Duplicar amplitud → +6 dB
