---
name: stem-electronica
description: Electrónica analógica y digital: diodos, transistores BJT/FET, amplificadores operacionales, retroalimentación, filtros, lógica booleana, flip-flops y convertidores A/D.
tags: [stem, engineering, electronics]
---

# Electrónica para Ingeniería

## Referencias de autoridad

- **Sedra & Smith**: Microelectronic Circuits, 8ª edición, Oxford
- **Millman & Halkias**: Electronic Devices and Circuits, 3ª edición, McGraw-Hill
- **Mano & Ciletti**: Digital Design, 6ª edición, Pearson
- **Razavi**: Fundamentals of Microelectronics, 2ª edición, Wiley

## Diodos

### Diodo semiconductor
- **Ecuación de Shockley**: I = I_S(e^(V_D/nV_T) - 1)
- I_S = corriente de saturación inversa
- n = factor de emisión (1-2)
- V_T = kT/q ≈ 26 mV a 300K

### Modelos del diodo
- **Ideal**: V_D = 0 si I > 0, I = 0 si V_D < 0
- **Caída constante**: V_D = V_on (0,7V Si, 0,3V Ge)
- **Modelo lineal**: V_D = V_on + I·r_d

### Rectificadores
- **Media onda**: V_dc = V_p/π, V_r(pp) = V_p (sin filtro)
- **Onda completa centro tap**: V_dc = 2V_p/π
- **Puente de diodos**: V_dc = 2V_p/π (pierde 2V_on)
- **Filtro capacitor**: V_r(pp) ≈ V_p/(fRC) (media onda)
  - V_r(pp) ≈ V_p/(2fRC) (onda completa)

### Diodo Zener
- **Regulación**: V_out ≈ V_Z cuando I_Z > I_Z(min)
- **Resistencia serie**: R = (V_in - V_Z)/I_Z
- **Regulación**: Z_Z = ΔV_Z/ΔI_Z (impedancia dinámica)

## Transistores BJT

### Configuraciones
- **Emisor común (EC)**: alta ganancia de voltaje y corriente
- **Colector común (CC)**: ganancia de voltaje ≈ 1, alta impedancia entrada
- **Base común (BC)**: alta impedancia salida, buena a alta frecuencia

### Polarización EC
- **Divisor de tensión**: R₁, R₂ establecen V_B
- V_B = V_CC·R₂/(R₁ + R₂)
- V_E = V_B - V_BE ≈ V_B - 0,7V
- I_C ≈ I_E = V_E/R_E
- V_CE = V_CC - I_C(R_C + R_E)

### Modelo de pequeño signo
- **g_m** = I_C/V_T = transconductancia
- **r_π** = β/g_m = resistencia base-emisor
- **r_o** = V_A/I_C = resistencia de salida (Early)
- **Ganancia EC**: A_v = -g_m·(R_C || r_o) ≈ -g_m·R_C
- **Ganancia CC (emisor seguidor)**: A_v ≈ 1

### Curva de carga y punto Q
- **Curva de carga DC**: V_CE = V_CC - I_C·R_C
- **Punto Q**: punto de operación en reposo
- **Centro de carga**: V_CEQ = V_CC/2, I_CQ = V_CC/(2R_C)

## Transistores FET

### MOSFET (canal N)
- **Región de corte**: V_GS < V_th → I_D = 0
- **Región lineal (triódica)**: V_GS > V_th, V_DS < V_GS - V_th
  - I_D = k[(V_GS - V_th)V_DS - V_DS²/2]
- **Región de saturación**: V_GS > V_th, V_DS ≥ V_GS - V_th
  - I_D = ½k(V_GS - V_th)²(1 + λV_DS)
  - k = μ_n·C_ox·W/L

### JFET
- **Región de saturación**: I_D = I_DSS(1 - V_GS/V_P)²
- I_DSS = corriente de saturación (V_GS = 0)
- V_P = voltaje de pinch-off

### Amplificador MOSFET EC
- **Ganancia**: A_v = -g_m·(R_D || r_o)
- **Impedancia entrada**: R_in = R_G (muy alta)
- **Impedancia salida**: R_out = R_D || r_o

## Amplificadores operacionales

### Op-amp ideal
- **Ganancia en lazo abierto**: A_OL → ∞
- **Impedancia entrada**: R_in → ∞
- **Impedancia salida**: R_out → 0
- **Ancho de banda**: ∞
- **Offset**: 0

