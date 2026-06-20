---
name: skill-physics-mechanics
version: 1.0.0
category: STEM/Física/Mecánica
description: "Skill integral de Mecánica clásica: Cinemática, Dinámica, Termodinámica y Trabajo-Energía. Cubre MRU, MRUA, MCU, caída libre, tiro parabólico, leyes de Newton, rozamiento, poleas, gases ideales, calorimetría y conservación de energía."
---

# Skill: Física Mecánica (Mecánica Clásica)

## Descripción

Este skill proporciona las herramientas y conocimiento para resolver problemas de **mecánica clásica** a nivel de bachillerato y primeros cursos universitarios. Cubre cuatro grandes bloques temáticos interconectados:

1. **Cinemática** — Descripción del movimiento sin considerar sus causas.
2. **Dinámica** — Estudio de las causas del movimiento (fuerzas).
3. **Termodinámica** — Calor, temperatura, gases ideales y ciclos termodinámicos.
4. **Trabajo y Energía** — Relaciones entre fuerza, desplazamiento y formas de energía.

## Cuándo usar este skill

- El usuario necesita resolver problemas de movimiento (trayectorias, velocidades, aceleraciones).
- Se requiere analizar fuerzas en sistemas en equilibrio o acelerados.
- Hay problemas de calor, temperatura, gases o eficiencia térmica.
- Se pide calcular trabajo, energía cinética/potencial, potencia o conservación de energía.
- El problema combina conceptos de más de un bloque (ej. caída libre + conservación de energía).

## Instrucciones paso a paso

### Paso 1: Identificar el bloque temático

Clasifique el problema en uno o más bloques:

| Síntoma | Bloque |
|---|---|
| "velocidad", "posición", "trayectoria", "tiempo de vuelo" | Cinemática |
| "fuerza", "masa", "aceleración", "rozamiento", "polea" | Dinámica |
| "calor", "temperatura", "gas", "presión", "ciclo" | Termodinámica |
| "trabajo", "energía cinética", "potencial", "conservación", "potencia" | Trabajo y Energía |

### Paso 2: Extraer datos conocidos y desconocidos

Liste explícitamente:
- **Datos conocidos**: valores numéricos con unidades.
- **Datos desconocidos**: qué se pide calcular.
- **Suposiciones implícitas**: "parte del reposo" → v₀ = 0, "sin rozamiento" → μ = 0.

### Paso 3: Seleccionar fórmulas relevantes

#### A) CINEMÁTICA

**MRU (Movimiento Rectilíneo Uniforme):**
```
x = x₀ + v·t          (v = constante)
```

**MRUA (Movimiento Rectilíneo Uniformemente Acelerado):**
```
x = x₀ + v₀·t + ½·a·t²
v = v₀ + a·t
v² = v₀² + 2·a·(x - x₀)
```

**Caída libre** (caso particular de MRUA con a = g = 9.81 m/s²):
```
y = y₀ + v₀·t - ½·g·t²
v = v₀ - g·t
```

**MCU (Movimiento Circular Uniforme):**
```
v = ω·r
a_c = v²/r = ω²·r
T = 2π/ω = 2π·r/v
f = 1/T
```

**Tiro parabólico** (descomponer en x e y):
```
x = v₀·cos(θ)·t
y = y₀ + v₀·sin(θ)·t - ½·g·t²
Alcance máximo: R = v₀²·sin(2θ)/g      (y₀ = 0)
Altura máxima: H = v₀²·sin²(θ)/(2g)   (y₀ = 0)
```

#### B) DINÁMICA

**1ª Ley de Newton (Inercia):** Si ΣF = 0 → v = constante.

**2ª Ley de Newton:**
```
ΣF = m·a
```

**3ª Ley de Newton:** Toda acción tiene una reacción igual y opuesta.

**Fuerzas comunes:**
```
Peso:           P = m·g
Rozamiento:     F_r = μ·N
Elasticidad:    F = -k·x  (Ley de Hooke)
Tensión en polea: misma en todo el hilo ideal
```

**Diagrama de cuerpo libre:**
1. Aislar el cuerpo.
2. Dibujar TODAS las fuerzas que actúan sobre él.
3. Elegir sistema de ejes.
4. Descomponer fuerzas en ejes.
5. Aplicar ΣF_x = m·a_x y ΣF_y = m·a_y.

#### C) TERMODINÁMICA

**Ley de los gases ideales:**
```
P·V = n·R·T
R = 8.314 J/(mol·K)
```

