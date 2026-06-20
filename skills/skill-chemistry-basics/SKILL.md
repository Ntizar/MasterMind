---
name: skill-chemistry-basics
version: 1.0.0
category: STEM/Química/Básica
description: "Skill integral de Química general: Estructura atómica, tabla periódica, enlaces químicos, estequiometría y reacciones químicas. Cubre números cuánticos, configuración electrónica, propiedades periódicas, enlaces iónico/covalente/metálico, moles, balanceo y equilibrio."
---

# Skill: Química Básica (Química General)

## Descripción

Este skill proporciona las herramientas y conocimiento para resolver problemas de **química general** a nivel de bachillerato y primeros cursos universitarios. Cubre cinco grandes bloques temáticos fundamentales:

1. **Estructura atómica** — Modelo atómico, números cuánticos y configuración electrónica.
2. **Tabla periódica** — Propiedades periódicas, grupos, períodos y tendencias.
3. **Enlaces químicos** — Iónico, covalente, metálico e intermoleculares.
4. **Estequiometría** — Moles, reacciones químicas, balanceo y rendimiento.
5. **Reacciones químicas** — Tipos, cinética, equilibrio y pH.

## Cuándo usar este skill

- El usuario necesita escribir configuraciones electrónicas o determinar números cuánticos.
- Hay problemas de tabla periódica (radio atómico, energía de ionización, electronegatividad).
- Se requiere predecir el tipo de enlace o la geometría molecular.
- Hay problemas de estequiometría (moles, masa, rendimiento, reactivo limitante).
- Se pide calcular pH, analizar equilibrios químicos o predecir productos de reacción.
- El problema combina conceptos de más de un bloque (ej. enlace + geometría + polaridad).

## Instrucciones paso a paso

### Paso 1: Identificar el bloque temático

Clasifique el problema en uno o más bloques:

| Síntoma | Bloque |
|---|---|
| "número cuántico", "configuración electrónica", "orbital", "electrones" | Estructura atómica |
| "radio atómico", "electronegatividad", "energía de ionización", "grupo", "período" | Tabla periódica |
| "enlace iónico", "enlace covalente", "polaridad", "geometría", "Lewis" | Enlaces químicos |
| "moles", "masa molar", "reactivo limitante", "rendimiento", "balanceo" | Estequiometría |
| "pH", "equilibrio", "Kc", "Kp", "cinética", "velocidad de reacción" | Reacciones químicas |

### Paso 2: Extraer datos conocidos y desconocidos

Liste explícitamente:
- **Datos conocidos**: valores numéricos, fórmulas químicas, condiciones.
- **Datos desconocidos**: qué se pide calcular.
- **Constantes y datos atómicos**:
  ```
  N_A = 6.022 × 10²³ mol⁻¹    (número de Avogadro)
  R = 0.08206 L·atm/(mol·K)   (constante de los gases)
  R = 8.314 J/(mol·K)         (constante de los gases en SI)
  F = 96485 C/mol             (constante de Faraday)
  ```

### Paso 3: Seleccionar fórmulas relevantes

#### A) ESTRUCTURA ATÓMICA

**Modelo atómico actual (mecánica cuántica):**
- Los electrones se describen mediante **orbitales** (funciones de onda).
- Cada orbital se define por 4 números cuánticos.

**Números cuánticos:**

| Número | Símbolo | Valores | Significado |
|---|---|---|---|
| Principal | n | 1, 2, 3, ... | Nivel de energía, tamaño del orbital |
| Angular | l | 0, 1, 2, ..., n-1 | Forma del orbital (s=0, p=1, d=2, f=3) |
| Magnético | m_l | -l, ..., 0, ..., +l | Orientación del orbital |
| Spin | m_s | +½, -½ | Dirección del espín |

**Principio de Aufbau** (relleno de orbitales):
```
1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → 5s → 4d → 5p → 6s → 4f → 5d → 6p → 7s → 5f → 6d → 7p
```

**Principio de exclusión de Pauli**: Un orbital contiene máximo 2 electrones con espines opuestos.

**Regla de Hund**: En orbitales de igual energía, los electrones se distribuyen con espines paralelos antes de emparejarse.

**Configuración electrónica** (ejemplo: Fe, Z = 26):
```
1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶
[Ar] 4s² 3d⁶
```

**Capacidad máxima por subnivel:**
```
s: 2 electrones
p: 6 electrones
d: 10 electrones
f: 14 electrones
```

