---
name: skill-physics-electromagnetism
version: 1.0.0
category: STEM/Física/Electromagnetismo
description: "Skill integral de Electromagnetismo: Electrostática, Magnetismo, Circuitos eléctricos y Ondas electromagnéticas. Cubre Ley de Coulomb, campo eléctrico, potencial, condensadores, fuerza de Lorentz, inducción de Faraday, circuitos RC/RL/RLC y ecuaciones de Maxwell."
---

# Skill: Física Electromagnetismo

## Descripción

Este skill proporciona las herramientas y conocimiento para resolver problemas de **electromagnetismo** a nivel de bachillerato y primeros cursos universitarios. Cubre cuatro grandes bloques temáticos interconectados:

1. **Electrostática** — Cargas en reposo: campo, potencial y condensadores.
2. **Magnetismo** — Campos magnéticos, fuerza de Lorentz e inducción electromagnética.
3. **Circuitos eléctricos** — Leyes de Ohm y Kirchhoff, circuitos RC, RL y RLC.
4. **Ondas electromagnéticas** — Espectro, propagación y ecuaciones de Maxwell.

## Cuándo usar este skill

- El usuario necesita resolver problemas con cargas eléctricas, campos eléctricos o potenciales.
- Hay problemas de magnetismo, fuerza magnética sobre cargas o corrientes.
- Se requiere analizar circuitos eléctricos (resistencias, capacitores, inductores).
- Hay preguntas sobre ondas electromagnéticas, espectro o ecuaciones de Maxwell.
- El problema combina electrostática con circuitos o magnetismo con inducción.

## Instrucciones paso a paso

### Paso 1: Identificar el bloque temático

Clasifique el problema en uno o más bloques:

| Síntoma | Bloque |
|---|---|
| "carga eléctrica", "campo eléctrico", "potencial", "condensador", "capacitor" | Electrostática |
| "campo magnético", "fuerza magnética", "Lorentz", "inducción", "Faraday" | Magnetismo |
| "circuito", "resistencia", "voltaje", "corriente", "Ohm", "Kirchhoff", "RC", "RL" | Circuitos eléctricos |
| "onda electromagnética", "espectro", "frecuencia", "Maxwell", "longitud de onda" | Ondas electromagnéticas |

### Paso 2: Extraer datos conocidos y desconocidos

Liste explícitamente:
- **Datos conocidos**: valores numéricos con unidades (C, V, A, Ω, T, F, H, Hz, m).
- **Datos desconocidos**: qué se pide calcular.
- **Constantes fundamentales**:
  ```
  k_e = 8.99 × 10⁹ N·m²/C²  (constante de Coulomb)
  ε₀ = 8.854 × 10⁻¹² F/m    (permitividad del vacío)
  μ₀ = 4π × 10⁻⁷ T·m/A      (permeabilidad del vacío)
  e = 1.602 × 10⁻¹⁹ C        (carga elemental)
  c = 3 × 10⁸ m/s            (velocidad de la luz)
  ```

### Paso 3: Seleccionar fórmulas relevantes

#### A) ELECTROSTÁTICA

**Ley de Coulomb:**
```
F = k_e · |q₁·q₂| / r²
F = (1/(4πε₀)) · |q₁·q₂| / r²
```

**Campo eléctrico de una carga puntual:**
```
E = k_e · |q| / r²
E = F / q₀    (campo definido como fuerza por unidad de carga de prueba)
```

**Principio de superposición:**
```
E_total = E₁ + E₂ + E₃ + ...  (suma vectorial)
```

**Potencial eléctrico:**
```
V = k_e · q / r
V = W / q₀
ΔV = -∫E·dl
```

**Energía potencial eléctrica:**
```
U = k_e · q₁ · q₂ / r
U = q·V
```

**Condensadores:**
```
Capacitancia:     C = Q / V
Placas paralelas: C = ε₀·A / d
En serie:          1/C_eq = 1/C₁ + 1/C₂ + ...
En paralelo:        C_eq = C₁ + C₂ + ...
Energía almacenada: U = ½·C·V² = ½·Q²/C = ½·Q·V
```

**Flujo eléctrico y Ley de Gauss:**
```
Φ_E = ∫E·dA = Q_enc / ε₀
```

#### B) MAGNETISMO

**Campo magnético de un hilo recto:**
```
B = (μ₀·I) / (2π·r)
```

