---
name: physics-expert
description: Teoría cuántica de campos conceptual, física de partículas (modelo estándar), cosmología (Friedmann, CMB, materia/energía oscura), física de plasmas básica.
tags: [stem, physics, expert]
---

# Física Experimental/Expert

## Referencias de autoridad

- Peskin, M. & Schroeder, D. — *An Introduction to Quantum Field Theory*, Addison-Wesley
- Carroll, S. — *Spacetime and Geometry: An Introduction to General Relativity*, Addison-Wesley
- Hartle, J. — *Gravity: An Introduction to Einstein's General Relativity*, Addison-Wesley
- Griffiths, D. — *Introduction to Elementary Particles* (2nd ed.), Wiley
- Ryden, B. — *Introduction to Cosmology* (2nd ed.), Cambridge University Press

## Contenido clave

### Teoría cuántica de campos (conceptos)

**Principio de mínima acción**:
- Acción: S = ∫ℒ d⁴x (integral del lagrangiano sobre el espaciotiempo)
- Las ecuaciones del movimiento se obtienen de δS = 0 (principio de Hamilton)
- Ecuaciones de Euler-Lagrange: ∂ℒ/∂φ - ∂_μ(∂ℒ/∂(∂_μφ)) = 0

**Lagrangianos clásicos de campos**:
- Campo escalar libre: ℒ = ½(∂_μφ)(∂^μφ) - ½m²φ²
- Ecuación de Euler-Lagrange → ecuación de Klein-Gordon: (∂²/∂t² - ∇² + m²)φ = 0
- Campo electromagnético: ℒ = -¼F_μνF^μν - J^μA_μ
  - F_μν = ∂_μA_ν - ∂_νA_μ (tensor de campo electromagnético)

**Campos cuánticos**:
- Cuantización canónica: campos se convierten en operadores que satisfacen relaciones de conmutación (bosones) o anticonmutación (fermiones).
- Bosones: espín entero (0, 1, 2, ...). Ej: fotón (espín 1), bosón de Higgs (espín 0).
- Fermiones: espín semientero (½, 3/2, ...). Ej: electrón (espín ½), quark (espín ½).
- Teorema spin-estadística: bosones siguen estadística de Bose-Einstein; fermiones siguen estadística de Fermi-Dirac.

**Diagramas de Feynman**:
- Representación pictórica de amplitudes de scattering en teoría de perturbaciones.
- Líneas externas: partículas iniciales/finales.
- Líneas internas: partículas virtuales (propagadores).
- Vértices: interacciones. Cada vértice aporta un factor de acoplamiento (ej: e para QED).
- Reglas de Feynman: cada elemento del diagrama se traduce en una expresión matemática.
- Orden perturbativo: cada orden en la constante de acoplamiento añade un bucle.

**QED (Electrodinámica Cuántica)**:
- Interacción entre campos electromagnéticos y campos de electrones/positrones.
- Constante de estructura fina: α = e²/(4πε₀ℏc) ≈ 1/137 ≈ 0.007297
- α ≪ 1 → la expansión perturbativa converge bien.
- Predicción más precisa de la física: momento magnético anómalo del electrón, a_e = (g-2)/2 ≈ 0.001159652181...

### Física de partículas — Modelo Estándar

**Quarks** (fermiones de espín ½, sienten interacción fuerte):
- Generación 1: up (u, carga +2/3e), down (d, carga -1/3e)
- Generación 2: charm (c, +2/3e), strange (s, -1/3e)
- Generación 3: top (t, +2/3e), bottom (b, -1/3e)
- Colores: rojo, verde, azul (carga de color). Los hadrones son singletes de color.
- Bariones: 3 quarks (uud = protón, udd = neutrón)
- Mesones: quark + antiquark (π⁺ = uanti-d, K⁺ = uantis)

**Leptones** (fermiones de espín ½, NO sienten interacción fuerte):
- Generación 1: electrón (e⁻, -1e), neutrino electrónico (νₑ, 0)
- Generación 2: muón (μ⁻, -1e), neutrino muónico (ν_μ, 0)
- Generación 3: tau (τ⁻, -1e), neutrino tauónico (ν_τ, 0)
- Cada leptón tiene su antipartícula.

**Bosones mediadores** (espín 1, portadores de interacciones):
- Fotón (γ): interacción electromagnética. Masa = 0. Alcance = ∞.
- Gluones (g, 8 tipos): interacción fuerte. Masa = 0. Alcance ~ 1 fm (confinamiento).
- Bosones W⁺, W⁻, Z⁰: interacción débil. Masa ~ 80-91 GeV/c². Alcance ~ 10⁻¹⁸ m.
- Bosón de Higgs (H⁰, espín 0): mecanismo de Higgs, da masa a partículas fundamentales. Masa ≈ 125 GeV/c² (descubierto en 2012, LHC).

