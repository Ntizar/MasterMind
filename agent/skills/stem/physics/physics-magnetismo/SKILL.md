---
name: physics-magnetismo
description: Magnetismo: campo magnético, Ley de Ampere, fuerza de Lorentz, inducción de Faraday, Ley de Lenz, autoinducción y materiales magnéticos.
tags: [stem, physics, intermediate]
---

# Magnetismo

## Campo magnético

- B⃗: Tesla (T) = N/(A·m)
- **Líneas de campo**: cerradas. Salen del polo N, entran en el S
- No existen monopolos magnéticos (no se puede aislar un polo N o S)

### Campo creado por corrientes
- **Hilo rectilíneo**: B = μ₀I/(2πr) (las líneas son circunferencias alrededor del hilo)
- **Espira en su centro**: B = μ₀I/(2R)
- **Solenoide (bobina ideal)**: B = μ₀·n·I (n = N/L = vueltas por metro)
- **μ₀** = 4π × 10⁻⁷ T·m/A (permeabilidad magnética del vacío)

## Fuerza de Lorentz

- F⃗ = q·(v⃗ × B⃗)
- |F| = qv·B·sen(θ) (θ = ángulo entre v y B)
- F⃗ ⊥ v⃗ y F⃗ ⊥ B⃗ (regla de la mano izquierda para electrones, derecha para corrientes)

### Movimiento de cargas en campo uniforme
- **Perpendicular**: movimiento circular. r = mv/(qB)
- **Oblicua**: hélice (movimiento circular + desplazamiento a lo largo de B)

### Fuerza sobre un conductor
- F⃗ = I·(L⃗ × B⃗)
- |F| = IL·B·sen(θ)
- **Dos hilos paralelos**: F/L = μ₀·I₁·I₂/(2πd)
  - Misma dirección: atracción
  - Dirección contraria: repulsión

## Momento magnético

- **Espira**: μ⃗ = I·A·n̂ (A = área de la espira, n̂ normal)
- **Torque**: τ⃗ = μ⃗ × B⃗
- **Energía potencial**: U = -μ⃗ · B⃗

## Ley de Ampere

- ∮B⃗ · dl⃗ = μ₀·I_encerrada
- Aplicaciones:
  - **Hilo rectilíneo**: B·2πr = μ₀I → B = μ₀I/(2πr)
  - **Solenoide**: B·L = μ₀·N·I → B = μ₀·n·I

## Inducción electromagnética

### Ley de Faraday
- ε = -dΦ_B/dt
- ε = fem inducida (V)
- Φ_B = ∫B⃗ · dA⃗ (flujo magnético, Wb = Weber = T·m²)

### Ley de Lenz
La fem inducida se opone al cambio que la produce.
- Signo en Faraday: el - indica oposición

### Fem en un conductor en movimiento
- ε = vBL (conductor de longitud L moviéndose perpendicular a B)

## Autoinducción

- ε = -L·dI/dt
- L = autoinducción (H = Henrio = V·s/A)
- **Solenoide**: L = μ₀·N²·A/L (= μ₀·n²·A·l)
- **Energía almacenada**: U = ½LI²

## Circuitos RL

- **Conexión**: I(t) = I₀(1 - e^(-t/τ)), τ = L/R
- **Desconexión**: I(t) = I₀·e^(-t/τ), τ = L/R

## Materiales magnéticos

- **Paramagnéticos**: μ > μ₀, ligeramente atraídos
- **Diamagnéticos**: μ < μ₀, ligeramente repelidos
- **Ferromagnéticos**: μ >> μ₀, fuertemente atraídos. Histéresis
- B = μ₀·(H + M) = μH donde μ = μ₀·μ_r

## Errores comunes / Pitfalls

- **Lorentz**: F = qvB para v ⊥ B. Para v ∥ B, F = 0
- **Regla de la mano**: corriente positiva = movimiento de cargas positivas. Electrones son negativos
- **Faraday**: ε depende del cambio de flujo, no del flujo. Si Φ_B es constante, ε = 0
- **Lenz**: la corriente inducida siempre se opone al cambio de flujo. Si B aumenta, el campo inducido se opone
- **Ampere**: solo funciona con corrientes estacionarias. Para corrientes variables, corregir con Maxwell
- **Solenoide**: B = μ₀nI, independiente de la sección (para solenoide ideal infinito)

## Verificación

- [ ] Lorentz: F = qvBsen(θ). Si v ∥ B, F = 0
- [ ] Ampere: ∮B·dl = μ₀I. Verificar para hilo: B = μ₀I/(2πr)
- [ ] Faraday: ε = -dΦ/dt. El signo determina la dirección de la corriente inducida
- [ ] Autoinducción: ε = -L·dI/dt. τ = L/R en RL
- [ ] Momento magnético: τ = μ × B. Si μ ∥ B, τ = 0