**Calorimetría:**
```
Q = m·c·ΔT           (calor sensible)
Q = m·L              (calor latente)
Q = m·c_vapor·ΔT + m·L_vaporización   (cambios de estado)
```

**1ª Ley de la Termodinámica:**
```
ΔU = Q - W
```

**Ciclos termodinámicos:**
```
Rendimiento motor: η = W_neto / Q_entrante = 1 - Q_saliente/Q_entrante
Rendimiento Carnot: η = 1 - T_fría/T_caliente
```

#### D) TRABAJO Y ENERGÍA

**Trabajo:**
```
W = F·d·cos(α)
```

**Energía cinética:**
```
E_c = ½·m·v²
```

**Energía potencial gravitatoria:**
```
E_p = m·g·h
```

**Energía potencial elástica:**
```
E_pe = ½·k·x²
```

**Conservación de la energía mecánica** (sin rozamiento):
```
E_mech_inicial = E_mech_final
½·m·v₁² + m·g·h₁ = ½·m·v₂² + m·g·h₂
```

**Con rozamiento:**
```
E_inicial + W_rozamiento = E_final
```

**Potencia:**
```
P = W/t = F·v
```

### Paso 4: Resolver algebraicamente antes de sustituir

Despejar la incógnita en función de los datos. Solo al final sustituir valores numéricos.

### Paso 5: Verificar unidades y sentido físico

- Verificar que las unidades sean coherentes (SI: kg, m, s, N, J, W, Pa, K).
- El resultado debe tener sentido físico (velocidades < c, energías positivas donde corresponda, etc.).

## Ejemplos de uso

### Ejemplo 1: Cinemática — Tiro parabólico
> **Prompt:** "Un proyectil se lanza con velocidad inicial de 50 m/s a un ángulo de 30° sobre la horizontal. Calcular: a) tiempo de vuelo, b) altura máxima, c) alcance horizontal."

```
Solución paso a paso:
v₀ = 50 m/s, θ = 30°, g = 9.81 m/s²

a) Tiempo de vuelo: T = 2·v₀·sin(θ)/g = 2·50·0.5/9.81 = 5.10 s
b) Altura máxima: H = v₀²·sin²(θ)/(2g) = 2500·0.25/(2·9.81) = 31.85 m
c) Alcance: R = v₀²·sin(2θ)/g = 2500·sin(60°)/9.81 = 220.93 m
```

### Ejemplo 2: Dinámica — Sistema de poleas
> **Prompt:** "Dos bloques de 5 kg y 3 kg están conectados por una cuerda que pasa por una polea sin fricción. Calcular la aceleración del sistema y la tensión en la cuerda."

```
Solución paso a paso:
m₁ = 5 kg, m₂ = 3 kg, g = 9.81 m/s²

Ecuaciones:
m₁·g - T = m₁·a
T - m₂·g = m₂·a

Sumando: (m₁ - m₂)·g = (m₁ + m₂)·a
a = (m₁ - m₂)·g/(m₁ + m₂) = 2·9.81/8 = 2.45 m/s²

T = m₂·(g + a) = 3·(9.81 + 2.45) = 36.78 N
```

### Ejemplo 3: Trabajo y Energía — Conservación
> **Prompt:** "Un bloque de 2 kg desliza sin fricción desde una altura de 10 m. Calcular su velocidad al llegar al suelo."

```
Solución paso a paso:
E_p_inicial = E_c_final
m·g·h = ½·m·v²
v = √(2·g·h) = √(2·9.81·10) = 14.0 m/s
```

### Ejemplo 4: Termodinámica — Gases ideales
> **Prompt:** "Un gas ideal ocupa 2 L a 300 K y 2 atm. Si se calienta a 600 K manteniendo el volumen constante, ¿cuál es la nueva presión?"

```
Solución paso a paso:
Proceso isocórico: P₁/T₁ = P₂/T₂
P₂ = P₁·T₂/T₁ = 2·600/300 = 4 atm
```

### Ejemplo 5: Problema combinado
> **Prompt:** "Un coche de 1000 kg frena desde 30 m/s hasta detenerse en 50 m. Calcular: a) la fuerza de frenado, b) el trabajo realizado, c) la potencia media si la frenada dura 3.33 s."

```
a) v² = v₀² + 2·a·d → 0 = 900 + 2·a·50 → a = -9 m/s²
   F = m·a = 1000·(-9) = -9000 N

b) W = F·d = -9000·50 = -450,000 J

c) P = W/t = -450,000/3.33 = -135,135 W ≈ -135 kW
```