#### B) TABLA PERIÓDICA

**Grupos (columnas) y períodos (filas):**
- Grupos 1-2: metales alcalinos y alcalinotérreos (bloques s)
- Grupos 3-12: metales de transición (bloque d)
- Grupos 13-18: bloques p
- Lantánidos y actínidos: bloque f

**Propiedades periódicas:**

| Propiedad | Tendencia en el período (←→) | Tendencia en el grupo (↑↓) |
|---|---|---|
| Radio atómico | Disminuye | Aumenta |
| Energía de ionización | Aumenta | Disminuye |
| Electronegatividad | Aumenta | Disminuye |
| Afinidad electrónica | Aumenta (generalmente) | Disminuye |
| Carácter metálico | Disminuye | Aumenta |

**Energía de ionización (EI):**
```
EI₁: X → X⁺ + e⁻
EI₂: X⁺ → X²⁺ + e⁻
```

**Electronegatividad (escala de Pauling):**
```
F = 4.0 (más electronegativo)
O = 3.5
Cl = 3.0
C = 2.5
H = 2.1
```

#### C) ENLACES QUÍMICOS

**Enlace iónico** (metal + no metal):
- Transferencia de electrones.
- Formación de iones positivos (cationes) y negativos (aniones).
- Ejemplo: NaCl → Na⁺ + Cl⁻

**Enlace covalente** (no metal + no metal):
- Compartición de electrones.
- **Polar**: diferencia de electronegatividad 0.4 - 1.7 (ej. HCl)
- **Apolar**: diferencia < 0.4 (ej. H₂, Cl₂)
- **Dativo/coordinado**: ambos electrones provienen del mismo átomo

**Enlace metálico:**
- "Mar de electrones" compartidos entre cationes metálicos.
- Explica conductividad, maleabilidad y brillo metálico.

**Estructuras de Lewis:**
1. Contar electrones de valencia totales.
2. Colocar átomo central (menos electronegativo, excepto H).
3. Dibujar enlaces simples.
4. Completar octetos de átomos externos.
5. Completar octeto del central (puede tener expandido en período ≥ 3).
6. Formar enlaces múltiples si es necesario.

**Geometría molecular (VSEPR):**

| Electrones alrededor del central | Geometría electrónica | Geometría molecular (ejemplo) | Ángulo |
|---|---|---|---|
| 2 | Lineal | Lineal (CO₂) | 180° |
| 3 | Trigonal plana | Trigonal plana (BF₃) | 120° |
| 3 | Trigonal plana | Angular (SO₂) | ~120° |
| 4 | Tetraédrica | Tetraédrica (CH₄) | 109.5° |
| 4 | Tetraédrica | Pirámide trigonal (NH₃) | ~107° |
| 4 | Tetraédrica | Angular (H₂O) | ~104.5° |
| 5 | Bipirámide trigonal | Bipirámide trigonal (PCl₅) | 90°, 120° |
| 6 | Octaédrica | Octaédrica (SF₆) | 90° |

**Fuerzas intermoleculares** (de menor a mayor intensidad):
```
1. London (dispersión) — todas las moléculas
2. Dipolo-dipolo — moléculas polares
3. Puente de hidrógeno — H unido a F, O o N
```

#### D) ESTEQUIOMETRÍA

**Moles y masa molar:**
```
n = m / M       (moles = masa / masa molar)
m = n × M
M = Σ(masas atómicas)    (masa molar de un compuesto)
n = N / N_A            (moles = número de partículas / Avogadro)
n = V / V_m            (moles = volumen / volumen molar, CNPT: V_m = 22.4 L/mol)
```

**Porcentaje en masa:**
```
% en masa = (masa del elemento / masa del compuesto) × 100
```

**Fórmula empírica vs molecular:**
```
Empírica: relación más simple de átomos
Molecular: fórmula real (n × empírica)
n = masa molecular / masa empírica
```

**Balanceo de ecuaciones:**
1. Escribir la ecuación sin balancear.
2. Balancear metales primero, luego no metales, después H y O.
3. Verificar que átomos y carga estén balanceados.

**Métodos de balanceo:**
- **Inspección directa**: para ecuaciones simples.
- **Redox (número de oxidación)**: identificar qué se oxida y qué se reduce.
- **Redox (ión-electrón)**: para medio acuoso.

