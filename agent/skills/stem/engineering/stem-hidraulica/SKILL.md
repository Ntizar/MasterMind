---
name: stem-hidraulica
description: Hidráulica e hidráulica de tuberías: ecuación de Bernoulli, pérdida de carga, Darcy-Weisbach, Moody, bombas, caudal, régimen de flujo y redes de tuberías.
tags: [stem, engineering, fluid]
---

# Hidráulica e Ingeniería de Fluidos

## Referencias de autoridad

- **White**: Fluid Mechanics, 8ª edición, McGraw-Hill
- **Munson**: Fundamentals of Fluid Mechanics, 8ª edición, Wiley
- **Fox & McDonald**: Introduction to Fluid Mechanics, 9ª edición, Wiley
- **CEDEX**: Manual de Canalización, España

## Ecuaciones fundamentales

### Ecuación de continuidad
- ρ₁A₁v₁ = ρ₂A₂v₂ (conservación de masa)
- A₁v₁ = A₂v₂ (incompresible)
- Q = Av (caudal volumétrico)

### Ecuación de Bernoulli
- P₁/ρg + v₁²/2g + z₁ = P₂/ρg + v₂²/2g + z₂ + h_p - h_t - h_L
- **Carga de presión**: P/ρg (m)
- **Carga cinética**: v²/2g (m)
- **Carga de posición**: z (m)
- **h_p**: carga añadida por bomba (m)
- **h_t**: carga extraída por turbina (m)
- **h_L**: pérdidas de carga (m)

### Ecuación de energía (forma general)
- P₁/γ + α₁v₁²/2g + z₁ + h_bomba = P₂/γ + α₂v₂²/2g + z₂ + h_turbina + h_pérdidas
- α = coeficiente de Coriolis (α = 2 laminar, α ≈ 1 turbulento)

## Pérdidas de carga

### Pérdidas primarias (fricción en tuberías)
- **Darcy-Weisbach**: h_f = f·(L/D)·(v²/2g)
- **f** = factor de fricción (Moody chart)
- **Laminar**: f = 64/Re
- **Turbulento**: Colebrook-White: 1/√f = -2log₁₀(ε/3,7D + 2,51/(Re√f))
- **Swamee-Jain** (explícita): f = 0,25/[log₁₀(ε/3,7D + 5,74/Re^0,9)]²

### Pérdidas secundarias (accidentes)
- h_m = K·(v²/2g)
- **K valores típicos**:
  - Codo 90° estándar: K ≈ 0,9
  - Codo 90° largo: K ≈ 0,2
  - Válvula de bola abierta: K ≈ 0,05
  - Válvula de globo abierta: K ≈ 10
  - Entrada brusca: K ≈ 0,5
  - Entrada suave: K ≈ 0,04
  - Salida: K = 1,0
  - Contracción brusca: K ≈ 0,5(1 - A₂/A₁)
  - Expansión brusca: K = (1 - A₁/A₂)²

### Longitud equivalente
- L_eq = K·D/f
- Representa la longitud de tubería recta que produce la misma pérdida

## Número de Reynolds y regímenes

### Cálculo
- Re = ρvD/μ = vD/ν
- ν = viscosidad cinemática (m²/s)
- **Laminar**: Re < 2300
- **Transición**: 2300 < Re < 4000
- **Turbulento**: Re > 4000

### Viscosidades típicas (20°C)
- **Agua**: ν = 1,004 × 10⁻⁶ m²/s
- **Aire**: ν = 1,51 × 10⁻⁵ m²/s
- **Aceite SAE 30**: ν ≈ 1,0 × 10⁻⁴ m²/s

## Bombas

### Parámetros de bomba
- **Caudal**: Q (m³/s o l/s)
- **Altura manométrica**: H (m)
- **Potencia hidráulica**: P_h = γQH = ρgQH (W)
- **Potencia al eje**: P_e = P_h/η = ρgQH/η
- **RPM**: velocidad de rotación (rpm)
- **NPSH**: Net Positive Suction Head (m)

### Curva característica
- H = H₀ - aQ² (parábola típica)
- **Punto de operación**: intersección curva bomba-curva sistema

### Curva del sistema
- H_sistema = Δz + h_f + h_m
- H_sistema = Δz + K_total·Q²

### NPSH disponible vs requerido
- NPSH_disponible = P_atm/γ + z_succión - h_f_succión - P_vapor/γ
- NPSH_disponible > NPSH_requerido + margen (0,5-1 m)

### Similitud de bombas
- Q₁/Q₂ = (n₁/n₂)·(D₁/D₂)³
- H₁/H₂ = (n₁/n₂)²·(D₁/D₂)²
- P₁/P₂ = (ρ₁/ρ₂)·(n₁/n₂)³·(D₁/D₂)⁵

## Redes de tuberías

### Tipos de redes
- **En serie**: Q₁ = Q₂ = Q₃, h_L_total = h_L₁ + h_L₂ + h_L₃
- **En paralelo**: h_L₁ = h_L₂ = h_L₃, Q_total = Q₁ + Q₂
- **Ramificada**: ley de Kirchhoff: ΣQ_nodo = 0

### Método de Hardy Cross
- **Iterativo**: corregir caudales hasta equilibrar pérdidas en cada lazo
- ΔQ = -Σh_f / (5Σh_f/Q) (para tubería circular, f ≈ cte)

### Tuberías equivalentes
- **Serie**: L_eq = ΣLᵢ·(D/Dᵢ)^5
- **Paralelo**: 1/√f_eq·(L_eq/D_eq)^0,5 = Σ1/√fᵢ·(Lᵢ/Dᵢ)^0,5

## Canal abierto

### Flujo uniforme (Manning)
- v = (1/n)·R^(2/3)·S^(1/2) (SI)
- Q = Av = (A/n)·R^(2/3)·S^(1/2)
- n = coeficiente de Manning
- R = A/P (radio hidráulico)
- S = pendiente del fondo

### Números adimensionales
- **Froude**: Fr = v/√(gD_h)
  - Fr < 1: subcrítico (tranquilo)
  - Fr = 1: crítico
  - Fr > 1: supersónico (rápido)
- **Energía específica**: E = y + v²/2g

### Profundidad crítica
- Q²T/g = A³ (condición crítica)
- Para canal rectangular: y_c = (q²/g)^(1/3), q = Q/b

## Errores comunes / Pitfalls

- **Bernoulli**: incluir TODAS las pérdidas (primarias + secundarias)
- **Darcy-Weisbach**: f depende de Re y rugosidad. No usar f = 0,02 por defecto sin verificar
- **Colebrook-White**: ecuación implícita. Usar Swamee-Jain o iteración de Newton
- **NPSH**: calcular SIEMPRE en el punto más desfavorable (máxima temperatura, máxima altura de succión)
- **Manning**: solo para flujo en canal abierto, NO para tuberías a presión
- **Re**: verificar si es laminar o turbulento antes de elegir fórmula de f

## Verificación

- [ ] Bernoulli: todos los términos en metros (carga)
- [ ] Darcy-Weisbach: h_f = f·(L/D)·(v²/2g). Verificar: [adimensional]·[m/m]·[m²/s²]/[m/s²] = m ✓
- [ ] Re: Re = vD/ν. Verificar: [m/s]·[m]/[m²/s] = adimensional ✓
- [ ] Manning: Q = (A/n)·R^(2/3)·S^(1/2). Verificar unidades SI
- [ ] Potencia bomba: P = ρgQH/η. Verificar: [kg/m³]·[m/s²]·[m³/s]·[m] = W ✓
