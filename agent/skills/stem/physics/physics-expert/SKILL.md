---
name: physics-expert
description: Física experta: teoría cuántica de campos, física de partículas, cosmología y física de plasmas.
tags: [stem, physics, expert]
---

# Física Experta: Teoría Cuántica de Campos, Partículas, Cosmología y Plasmas

## Referencias de autoridad

- Michael E. Peskin y Daniel V. Schroeder, "An Introduction to Quantum Field Theory", Westview Press, 1995. ISBN 978-0-201-50397-5.
- Sean M. Carroll, "Spacetime and Geometry: An Introduction to General Relativity", Addison-Wesley, 2004. ISBN 978-0-8053-8732-2.
- James B. Hartle, "Gravity: An Introduction to Einstein's General Relativity", Addison-Wesley, 2003. ISBN 978-0-8053-8662-2.
- Norma ISO 80000-10:2019, "Quantities and units — Part 10: Quantum physics".

## Contenido clave

### Teoría Cuántica de Campos (Conceptos)

- **Principio de mínima acción**:
  - La dinámica de un sistema físico se determina minimizando (o más precisamente, haciendo estacionaria) la acción S.
  - Acción: S = ∫ L dt, donde L es el lagrangiano del sistema.
  - En teoría de campos: S = ∫ ℒ d⁴x = ∫ ℒ(φ, ∂μφ) d³x dt
  - Donde ℒ es la densidad lagrangiana y d⁴x = dt dx dy dz.
  - Las ecuaciones del movimiento se obtienen del principio variacional: δS = 0, lo que lleva a las ecuaciones de Euler-Lagrange:
    - ∂ℒ/∂φ - ∂μ(∂ℒ/∂(∂μφ)) = 0
  - Nota: Este principio unifica la mecánica clásica, la relatividad y la mecánica cuántica de campos.

- **Campos clásicos y cuantización**:
  - Un campo φ(x⃗, t) es una función que asigna un valor (escalar, vectorial o espinorial) a cada punto del espacio-tiempo.
  - La cuantización canónica promueve el campo y su momento conjugado π = ∂ℒ/∂(∂₀φ) a operadores que satisfacen relaciones de conmutación (campos bosónicos) o anticonmutación (campos fermiónicos):
    - [φ(x⃗, t), π(y⃗, t)] = iℏ · δ³(x⃗ - y⃗) (bosones)
    - {ψ_α(x⃗, t), ψ†_β(y⃗, t)} = δ_αβ · δ³(x⃗ - y⃗) (fermiones)
  - Nota: Los bosones obedecen la estadística de Bose-Einstein (varias partículas pueden ocupar el mismo estado); los fermiones obedecen la estadística de Fermi-Dirac (principio de exclusión de Pauli).

- **Lagrangianos fundamentales**:
  - Campo escalar libre (Klein-Gordon): ℒ = ½(∂μφ)(∂^μφ) - ½m²φ²
  - Ecuación resultante: (∂μ∂^μ + m²)φ = 0, es decir, (□ + m²)φ = 0
  - Campo de Dirac (fermiones): ℒ = ψ̄(iγ^μ∂_μ - m)ψ
  - Donde γ^μ son las matrices de Dirac y ψ̄ = ψ†γ⁰.
  - Electrodinámica cuántica (QED): ℒ_QED = ψ̄(iγ^μD_μ - m)ψ - ¼F_μνF^μν
  - Donde D_μ = ∂_μ + ieA_μ es la derivada covariante y F_μν = ∂_μA_ν - ∂_νA_μ es el tensor de campo electromagnético.
  - Nota: La interacción se introduce mediante el acoplamiento mínimo (reemplazar ∂_μ por D_μ).

- **Teorema de Noether**:
  - Cada simetría continua del lagrangiano implica una ley de conservación.
  - Simetría traslacional en el tiempo → conservación de la energía.
  - Simetría traslacional en el espacio → conservación del momento lineal.
  - Simetría rotacional → conservación del momento angular.
  - Simetría de gauge U(1) → conservación de la carga eléctrica.

