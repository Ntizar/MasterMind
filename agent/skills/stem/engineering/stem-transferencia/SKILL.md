---
name: stem-transferencia
description: Transferencia de calor y masa: conducción (estacionaria/transitoria), convección (forzada/natural), radiación, intercambiadores de calor y coeficientes de transferencia.
tags: [stem, engineering, thermal]
---

# Transferencia de Calor

## Referencias de autoridad

- **Incropera & DeWitt**: Fundamentals of Heat and Mass Transfer, 7ª edición, Wiley
- **Holman**: Heat Transfer, 10ª edición, McGraw-Hill
- **Cengel**: Heat and Mass Transfer, 4ª edición, McGraw-Hill

## Conducción de calor

### Ley de Fourier
- q = -kA·dT/dx (W)
- q'' = q/A = -k·dT/dx (W/m²)
- k = conductividad térmica (W/m·K)

### Pared plana
- **Estacionaria**: q = kA·(T₁ - T₂)/L
- **Resistencia térmica**: R_cond = L/(kA)
- **Red de resistencias**: serie y paralelo como circuitos eléctricos

### Pared compuesta
- **Serie**: R_total = R₁ + R₂ + ... = ΣLᵢ/(kᵢA)
- **Paralelo**: 1/R_total = 1/R₁ + 1/R₂ + ...
- **Convección en superficies**: R_conv = 1/(hA)

### Cilindro y esfera
- **Cilindro**: R_cond = ln(r₂/r₁)/(2πkL)
- **Esfera**: R_cond = (r₂ - r₁)/(4πkr₁r₂)
- **Radio crítico de aislamiento** (cilindro): r_cr = k/h

### Conducción transitoria

#### Capacitancia lumped (Biot < 0,1)
- θ/θ_i = e^(-t/τ)
- τ = ρVc_p/(hA) = R_th·C_th
- Bi = hL_c/k < 0,1 (L_c = V/A)
- **Número de Fourier**: Fo = αt/L_c²

#### Carta de Heisler (Bi > 0,1)
- **Centro de esfera**: θ₀* = f(Fo, Bi)
- **Centro de cilindro**: θ₀* = f(Fo, Bi)
- **Pared plana**: θ₀* = f(Fo, Bi)

