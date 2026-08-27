---
name: physics-advanced
description: Relatividad especial, mecánica cuántica básica, física estadística, ecuaciones de Maxwell.
tags: [stem, physics, advanced]
---

# Física Avanzada

## Referencias de autoridad

- Griffiths, D. — *Introduction to Electrodynamics* (4th ed.), Cambridge University Press
- Griffiths, D. — *Introduction to Quantum Mechanics* (2nd ed.), Cambridge University Press
- Taylor, E. & Zafiratos, D. — *Special Relativity and Electromagnetism*, W.H. Freeman
- Taylor, E. & Wheeler, J. — *Spacetime Physics* (2nd ed.), W.H. Freeman
- Schroeder, D. — *An Introduction to Thermal Physics*, Addison-Wesley

## Contenido clave

### Relatividad especial

**Postulados de Einstein** (1905):
1. Las leyes de la física son las mismas en todos los sistemas de referencia inerciales.
2. La velocidad de la luz en el vacío c es la misma para todos los observadores inerciales, independientemente del movimiento de la fuente.

**Transformaciones de Lorentz**:
- γ = 1/√(1 - v²/c²) = 1/√(1 - β²), donde β = v/c
- x' = γ(x - vt)
- t' = γ(t - vx/c²)
- y' = y, z' = z
- Para v ≪ c: γ → 1, las transformaciones se reducen a las de Galileo.

**Dilatación del tiempo**: Δt = γΔt₀
- Δt₀ = tiempo propio (medido en el marco donde los eventos ocurren en el mismo lugar)
- Δt > Δt₀: el tiempo se dilata (pasa más lento) en el marco en movimiento
- Ejemplo: muones atmosféricos llegan a superficie porque su "reloj" va más lento

**Contracción de longitud**: L = L₀/γ = L₀√(1 - v²/c²)
- L₀ = longitud propia (medida en el marco en reposo del objeto)
- L < L₀: el objeto se contrae en la dirección del movimiento
- Solo se contrae en la dirección del movimiento; perpendicular no cambia.

**Relatividad del simultáneo**: Dos eventos simultáneos en un marco NO son simultáneos en otro marco en movimiento relativo.

**Energía y momento relativistas**:
- Energía total: E = γmc²
- Energía en reposo: E₀ = mc²
- Energía cinética: K = E - E₀ = (γ - 1)mc²
- Momento: p⃗ = γmv⃗
- Relación energía-momento: E² = (pc)² + (mc²)²
- Para fotones (m = 0): E = pc, p = E/c = h/λ

**Composición de velocidades**:
- u = (u' + v)/(1 + u'v/c²) (en la dirección del movimiento)
- Nunca se supera c: si u' = c, entonces u = c.

### Mecánica cuántica básica

**Dualidad onda-partícula**:
- De Broglie: λ = h/p = h/(mv) (longitud de onda asociada a partícula)
- h = 6.626 × 10⁻³⁴ J·s (constante de Planck)
- Fotón: E = hf = hc/λ, p = h/λ

**Principio de incertidumbre de Heisenberg**:
- Δx · Δp ≥ ℏ/2 (posición-momento)
- ΔE · Δt ≥ ℏ/2 (energía-tiempo)
- ℏ = h/(2π) = 1.055 × 10⁻³⁴ J·s (constante de Planck reducida)

**Ecuación de Schrödinger**:
- **Dependiente del tiempo**: iℏ ∂Ψ/∂t = ĤΨ
  - Ĥ = -ℏ²/(2m)∇² + V(x,t) (operador hamiltoniano)
  - Ψ(x,t) = función de onda completa
- **Independiente del tiempo** (V = V(x), estados estacionarios):
  - Ĥψ = Eψ → -ℏ²/(2m) · d²ψ/dx² + V(x)ψ = Eψ
  - Ψ(x,t) = ψ(x) · e^(-iEt/ℏ)

