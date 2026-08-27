---
name: physics-basics
description: Cinemática (MRU, MRUA, caída libre, tiro parabólico), 3 leyes de Newton, fricción, trabajo y energía, conservación de energía, potencia, presión, empuje, ondas elementales.
tags: [stem, physics, basics]
---

# Física Básica

## Referencias de autoridad

- Sears & Zemansky — *University Physics with Modern Physics*, Addison-Wesley (cap. 1-14)
- Halliday, Resnick & Walker — *Fundamentals of Physics*, Wiley (10th ed.)
- Young & Freedman — *University Physics*, Pearson
- Giancoli, D. — *Physics: Principles with Applications*, Pearson

## Contenido clave

### Cinemática

**MRU (Movimiento Rectilíneo Uniforme)**:
- v = constante
- x(t) = x₀ + vt
- a = 0

**MRUA (Movimiento Rectilíneo Uniformemente Acelerado)**:
- a = constante
- v(t) = v₀ + at
- x(t) = x₀ + v₀t + ½at²
- v² = v₀² + 2a(x - x₀)
- x - x₀ = ½(v₀ + v)t (desplazamiento = velocidad media × tiempo)

**Caída libre** (caso particular de MRUA, a = -g):
- g = 9.81 m/s² (valor estándar al nivel del mar)
- y(t) = y₀ + v₀t - ½gt²
- v(t) = v₀ - gt
- v² = v₀² - 2g(y - y₀)

**Tiro parabólico**:
- Componente horizontal: x = v₀cos(θ)t (MRU, aₓ = 0)
- Componente vertical: y = v₀sen(θ)t - ½gt² (MRUA, aᵧ = -g)
- Alcance máximo: R = v₀²sen(2θ)/g. Máximo cuando θ = 45°.
- Altura máxima: H = v₀²sen²(θ)/(2g)
- Tiempo de vuelo: T = 2v₀sen(θ)/g

**Movimiento circular uniforme** (MCU):
- Velocidad angular: ω = 2π/T = 2πf
- Velocidad lineal: v = ωr
- Aceleración centrípeta: aᶜ = v²/r = ω²r (dirigida al centro)

### Dinámica — Leyes de Newton

**Primera ley (inercia)**: Un cuerpo permanece en reposo o movimiento rectilíneo uniforme a menos que una fuerza neta actúe sobre él.

**Segunda ley**: F⃗ = ma⃗ (vectorial). En componentes:
- Fₓ = maₓ, Fᵧ = maᵧ, Fᵥ = maᵥ

**Tercera ley (acción-reacción)**: Si A ejerce fuerza sobre B, B ejerce sobre A una fuerza igual en magnitud y dirección pero de sentido contrario: F⃗_AB = -F⃗_BA

**Fuerza peso**: P⃗ = mg⃗. Magnitud: P = mg (g = 9.81 m/s²)

**Fuerza normal**: N⃗ perpendicular a la superficie de contacto. En plano horizontal sin otras fuerzas: N = mg.

**Fuerza de tensión**: T⃗ a lo largo de la cuerda/cable. Siempre tira, nunca empuja.

**Fuerza de fricción**:
- Estática: fₛ ≤ μₛN (se opone al inicio del movimiento). Valor máximo: fₛ,max = μₛN
- Cinética: fₖ = μₖN (se opone al movimiento en curso). μₖ < μₛ siempre.
- Dirección: siempre paralela a la superficie, opuesta al movimiento relativo o tendencial.

### Trabajo y energía

**Trabajo**: W = F⃗ · d⃗ = Fd cos(φ) = ΣFᵢdᵢ
- φ = ángulo entre fuerza y desplazamiento
- W > 0 si φ ∈ [0, 90°): fuerza ayuda al movimiento
- W = 0 si φ = 90°: fuerza perpendicular al desplazamiento
- W < 0 si φ ∈ (90°, 180°]: fuerza se opone al movimiento
- Unidad: joule (J) = N·m = kg·m²/s²

**Energía cinética**: K = ½mv²

**Teorema trabajo-energía**: Wₙₑₜ = ΔK = K_f - K_i

**Energía potencial gravitatoria**: U_g = mgy (y medido desde referencia arbitraria)

**Energía potencial elástica**: Uₑ = ½kx² (k = constante del resorte, x = deformación desde equilibrio)

**Ley de conservación de energía mecánica** (sin fricción):
E = K + U = constante
Kᵢ + Uᵢ = K_f + U_f

**Potencia**:
- Media: Pₘₑ𝒹 = W/Δt = ΔE/Δt
- Instantánea: P = F⃗ · v⃗ = Fv cos(φ)
- Unidad: watt (W) = J/s

