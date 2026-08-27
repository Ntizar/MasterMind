---
name: physics-electrostatica
description: Electroestática: Ley de Coulomb, campo eléctrico, potencial, ley de Gauss, capacitancia, dieléctricos y energía electrostática.
tags: [stem, physics, intermediate]
---

# Electroestática

## Carga eléctrica

- Carga elemental: e = 1,602 × 10⁻¹⁹ C
- Conservación de la carga: no se crea ni destruye, solo se transfiere
- Cuantización: q = ±n·e
- Unidad: Coulomb (C)

## Ley de Coulomb

- F⃗ = k·q₁·q₂·r̂ / r²
- k = 1/(4πε₀) = 8,988 × 10⁹ N·m²/C²
- ε₀ = 8,854 × 10⁻¹² C²/(N·m²) (permitividad del vacío)
- F > 0: repulsión (cargas del mismo signo)
- F < 0: atracción (cargas opuestas)

## Campo eléctrico

- E⃗ = F⃗/q₀ (campo producido sobre una carga testigo q₀)
- E⃗ = k·q·r̂/r² (carga puntual)
- **Líneas de campo**: salen de cargas positivas, entran en negativas
- **Superposición**: E⃗_total = ΣE⃗ᵢ

### Campos notables
- **Dipolo eléctrico**: E ∝ 1/r³ (lejos del dipolo)
- **Anillo cargado**: E en el eje = k·Q·z / (R² + z²)^(3/2)
- **Plano infinito uniformemente cargado**: E = σ/(2ε₀) (constante)

## Potencial eléctrico

- V(r) = k·q/r (carga puntual, V = 0 en ∞)
- ΔV = -∫E⃗ · dr⃗
- V en voltios (V = J/C)
- **Diferencia de potencial**: V_AB = V_B - V_A = W_AB / q

### Relación campo-potencial
- E⃗ = -∇V
- E_x = -∂V/∂x, E_y = -∂V/∂y, E_z = -∂V/∂z
- En campo uniforme: E = -ΔV/d

## Energía potencial electrostática

- U = q·V (para una carga en un potencial V)
- U = k·q₁·q₂/r (para dos cargas)
- U_tot = ½Σqᵢ·Vᵢ (para un sistema de cargas)

## Ley de Gauss

- Φ_E = ∮E⃗ · dA⃗ = Q_encerrada / ε₀
- **Aplicaciones** (elegir superficie gaussiana con simetría):
  - Esfera cargada (simetría esférica): E = k·Q/r² (fuera), E = 0 (dentro, esfera conductora)
  - Cilindro infinito: E = λ/(2πε₀r)
  - Plano infinito: E = σ/(2ε₀)

## Conductores en equilibrio electrostático

- E = 0 en el interior del conductor
- Toda la carga en la superficie
- Potencial constante en toda la superficie del conductor
- E justo fuera = σ·n̂/ε₀

## Capacitancia y condensadores

- **Capacitancia**: C = Q/V (F = C/V = faradios)
- **Condensador de placas paralelas**: C = ε₀·A/d
- **Condensador esférico**: C = 4πε₀·r₁r₂/(r₂ - r₁)
- **Energía almacenada**: U = ½QV = ½CV² = ½Q²/C

### Asociación de condensadores
- **Serie**: 1/C_eq = 1/C₁ + 1/C₂ + ... (Q igual en todos)
- **Paralelo**: C_eq = C₁ + C₂ + ... (V igual en todos)

## Dieléctricos

- C = κ·C₀ (κ = constante dieléctrica)
- ε = κ·ε₀ (permitividad del medio)
- El dieléctrico aumenta la capacidad y reduce el campo

## Errores comunes / Pitfalls

- **Signo de la carga**: F = k·q₁·q₂/r². Cargas del mismo signo se repelen
- **Campo vs potencial**: E es vector, V es escalar. Diferencia fundamental
- **Gauss**: solo útil para simetrías simple (esférica, cilíndrica, plana)
- **Coulomb**: r es la distancia entre las cargas, no la posición absoluta
- **Energía del condensador**: U = ½CV². NO confundir con la energía de una carga puntual
- **Dieléctrico**: κ > 1 en materiales (vacío: κ = 1)

## Verificación

- [ ] Coulomb: F ∝ 1/r². Si r se duplica, F se divide por 4
- [ ] Campo de carga puntual: E ∝ 1/r² (inverso cuadrado)
- [ ] Gauss: Φ_E en N·m²/C = Q_enc/ε₀
- [ ] Capacitancia: C en F, V en V, Q en C → Q = CV
- [ ] Energía: U = ½CV². Verificar que U ≥ 0
