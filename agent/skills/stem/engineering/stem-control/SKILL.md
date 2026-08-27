---
name: stem-control
description: Teoría de control: modelos en dominio del tiempo y frecuencia, función de transferencia, respuesta transitoria, estabilidad (Routh, Nyquist, Bode), compensadores y control PID.
tags: [stem, engineering, control]
---

# Teoría de Control

## Referencias de autoridad

- **Ogata**: Modern Control Engineering, 5ª edición, Prentice Hall
- **Katsuhiko**: Control Systems Engineering, 7ª edición, Wiley
- **Nise**: Control Systems Engineering, 7ª edición, Wiley
- **Franklin**: Feedback Control of Dynamic Systems, 7ª edición, Pearson

## Modelado en dominio del tiempo

### Ecuación diferencial lineal
- aₙy⁽ⁿ⁾ + ... + a₁y' + a₀y = bₘu⁽ᵐ⁾ + ... + b₁u' + b₀u
- **Lineal**: cumple superposición y homogeneidad
- **Invariantes en el tiempo**: coeficientes constantes

### Función de transferencia
- G(s) = Y(s)/U(s) = B(s)/A(s) (condiciones iniciales = 0)
- **Polos**: raíces de A(s) = 0
- **Ceros**: raíces de B(s) = 0
- **Orden**: grado máximo de A(s)

### Diagrama de bloques

#### Elementos básicos
- **Bloque**: G(s)
- **Sumador**: ±
- **Take-off point**: señal se divide sin alterar

#### Reglas de simplificación
- **Cascada**: G₁(s)·G₂(s)
- **Paralelo**: G₁(s) ± G₂(s)
- **Feedback negativo**: G/(1 + GH)
- **Feedback positivo**: G/(1 - GH)
- **Mover sumador**: cruzar bloque = multiplicar por G o 1/G

#### Ganancia en lazo cerrado
- T(s) = G(s)/(1 + G(s)H(s))
- **Lazo abierto**: G(s)
- **Error**: E(s) = U(s) - H(s)Y(s)

### Respuesta transitoria (1º orden)

#### Sistema de primer orden
- τy' + y = Ku(t)
- **Respuesta a escalón**: y(t) = K(1 - e^(-t/τ))
- **Constante de tiempo**: τ
  - t = τ: y = 0,632·K
  - t = 4τ: y = 0,982·K (~98%)
- **Tiempo de establecimiento**: t_s ≈ 4τ (±2%)

#### Sistema de segundo orden
- s² + 2ζωₙs + ωₙ² = 0
- **ωₙ** = frecuencia natural (rad/s)
- **ζ** = factor de amortiguamiento (adimensional)
- **Polos**: s = -ζωₙ ± ωₙ√(ζ² - 1)

##### Casos de ζ:
- **ζ = 0**: oscilación sostenida (polos imaginarios puros)
- **0 < ζ < 1**: subamortiguado (polos complejos conjugados)
- **ζ = 1**: críticamente amortiguado (polos reales iguales)
- **ζ > 1**: sobreamortiguado (polos reales distintos)

##### Respuesta a escalón (0 < ζ < 1):
- **Tiempo de subida** (10%-90%): t_r ≈ 1,8/ωₙ
- **Tiempo pico**: t_p = π/(ωₙ√(1-ζ²)) = π/ω_d
- **Sobrepaso máximo**: MP = e^(-ζπ/√(1-ζ²)) × 100%
- **Tiempo de establecimiento** (±2%): t_s ≈ 4/(ζωₙ)
- **Frecuencia oscilatoria**: ω_d = ωₙ√(1-ζ²)

## Estabilidad

### Criterio de Routh-Hurwitz
- **Condición necesaria**: todos los coeficientes ≠ 0 y mismo signo
- **Tabla de Routh**:
  - Primera fila: coeficientes pares
  - Segunda fila: coeficientes impares
  - Filas siguientes: se calculan con determinantes
- **Número de cambios de signo en 1ª columna** = número de polos en RHP