- **Diagramas de Feynman**:
  - Representación gráfica de los términos en la expansión perturbativa de la matriz S (matriz de dispersión).
  - Líneas externas: partículas entrantes y salientes.
  - Líneas internas (propagadores): partículas virtuales intermedias.
  - Vértices: puntos de interacción. Cada vértice en QED aporta un factor -ieγ^μ.
  - Reglas de Feynman permiten calcular amplitudes de probabilidad a partir de los diagramas.

### Física de Partículas (Modelo Estándar)

- **Quarks**:
  - Fermiones de espín ½ que experimentan la interacción fuerte.
  - Sabores: arriba (u), abajo (d), encanto (c), extrañeza (s), cima (t), fondo (b).
  - Cargas eléctricas: u, c, t tienen carga +2/3 e; d, s, b tienen carga -1/3 e.
  - Cada quark tiene tres colores (rojo, verde, azul) y su antiquark tiene anticolor.
  - Los hadrones se componen de quarks:
    - Bariones: tres quarks (qqq), p. ej., protón = uud, neutrón = udd.
    - Mesones: quark-antiquark (q q̄), p. ej., π⁺ = u d̄.
  - Nota: Los quarks nunca se observan aislados (confinamiento de color).

- **Leptones**:
  - Fermiones de espín ½ que NO experimentan la interacción fuerte.
  - Tres generaciones:
    - Generación 1: electrón (e⁻), neutrino electrónico (νₑ)
    - Generación 2: muón (μ⁻), neutrino muónico (ν_μ)
    - Generación 3: tau (τ⁻), neutrino tauónico (ν_τ)
  - Los leptones cargados tienen carga -1 e; los neutrinos tienen carga 0.
  - Cada leptón tiene un antipartícula correspondiente (p. ej., positrón e⁺).
  - Nota: Los neutrinos tienen masa extremadamente pequeña pero no nula (oscilación de neutrinos).

- **Bosones de gauge (mediadores de interacciones)**:
  - Fotón (γ): mediador de la interacción electromagnética. Masa = 0. Espín = 1. Alcance infinito.
  - Bosones W⁺, W⁻, Z⁰: mediadores de la interacción débil. Masas: M_W ≈ 80,4 GeV/c², M_Z ≈ 91,2 GeV/c². Espín = 1. Alcance ≈ 10⁻¹⁸ m.
  - Gluones (g): mediadores de la interacción fuerte. Masa = 0. Espín = 1. Existencia de 8 tipos de gluones. Alcance ≈ 10⁻¹⁵ m (confinamiento).
  - Bosón de Higgs (H⁰): mediador del mecanismo de Brout-Englert-Higgs que da masa a las partículas elementales. Masa ≈ 125 GeV/c². Espín = 0. Descubierto en 2012 en el LHC (CERN).

- **Interacciones fundamentales** (de mayor a menor intensidad a escala atómica):
  1. Interacción fuerte: acoplamiento α_s ≈ 1. Actúa sobre quarks y gluones (carga de color). Alcance ≈ 10⁻¹⁵ m.
  2. Interacción electromagnética: constante de estructura fina α ≈ 1/137 ≈ 0,0073. Actúa sobre partículas cargadas. Alcance infinito.
  3. Interacción débil: acoplamiento α_w ≈ 10⁻⁶. Actúa sobre todos los fermiones. Responsable de la desintegración beta. Alcance ≈ 10⁻¹⁸ m.
  4. Gravedad: constante de acoplamiento G_N. Extremadamente débil a escala de partículas (≈ 10⁻³⁹ veces la fuerza electromagnética entre dos protones). Alcance infinito.

- **Simetrías y leyes de conservación**:
  - Número bariónico (B): se conserva en el Modelo Estándar. Los bariones tienen B = 1, los antibariones B = -1, los mesones B = 0.
  - Número leptónico por generación (Lₑ, L_μ, L_τ): se conserva aproximadamente (violado por oscilación de neutrinos).
  - Carga eléctrica (Q): se conserva siempre.
  - Paridad (P), conjugación de carga (C) y combinación CP: se violan en interacciones débiles.

### Cosmología

