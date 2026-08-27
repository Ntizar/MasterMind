---
name: physics-intermediate
description: Termodinámica, electromagnetismo (Coulomb, campos, circuitos, Faraday, Lenz), óptica geométrica, MCA y colisiones.
tags: [stem, physics, intermediate]
---

# Física Intermedia

## Referencias de autoridad

- Sears & Zemansky — *University Physics with Modern Physics*, Addison-Wesley (cap. 17-30)
- Halliday, Resnick & Walker — *Fundamentals of Physics*, Wiley (cap. 21-36)
- Serway & Jewett — *Physics for Scientists and Engineers*, Cengage Learning
- Giancoli, D. — *Physics: Principles with Applications*, Pearson

## Contenido clave

### Termodinámica

**Ley cero**: Si A está en equilibrio térmico con C, y B también, entonces A y B están en equilibrio térmico entre sí. Define la temperatura.

**Primera ley**: ΔU = Q - W
- ΔU = cambio en energía interna
- Q = calor transferido AL sistema (Q > 0 entra, Q < 0 sale)
- W = trabajo realizado POR el sistema (W > 0 expande, W < 0 comprime)
- Para gas ideal: ΔU = nCᵥΔT (solo depende de T)

**Segunda ley**:
- Enunciado de Clausius: el calor no fluye espontáneamente de frío a caliente.
- Enunciado de Kelvin-Planck: es imposible construir una máquina térmica que convierta TODO el calor en trabajo (rendimiento < 100%).
- Entropía: ΔS ≥ 0 para sistema aislado. ΔS = Q/T (proceso reversible).
- La entropía total del universo siempre aumenta en procesos irreversibles.

**Tercera ley**: Al acercarse T → 0 K, la entropía de un cristal perfecto tiende a cero.

**Gas ideal**: PV = nRT
- R = 8.314 J/(mol·K) = 0.08206 L·atm/(mol·K)
- n = masa / masa molar = m/M
- Número de Avogadro: Nₐ = 6.022 × 10²³ mol⁻¹

**Procesos termodinámicos**:
- Isocórico (V constante): W = 0, Q = nCᵥΔT, ΔU = Q
- Isobárico (P constante): W = PΔV, Q = nCₚΔT, ΔU = nCᵥΔT
- Isotérmico (T constante, gas ideal): ΔU = 0, Q = W = nRT ln(V_f/V_i)
- Adiabático (Q = 0): ΔU = -W, PV^γ = constante, γ = Cₚ/Cᵥ

**Ciclos termodinámicos**:
- Rendimiento: η = Wₙₑₜ/Qₑₙₜ�ᵣₐ = 1 - Qₛₐₗₑ/Qₑₙₜᵣₐ
- Ciclo de Carnot (máximo teórico): η = 1 - T_c/Tₕ (T en Kelvin)
- Refrigerador: COP = Q_fría/W = T_c/(Tₕ - T_c) (Carnot)

### Electrostática

**Ley de Coulomb**: F⃗ = k · q₁q₂/r² · r̂
- k = 1/(4πε₀) = 8.99 × 10⁹ N·m²/C²
- ε₀ = 8.854 × 10⁻¹² C²/(N·m²) (permitividad del vacío)
- F es atractiva si signos opuestos, repulsiva si mismos signos

**Campo eléctrico**: E⃗ = F⃗/q₀ = kQ/r² · r̂ (punto)
- Superposición: E⃗_total = ΣE⃗ᵢ
- Líneas de campo: salen de cargas positivas, entran en negativas

**Potencial eléctrico**:
- V = kQ/r (potencial de carga puntual)
- ΔV = -∫E⃗ · dl⃗ (diferencia de potencial)
- E⃗ = -∇V (campo es gradiente negativo del potencial)
- Unidad: volt (V) = J/C

**Capacitancia**: C = Q/V
- Condensador paralelo: C = ε₀A/d
- En paralelo: Cₜₒₜ = C₁ + C₂ + ...
- En serie: 1/Cₜₒₜ = 1/C₁ + 1/C₂ + ...
- Energía almacenada: U = ½CV² = ½QV = Q²/(2C)

### Circuitos eléctricos

**Ley de Ohm**: V = IR
- R = resistancia (ohm, Ω)
- I = corriente (amperio, A)
- V = diferencia de potencial (volt, V)

**Resistencias**:
- Serie: Rₜₒₜ = R₁ + R₂ + ...
- Paralelo: 1/Rₜₒₜ = 1/R₁ + 1/R₂ + ...
- Potencia disipada: P = IV = I²R = V²/R

**Leyes de Kirchhoff**:
- Nodos (KCL): ΣIₑₙₜᵣₐ = ΣIₛₐₗₑ (conservación de carga)
- Mallas (KVL): ΣV = 0 alrededor de cualquier malla cerrada (conservación de energía)

### Inducción electromagnética

**Ley de Faraday**: ε = -dΦ_B/dt
- Φ_B = ∫B⃗ · dA⃗ = BA cos(θ) (flujo magnético)
- ε = fuerza electromotriz inducida
- Para N espiras: ε = -N · dΦ_B/dt

**Ley de Lenz**: La corriente inducida fluye en dirección tal que su campo magnético se OPONE al cambio de flujo que la produjo. El signo negativo en Faraday refleja esto.

### Óptica geométrica

**Ley de reflexión**: θᵢ = θᵣ (ángulo de incidencia = ángulo de reflexión)