**Reactivo limitante:**
```
1. Calcular moles de cada reactivo.
2. Dividir por coeficiente estequiométrico.
3. El que da el menor cociente es el limitante.
4. Calcular productos a partir del reactivo limitante.
```

**Rendimiento:**
```
Rendimiento (%) = (rendimiento real / rendimiento teórico) × 100
```

**Pureza:**
```
% pureza = (masa pura / masa muestra) × 100
```

**Concentración:**
```
Molaridad (M) = n_soluto / V_solución (L)
Molalidad (m) = n_soluto / masa_solvente (kg)
% masa = (masa_soluto / masa_solución) × 100
Fracción molar (X_A) = n_A / n_total
```

#### E) REACCIONES QUÍMICAS

**Tipos de reacciones:**
```
Síntesis:        A + B → AB
Descomposición:  AB → A + B
Desplazamiento:  A + BC → AC + B
Doble desplazamiento: AB + CD → AD + CB
Combustión:      C_xH_y + O₂ → CO₂ + H₂O
Ácido-base:      Ácido + Base → Sal + H₂O
Redox:           Transferencia de electrones
```

**Cinética química:**
```
Velocidad = k·[A]^m·[B]^n    (ley de velocidad)
k = A·e^(-Ea/RT)             (ecuación de Arrhenius)
Ea: energía de activación
A: factor preexponencial
T: temperatura (K)
```

**Factores que afectan la velocidad:**
- Concentración (mayor → mayor velocidad)
- Temperatura (mayor → mayor velocidad, regla práctica: se duplica cada 10°C)
- Catalizador (disminuye Ea, no se consume)
- Superficie de contacto (mayor → mayor velocidad)
- Naturaleza de los reactivos

**Equilibrio químico:**
```
Kc = [C]^c·[D]^d / [A]^a·[B]^b    (para aA + bB ⇌ cC + dD)
Kp = Kc·(RT)^Δn    (Δn = moles_gaseosos_productos - moles_gaseosos_reactivos)
```

**Principio de Le Chatelier:**
- Aumentar concentración de un reactivo → equilibrio se desplaza a productos.
- Aumentar presión (gas) → equilibrio se desplaza al lado con menos moles gaseosos.
- Aumentar temperatura → equilibrio se desplaza en sentido endotérmico.

**pH y pOH:**
```
pH = -log[H⁺]
pOH = -log[OH⁻]
pH + pOH = 14    (a 25°C)
[H⁺] = 10^(-pH)
[OH⁻] = 10^(-pOH)
Kw = [H⁺]·[OH⁻] = 1.0 × 10⁻¹⁴    (a 25°C)
```

**Ácidos y bases:**
```
Ácido fuerte: HCl, HBr, HI, HNO₃, H₂SO₄, HClO₄ (se disocian completamente)
Base fuerte: NaOH, KOH, Ca(OH)₂ (se disocian completamente)

pH de ácido fuerte: pH = -log[H⁺] = -log(C_acido)
pH de base fuerte: pOH = -log[OH⁻], pH = 14 - pOH
```

**Constantes de equilibrio ácido-base:**
```
Ka·Kb = Kw = 10⁻¹⁴
pH = ½(pKa - log[C])    (ácido débil)
pOH = ½(pKb - log[C])   (base débil)
pH = ½(pKa + pKw + log[C])    (sal de ácido débil + base fuerte)
```

**Buffer (solución amortiguadora):**
```
pH = pKa + log([base]/[ácido])    (ecuación de Henderson-Hasselbalch)
```

### Paso 4: Resolver algebraicamente antes de sustituir

Despejar la incógnita en función de los datos. Solo al final sustituir valores numéricos.

### Paso 5: Verificar unidades y sentido físico

- Verificar que las unidades sean coherentes (SI: g, mol, L, atm, K, M).
- En estequiometría, verificar que la ecuación esté balanceada.
- En equilibrio, verificar que Q y K tengan las mismas unidades.
- En pH, verificar que el resultado esté entre 0 y 14 (para soluciones acuosas diluidas).

## Ejemplos de uso

### Ejemplo 1: Estructura atómica — Configuración electrónica
> **Prompt:** "Escribir la configuración electrónica del hierro (Fe, Z=26) y determinar sus números cuánticos del último electrón."