- **Expansión del universo y métrica de Friedmann-Lemaître-Robertson-Walker (FLRW)**:
  - La métrica describe un universo homogéneo e isótropo en expansión:
    - ds² = -c²dt² + a(t)² [dr²/(1 - kr²) + r²(dθ² + sen²θ dφ²)]
  - Donde a(t) es el factor de escala y k es la curvatura espacial (k = 0: plano; k > 0: cerrado; k < 0: abierto).
  - El corrimiento al rojo cosmológico: 1 + z = a(t_obs) / a(t_em) = a₀ / a(t_em)
  - Nota: El corrimiento al rojo no es un efecto Doppler, sino una consecuencia de la expansión del espacio mismo.

- **Ecuaciones de Friedmann**:
  - Primera ecuación de Friedmann:
    - H² = (8πG/3)·ρ - kc²/a² + Λc²/3
  - Segunda ecuación de Friedmann:
    - ä/a = -(4πG/3)·(ρ + 3p/c²) + Λc²/3
  - Donde H = ȧ/a es el parámetro de Hubble, ρ la densidad de energía total, p la presión, G la constante gravitacional y Λ la constante cosmológica.
  - Ecuación de continuidad: ρ̇ + 3H(ρ + p/c²) = 0
  - Nota: Para materia no relativista, p ≈ 0 y ρ ∝ a⁻³. Para radiación, p = ρc²/3 y ρ ∝ a⁻⁴. Para energía oscura (Λ), ρ = constante.

- **Parámetro de Hubble y edad del universo**:
  - H₀ ≈ 67,4 km/(s·Mpc) (valor de Planck 2018).
  - 1 Mpc (megaparsec) ≈ 3,086 × 10²² m ≈ 3,26 millones de años-luz.
  - Edad aproximada del universo (modelo ΛCDM): t₀ ≈ 13,8 mil millones de años.
  - Nota: La tensión de Hubble (diferencia entre mediciones locales y del CMB) es un problema abierto.

- **Fondo cósmico de microondas (CMB)**:
  - Radiación fósil emitida cuando el universo tenía ≈ 380 000 años (época de recombinación).
  - Temperatura actual: T₀ ≈ 2,725 K.
  - Espectro de cuerpo negro casi perfecto.
  - Anisotropías de temperatura del orden de ΔT/T ≈ 10⁻⁵.
  - Las anisotropías reflejan fluctuaciones de densidad primordiales que dieron origen a la estructura a gran escala del universo.

- **Materia oscura**:
  - Evidencia: curvas de rotación galáctica planas, lentes gravitacionales, estructura a gran escala, anisotropías del CMB.
  - Constituye ≈ 27% de la densidad de energía del universo actual (Ω_dm ≈ 0,27).
  - No interactúa electromagnéticamente (no emite, absorbe ni refleja luz).
  - Se clasifica en: materia oscura fría (CDM, movimiento no relativista), caliente (HDM, p. ej., neutrinos) y tibia (WDM).
  - Candidatos: WIMPs (partículas masivas de interacción débil), axiones, MACHOs.
  - Nota: La materia oscura es diferente de la materia bariónica ordinaria (estrellas, planetas, gas).

- **Energía oscura**:
  - Constituye ≈ 68% de la densidad de energía del universo actual (Ω_Λ ≈ 0,68).
  - Responsable de la aceleración de la expansión cósmica (descubierta en 1998 mediante observaciones de supernovas tipo Ia).
  - La interpretación más simple es la constante cosmológica Λ (energía del vacío).
  - Presión negativa: p_Λ = -ρ_Λc². Esta presión negativa impulsa la aceleración.
  - Alternativas: quintessence (campo escalar dinámico), modificaciones de la relatividad general.
  - Nota: La naturaleza de la energía oscura es uno de los mayores problemas abiertos de la física.

- **Composición del universo actual (modelo ΛCDM)**:
  - Energía oscura: ≈ 68%
  - Materia oscura: ≈ 27%
  - Materia bariónica (ordinaria): ≈ 5%
  - Nota: Los porcentajes se refieren a la densidad de energía total del universo.

### Física de Plasmas Básica

