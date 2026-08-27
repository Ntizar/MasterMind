---
name: stem-physics-engineering
description: Física para ingeniería: ondas EM, circuitos CA, circuitos RLC, termodinámica avanzada, mecánica de fluidos, electricidad y magnetismo a nivel universitario.
tags: [stem, physics, engineering]
---

# Física para Ingeniería

## Referencias de autoridad

- **Sears & Zemansky**: University Physics with Modern Physics, 14ª edición, Pearson
- **Griffiths**: Introduction to Electrodynamics, 4ª edición, Cambridge
- **Morin**: Introduction to Classical Mechanics, Cambridge
- **Feynman**: The Feynman Lectures on Physics, Vol. I-III

## Ondas electromagnéticas

### Ecuaciones de Maxwell (forma diferencial)
1. **Gauss eléctrico**: ∇ · E⃗ = ρ/ε₀
2. **Gauss magnético**: ∇ · B⃗ = 0
3. **Faraday**: ∇ × E⃗ = -∂B⃗/∂t
4. **Ampere-Maxwell**: ∇ × B⃗ = μ₀J⃗ + μ₀ε₀∂E⃗/∂t

### Ecuación de onda EM
- ∇²E⃗ = μ₀ε₀∂²E⃗/∂t²
- c = 1/√(μ₀ε₀) ≈ 3 × 10⁸ m/s (velocidad de la luz)
- **Solución plana**: E⃗ = E₀sen(kx - ωt)k⃗
- ω = ck, λ = 2π/k = 2πc/ω

### Energía e intensidad
- **Densidad de energía**: u = ½ε₀E² + ½B²/μ₀
- **Vector de Poynting**: S⃗ = (1/μ₀)E⃗ × B⃗
- **Intensidad**: I = |S⃗|_promedio = ½cε₀E₀² = E₀²/(2μ₀c)

### Polarización
- **Lineal**: E⃗ oscila en un solo plano
- **Circular**: |Eₓ| = |Eᵧ|, Δφ = π/2
- **Elíptica**: caso general

### Reflexión y refracción (óptica EM)
- n = c/v = √(εᵣμᵣ) ≈ √εᵣ (no magnético)
- sen(θᵢ)/sen(θᵣ) = n₂/n₁ (Snell)
- **Reflexión total**: sen(θc) = n₂/n₁ (n₁ > n₂)

## Circuitos CA (corriente alterna)

### Fasores
- v(t) = V₀cos(ωt + φ) → V⃗ = V₀∠φ = V₀e^(jφ)
- **Impedancia**: Z = R + jX (Ω)
  - R: resistencia (Ω)
  - X: reactancia (Ω)
  - j = √(-1)

### Reactancias
- **Resistor**: Z_R = R
- **Inductor**: Z_L = jωL = j2πfL
- **Capacitor**: Z_C = 1/(jωC) = -j/(ωC)

### Impedancia total
- **Serie**: Z = R + j(X_L - X_C)
- **Paralelo**: 1/Z = 1/Z₁ + 1/Z₂ + ...

### Potencia en CA
- **Instantánea**: p(t) = v(t)·i(t)
- **Media**: P = V_eff · I_eff · cos(φ) = I_eff²R
- **Reactiva**: Q = V_eff · I_eff · sen(φ) (VAR)
- **Aparente**: S = V_eff · I_eff (VA)
- **Factor de potencia**: fp = cos(φ) = P/S
- **Triángulo de potencias**: S² = P² + Q²

### Resonancia RLC serie
- **Frecuencia de resonancia**: ω₀ = 1/√(LC)
- **Impedancia en resonancia**: Z = R (mínima)
- **Corriente en resonancia**: I = V/R (máxima)
- **Factor de calidad**: Q = ω₀L/R = 1/(ω₀CR)
- **Ancho de banda**: Δω = ω₀/Q = R/L

## Mecánica de fluidos avanzada

### Ecuación de Bernoulli (forma general)
- P + ½ρv² + ρgz = constante (a lo largo de una línea de corriente)
- **Presión estática**: P
- **Presión dinámica**: ½ρv²
- **Presión hidrostática**: ρgz

### Flujo en tuberías

#### Número de Reynolds
- Re = ρvD/μ = vD/ν
- **Laminar**: Re < 2000
- **Transición**: 2000 < Re < 4000
- **Turbulento**: Re > 4000

#### Ecuación de Darcy-Weisbach
- ΔP = f·(L/D)·(½ρv²)
- f = factor de fricción ( Moody chart)
- **Laminar**: f = 64/Re
- **Turbulento**: Colebrook-White

#### Ecuación de continuidad
- ρ₁A₁v₁ = ρ₂A₂v₂ (masa)
- A₁v₁ = A₂v₂ (incompresible)

### Capa límite
- **Espesor de capa límite**: δ(x) ≈ 5x/√(Re_x) (laminar)
- **Tensión cortante en pared**: τ_w = μ(∂u/∂y)|_y=0
- **Separación de capa límite**: gradiente de presión adverso

## Termodinámica avanzada

### Propiedades termodinámicas
- **Entalpía**: H = U + PV
- **Energía libre de Gibbs**: G = H - TS
- **Energía libre de Helmholtz**: A = U - TS
- **Relaciones de Maxwell**:
  - dU = TdS - PdV
  - dH = TdS + VdP
  - dA = -SdT - PdV
  - dG = -SdT + VdP

### Ciclos de potencia
- **Ciclo Rankine** (vapor): bomba → caldera → turbina → condensador
- **Ciclo Brayton** (gas): compresor → combustión → turbina → escape
- **Eficiencia Rankine**: η = W_turbina - W_bomba / Q_caldera
- **Eficiencia Brayton**: η = 1 - 1/r_p^((γ-1)/γ)

### Transferencia de calor
- **Conducción**: Q = -kA·dT/dx (Ley de Fourier)
  - Pared plana: Q = kA·ΔT/L
  - Cilindro: Q = 2πkL·ΔT/ln(r₂/r₁)
- **Convección**: Q = hA·(T_s - T_∞) (Ley de enfriamiento de Newton)
- **Radiación**: Q = εσA(T⁴ - T_amb⁴) (Stefan-Boltzmann)
- **Resistencia térmica**: R_th = ΔT/Q

### Difusión de calor
- **Ecuación de calor**: ∂T/∂t = α∇²T
- α = k/(ρc_p) = difusividad térmica

## Errores comunes / Pitfalls

- **Fasores**: usar V_eff (RMS), no V₀ (pico). V_eff = V₀/√2
- **Resonancia RLC**: en resonancia, Z = R (no Z = 0). X_L = X_C se cancelan
- **Número de Reynolds**: verificar si es laminar o turbulento antes de elegir fórmula
- **Capa límite**: la separación ocurre con gradiente de presión adverso (presión aumenta en dirección del flujo)
- **Relaciones de Maxwell**: verificar el signo en dU = TdS - PdV
- **Darcy-Weisbach**: verificar si f es para flujo laminar o turbulento

## Verificación

- [ ] Fasores: Z_R = R, Z_L = jωL, Z_C = 1/(jωC)
- [ ] Resonancia: ω₀ = 1/√(LC). Verificar dimensiones: [LC] = T²
- [ ] Bernoulli: todos los términos en Pa (N/m²)
- [ ] Reynolds: Re = vD/ν. Verificar: [vD/ν] = (L/T)(L)/(L²/T) = 1 (adimensional)
- [ ] Conducción: Q = kAΔT/L. Verificar: [W/(m·K)]·[m²]·[K]/[m] = W ✓
