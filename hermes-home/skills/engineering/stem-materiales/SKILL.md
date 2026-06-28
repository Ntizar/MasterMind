---
name: stem-materiales
description: Ciencia de materiales: estructura cristalina, diagramas de fase, ensayos mecánicos, deformación, fractura, tratamientos térmicos y selección de materiales.
tags: [stem, engineering, materials]
---

# Ciencia de Materiales

## Referencias de autoridad

- **Callister**: Materials Science and Engineering, 9ª edición, Wiley
- **Ashby & Jones**: Engineering Materials, 4ª edición, Butterworth-Heinemann
- **ASM Handbook**: Volume 1, Properties and Selection

## Estructura cristalina

### Sistemas cristalinos
- **Cúbica simple (SC)**: 1 átomo/celda, APF = 0,52
- **Cúbica centrada en el cuerpo (BCC)**: 2 átomos/celda, APF = 0,68
- **Cúbica centrada en las caras (FCC)**: 4 átomos/celda, APF = 0,74
- **Hexagonal compacta (HCP)**: 6 átomos/celda, APF = 0,74
- **APF** = Atomic Packing Factor = volumen átomos / volumen celda

### Planos y direcciones cristalinas
- **Notación de Miller**: (hkl) para planos, [uvw] para direcciones
- **Familias**: {hkl} = todos los planos equivalentes por simetría
- <uvw> = todas las direcciones equivalentes

### Defectos cristalinos
- **Puntuales**: vacantes, intersticiales, sustitucionales
- **Lineales**: dislocaciones (borde, tornillo, mixta)
- **Superficiales**: límites de grano, superficies
- **Volumétricos**: poros, grietas, inclusiones

### Dislocaciones
- **Dislocación de borde**: línea extra de átomos, b⊥ a la línea
- **Dislocación de tornillo**: desplazamiento helicoidal, b∥ a la línea
- **Esfuerzo de cizalla para mover dislocación**: τ = Gb/L
- **Endurecimiento por deformación**: aumento de densidad de dislocaciones

## Diagramas de fase

### Diagrama de fase binario simple
- **Líquido (L)**: fase fundida
- **α, β**: fases sólidas
- **Líquidus**: por encima, todo líquido
- **Solidus**: por debajo, todo sólido
- **Regla de la palanca**: fracción de fase = longitud del brazo opuesto / longitud total

#### Regla de la palanca
- f_α = (C_β - C_0)/(C_β - C_α)
- f_β = (C_0 - C_α)/(C_β - C_α)
- C_0 = composición global, C_α = composición fase α, C_β = composición fase β

### Tipos de diagramas
- **Eutéctico**: L → α + β a temperatura constante
- **Eutectoide**: γ → α + β a temperatura constante
- **Peritéctico**: L + α → β a temperatura constante
- **Solid solución completa**: miscibilidad total en estado sólido y líquido

### Transformaciones de fase
- **Nucleación homogénea**: ΔG* = 16πγ³/(3ΔG_v²)
- **Nucleación heterogénea**: ΔG*_het = ΔG*_hom · f(θ)
- **CCT (Continuous Cooling)**: curvas de enfriamiento continuo
- **TTT (Isothermal)**: curvas de transformación isotérmica

## Propiedades mecánicas

### Ensayo de tracción
- **Esfuerzo (σ)**: σ = F/A₀ (Pa)
- **Deformación (ε)**: ε = ΔL/L₀ (adimensional)
- **Límite elástico (σ_y)**: punto de deformación plástica
- **Resistencia a la tracción (UTS)**: máximo esfuerzo soportado
- **Energía de deformación**: área bajo la curva σ-ε
- **Módulo de Young**: E = σ/ε (zona elástica)

### Ductilidad
- **Elongación**: %EL = (L_f - L₀)/L₀ × 100
- **Reducción de área**: %RA = (A₀ - A_f)/A₀ × 100