```
Solución paso a paso:
Z = 26 → 26 electrones

Configuración: 1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁶
Configución abreviada: [Ar] 4s² 3d⁶

Último electrón entra en 3d:
n = 3
l = 2 (d)
m_l = -2 (primer electrón en subnivel d, siguiendo Hund)
m_s = +½ (primer electrón en ese orbital)
```

### Ejemplo 2: Tabla periódica — Predicción de propiedades
> **Prompt:** "Comparar la electronegatividad y el radio atómico de Na, Mg, Al, Cl."

```
Solución paso a paso:
Todos están en el período 3.

Electronegatividad (aumenta ←→):
Na (0.9) < Mg (1.3) < Al (1.6) < Cl (3.0)

Radio atómico (disminuye ←→):
Na (186 pm) > Mg (160 pm) > Al (143 pm) > Cl (99 pm)
```

### Ejemplo 3: Estequiometría — Reactivo limitante
> **Prompt:** "Se hacen reaccionar 10 g de H₂ con 64 g de O₂ para formar H₂O. Calcular: a) el reactivo limitante, b) la masa de agua formada, c) el exceso."

```
Solución paso a paso:
Ecuación: 2H₂ + O₂ → 2H₂O

a) Moles:
   n(H₂) = 10/2 = 5 mol
   n(O₂) = 64/32 = 2 mol

   Cocientes: H₂ → 5/2 = 2.5; O₂ → 2/1 = 2
   O₂ es el reactivo limitante.

b) Masa de H₂O:
   n(H₂O) = 2 × n(O₂) = 4 mol
   m(H₂O) = 4 × 18 = 72 g

c) Exceso de H₂:
   H₂ consumido = 2 × n(O₂) = 4 mol
   H₂ restante = 5 - 4 = 1 mol = 2 g
```

### Ejemplo 4: pH — Solución de ácido fuerte
> **Prompt:** "Calcular el pH de una disolución 0.01 M de HCl."

```
Solución paso a paso:
HCl es ácido fuerte → se disocia completamente: [H⁺] = 0.01 M

pH = -log(0.01) = 2.00
pOH = 14 - 2 = 12
```

### Ejemplo 5: Enlaces — Geometría molecular
> **Prompt:** "Determinar la geometría molecular del CO₂ y predecir si es polar o apolar."

```
Solución paso a paso:
1. Estructura de Lewis: O=C=O (carbono central con 2 dobles enlaces)
2. Electrones alrededor del C: 2 regiones de densidad electrónica
3. Geometría: Lineal (180°)
4. Los enlaces C=O son polares (ΔEN = 1.0), pero la molécula es simétrica.
5. Los momentos dipolares se cancelan → molécula APOLAR.
```

### Ejemplo 6: Equilibrio — Constante Kc
> **Prompt:** "Para la reacción N₂(g) + 3H₂(g) ⇌ 2NH₃(g), las concentraciones en equilibrio son: [N₂] = 0.5 M, [H₂] = 0.3 M, [NH₃] = 0.4 M. Calcular Kc."

```
Solución paso a paso:
Kc = [NH₃]² / ([N₂]·[H₂]³)
Kc = (0.4)² / (0.5 × 0.3³)
Kc = 0.16 / (0.5 × 0.027)
Kc = 0.16 / 0.0135 = 11.85
```

### Ejemplo 7: Estequiometría — Rendimiento
> **Prompt:** "Se obtienen 45 g de NaCl al hacer reaccionar 50 g de Na con exceso de Cl₂. Calcular el rendimiento. (Na = 23, Cl = 35.5)"

```
Solución paso a paso:
2Na + Cl₂ → 2NaCl

Rendimiento teórico:
n(Na) = 50/23 = 2.174 mol
n(NaCl) teórico = 2.174 mol
m(NaCl) teórico = 2.174 × 58.5 = 127.18 g

Rendimiento = (45 / 127.18) × 100 = 35.4%
```

## Referencias cruzadas

Skills STEM existentes que complementan este skill:

| Skill | Ruta | Relación |
|---|---|---|
| `stem-basics` | `/hermes-home/skills/stem-basics/` | Conceptos básicos de ciencia para fundamentos |
| `skill-math-foundations` | `/hermes-home/skills/skill-math-foundations/` | Matemáticas fundamentales para química (logaritmos, álgebra) |