## Referencias cruzadas

Skills STEM existentes que complementan este skill:

| Skill | Ruta | Relación |
|---|---|---|
| `physics-cinematica` | `/hermes-home/skills/stem/physics/physics-cinematica` | Cinemática detallada con problemas adicionales |
| `physics-dinamica` | `/hermes-home/skills/stem/physics/physics-dinamica` | Análisis de fuerzas y diagramas de cuerpo libre |
| `physics-energia-trabajo` | `/hermes-home/skills/stem/physics/physics-energia-trabajo` | Trabajo, energía y potencia con ejercicios |
| `physics-fluidos` | `/hermes-home/skills/stem/physics/physics-fluidos` | Hidrostática, hidrodinámica, principio de Pascal y Arquímedes |
| `physics-termodinamica` | `/hermes-home/skills/stem/physics/physics-termodinamica` | Termodinámica avanzada: entropía, ciclos, leyes |
| `physics-expert` | `/hermes-home/skills/stem/physics/physics-expert` | Problemas de mecánica avanzada y resolución experta |

**Cuándo derivar a otros skills:**
- Problemas de fluidos → usar `physics-fluidos`
- Termodinámica avanzada (entropía, ciclos complejos) → usar `physics-termodinamica`
- Problemas de dinámica complejos con múltiples cuerpos → usar `physics-dinamica`
- Problemas de energía avanzados con rozamiento variable → usar `physics-energia-trabajo`
- Problemas de cinemática avanzada (movimiento relativo, coordenadas polares) → usar `physics-cinematica`
- Problemas de nivel olímpico o universitario avanzado → usar `physics-expert`

## Pitfalls (Errores comunes)

1. **Olvidar convertir unidades**: °C a K en termodinámica (T[K] = T[°C] + 273.15), km/h a m/s, cm a m, etc.
2. **Confender ángulos**: en tiro parabólico, usar radianes vs grados en calculadora. Verificar siempre.
3. **Signos en caída libre**: definir convención de signos clara (+↑ o +↓) y mantenerla en todo el problema.
4. **Rozamiento estático vs dinámico**: μ_s ≠ μ_d. El rozamiento estático es una cota máxima: F_r ≤ μ_s·N.
5. **Poleas**: no olvidar que en poleas dobles la tensión se distribuye diferente y el desplazamiento se multiplica.
6. **Conservación de energía con rozamiento**: W_rozamiento = -F_r·d (trabajo negativo). No olvidar el signo.
7. **Gases ideales**: usar SI (Pa, m³, K) o ser consistente con las unidades de R.
8. **MCU**: confundir velocidad angular (rad/s) con frecuencia (Hz). ω = 2πf.
9. **Tiro parabólico**: el tiempo de subida = tiempo de bajada SOLO si y₀ = y_final.
10. **Trabajo de fuerza variable**: W = ∫F·dx, no W = F·d (solo vale para fuerza constante).

## Fórmulas de referencia rápida

```
CINEMÁTICA:
  MRU:          x = x₀ + v·t
  MRUA:         x = x₀ + v₀·t + ½·a·t²
                v = v₀ + a·t
                v² = v₀² + 2·a·Δx
  MCU:          v = ω·r,  a_c = v²/r = ω²·r
  Tiro parab:   R = v₀²·sin(2θ)/g,  H = v₀²·sin²(θ)/(2g)

DINÁMICA:
  2ª Ley:       ΣF = m·a
  Peso:         P = m·g
  Rozamiento:   F_r = μ·N
  Hooke:        F = -k·x

TERMODINÁMICA:
  Gases ideales: P·V = n·R·T
  Calor:        Q = m·c·ΔT,  Q = m·L
  1ª Ley:       ΔU = Q - W
  Carnot:       η = 1 - T_fría/T_caliente

ENERGÍA:
  Cinética:     E_c = ½·m·v²
  Potencial g:  E_p = m·g·h
  Potencial e:  E_pe = ½·k·x²
  Trabajo:      W = F·d·cos(α)
  Potencia:     P = W/t = F·v
```

## Notas de implementación para el agente

- Siempre mostrar el razonamiento algebraico antes de sustituir números.
- Indicar las unidades en cada paso intermedio.
- Si el problema es ambiguo, hacer explícitas las suposiciones.
- Para problemas complejos, descomponer en subproblemas por bloque temático.
- Cuando corresponda, ofrecer la solución numérica y la interpretación física.
- Usar `physics-expert` como skill de fallback para problemas de nivel avanzado.