**Interacciones fundamentales** (ordenadas por intensidad a escala atómica):
1. Fuerte: αₛ ≈ 1 (a escala de 1 GeV). Alcance ~ 1 fm.
2. Electromagnética: α ≈ 1/137. Alcance ∞.
3. Débil: α_w ≈ 10⁻⁶. Alcance ~ 10⁻¹⁸ m.
4. Gravitatoria: α_g ≈ 10⁻³⁹. Alcance ∞. (No incluida en Modelo Estándar)

**Simetrías y conservación**:
- U(1): conservación de carga eléctrica.
- SU(3)_c: cromodinámica cuántica (QCD), conservación de color.
- SU(2)_L × U(1)_Y: interacción electrodébil (Glashow-Weinberg-Salam).
- Ruptura espontánea de simetría electrodébil → W y Z adquieren masa, fotón permanece sin masa.
- Violación CP: observada en kaones (1964) y mesones B. Asimetría materia-antimateria.

### Cosmología

**Métrica de Friedmann-Lemaître-Robertson-Walker (FLRW)**:
- ds² = -c²dt² + a(t)² [dr²/(1-kr²) + r²dΩ²]
- a(t) = factor de escala. a(t₀) = 1 (hoy).
- k = 0 (plano), k > 0 (cerrado/esférico), k < 0 (abierto/hiperbólico)

**Ecuaciones de Friedmann**:
1. (ȧ/a)² = H² = (8πG/3)ρ - kc²/a² + Λc²/3
2. ä/a = -(4πG/3)(ρ + 3p/c²) + Λc²/3

- H = ȧ/a = constante de Hubble (actualmente H₀ ≈ 67.4 km/s/Mpc)
- H(z) = H₀√(Ωᵣ(1+z)⁴ + Ωₘ(1+z)³ + Ωₖ(1+z)² + Ω_Λ)
- Ωᵣ: densidad de radiación, Ωₘ: materia, Ωₖ: curvatura, Ω_Λ: energía oscura
- Ω_total = Ωᵣ + Ωₘ + Ωₖ + Ω_Λ ≈ 1 (universo plano)

**Parámetros actuales** (Planck 2018):
- Ω_b ≈ 0.049 (materia bariónica)
- Ω_c ≈ 0.262 (materia oscura fría)
- Ωₘ ≈ 0.311 (materia total)
- Ω_Λ ≈ 0.689 (energía oscura)
- Ωᵣ ≈ 9 × 10⁻⁵ (radiación)
- H₀ ≈ 67.4 km/s/Mpc
- Edad del universo: t₀ ≈ 13.80 × 10⁹ años

**Radiación cósmica de fondo (CMB)**:
- T₀ = 2.7255 K (temperatura actual)
- T(z) = T₀(1+z)
- Desacoplamiento: z* ≈ 1100, t* ≈ 380000 años
- Fluctuaciones de temperatura: ΔT/T ≈ 10⁻⁵
- Espectro de cuerpo negro casi perfecto

**Expansión del universo**:
- Corrimiento al rojo cosmológico: 1 + z = a(t₀)/a(t_em) = λ_observado/λ_emitido
- Ley de Hubble: v = H₀d (para z ≪ 1)
- Distancia comóvil vs distancia propia
- Horizontes: horizonte de partículas, horizonte de eventos

**Materia oscura**:
- Evidencia: curvas de rotación galáctica planas (Rubin, 1970s), lentes gravitacionales, CMB, estructura a gran escala.
- NO emite, absorbe ni refleja luz. Interactúa gravitatoriamente.
- Candidatos: WIMPs, axiones, neutrinos estériles.
- No es materia bariónica oscura (BBN y CMB restringen Ω_b).

**Energía oscura**:
- Responsable de la aceleración de la expansión (ää > 0).
- Requiere: ρ + 3p/c² < 0 → p < -ρc²/3
- Constante cosmológica (Λ): p = -ρc² (ecuación de estado w = -1)
- w = p/(ρc²) ≈ -1 ± 0.05 (observaciones actuales)
- Naturaleza: desconocida. ¿Λ? ¿quintaesencia? ¿modificación de gravedad?

### Física de plasmas básica

**Plasma**: cuarto estado de la materia. Gas ionizado con comportamiento colectivo.
- Condición de cuasi-neutralidad: nₑ ≈ ΣZᵢnᵢ (densidad de cargas positivas ≈ negativa)
- Longitud de Debye: λ_D = √(ε₀kTₑ/(nₑe²)) — escala de blindaje eléctrico
- Número de Debye: N_D = (4π/3)nₑλ_D³ ≫ 1 (comportamiento colectivo)

**Frecuencia plasma**: ωₚₑ = √(nₑe²/(ε₀mₑ))
- Oscilaciones de electrones a esta frecuencia si se desplazan del equilibrio.

**Temperatura de ionización** (Saha):
- nᵢ₊₁nₑ/nᵢ = (2Zᵢ₊₁/Zᵢ)(2πmₑkT/h²)^(3/2)e^(-χᵢ/kT)
- χᵢ = energía de ionización

