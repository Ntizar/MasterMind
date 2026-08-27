---
name: physics-electrodinamica
description: Electrodinámica: corriente eléctrica, Ley de Ohm, resistencias en serie/paralelo, circuitos, potencia eléctrica, Leyes de Kirchhoff y circuitos RC.
tags: [stem, physics, intermediate]
---

# Electrodinámica

## Corriente eléctrica

- **Intensidad**: I = dQ/dt (A = C/s = Amperio)
- **Densidad de corriente**: J = I/A (A/m²)
- **Velocidad de deriva**: v_d = I/(n·e·A) (típica: mm/s)
- **Sentido convencional**: de + a -. Sentido real de electrones: de - a +

## Ley de Ohm

- V = IR
- R = resistividad·L/A = ρL/A
- ρ = resistividad (Ω·m). Aislantes: ρ alto. Conductores: ρ bajo.
- **Resistividad del cobre**: ρ_Cu ≈ 1,68 × 10⁻⁸ Ω·m (a 20°C)
- **Dependencia con T**: ρ = ρ₀[1 + α(T - T₀)]

## Resistencias

### Asociación en serie
- R_eq = R₁ + R₂ + ... + Rₙ
- Misma corriente por todas
- Misma corriente I

### Asociación en paralelo
- 1/R_eq = 1/R₁ + 1/R₂ + ... + 1/Rₙ
- Misma tensión en todas
- Para dos: R_eq = R₁R₂/(R₁ + R₂)

## Potencia eléctrica

- P = IV = I²R = V²/R (W)
- Energía: E = Pt (J)
- **1 kWh** = 3,6 × 10⁶ J

## Leyes de Kirchhoff

### 1ª Ley (nodos)
ΣI_entrante = ΣI_saliente (conservación de carga)
ΣI = 0 (convención: entrante +, saliente -)

### 2ª Ley (mallas)
ΣV = 0 en cualquier malla cerrada (conservación de energía)
ΣΔV = Σfem

## Medidores

- **Voltímetro**: en paralelo, R → ∞ (ideal)
- **Amperímetro**: en serie, R → 0 (ideal)
- **Ohmímetro**: mide R directamente

## Circuitos RC

### Carga de un condensador
- Q(t) = Q₀(1 - e^(-t/RC))
- V_c(t) = V₀(1 - e^(-t/RC))
- I(t) = I₀·e^(-t/RC)

### Descarga de un condensador
- Q(t) = Q₀·e^(-t/RC)
- V_c(t) = V₀·e^(-t/RC)
- I(t) = -I₀·e^(-t/RC)

### Constante de tiempo
- τ = RC (segundos)
- A t = τ: Q = 0,632·Q₀ (carga) o Q = 0,368·Q₀ (descarga)
- A t = 5τ: carga/descarga ≈ completa (> 99%)

## Circuitos CC vs CA

### Corriente continua (CC/DC)
- V e I constantes en el tiempo
- Análisis con Ohm y Kirchhoff directamente

### Corriente alterna (CA/AC)
- V(t) = V₀sen(ωt), I(t) = I₀sen(ωt + φ)
- Valores eficaces (RMS): V_eff = V₀/√2, I_eff = I₀/√2
- Potencia media: P = V_eff · I_eff · cos(φ)
- cos(φ) = factor de potencia

## Errores comunes / Pitfalls

- **Ohm**: V = IR. Si R = 0 (cortocircuito), V = 0. Si R → ∞ (circuito abierto), I = 0
- **Serie vs paralelo**: en serie la corriente es la misma; en paralelo el voltaje es el mismo
- **Voltímetro**: siempre en paralelo. Si se conecta en serie, mide todo el voltaje (R muy alta)
- **Amperímetro**: siempre en serie. Si se conecta en paralelo, se quema (R muy baja)
- **RC**: τ = RC. A mayor R o C, más lento carga/descarga
- **Potencia**: P = I²R (siempre positiva en resistores). Un resistor SIEMPRE disipa potencia

## Verificación

- [ ] Kirchhoff 1ª: sumar corrientes en un nodo = 0
- [ ] Kirchhoff 2ª: recorrer una malla, suma de voltajes = 0
- [ ] Resistencias: en serie R_eq > R_mayor. En paralelo R_eq < R_menor
- [ ] Potencia: P = IV. Verificar unidades (W)
- [ ] RC: τ = RC. Verificar unidades (Ω·F = s)