### Fluidos

**Presión**: P = F/A (fuerza normal por unidad de área)
- Unidad: pascal (Pa) = N/m²
- 1 atm = 101325 Pa = 760 mmHg = 1.01325 bar
- Presión hidrostática: P = P₀ + ρgh (P₀ = presión en superficie, ρ = densidad, h = profundidad)

**Principio de Pascal**: La presión aplicada a un fluido encerrado se transmite íntegramente a todos los puntos.

**Principio de Arquímedes**: Todo cuerpo sumergido total o parcialmente en un fluido experimenta un empuje vertical hacia arriba igual al peso del fluido desalojado.
- E = ρ_fluido · V_sumergido · g

### Ondas elementales

- Relación fundamental: v = λf (velocidad = longitud de onda × frecuencia)
- Período: T = 1/f
- Velocidad de onda en cuerda: v = √(T/μ) (T = tensión, μ = densidad lineal)
- Velocidad del sonido en aire (20°C): v ≈ 343 m/s
- Velocidad de la luz: c = 299792458 m/s ≈ 3 × 10⁸ m/s

## Unidades y sistema SI

| Magnitud | Unidad SI | Símbolo | Equivalencias |
|----------|-----------|---------|---------------|
| Masa | kilogramo | kg | 1 kg = 1000 g |
| Longitud | metro | m | 1 km = 1000 m |
| Tiempo | segundo | s | |
| Velocidad | m/s | m/s | 1 km/h = 1/3.6 m/s |
| Aceleración | m/s² | m/s² | |
| Fuerza | newton | N | 1 N = 1 kg·m/s² |
| Trabajo/Energía | joule | J | 1 J = 1 N·m |
| Potencia | watt | W | 1 W = 1 J/s |
| Presión | pascal | Pa | 1 Pa = 1 N/m² |
| Densidad | kg/m³ | kg/m³ | 1 g/cm³ = 1000 kg/m³ |
| Frecuencia | hertz | Hz | 1 Hz = 1 s⁻¹ |

## Errores comunes / Pitfalls

- **Confundir velocidad con aceleración**: velocidad = tasa de cambio de posición; aceleración = tasa de cambio de velocidad. Un objeto puede tener velocidad alta y aceleración cero (MRU).
- **Signo en gravedad**: por convención, g se toma como positivo (9.81 m/s²) y el signo negativo va en la ecuación (-g). No usar a = -9.81 y también poner -g en la ecuación (doble negativo).
- **Trabajo positivo/negativo**: W = Fd cos(φ). Si φ = 180° (fuerza opuesta al desplazamiento), cos(180°) = -1, W < 0. La fricción SIEMPRE hace trabajo negativo.
- **Fricción estática vs cinética**: fₛ ≤ μₛN (desigualdad, no igualdad). Solo alcanza μₛN en el límite del deslizamiento. Una vez que se desliza, fₖ = μₖN.
- **Peso vs masa**: masa es invariante (kg), peso depende de g (N). En la Luna, misma masa, peso ~1/6.
- **Energía potencial referencia**: U = mgy es relativa. Solo ΔU tiene significado físico. Elegir y = 0 en el punto más conveniente.
- **Conservación de energía**: solo se conserva la energía MECÁNICA si no hay fuerzas no conservativas (fricción). Con fricción: ΔE_mec = W_fricción.
- **Tiro parabólico**: el tiempo de subida = tiempo de bajada (si se lanza y aterriza a la misma altura). La velocidad en el punto más alto NO es cero: vₓ = v₀cos(θ) ≠ 0.

## Verificación

- [ ] Cinemática: verificar dimensiones: [x] = L, [v] = L/T, [a] = L/T²
- [ ] MRUA: comprobar que v(t) se obtiene derivando x(t): dx/dt = v₀ + at ✓
- [ ] Tiro parabólico: verificar que en t = T/2 se alcanza altura máxima (vᵧ = 0)
- [ ] Segunda ley de Newton: verificar que ΣF⃗ = ma⃗ en cada eje por separado
- [ ] Fricción: verificar μₖ < μₛ (si no, algo está mal)
- [ ] Trabajo: verificar unidades: N × m = J ✓
- [ ] Conservación energía: verificar Kᵢ + Uᵢ = K_f + U_f + E_disipada
- [ ] Potencia: verificar P = Fv (N × m/s = J/s = W) ✓
- [ ] Arquímedes: verificar que empuje = peso del fluido desalojado (ρ_fluido × V × g)
- [ ] Relación onda: verificar v = λf → [L/T] = [L] × [1/T] ✓