- **Definición de plasma**:
  - Un plasma es un gas ionizado compuesto de iones positivos, electrones libres y posiblemente átomos neutros.
  - Se considera plasma si cumple el criterio de cuasineutralidad: la densidad de cargas positivas y negativas se compensan a gran escala (n₊ ≈ n₋).
  - Es el cuarto estado de la materia (además de sólido, líquido y gaseoso).
  - Más del 99% de la materia visible del universo está en estado de plasma (estrellas, nebulosas, viento solar).

- **Criterio de plasma**:
  - El número de partículas en la esfera de Debye (N_D) debe ser mucho mayor que 1: N_D >> 1.
  - La longitud de Debye (λ_D) caracteriza la escala de apantallamiento de cargas:
    - λ_D = √(ε₀·kT / (nₑ·e²)) (para plasma de electrones e iones)
  - Nota: Si λ_D es pequeña comparada con las dimensiones del sistema, el plasma apantalla eficazmente los campos eléctricos.

- **Frecuencia de plasma (electrones)**:
  - ω_pe = √(nₑ·e² / (ε₀·mₑ))
  - Nota: Si una perturbación eléctrica intenta perturbar el plasma, los electrones oscilan a esta frecuencia para restaurar la cuasineutralidad.

- **Temperatura de ionización y grado de ionización**:
  - Ecuación de Saha (equilibrio de ionización):
    - nₑ·nᵢ / nₙ = (2πmₑkT/h²)^(3/2) · (2Zᵢ/Zₙ) · exp(-E_ion / kT)
  - Donde nₑ, nᵢ, nₙ son las densidades de electrones, iones y átomos neutros, y E_ion es la energía de ionización.
  - Nota: A temperaturas muy altas, el plasma está completamente ionizado; a temperaturas bajas, es neutro.

- **Magnetohidrodinámica (MHD)**:
  - Describe el plasma como un fluido conductor en presencia de campos electromagnéticos.
  - Ecuaciones fundamentales: ecuaciones de continuidad, ecuación de movimiento (Navier-Stokes con fuerza de Lorentz), ecuaciones de Maxwell.
  - Fuerza de Lorentz por unidad de volumen: f⃗ = ρ_c·E⃗ + J⃗ × B⃗
  - Número de plasma β = p_térmica / p_magnética = (n·kT) / (B²/(2μ₀))
  - Si β << 1: el campo magnético domina el comportamiento del plasma.
  - Si β >> 1: la presión térmica domina.

- **Tipos de ondas en plasmas**:
  - Ondas de Langmuir (ondas de plasma electrónico): oscilaciones longitudinales de electrones.
  - Ondas ion-acústicas: ondas de presión en el plasma donde los electrones proporcionan la presión y los iones la inercia.
  - Ondas Alfvén: ondas transversales magnetohidrodinámicas que se propagan a lo largo de las líneas del campo magnético.
  - Velocidad de Alfvén: v_A = B / √(μ₀·ρ_m)
  - Donde ρ_m es la densidad de masa del plasma.

## Unidades y sistema SI

- Energía en física de partículas: electrón-voltio (eV). 1 eV = 1,602 × 10⁻¹⁹ J.
  - keV = 10³ eV; MeV = 10⁶ eV; GeV = 10⁹ eV; TeV = 10¹² eV.
- Masa en física de partículas: GeV/c².
  - Masa del protón: ≈ 0,938 GeV/c². Masa del electrón: ≈ 0,511 MeV/c².
  - Masa del bosón W: ≈ 80,4 GeV/c². Masa del bosón Z: ≈ 91,2 GeV/c².
  - Masa del bosón de Higgs: ≈ 125 GeV/c².
- Constante gravitacional: G ≈ 6,674 × 10⁻¹¹ N·m²/kg².
- Constante cosmológica: Λ ≈ 1,1 × 10⁻⁵² m⁻².
- Densidad crítica del universo: ρ_c = 3H₀²/(8πG) ≈ 9,2 × 10⁻²⁷ kg/m³.
- Parámetro de Hubble: H₀ ≈ 67,4 km/(s·Mpc).
  - 1 Mpc = 3,086 × 10²² m.