**Fuerza de Lorentz sobre una carga:**
```
F = q·v × B
|F| = q·v·B·sin(θ)
```

**Fuerza sobre un hilo con corriente:**
```
F = I·L × B
|F| = I·L·B·sin(θ)
```

**Fuerza entre dos hilos paralelos:**
```
F/L = (μ₀·I₁·I₂) / (2π·d)
```

**Inducción de Faraday:**
```
FEM inducida: ε = -dΦ_B/dt
FEM media:     ε = -ΔΦ_B/Δt
FEM en espira: ε = -N·ΔΦ_B/Δt
```

**Flujo magnético:**
```
Φ_B = B·A·cos(θ)
```

**FEM motriz:**
```
ε = B·L·v    (hilo moviéndose en campo B)
```

**Solenoide:**
```
B = μ₀·n·I    (n = N/L, densidad de espiras)
L = μ₀·N²·A / l    (inductancia)
```

#### C) CIRCUITOS ELÉCTRICOS

**Ley de Ohm:**
```
V = I·R
P = V·I = I²·R = V²/R
```

**Resistencias:**
```
En serie:  R_eq = R₁ + R₂ + ...
En paralelo: 1/R_eq = 1/R₁ + 1/R₂ + ...
```

**Leyes de Kirchhoff:**
```
1ª Ley (nodos):   ΣI_entrante = ΣI_saliente
2ª Ley (mallas):  ΣΔV = 0  (recorriendo una malla cerrada)
```

**Circuitos RC (carga):**
```
q(t) = Q_max·(1 - e^(-t/τ))
I(t) = I₀·e^(-t/τ)
τ = R·C    (constante de tiempo)
Q_max = C·V₀
```

**Circuitos RC (descarga):**
```
q(t) = Q₀·e^(-t/τ)
I(t) = -(Q₀/τ)·e^(-t/τ)
```

**Circuitos RL:**
```
τ = L/R
I(t) = (V/R)·(1 - e^(-t/τ))    (crecimiento)
I(t) = I₀·e^(-t/τ)              (decaimiento)
```

**Circuitos RLC serie (oscilaciones):**
```
ω₀ = 1/√(LC)    (frecuencia natural)
f₀ = 1/(2π√(LC))
Impedancia: Z = √(R² + (X_L - X_C)²)
X_L = ω·L
X_C = 1/(ω·C)
```

**Resonancia en RLC:**
```
ω_res = 1/√(LC)    (cuando X_L = X_C)
Z_min = R    (impedancia mínima en resonancia)
```

#### D) ONDAS ELECTROMAGNÉTICAS

**Relación fundamental:**
```
c = λ·f
λ = c/f
f = c/λ
```

**Energía del fotón:**
```
E = h·f = h·c/λ
h = 6.626 × 10⁻³⁴ J·s
```

**Espectro electromagnético** (de mayor a menor longitud de onda):
```
Ondas de radio > Microondas > Infrarrojo > Visible > Ultravioleta > Rayos X > Rayos gamma
```

**Intensidad y presión de radiación:**
```
I = P/A = ½·ε₀·c·E₀²
p = I/c    (presión de radiación)
```

**Ecuaciones de Maxwell** (forma integral):
```
1. ∮E·dA = Q_enc/ε₀          (Gauss eléctrico)
2. ∮B·dA = 0                  (Gauss magnético)
3. ∮E·dl = -dΦ_B/dt           (Faraday)
4. ∮B·dl = μ₀·I_enc + μ₀·ε₀·dΦ_E/dt  (Ampère-Maxwell)
```

**Velocidad de la luz desde Maxwell:**
```
c = 1/√(μ₀·ε₀) ≈ 3 × 10⁸ m/s
```

### Paso 4: Resolver algebraicamente antes de sustituir

Despejar la incógnita en función de los datos. Solo al final sustituir valores numéricos.

### Paso 5: Verificar unidades y sentido físico

- Verificar que las unidades sean coherentes (SI: C, V, A, Ω, T, F, H, Hz, m).
- Recordar: 1 F = 1 C/V, 1 H = 1 V·s/A, 1 T = 1 N/(A·m).
- En circuitos AC, usar fasores y considerar fase.

## Ejemplos de uso

### Ejemplo 1: Electrostática — Ley de Coulomb
> **Prompt:** "Dos cargas de +3 μC y -5 μC están separadas 0.2 m. Calcular la fuerza entre ellas."