**Magnetohidrodinámica (MHD)**:
- Plasma como fluido conductor en campo magnético.
- Número de plasma β = p/(B²/(2μ₀)) = relación presión cinética / presión magnética
- β ≪ 1: campo magnético domina (ej: corona solar)
- β ≫ 1: presión cinética domina (ej: interior estelar)

## Unidades y sistema SI

| Magnitud | Unidad SI | Símbolo | Equivalencias útiles |
|----------|-----------|---------|---------------------|
| Masa en física de partículas | eV/c² | eV/c² | 1 GeV/c² ≈ 1.783 × 10⁻²⁷ kg |
| Energía | eV | eV | 1 eV = 1.602 × 10⁻¹⁹ J |
| Constante de Hubble | km/s/Mpc | km/s/Mpc | 1 Mpc = 3.086 × 10¹⁹ km |
| Densidad crítica | kg/m³ | kg/m³ | ρ_c = 3H₀²/(8πG) ≈ 9 × 10⁻²⁷ kg/m³ |
| Temperatura CMB | kelvin | K | 2.7255 K |
| Sección eficaz | metro² | m² | 1 barn = 10⁻²⁸ m² |

## Errores comunes / Pitfalls

- **Interpretar mal diagramas de Feynman**: las líneas temporales pueden ir de izquierda a derecha O de abajo arriba (convención de tiempo hacia arriba). Los antipartículas se representan como partículas viajando hacia atrás en el tiempo en la convención de Feynman-Stückelberg.
- **Confusión materia oscura/energía oscura**: son COSAS DISTINTAS. Materia oscura atrae gravitatoriamente (agrupa estructura). Energía oscura repele (acelera expansión). Ω_m ≈ 0.31, Ω_Λ ≈ 0.69.
- **Unidades naturales**: en física de partículas, se usan unidades donde ℏ = c = 1. Entonces masa, energía, momento tienen todas dimensiones de [energía]. Convertir: 1 GeV = 1.783 × 10⁻²⁷ kg = 5.61 × 10²¹ Hz (en frecuencia).
- **Constante de Hubble vs parámetro de Hubble**: H₀ es el valor ACTUAL. H(z) varía con el tiempo. No usar H₀ para z alto.
- **Ecuación de Friedmann 2**: ä/a = -(4πG/3)(ρ + 3p/c²) + Λc²/3. La aceleración requiere Λc²/3 > (4πG/3)(ρ + 3p/c²). Para materia (p ≈ 0), Λ domina cuando ρ_Λ > ρₘ/2.
- **Corrimiento al rojo**: z = Δλ/λ_emitido = λ_obs/λ_emit - 1. NO es velocidad. Para z alto, usar relatividad completa. v = cz solo vale para z ≪ 1.
- **Plasma cuasi-neutral**: el plasma NO es neutro en escalas < λ_D. Solo es neutro en escalas >> λ_D. Esta es la condición fundamental para tratarlo como fluido (MHD).

## Verificación

- [ ] Diagrama Feynman: verificar que se conservan carga, número bariónico, número leptónico en cada vértice
- [ ] Modelo estándar: verificar que todos los hadrones son singletes de color (combinaciones r+g+b o q+anti-q de color-opuesto)
- [ ] Materia oscura vs energía oscura: verificar Ω_m + Ω_Λ + Ωᵣ + Ωₖ ≈ 1 (Planck 2018)
- [ ] Friedmann: verificar que para Λ = 0, k = 0, materia: a(t) ∝ t^(2/3)
- [ ] Para radiación dominante: a(t) ∝ t^(1/2)
- [ ] Para Λ dominante: a(t) ∝ e^(Ht) (exponencial, de Sitter)
- [ ] CMB: verificar T(z) = T₀(1+z) → a z = 1100, T ≈ 3000 K (desacoplamiento, recombinación)
- [ ] Longitud Debye: verificar dimensiones: [λ_D] = √([ε₀][k][T]/[n][e²]) = √([C²/N·m²][J][K⁻¹][K]/[m⁻³][C²]) = √([N·m]/[N/m³]) = √(m⁴) = m²... revisar: λ_D = √(ε₀kTₑ/(nₑe²)), unidades: √(C²/(N·m²) × J/(m⁻³ × C²)) = √(J·m³/(N·m²·m⁻³))... mejor: ε₀ en F/m = C²/(N·m²), kT en J = N·m, nₑ en m⁻³, e² en C². λ_D² = C²/(N·m²) × N·m/(m⁻³ × C²) = m⁴/m² = m². λ_D en metros ✓
- [ ] Frecuencia plasma: ωₚₑ = √(nₑe²/(ε₀mₑ)), unidades: √(m⁻³ × C²/(C²/(N·m²) × kg)) = √(N·m²/(m⁻³ × kg)) = √(kg·m/s² × m⁵/kg) = √(m⁶/s²) = m³/s... revisar: nₑe²/(ε₀mₑ) = m⁻³ × C²/(C²/(N·m²) × kg) = m⁻³ × N·m²/kg = m⁻³ × kg·m/s² × m²/kg = m⁻³ × m³/s² = 1/s². ωₚₑ = √(1/s²) = 1/s ✓
