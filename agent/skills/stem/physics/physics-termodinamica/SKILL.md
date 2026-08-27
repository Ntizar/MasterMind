---
name: physics-termodinamica
description: Termodinámica: leyes, gases ideales, ciclos termodinámicos, entropía, trabajo termodinámico, calor y temperatura.
tags: [stem, physics, intermediate]
---

# Termodinámica

## Temperatura y calor

- **Temperatura** (T): K (SI). T(K) = T(°C) + 273,15
- **Calor** (Q): J (SI). Energía en tránsito por diferencia de temperatura
- **Equilibrio térmico**: dos cuerpos en contacto alcanzan la misma temperatura
- **Calor específico**: Q = mcΔT (c en J/(kg·K))
- **Calor latente**: Q = mL (cambio de fase, sin cambio de temperatura)

### Dilatación térmica
- Lineal: ΔL = α·L₀·ΔT
- Superficial: ΔA = 2α·A₀·ΔT
- Volumétrica: ΔV = β·V₀·ΔT ≈ 3α·V₀·ΔT

## Gases ideales

### Ecuación de estado
- PV = nRT = NkT
- R = 8,314 J/(mol·K)
- k = 1,381 × 10⁻²³ J/K (Boltzmann)
- N = n·N_A, N_A = 6,022 × 10²³ (Avogadro)

### Energía interna de gas ideal monoatómico
- U = (3/2)nRT
- U = (f/2)nRT donde f = grados de libertad (3 monoatómico, 5 diatómico)

### Trabajo en transformación de gas ideal
- **Isotérmica** (T constante): W = nRT·ln(V_f/V_i) = nRT·ln(P_i/P_f)
- **Isobárica** (P constante): W = P·ΔV
- **Isocórica** (V constante): W = 0
- **Adiabática** (Q = 0): PV^γ = constante, γ = c_p/c_v

## Primera ley de la termodinámica

- ΔU = Q - W
- ΔU = cambio de energía interna
- Q = calor absorbido por el sistema (+) o cedido (-)
- W = trabajo realizado POR el sistema (+) o sobre el sistema (-)

### Convención de signos
- Q > 0: el sistema absorbe calor
- Q < 0: el sistema cede calor
- W > 0: el sistema realiza trabajo (se expande)
- W < 0: trabajo realizado sobre el sistema (se comprime)

## Segunda ley de la termodinámica

### Enunciado de Kelvin-Planck
Es imposible construir una máquina térmica que, operando en un ciclo, absorba calor de una sola fuente y lo convierta íntegramente en trabajo.

### Enunciado de Clausius
El calor no fluye espontáneamente de un cuerpo frío a uno caliente.

### Entropía
- ΔS = ∫dQ/T (proceso reversible)
- ΔS ≥ 0 para sistemas aislados (segunda ley)
- S = k·ln(W) (Boltzmann, W = número de microestados)

### Máquina de Carnot (máxima eficiencia)
- η_Carnot = 1 - T_fría/T_caliente (T en Kelvin)
- η ≤ η_Carnot para cualquier máquina real
- Ciclo reversible: isoterma + isotermia + isocora + isotermia

## Ciclos termodinámicos

### Ciclo de Carnot
1. Expansión isotérmica (T_caliente)
2. Expansión adiabática
3. Compresión isotérmica (T_fría)
4. Compresión adiabática

### Ciclo Otto (motor de gasolina)
- Compresión adiabática → combustión isocora → expansión adiabática → escape isocora
- η = 1 - (1/r^(γ-1)) donde r = relación de compresión

### Ciclo Diesel
- Compresión adiabática → combustión isobara → expansión adiabática → escape isocora

## Capacidades caloríficas

- c_v = (∂U/∂T)_v (a volumen constante)
- c_p = (∂H/∂T)_p (a presión constante)
- c_p - c_v = R (gas ideal)
- γ = c_p/c_v (monoatómico: γ = 5/3 ≈ 1,67; diatómico: γ = 7/5 = 1,4)

## Errores comunes / Pitfalls

- **Temperatura**: SIEMPRE en Kelvin para ecuaciones de gases y termodinámica
- **Signo del trabajo**: W = PΔV > 0 si el gas se expande (realiza trabajo)
- **Primera ley**: ΔU = Q - W, NO Q + W (depende de la convención. Usar: W = trabajo del sistema)
- **Entropía**: solo aumenta en procesos irreversibles. En Carnot (reversible): ΔS_total = 0
- **Adiabática**: Q = 0, pero ΔU ≠ 0. El gas se enfría al expandirse
- **γ**: monoatómico = 5/3, diatómico = 7/5. No confundir

## Verificación

- [ ] PV = nRT: verificar unidades (Pa·m³ = J)
- [ ] Primera ley: ΔU = Q - W. Verificar signos
- [ ] Carnot: η < 1 siempre. Si T_fría = 0 K: η = 1 (imposible en la práctica)
- [ ] Entropía: ΔS_sistema + ΔS_entorno ≥ 0
- [ ] Calor específico: c_agua = 4186 J/(kg·K) ≈ 1 cal/(g·°C)