**Interpretación probabilística (Born)**:
- |Ψ(x,t)|² = probabilidad por unidad de volumen de encontrar la partícula en x en el tiempo t
- Normalización: ∫|Ψ|²dV = 1 (sobre todo el espacio)

**Pozo de potencial infinito (1D)**:
- V(x) = 0 para 0 < x < L, V = ∞ fuera
- ψₙ(x) = √(2/L) sen(nπx/L), n = 1, 2, 3, ...
- Eₙ = n²h²/(8mL²) = n²π²ℏ²/(2mL²)
- E₁ = h²/(8mL²) (energía de punto cero, NUNCA cero)

**Átomo de Bohr** (hidrógeno):
- Radio de Bohr: a₀ = 4πε₀ℏ²/(mₑe²) = 5.292 × 10⁻¹¹ m = 0.529 Å
- Eₙ = -13.6 eV/n² (n = 1, 2, 3, ...)
- E₁ = -13.6 eV (estado fundamental)
- λ = 1/R_H · n₁²n₂²/(n₂² - n₁²) (fórmula de Rydberg para líneas espectrales)
- R_H = 1.097 × 10⁷ m⁻¹ (constante de Rydberg)

### Física estadística

**Distribución de Maxwell-Boltzmann** (velocidades en gas ideal):
- f(v) = 4π(m/2πkT)^(3/2) · v² · e^(-mv²/(2kT))
- v_más_probable = √(2kT/m) = √(2RT/M)
- v_promedio = √(8kT/(πm)) = √(8RT/(πM))
- v_rms = √(3kT/m) = √(3RT/M)
- k = 1.381 × 10⁻²³ J/K (constante de Boltzmann)

**Entropía estadística (Boltzmann)**:
- S = k ln Ω
- Ω = número de microestados compatibles con un macroestado dado
- Conexión con termodinámica: ΔS = Q_rev/T

**Energía interna de gas ideal monoatómico**: U = (3/2)nRT
- Gas diatómico (a temperatura ambiente): U = (5/2)nRT
- Cᵥ = (∂U/∂T)ᵥ, Cₚ = Cᵥ + R, γ = Cₚ/Cᵥ

### Ecuaciones de Maxwell

**Forma integral** (sobre superficies/volumenes/curvas):

1. **Gauss para E⃗**: ∮ E⃗ · dA⃗ = Q_int/ε₀
   - El flujo eléctrico a través de una superficie cerrada = carga encerrada / ε₀

2. **Gauss para B⃗**: ∮ B⃗ · dA⃗ = 0
   - No existen monopolos magnéticos. El flujo magnético neto siempre es cero.

3. **Faraday**: ∮ E⃗ · dl⃗ = -dΦ_B/dt
   - Un campo magnético variable induce un campo eléctrico.

4. **Ampère-Maxwell**: ∮ B⃗ · dl⃗ = μ₀I + μ₀ε₀dΦ_E/dt
   - Corriente + desplazamiento eléctrico generan campo magnético.
   - μ₀ = 4π × 10⁻⁷ T·m/A (permeabilidad del vacío)

**Forma diferencial** (teorema de Stokes y Gauss):

1. ∇ · E⃗ = ρ/ε₀
2. ∇ · B⃗ = 0
3. ∇ × E⃗ = -∂B⃗/∂t
4. ∇ × B⃗ = μ₀J⃗ + μ₀ε₀∂E⃗/∂t

**Ondas electromagnéticas**:
- Ecuación de onda: ∇²E⃗ = μ₀ε₀ ∂²E⃗/∂t²
- Velocidad: c = 1/√(μ₀ε₀) = 299792458 m/s
- Relación E/B: E = cB (en módulo)
- E⃗ y B⃗ son perpendiculares entre sí y a la dirección de propagación (onda transversal)
- Vector de Poynting: S⃗ = (1/μ₀)E⃗ × B⃗ (flujo de energía por unidad de área)
- Intensidad media: I = ⟨S⟩ = E₀²/(2μ₀c) = ½ε₀cE₀²