**Ley de Snell (refracción)**: n₁sen(θ₁) = n₂sen(θ₂)
- n = c/v = índice de refracción
- n_agua ≈ 1.33, n_vidrio ≈ 1.5, n_air ≈ 1.0003

**Ángulo crítico** (reflexión total interna): sen(θ_c) = n₂/n₁ (n₁ > n₂)
- θ_c = arcsen(n₂/n₁)

**Espejos esféricos**:
- Espejo cóncavo: 1/f = 1/dₒ + 1/dᵢ, f = R/2 (f > 0)
- Espejo convexo: f < 0 (focal virtual)
- Aumento: M = -dᵢ/dₒ = hᵢ/hₒ

**Lentes delgadas**:
- 1/f = 1/dₒ + 1/dᵢ (misma fórmula que espejos)
- Lente convergente: f > 0
- Lente divergente: f < 0
- Potencia: P = 1/f (dioptrías, f en metros)

### MCA — Momento lineal y colisiones

**Momento lineal**: p⃗ = mv⃗ (vector)

**Teorema impulso-momento**: J⃗ = ∫F⃗dt = Δp⃗

**Conservación del momento**: Si ΣF⃗_ext = 0, entonces p⃗_total = constante.

**Colisiones**:
- **Elástica**: se conserva momento Y energía cinética.
  - m₁v₁ᵢ + m₂v₂ᵢ = m₁v₁f + m₂v₂f
  - ½m₁v₁ᵢ² + ½m₂v₂ᵢ² = ½m₁v₁f² + ½m₂v₂f²
  - Para masas iguales: intercambian velocidades
- **Inelástica**: se conserva momento, NO energía cinética.
- **Completamente inelástica**: cuerpos quedan unidos tras colisión.
  - m₁v₁ᵢ + m₂v₂ᵢ = (m₁ + m₂)v_f
  - Máxima pérdida de energía cinética posible sin violar conservación de momento

**Centro de masas**: R⃗_cm = Σmᵢr⃗ᵢ/Σmᵢ

## Unidades y sistema SI

| Magnitud | Unidad SI | Símbolo | Equivalencias |
|----------|-----------|---------|---------------|
| Temperatura | kelvin | K | T(K) = T(°C) + 273.15 |
| Calor/Energía | joule | J | 1 cal = 4.186 J |
| Calor específico | J/(kg·K) | J/(kg·K) | |
| Entropía | J/K | J/K | |
| Carga eléctrica | culombio | C | 1 C = 1 A·s |
| Campo eléctrico | N/C o V/m | N/C, V/m | |
| Potencial eléctrico | volt | V | 1 V = 1 J/C |
| Capacitancia | faradio | F | 1 F = 1 C/V |
| Resistencia | ohm | Ω | 1 Ω = 1 V/A |
| Corriente | amperio | A | |
| Flujo magnético | weber | Wb | 1 Wb = 1 V·s |
| Inducción magnética | tesla | T | 1 T = 1 N/(A·m) |
| Índice de refracción | adimensional | — | |

## Errores comunes / Pitfalls

- **Confusión campo/potencial eléctrico**: E⃗ es vectorial (N/C), V es escalar (V). E⃗ = -∇V. Campo cero NO implica potencial cero (ej: punto medio entre dos cargas iguales: E⃗ = 0, V ≠ 0).
- **Signo en Ley de Lenz**: el signo negativo NO es arbitrario. Indica que la FEM inducida se OPONE al cambio de flujo. Si el flujo aumenta, la FEM tiende a reducirlo; si disminuye, tiende a aumentarlo.
- **Tipo de colisiones**: en elástica se conservan momento Y energía cinética. En inelástica SOLO momento. En completamente inelástica, los cuerpos se unen y hay MÁXIMA pérdida de energía cinética compatible con conservación de momento.
- **Unidades termodinámicas (K vs °C)**: todas las ecuaciones termodinámicas (gas ideal, Carnot, entropía) requieren Kelvin. T(K) = T(°C) + 273.15. NUNCA usar °C en PV = nRT o η = 1 - T_c/Tₕ.
- **Lente vs espejo**: la fórmula 1/f = 1/dₒ + 1/dᵢ es la misma, pero los signos de f cambian. Cóncavo: f > 0; convexo: f < 0. Convergente: f > 0; divergente: f < 0.
- **Capacitores en serie/paralelo**: en paralelo, V es igual y Q se suma. En serie, Q es igual y V se suma. Invertido respecto a resistencias.
- **Resistencia vs conductancia**: R = ρL/A. Si duplicas longitud, R se duplica. Si duplicas área, R se reduce a la mitad.

## Verificación

- [ ] Gas ideal: verificar PV/nT = R constante para diferentes estados
- [ ] Carnot: verificar η = 1 - T_c/Tₕ < 1 siempre (T en Kelvin)
- [ ] Ley de Coulomb: verificar unidades: [kq₁q₂/r²] = [N·m²/C² × C²/m²] = [N] ✓
- [ ] Capacitancia serie/paralelo: verificar que C_paralelo > cada Cᵢ y C_serie < cada Cᵢ
- [ ] Snell: verificar que si n₂ > n₁, entonces θ₂ < θ₁ (la luz se acerca a la normal)
- [ ] Colisión elástica: verificar que tanto Σp como ΣK se conservan independientemente
- [ ] Kirchhoff KVL: verificar que la suma algebraica de voltajes en malla = 0
- [ ] Lenz: verificar dirección de corriente inducida: si flujo entra y aumenta, campo inducido sale
- [ ] Centro de masas: verificar que R_cm está entre las posiciones de las masas
