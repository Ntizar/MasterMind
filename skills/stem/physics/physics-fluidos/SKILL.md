---
name: physics-fluidos
description: Hidrostática, presión, empuje de Arquímedes, ecuación de Bernoulli, caudal, viscosidad y tensión superficial.
tags: [stem, physics, basics]
---

# Fluidos

## Presión

- **Definición**: P = F⃗ / A⃗ (Pa = N/m²)
- **Presión atmosférica**: P_atm = 101 325 Pa = 1 atm = 760 mmHg = 1,013 bar
- **Presión manométrica**: P_man = P_abs - P_atm
- **Presión absoluta**: P_abs = P_atm + P_man
- **1 bar** = 10⁵ Pa
- **1 atm** = 101 325 Pa = 760 Torr

## Hidrostática

- **Presión a profundidad h**: P = P₀ + ρgh
- P₀ = presión en la superficie
- ρ = densidad del fluido (kg/m³)
- g = 9,81 m/s²
- La presión depende SOLO de la profundidad, no de la forma del recipiente

### Principio de Pascal
- Un cambio de presión en un fluido encerrado se transmite íntegramente a todos los puntos
- F₁/A₁ = F₂/A₂ (prensa hidráulica)

### Principio de Stevin
- La diferencia de presión entre dos puntos de un fluido en reposo: ΔP = ρg·Δh

## Empuje (Arquímedes)

- E = ρ_fluido · V_sumergido · g
- Empuje hacia arriba = peso del fluido desalojado
- **Flota** si: E ≥ P (peso del cuerpo)
- **Se hunde** si: E < P
- Fracción sumergida: V_sub/V_total = ρ_cuerpo/ρ_fluido

## Dinámica de fluidos

### Caudal
- Q = A·v (m³/s)
- A = área de la sección, v = velocidad media
- **Ecuación de continuidad**: A₁v₁ = A₂v₂ (fluido incompresible)

### Ecuación de Bernoulli
- P + ½ρv² + ρgh = constante (a lo largo de una línea de corriente)
- P = presión estática
- ½ρv² = presión dinámica
- ρgh = presión hidrostática

### Teorema de Torricelli
- v = √(2gh) (velocidad de salida por un orificio a profundidad h)

## Viscosidad

- **Ley de Poiseuille** (tubo cilíndrico):
  Q = π·ΔP·r⁴ / (8ηL)
  η = viscosidad (Pa·s)
- Fluidos newtonianos: η es constante
- Fluidos no newtonianos: η depende de la velocidad de deformación

## Tensión superficial

- γ = F/L (N/m)
- Fuerza que actúa paralela a la superficie
- Explica la capilaridad, formación de gotas, insectos sobre el agua

## Gases

### Leyes de los gases ideales
- **PV = nRT**
- R = 8,314 J/(mol·K)
- n = moles, T = temperatura absoluta (K)

### Leyes derivadas
- **Boyle**: P₁V₁ = P₂V₂ (T constante)
- **Charles**: V₁/T₁ = V₂/T₂ (P constante)
- **Gay-Lussac**: P₁/T₁ = P₂/T₂ (V constante)

## Errores comunes / Pitfalls

- **Presión**: SIEMPRE usar Pa (N/m²) en cálculos. No usar atm o bar directamente
- **Empuje**: usar la densidad del FLUIDO, no del cuerpo
- **Bernoulli**: solo aplica a fluidos ideales (incompresibles, no viscosos, flujo estacionario)
- **Temperatura en gases**: SIEMPRE en Kelvin. T(K) = T(°C) + 273,15
- **Caudal**: Q = A·v, verificar que A esté en m² y v en m/s
- **Hidrostática**: la presión depende de la profundidad, NO de la forma del recipiente (paradoja hidrostática)

## Verificación

- [ ] Dimensiones: [P] = M/(L·T²), [Q] = L³/T
- [ ] Bernoulli: todos los términos tienen unidades de presión (Pa)
- [ ] Empuje: ρ_fluido·V·g → (kg/m³)(m³)(m/s²) = kg·m/s² = N ✓
- [ ] Gases: T en Kelvin, P en Pa, V en m³
- [ ] Continuidad: si A se reduce, v aumenta