### Conducción con generación interna
- **Pared plana**: T(x) = T_s + q'''L²/(2k)[1 - (x/L)²]
- **T máx en el centro**: T_max = T_s + q'''L²/(8k) (pared doblemente aislada)
- **Cilindro**: T_max = T_s + q'''r₂²/(4k)

## Convección

### Ley de enfriamiento de Newton
- q = hA·(T_s - T_∞)
- h = coeficiente de convección (W/m²·K)

### Regímenes de convección
- **Forzada**: fluido movido por medio externo (bombeo, ventilador)
- **Natural**: fluido movido por diferencias de densidad (flotabilidad)
- **Ebullición**: cambio de fase líquido → vapor
- **Condensación**: cambio de fase vapor → líquido

### Capa límite
- **Capa límite térmica**: δ_t ≈ δ/Pr^(1/3)
- **Capa límite de velocidad**: δ
- **Número de Prandtl**: Pr = ν/α = μc_p/k
  - Aire: Pr ≈ 0,7
  - Agua: Pr ≈ 6
  - Aceite: Pr ≈ 100-10000

### Correlaciones típicas

#### Flujo interno (tubería)
- **Re > 10000 (turbulento)**: Dittus-Boelter
  - Nu = 0,023·Re^0,8·Pr^n
  - n = 0,4 (calentamiento), n = 0,3 (enfriamiento)
- **Laminar (Re < 2300)**: Nu = 4,36 (T_s constante), Nu = 4,36 (q constante)
- **Longitud de entrada**: L_turb ≈ 10D, L_lam ≈ 0,05·Re·D

#### Flujo externo (placa plana)
- **Laminar (Re < 5×10⁵)**: Nu_x = 0,332·Re_x^0,5·Pr^(1/3)
- **Turbulento (Re > 5×10⁵)**: Nu_x = 0,0296·Re_x^0,8·Pr^(1/3)
- **Promedio placa completa**: Nu_L = 0,664·Re_L^0,5·Pr^(1/3) (lam.)

#### Número de Nusselt
- Nu = hL/k (adimensional)
- Representa la mejora de transferencia por convección vs conducción

## Radiación

### Ley de Stefan-Boltzmann
- E_b = σT⁴ (W/m²)
- σ = 5,67 × 10⁻⁸ W/(m²·K⁴)
- E = εσT⁴ (superficie real)
- ε = emisividad (0 ≤ ε ≤ 1)

### Intercambio radiativo

#### Superficie gris en recinto grande
- q = εσA(T_s⁴ - T_surr⁴)

#### Dos placas paralelas infinitas
- q = σA(T₁⁴ - T₂⁴)/((1/ε₁) + (1/ε₂) - 1)

#### Dos esferas concéntricas
- q = σA₁(T₁⁴ - T₂⁴)/((1/ε₁) + (1-ε₂)/ε₂·(r₁/r₂)²)

### Factor de vista (view factor)
- F_ij = fracción de energía que sale de i y llega a j
- **Reciprocidad**: A_i·F_ij = A_j·F_ji
- **Suma**: ΣF_ij = 1 (para superficie cerrada)
- **Superficie plana**: F_ii = 0

## Intercambiadores de calor

### Tipos
- **Contracorriente**: mayor ΔT medio, mayor eficiencia
- **Corriente paralela**: menor ΔT medio
- **Cross-flow**: flujo cruzado
- **Tubo y carcasa**: múltiples pasadas

### Método ΔT media logarítmica (LMTD)
- ΔT_lm = (ΔT₁ - ΔT₂)/ln(ΔT₁/ΔT₂)
- q = U·A·ΔT_lm
- **Contracorriente**: ΔT₁ = T_h,in - T_c,out, ΔT₂ = T_h,out - T_c,in
- **Corriente paralela**: ΔT₁ = T_h,in - T_c,in, ΔT₂ = T_h,out - T_c,out

### Método ε-NTU
- **Efectividad**: ε = q/q_max = q/(C_min·(T_h,in - T_c,in))
- **NTU**: NTU = UA/C_min
- **C_max, C_min**: C = ṁ·c_p, C_min = menor de los dos

### Resistencia térmica total
- 1/(UA) = 1/(h_iA_i) + R_foul,i/A_i + R_wall + R_foul,o/A_o + 1/(h_oA_o)

## Errores comunes / Pitfalls

- **Conducción transitoria**: Bi < 0,1 para usar capacitancia lumped. Si no, usar Heisler
- **Radio crítico**: solo aplica a cilindros y esferas, NO a paredes planas
- **Prandtl**: Pr < 1 (metales líquidos), Pr ≈ 1 (gases), Pr > 1 (líquidos)
- **Radiación**: SIEMPRE en Kelvin. T⁴ no se puede linealizar
- **LMTD**: ΔT₁ y ΔT₂ deben ser positivos. Si uno es negativo, usar ε-NTU
- **NTU**: C_min = min(C_h, C_c). Verificar cuál es el mínimo

## Verificación

- [ ] Fourier: q = -kA·dT/dx. Verificar: [W/(m·K)]·[m²]·[K/m] = W ✓
- [ ] Bi = hL_c/k. Verificar: [W/(m²·K)]·[m]/[W/(m·K)] = adimensional ✓
- [ ] Re = ρvD/μ. Verificar: [kg/m³]·[m/s]·[m]/[kg/(m·s)] = adimensional ✓
- [ ] Nu = hL/k. Verificar: [W/(m²·K)]·[m]/[W/(m·K)] = adimensional ✓
- [ ] Stefan-Boltzmann: E = σT⁴. Verificar: [W/(m²·K⁴)]·[K⁴] = W/m² ✓
- [ ] LMTD: ΔT_lm > 0. Si ΔT₁ = ΔT₂, usar ΔT_lm = ΔT₁