### Dureza
- **Brinell (HB)**: d = 2D/(πD - √(D² - d²)) · P/(πDh)
- **Vickers (HV)**: HV = 1,854·P/d² (P en kgf, d en mm)
- **Rockwell (HR)**: escala B (esfera 1/16"), C (cono diamante 120°)
- **Correlación aproximada**: UTS (MPa) ≈ 3,45 × HB

### Tenacidad
- **Tenacidad a la fractura**: K_IC (MPa√m)
- **Criterio de fractura**: K_I ≥ K_IC → fractura
- K_I = Yσ√(πa) (Y = factor geométrico, a = longitud de grieta)
- **Energía de fractura**: G_IC = K_IC²/E' (E' = E para tensión plana)

### Fatiga
- **Curva S-N**: σ_a vs N (ciclos hasta fractura)
- **Límite de fatiga**: σ_e (para aceros, ~0,5·UTS)
- **Ecuación de Basquin**: σ_a = σ'_f(2N)^b
- **Crecimiento de grieta**: da/dN = C(ΔK)^m (Ley de Paris)

### Creep (fluencia)
- **Tercera etapa**: aceleración → fractura
- **Ecuación de Norton**: ε̇ = Aσⁿe^(-Q/RT)
- **Temperatura homologada**: T/T_m > 0,4 → creep significativo

## Tratamientos térmicos

### Recocido
- **Recocido completo**: austenitización + enfriamiento lento → ablandar
- **Recocido de normalizado**: enfriamiento al aire → grano fino
- **Recocido de recristalización**: eliminar endurecimiento por deformación

### Temple
- **Temple**: austenitización + enfriamiento rápido (agua/aceite)
- **Martensita**: fase metastable, muy dura y frágil
- **Profundidad de temple**: depende de la capacidad de templabilidad (Jomini)

### Temple y revenido
- **Revenido**: temple + calentamiento a T media → reducir fragilidad
- **Temple superficial**: inducción, llama, láser

### Transformación de austenita
- **Ferrita (α)**: BCC, C < 0,022%
- **Austenita (γ)**: FCC, C hasta 2,14%
- **Cementita (Fe₃C)**: 6,67% C, muy dura y frágil
- **Perlita**: α + Fe₃C en capas, ~0,8% C
- **Bainita**: transformación a T media, más tenaz que perlita
- **Martensita**: transformación sin difusión, muy dura

## Selección de materiales

### Diagrama de Ashby
- **E vs ρ**: rigidez vs densidad (aeroespacial)
- **σ_y vs ρ**: resistencia vs densidad
- **K_IC vs ρ**: tenacidad vs densidad
- **Índice de selección**: M = σ_y^(2/3)/ρ (viga ligera y resistente)

### Clasificación por aplicación
- **Estructurales**: aceros, aluminio, titanio, compuestos
- **Térmicos**: cerámicos, superaleaciones
- **Funcionales**: semiconductores, piezoeléctricos, superconductores
- **Corrosión**: acero inoxidable, titanio, níquel

## Errores comunes / Pitfalls

- **Regla de la palanca**: invertir los brazos. f_α usa el brazo OPUESTO a α
- **Límite elástico vs UTS**: σ_y < UTS. El material se deforma plásticamente antes del máximo
- **Temple**: enfriar demasiado rápido puede causar grietas. Elegir medio de temple adecuado
- **Fatiga**: el límite de fatiga NO existe para todos los materiales. Aluminio NO tiene límite claro
- **Creep**: solo significativo a T > 0,4·T_m (en Kelvin)

## Verificación

- [ ] APF: FCC = 0,74 (máximo para esferas iguales)
- [ ] Regla de la palanca: f_α + f_β = 1
- [ ] UTS ≈ 3,45 × HB para aceros al carbono
- [ ] K_I = Yσ√(πa). Verificar unidades: [MPa√m]
- [ ] Creep: T/T_m > 0,4 para que sea significativo