**Cuándo derivar a otros skills:**
- Para cálculos matemáticos avanzados (integrales en cinética, matrices en termodinámica) → usar `skill-math-foundations` o `skill-math-calculus`
- Para química orgánica avanzada → no hay skill específico, usar conocimiento general
- Para química inorgánica avanzada → no hay skill específico, usar conocimiento general
- Para química física (termodinámica química, electroquímica avanzada) → combinar con `skill-physics-mechanics` (termodinámica)
- Para análisis de datos experimentales → usar `data-science`

## Pitfalls (Errores comunes)

1. **Configuración electrónica**: el 4s se rellena antes que el 3d, pero al ionizarse los metales de transición pierden primero los electrones 4s.
2. **Números cuánticos**: l < n siempre. Si n=3, l puede ser 0, 1 o 2 (NO 3). m_l está entre -l y +l.
3. **Masa molar**: usar masas atómicas con suficientes decimales. No confundir masa atómica (uma) con masa molar (g/mol), aunque numéricamente son iguales.
4. **Reactivo limitante**: no confundir con el reactivo que tiene menor masa. Se compara por moles / coeficiente estequiométrico.
5. **Balanceo de redox**: verificar que tanto átomos como carga estén balanceados. En medio ácido se usan H⁺ y H₂O; en medio básico, OH⁻ y H₂O.
6. **pH de ácidos/bases débiles**: NO usar pH = -log(C). Se debe usar la constante Ka o Kb y resolver el equilibrio.
7. **Kc vs Kp**: recordar que Kp = Kc·(RT)^Δn. Solo hay diferencia si Δn ≠ 0 (cambio en moles gaseosos).
8. **Principio de Le Chatelier**: al cambiar volumen/presión, el equilibrio se desplaza al lado con MENOS moles gaseosos.
9. **Fuerzas intermoleculares**: el puente de hidrógeno solo se forma cuando H está unido a F, O o N (N es el tercer elemento clave).
10. **Estructura de Lewis**: no olvidar pares solitarios (electrones no enlazantes). Afectan la geometría molecular (VSEPR).
11. **Unidades de concentración**: M = mol/L (molaridad), m = mol/kg (molalidad). No confundirlas.
12. **Porcentaje de rendimiento**: siempre se compara contra el rendimiento TEÓRICO (calculado), no contra la masa inicial.

## Fórmulas de referencia rápida

```
ESTRUCTURA ATÓMICA:
  Números cuánticos:  n, l (0..n-1), m_l (-l..+l), m_s (±½)
  Aufbau:             1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p
  Capacidad:          s=2, p=6, d=10, f=14

TABLA PERIÓDICA:
  Radio atómico:      aumenta ↑↓, disminuye ←→
  Electronegatividad: aumenta ↑↓, aumenta ←→
  EI:                 aumenta ↑↓, aumenta ←→

ENLACES:
  Diferencia electronegatividad:
    < 0.4: covalente apolar
    0.4-1.7: covalente polar
    > 1.7: iónico
  VSEPR: 2=linear, 3=trigonal, 4=tetraédrico, 5=bipir. trig., 6=octaédrico

ESTEQUIOMETRÍA:
  n = m/M = N/N_A = V/V_m
  Molaridad: M = n/V(L)
  Rendimiento: % = (real/teórico) × 100

REACCIONES:
  pH = -log[H⁺], pOH = -log[OH⁻], pH + pOH = 14
  Kc = [C]^c·[D]^d / [A]^a·[B]^b
  Kp = Kc·(RT)^Δn
  pH = pKa + log([base]/[ácido])    (Henderson-Hasselbalch)
```

## Notas de implementación para el agente

- Siempre verificar que las ecuaciones estequiométricas estén balanceadas antes de calcular.
- Para configuraciones electrónicas de iones, recordar que se pierden/ganan electrones primero de los orbitales de mayor n.
- Al predecir geometría molecular, contar TODOS los pares de electrones (enlazantes y no enlazantes) alrededor del átomo central.
- En problemas de pH con ácidos/bases débiles, resolver el equilibrio usando Ka/Kb (no asumir disociación completa).
- Para cálculos de rendimiento, identificar siempre el reactivo limitante primero.
- Al balancear ecuaciones redox en medio básico, convertir H⁺ en OH⁻ al final añadiendo OH⁻ a ambos lados.
- Usar masas atómicas con al menos 2 decimales para precisión.
- Cuando corresponda, ofrecer tanto la solución numérica como la explicación conceptual.
- Combinar con `skill-math-foundations` para cálculos logarítmicos y algebraicos complejos.