### Configuraciones básicas
- **Inversor**: A_v = -R₂/R₁, R_in = R₁
- **No inversor**: A_v = 1 + R₂/R₁, R_in → ∞
- **Sumador**: V_out = -(R_f/R₁·V₁ + R_f/R₂·V₂ + ...)
- **Diferencial**: V_out = (R₂/R₁)(V₂ - V₁) (si R₂/R₁ = R₄/R₃)
- **Integrador**: V_out = -1/(R₁C)∫V_in dt
- **Derivador**: V_out = -R₁C·dV_in/dt
- **Comparador**: V_out = V_CC si V+ > V-, V_out = -V_CC si V+ < V-

### Retroalimentación
- **Ganancia con feedback**: A_f = A/(1 + Aβ)
- **Ancho de banda con feedback**: BW_f = BW·(1 + Aβ)
- **Principio**: feedback negativo → reduce ganancia pero mejora linealidad y ancho de banda

### Op-amps reales
- **Slew rate**: SR = dV_out/dt|max (V/μs)
- **Offset de entrada**: V_OS (mV)
- **CMRR**: Common Mode Rejection Ratio (dB)
- **GBW**: Gain-Bandwidth Product (MHz)

## Filtros

### Filtros pasivos RC/RL
- **Paso bajo RC**: f_c = 1/(2πRC), A_v = 1/√(1 + (f/f_c)²)
- **Paso alto RC**: f_c = 1/(2πRC), A_v = (f/f_c)/√(1 + (f/f_c)²)

### Filtros activos (Sallen-Key)
- **Paso bajo 2º orden**: A_v = K/(1 - (ω/ω₀)² + jω/(Qω₀))
- **ω₀** = 1/√(R₁R₂C₁C₂)
- **Q** = factor de calidad
- **Butterworth**: Q = 0,707 (resp. plana)
- **Chebyshev**: Q > 0,707 (rippi en banda pasante)
- **Atenuación**: -40 dB/década (2º orden)

### Frecuencias notables
- **Corte**: |A_v| = A_max/√2 = 0,707·A_max (-3 dB)
- **Banda pasante**: entre f_c_low y f_c_high

## Electrónica digital

### Álgebra booleana
- **Leyes**: A + 0 = A, A · 1 = A, A + A' = 1, A · A' = 0
- **De Morgan**: (A + B)' = A' · B', (A · B)' = A' + B'
- **Dualidad**: intercambiar + por · y 0 por 1

### Puertas lógicas
- AND, OR, NOT, NAND, NOR, XOR, XNOR
- **XOR**: A ⊕ B = A·B' + A'·B

### Minimización
- **Mapa de Karnaugh**: 2, 3, 4 variables
- **Quine-McCluskey**: método algebraico sistemático

### Flip-flops
- **SR**: Q(next) = S + R'·Q (R·S = 0)
- **D**: Q(next) = D
- **JK**: Q(next) = J·Q' + K'·Q
- **T**: Q(next) = T ⊕ Q (toggle si T = 1)

### Contadores y registros
- **Contador síncrono**: todos los FF con el mismo reloj
- **Contador asíncrono (ripple)**: clock del siguiente FF = salida del anterior
- **Registro de desplazamiento**: SER, SIPO, PISO, SIPO, PIPPO

### Convertidores
- **A/D (ADC)**:
  - **Flash**: 2ⁿ - 1 comparadores, más rápido
  - **Doble rampa**: precisa, lento
  - **Successive Approximation (SAR)**: equilibrado
  - Resolución: V_ref/2ⁿ
- **D/A (DAC)**:
  - **Red R-2R**: precisa, escalable
  - **Resistencias ponderadas**: simple, limitada resolución
  - Resolución: V_ref/2ⁿ

## Errores comunes / Pitfalls

- **Diodo**: V_on = 0,7V para Si, 0,3V para Ge. No confundir
- **BJT EC**: A_v = -g_m·R_C. El signo negativo indica inversión de fase
- **MOSFET**: en saturación, I_D ∝ (V_GS - V_th)². NO confundir con región lineal
- **Op-amp**: el concepto de "virtual short" (V+ = V-) solo aplica con feedback negativo
- **Filtros**: f_c = 1/(2πRC). No olvidar el 2π
- **ADC**: resolución = V_ref/2ⁿ. Para n = 12, V_ref = 5V: resolución = 1,22 mV

## Verificación

- [ ] Diodo: I = I_S(e^(V_D/nV_T) - 1). Verificar V_T = 26 mV a 300K
- [ ] BJT EC: g_m = I_C/26mV. r_π = β/g_m
- [ ] MOSFET saturación: V_DS ≥ V_GS - V_th
- [ ] Op-amp inversor: A_v = -R₂/R₁. Verificar con R₁ = R₂: A_v = -1
- [ ] Filtro RC: f_c = 1/(2πRC). Verificar: [1/(Ω·F)] = [1/s⁻¹] = Hz ✓
- [ ] ADC: resolución = V_ref/2ⁿ. n = 10, V_ref = 5V: 4,88 mV