```
Solución paso a paso:
q₁ = 3×10⁻⁶ C, q₂ = -5×10⁻⁶ C, r = 0.2 m

F = k_e·|q₁·q₂|/r² = (8.99×10⁹)·(3×10⁻⁶)·(5×10⁻⁶)/(0.2)²
F = (8.99×10⁹)·(15×10⁻¹²)/0.04 = 3.37 N

La fuerza es atractiva (cargas de signo opuesto).
```

### Ejemplo 2: Circuitos — Ley de Kirchhoff
> **Prompt:** "Un circuito con dos mallas: malla 1 con V₁=12V, R₁=4Ω, R₂=6Ω; malla 2 con V₂=6V, R₂=6Ω, R₃=3Ω. Calcular corrientes."

```
Solución paso a paso:
Malla 1: 12 - 4·I₁ - 6·(I₁ - I₂) = 0 → 10·I₁ - 6·I₂ = 12
Malla 2: 6 - 6·(I₂ - I₁) - 3·I₂ = 0 → -6·I₁ + 9·I₂ = 6

Resolviendo:
I₁ = 1.8 A, I₂ = 1.6 A
I_R2 = I₁ - I₂ = 0.2 A
```

### Ejemplo 3: Magnetismo — Fuerza de Lorentz
> **Prompt:** "Un protón (q = 1.6×10⁻¹⁹ C) se mueve a 2×10⁶ m/s perpendicular a un campo magnético de 0.5 T. Calcular la fuerza y el radio de la trayectoria."

```
Solución paso a paso:
a) F = q·v·B = (1.6×10⁻¹⁹)·(2×10⁶)·(0.5) = 1.6×10⁻¹³ N

b) Trayectoria circular: F_c = F_magnética
   m·v²/r = q·v·B
   r = m·v/(q·B) = (1.67×10⁻²⁷)·(2×10⁶)/((1.6×10⁻¹⁹)·0.5)
   r = 4.18×10⁻² m = 4.18 cm
```

### Ejemplo 4: Circuitos RC — Carga de condensador
> **Prompt:** "Un condensador de 100 μF se carga a través de una resistencia de 10 kΩ con una batería de 12 V. Calcular: a) constante de tiempo, b) carga a t = 1 s, c) corriente inicial."

```
Solución paso a paso:
τ = R·C = 10000·100×10⁻⁶ = 1 s

b) q(1) = C·V₀·(1 - e^(-1/τ)) = 100×10⁻⁶·12·(1 - e⁻¹)
   q(1) = 1.2×10⁻³·(1 - 0.368) = 7.58×10⁻⁴ C = 758 μC

c) I₀ = V₀/R = 12/10000 = 1.2 mA
```

### Ejemplo 5: Ondas electromagnéticas
> **Prompt:** "Una onda de luz tiene longitud de onda 500 nm. Calcular su frecuencia y la energía de cada fotón."

```
Solución paso a paso:
λ = 500 nm = 500×10⁻⁹ m = 5×10⁻⁷ m

f = c/λ = (3×10⁸)/(5×10⁻⁷) = 6×10¹⁴ Hz

E = h·f = (6.626×10⁻³⁴)·(6×10¹⁴) = 3.98×10⁻¹⁹ J
E = 3.98×10⁻¹⁹ / 1.602×10⁻¹⁹ = 2.48 eV
```

### Ejemplo 6: Inducción de Faraday
> **Prompt:** "Una espira circular de radio 0.1 m está en un campo magnético de 0.5 T perpendicular a su plano. Si el campo se anula en 0.02 s, calcular la FEM inducida."

```
Solución paso a paso:
A = π·r² = π·(0.1)² = 0.0314 m²
Φ_inicial = B·A = 0.5·0.0314 = 0.0157 Wb
Φ_final = 0

ε = -ΔΦ/Δt = -(0 - 0.0157)/0.02 = 0.785 V
```

## Referencias cruzadas

Skills STEM existentes que complementan este skill:

| Skill | Ruta | Relación |
|---|---|---|
| `physics-electrostatica` | `/hermes-home/skills/stem/physics/physics-electrostatica` | Electrostática detallada: campo, potencial y problemas adicionales |
| `physics-electrodinamica` | `/hermes-home/skills/stem/physics/physics-electrodinamica` | Electrodinámica avanzada: corrientes, circuitos complejos |
| `physics-magnetismo` | `/hermes-home/skills/stem/physics/physics-magnetismo` | Magnetismo detallado: campos, fuerzas e inducción |
| `physics-ondas-sonido` | `/hermes-home/skills/stem/physics/physics-ondas-sonido` | Ondas mecánicas y sonoras (complementa con ondas EM) |