- Temperatura del CMB: T₀ ≈ 2,725 K.
- Constante de Stefan-Boltzmann: σ = π²k⁴/(60ℏ³c²) ≈ 5,670 × 10⁻⁸ W/(m²·K⁴).
- Nota sobre unidades naturales: en muchas áreas de física de partículas y cosmología se usan unidades naturales donde ℏ = c = 1. En este sistema, la masa, la energía y el momento tienen la misma dimensión (generalmente eV o GeV). La longitud y el tiempo tienen dimensión inversa de energía: [L] = [T] = [E]⁻¹.

## Errores comunes / Pitfalls

- **Interpretar mal diagramas de Feynman**: Los diagramas de Feynman representan términos en una expansión perturbativa, no trayectorias reales de partículas. Las líneas internas corresponden a partículas virtuales (que no satisfacen la relación energía-momento E² = p²c² + m²c⁴). Cada vértice y línea tiene reglas de asignación de amplitud específicas. No interpretar las líneas como trayectorias clásicas.

- **Confundir materia oscura con energía oscura**: Son fenómenos distintos. La materia oscura ejerce atracción gravitatoria y aglutina estructuras (galaxias, cúmulos). La energía oscura ejerce presión negativa y acelera la expansión del universo a gran escala. La materia oscura domina a escalas galácticas y supra-galácticas; la energía oscura domina a escalas cosmológicas. Juntas constituyen ≈ 95% del contenido del universo, pero la materia oscura es ≈ 27% y la energía oscura ≈ 68%.

- **Unidades naturales**: En unidades naturales (ℏ = c = 1), la masa, energía, momento y temperatura se expresan en eV (o múltiplos). La longitud y el tiempo se expresan en eV⁻¹. Para convertir a unidades SI: 1 eV⁻¹ ≈ 1,973 × 10⁻⁷ m (longitud) y ≈ 6,582 × 10⁻¹⁶ s (tiempo). Confundir estas conversiones lleva a errores numéricos enormes.

- **Ecuaciones de Friedmann**: Es fácil olvidar el término de curvatura (kc²/a²) o la constante cosmológica (Λc²/3). La primera ecuación de Friedmann incluye tres contribuciones a la tasa de expansión: densidad de energía, curvatura y constante cosmológica. La segunda ecuación muestra que la aceleración (ä) depende de ρ + 3p/c²: la presión contribuye a la gravedad en relatividad general.

- **Corrimiento al rojo cosmológico vs. Doppler**: El corrimiento al rojo cosmológico z = Δλ/λ no es un efecto Doppler clásico. Es consecuencia de la expansión del espacio entre la emisión y la recepción. Para z pequeño, la aproximación v ≈ c·z funciona, pero para z grande debe usarse la relación cosmológica completa 1 + z = a₀/a_em.

- **Cuantización de campos**: No confundir la cuantización canónica (promover campos a operadores) con la cuantización por integrales de camino (S = ∫ℒ d⁴x en la formulación de integrales funcionales). Ambas son equivalentes pero dan lugar a herramientas computacionales diferentes.

## Verificación

- [ ] En teoría cuántica de campos, ¿las ecuaciones de Euler-Lagrange para campos tienen la forma correcta: ∂ℒ/∂φ - ∂μ(∂ℒ/∂(∂μφ)) = 0?
- [ ] En el Modelo Estándar, ¿los quarks tienen carga fraccionaria (±1/3 e o ±2/3 e) y los leptones carga entera (0 o ±1 e)?
- [ ] En cosmología, ¿las ecuaciones de Friedmann son dimensionalmente consistentes? (H² tiene unidades de 1/t²; 8πGρ/3 también).
- [ ] ¿Se distingue correctamente entre materia oscura (atractiva, aglutina) y energía oscura (repulsiva, expande)?
- [ ] En física de plasmas, ¿el criterio de cuasineutralidad se cumple (N_D >> 1)?
- [ ] En diagramas de Feynman, ¿se recuerda que las partículas internas son virtuales (fuera de la capa de masa)?
- [ ] En unidades naturales, ¿se aplican correctamente las conversiones a unidades SI cuando es necesario?
- [ ] ¿Los porcentajes de la composición del universo (68% energía oscura, 27% materia oscura, 5% bariónica) suman 100%?