### Estabilidad relativa
- **Margen de ganancia**: cuánto se puede aumentar K antes de inestabilidad
- **Margen de fase**: cuánto se puede retrasar la fase antes de inestabilidad

## Análisis en frecuencia

### Respuesta frecuencial
- G(jω) = |G(jω)|∠G(jω)
- **Módulo**: |G(jω)| = √(Re² + Im²)
- **Fase**: ∠G(jω) = arctan(Im/Re)

### Diagramas de Bode

#### Magnitud (dB)
- 20log₁₀|G(jω)|
- **Polo en origen**: -20 dB/década
- **Cero en origen**: +20 dB/década
- **Polo real**: -20 dB/década después de ω_c
- **Cero real**: +20 dB/década después de ω_c

#### Fase
- **Polo en origen**: -90°
- **Polo real**: 0° a -90° (centrado en ω_c)
- **Cero real**: 0° a +90° (centrado en ω_c)

### Márgenes de estabilidad
- **ω_gc** (corte de ganancia): |G(jω_gc)H(jω_gc)| = 1 (0 dB)
- **ω_pc** (corte de fase): ∠G(jω_pc)H(jω_pc) = -180°
- **Margen de ganancia**: GM = 1/|G(jω_pc)H(jω_pc)|
- **Margen de fase**: PM = 180° + ∠G(jω_gc)H(jω_gc)
- **Estable**: PM > 0° y GM > 1

### Diagrama de Nyquist
- **Criterio de Nyquist**: Z = N + P
  - Z = número de polos en RHP del sistema en lazo cerrado
  - N = número de giros horarios alrededor de -1
  - P = número de polos en RHP del sistema en lazo abierto
- **Estable**: Z = 0

## Compensación

### Compensador PID
- **P**: K_p. Reduce error en estado estacionario pero no lo elimina
- **I**: K_i/s. Elimina error en estado estacionario, pero reduce estabilidad
- **D**: K_d·s. Mejora estabilidad y respuesta transitoria
- **G_c(s) = K_p + K_i/s + K_d·s**

#### Efectos:
- **P**: ↑ ganancia, ↓ margen de fase
- **I**: ↓ estabilidad, elimina error estacionario
- **D**: ↑ estabilidad, reduce sobrepaso, ↑ velocidad de respuesta

### Compensador lead (anticipador)
- Mejora margen de fase y velocidad de respuesta
- G_c(s) = K·(s + z)/(s + p) con z < p
- **Máximo avance de fase**: φ_max = arcsen((p-z)/(p+z))
- Se coloca en ω_max ≈ √(zp)

### Compensador lag (retardador)
- Mejora error en estado estacionario sin afectar mucho la estabilidad
- G_c(s) = K·(s + z)/(s + p) con z > p
- **Atenuación**: 20log(p/z)
- Se coloca muy por debajo de ω_gc

### Compensador lead-lag
- Combina ambos: mejora transitoria y error estacionario

## Errores comunes / Pitfalls

- **Función de transferencia**: solo válida con condiciones iniciales = 0
- **Routh**: si hay un cero en la primera fila, usar ε → 0
- **Bode**: el polo real cambia fase de 0° a -90°, NO de -90° a 0°
- **Nyquist**: contar giros HORARIOS como positivos
- **PID**: el derivador puro amplifica ruido. Usar D con filtro: K_d·s/(1 + s/N)
- **Margen de fase**: PM > 45° es recomendable para buena estabilidad

## Verificación

- [ ] Función de transferencia: verificar condiciones iniciales = 0
- [ ] Routh: si todos los coeficientes tienen mismo signo, posible estabilidad
- [ ] Bode: cada polo real aporta -20 dB/década y -90° de fase
- [ ] Nyquist: Z = N + P. Estable si Z = 0
- [ ] PID: I elimina error estacionario, D mejora estabilidad
- [ ] Sobrepaso: MP = e^(-ζπ/√(1-ζ²)). Verificar con ζ = 0,5: MP ≈ 16%