**Cuándo derivar a otros skills:**
- Problemas de electrostática complejos (distribuciones continuas de carga) → usar `physics-electrostatica`
- Circuitos eléctricos avanzados (AC, impedancia compleja, transformadores) → usar `physics-electrodinamica`
- Magnetismo avanzado (Amperé, Biot-Savart, materiales magnéticos) → usar `physics-magnetismo`
- Ondas sonoras, interferencia, efecto Doppler → usar `physics-ondas-sonido`
- Electromagnetismo de nivel universitario avanzado → combinar con `physics-expert`

## Pitfalls (Errores comunes)

1. **Signo de cargas**: en la Ley de Coulomb, usar valores absolutos para la magnitud y determinar dirección por signos.
2. **Potencial vs campo**: no confundir V (escalar) con E (vectorial). E = -∇V.
3. **Unidades de capacitancia**: 1 μF = 10⁻⁶ F, 1 nF = 10⁻⁹ F, 1 pF = 10⁻¹² F. Error frecuente en potencias de 10.
4. **RC vs RL**: en RC, τ = RC; en RL, τ = L/R. Son dimensionalmente diferentes.
5. **Inducción de Faraday**: el signo negativo (Ley de Lenz) indica que la FEM se opone al cambio de flujo. No ignorarlo en problemas conceptuales.
6. **Resonancia RLC**: en resonancia, X_L = X_C, NO que ambas sean cero. La impedancia es mínima (Z = R), no cero.
7. **Ondas EM**: recordar que E y B están en fase y son perpendiculares entre sí y a la dirección de propagación.
8. **Energía del condensador**: U = ½·C·V², NO U = C·V². El factor ½ es fundamental.
9. **Flujo magnético**: Φ = B·A·cos(θ), donde θ es el ángulo entre B y la normal al área, NO el ángulo con el plano.
10. **Circuitos en paralelo**: la tensión es la misma en todos los elementos en paralelo, no la corriente.

## Fórmulas de referencia rápida

```
ELECTROSTÁTICA:
  Coulomb:        F = k_e·|q₁·q₂|/r²
  Campo:          E = k_e·q/r² = F/q₀
  Potencial:      V = k_e·q/r
  Condensador:    C = Q/V,  C = ε₀·A/d
  En serie:       1/C_eq = Σ(1/C_i)
  En paralelo:     C_eq = ΣC_i
  Energía:         U = ½·C·V² = ½·Q²/C

MAGNETISMO:
  Hilo recto:     B = μ₀·I/(2π·r)
  Lorentz:        F = q·v×B
  Hilo corriente: F = I·L×B
  Inducción:      ε = -dΦ_B/dt
  Solenoide:      B = μ₀·n·I
  Inductancia:    L = μ₀·N²·A/l

CIRCUITOS:
  Ohm:            V = I·R,  P = V·I = I²·R
  Serie:          R_eq = ΣR_i
  Paralelo:       1/R_eq = Σ(1/R_i)
  RC carga:       q(t) = CV₀(1-e^(-t/RC))
  RC descarga:    q(t) = Q₀e^(-t/RC)
  RL:             I(t) = (V/R)(1-e^(-tR/L))
  RLC:            Z = √(R²+(X_L-X_C)²), ω₀=1/√(LC)

ONDAS EM:
  c = λ·f
  E = h·f = h·c/λ
  c = 1/√(μ₀·ε₀)
```

## Notas de implementación para el agente

- Siempre verificar las unidades antes de sustituir (especialmente μ, n, p en capacitancias).
- Para problemas de circuitos, dibujar el circuito y etiquetar corrientes y tensiones.
- En problemas de inducción, aplicar la Ley de Lenz para determinar el sentido de la corriente inducida.
- Para circuitos AC, usar fasores y considerar la fase relativa.
- En ondas EM, recordar que E_max = c·B_max.
- Para problemas de nivel avanzado, derivar de las ecuaciones de Maxwell cuando sea necesario.
- Usar `physics-electrostatica`, `physics-electrodinamica` y `physics-magnetismo` como skills de apoyo para problemas específicos.