## Unidades y sistema SI

| Magnitud | Unidad SI | Símbolo | Valor constante |
|----------|-----------|---------|-----------------|
| Velocidad luz | m/s | c | 299792458 |
| Constante Planck | J·s | h | 6.626 × 10⁻³⁴ |
| ħ | J·s | ℏ | 1.055 × 10⁻³⁴ |
| Constante Boltzmann | J/K | k | 1.381 × 10⁻²³ |
| Permitividad vacío | C²/(N·m²) | ε₀ | 8.854 × 10⁻¹² |
| Permeabilidad vacío | T·m/A | μ₀ | 4π × 10⁻⁷ |
| Carga elemental | C | e | 1.602 × 10⁻¹⁹ |
| Masa electrón | kg | mₑ | 9.109 × 10⁻³¹ |
| Radio Bohr | m | a₀ | 5.292 × 10⁻¹¹ |

## Errores comunes / Pitfalls

- **Confusión marcos de referencia en relatividad**: Δt₀ (tiempo propio) SIEMPRE es el medido en el marco donde los eventos ocurren en el MISMO LUGAR. El tiempo dilataΔt = γΔt₀ SIEMPRE. No invertir.
- **γ siempre ≥ 1**: como v < c, entonces v²/c² < 1, entonces √(1 - v²/c²) < 1, entonces γ > 1. Para v = 0, γ = 1. No puede ser menor que 1.
- **Interpretación probabilística de Ψ**: |Ψ|² es densidad de probabilidad, NO probabilidad. P(x ∈ [a,b]) = ∫ₐᵇ |Ψ|²dx. Ψ misma puede ser compleja.
- **Energía de punto cero**: en pozo infinito, E₁ ≠ 0. E₁ = h²/(8mL²). El principio de incertidumbre prohíbe E = 0 (posición y momento bien definidos simultáneamente).
- **Átomo de Bohr**: solo es EXACTO para hidrógeno (un electrón). Para átomos multi-electrón, la energía depende también del momento angular (n y l).
- **Energía en átomo de Bohr**: Eₙ = -13.6 eV/n². El signo negativo significa estado ligado. E = 0 = partícula libre. E > 0 = estado no ligado (continuo).
- **Ecuaciones de Maxwell forma diferencial**: recordar que ∇ · B⃗ = 0 (NO hay monopolos). El término de desplazamiento de Maxwell (μ₀ε₀∂E⃗/∂t) es CRUCIAL para ondas EM.
- **Corriente de desplazamiento**: no es una corriente real de cargas. Es un término que completa la simetría y permite la conservación de carga en capacitores.

## Verificación

- [ ] Relatividad: verificar que γ → 1 cuando v/c → 0 (límite newtoniano)
- [ ] Energía-momento: verificar que para m = 0, E = pc (fotón)
- [ ] Dilatación tiempo: verificar que Δt > Δt₀ (γ > 1) siempre
- [ ] Contracción: verificar que L < L₀ (γ > 1, L = L₀/γ)
- [ ] Schrödinger 1D: verificar que ψₙ satisface -ℏ²/(2m)ψ'' = Eψ en 0 < x < L
- [ ] Normalización: verificar ∫₀ᴸ |ψₙ|²dx = 1
- [ ] Maxwell integral: verificar que para esfera de radio r con carga Q en centro, ∮E·dA = E(4πr²) = Q/ε₀ → E = Q/(4πε₀r²) ✓
- [ ] Onda EM: verificar c = 1/√(μ₀ε₀) = 1/√(4π×10⁻⁷ × 8.854×10⁻¹²) ≈ 3×10⁸ m/s ✓
- [ ] Maxwell-Boltzmann: verificar v_rms > v_promedio > v_más_probable (√3 > √(8/π) > √2)
