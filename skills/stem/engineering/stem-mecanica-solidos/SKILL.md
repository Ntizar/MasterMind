---
name: stem-mecanica-solidos
description: Mecánica de sólidos: esfuerzos y deformaciones, círculo de Mohr, vigas (flechas, cortante, momento), columnas, torsión y teoría de la elasticidad.
tags: [stem, engineering, mechanics]
---

# Mecánica de Sólidos

## Referencias de autoridad

- **Beer & Johnston**: Mechanics of Materials, 7ª edición, McGraw-Hill
- **Hibbeler**: Mechanics of Materials, 10ª edición, Pearson
- **Timoshenko**: Strength of Materials, 3ª edición, Krieger

## Esfuerzos y deformaciones

### Esfuerzo normal
- σ = F/A (Pa = N/m²)
- σ > 0: tracción. σ < 0: compresión
- Esfuerzo promedio en sección transversal

### Esfuerzo cortante
- τ = V/A (Pa)
- Distribución no uniforme: τ = VQ/(It) para secciones rectangulares

### Deformación normal
- ε = ΔL/L₀ (adimensional)
- ε > 0: elongación. ε < 0: contracción

### Ley de Hooke
- σ = E·ε (zona elástica)
- E = módulo de Young (Pa)
- **Relación de Poisson**: ν = -ε_transversal/ε_longitudinal
  - ν ≈ 0,3 para metales, 0,33 para acero

### Esfuerzo cortante en torsión
- τ = T·r/J
- T = torque (N·m)
- r = radio (m)
- J = momento polar de inercia (m⁴)
- **Sección circular maciza**: J = πd⁴/32
- **Sección circular hueca**: J = π(dₒ⁴ - dᵢ⁴)/32

### Ángulo de giro en torsión
- φ = TL/(JG)
- G = módulo de cortante (Pa)
- G = E/(2(1+ν))

## Vigas

### Relación entre cargas, cortante y momento
- dV/dx = -w(x) (carga distribuida)
- dM/dx = V(x) (cortante)
- d²M/dx² = -w(x)

### Esfuerzo en vigas
- **Esfuerzo normal por flexión**: σ = -M·y/I
  - M = momento flector (N·m)
  - y = distancia al eje neutro (m)
  - I = momento de inercia (m⁴)
  - σ_max = M·c/I = M/S (S = módulo de sección)

- **Esfuerzo cortante**: τ = V·Q/(I·t)
  - Q = ∫_A'y dA = primer momento de área
  - t = espesor en el punto

### Momentos de inercia notables
- **Rectángulo** (base b, altura h): I_x = bh³/12, I_y = hb³/12
- **Círculo**: I = πd⁴/64
- **Círculo hueco**: I = π(dₒ⁴ - dᵢ⁴)/64
- **Teorema de ejes paralelos**: I = I_c + Ad²

### Flechas de vigas

#### Método de integración directa
- EI·d⁴y/dx⁴ = -w(x)
- EI·d³y/dx³ = V(x)
- EI·d²y/dx² = M(x)
- EI·dy/dx = θ(x) (rotación)
- EI·y = δ(x) (flecha)

#### Método de la función de singularidad (Macaulay)
- Usar funciones de Macaulay ⟨x-a⟩ⁿ
- ⟨x-a⟩ⁿ = 0 si x < a, (x-a)ⁿ si x ≥ a

#### Formulas de flechas (casos típicos)
- **Viga simplemente apoyada, carga P en el centro**: δ_max = PL³/(48EI)
- **Viga empotrada-libre, carga P en el extremo**: δ_max = PL³/(3EI)
- **Viga simplemente apoyada, carga distribuida w**: δ_max = 5wL⁴/(384EI)
- **Viga empotrada-libre, carga distribuida w**: δ_max = wL⁴/(8EI)

### Teoremas de área-momento
- **Primer teorema**: cambio de ángulo entre A y B = área del diagrama M/EI entre A y B
- **Segundo teorema**: desviación tangencial de B respecto a la tangente en A = momento del área del diagrama M/EI entre A y B respecto a B

## Círculo de Mohr

### Esfuerzo plano
- σ_x, σ_y, τ_xy
- **Esfuerzos principales**:
  - σ₁,₂ = (σ_x + σ_y)/2 ± √[((σ_x - σ_y)/2)² + τ_xy²]
- **Esfuerzo cortante máximo**: τ_max = √[((σ_x - σ_y)/2)² + τ_xy²]
- **Ángulo de planos principales**: tan(2θ_p) = 2τ_xy/(σ_x - σ_y)
- **Ángulo de cortante máximo**: tan(2θ_s) = -(σ_x - σ_y)/(2τ_xy)

### Círculo de Mohr (trazado)
- Centro: C = ((σ_x + σ_y)/2, 0)
- Radio: R = √[((σ_x - σ_y)/2)² + τ_xy²]
- Puntos: A(σ_x, -τ_xy), B(σ_y, τ_xy)
- **Esfuerzos principales**: σ₁ = C + R, σ₂ = C - R
- **Cortante máximo**: τ_max = R

### Criterios de fallo

#### Esfuerzo cortante máximo (Tresca)
- τ_max = (σ₁ - σ₃)/2 ≤ σ_y/2·FS
- FS = factor de seguridad

#### Esfuerzo distorsional (Von Mises)
- σ_vm = √[((σ₁ - σ₂)² + (σ₂ - σ₃)² + (σ₃ - σ₁)²)/2] ≤ σ_y/FS
- Para esfuerzo plano (σ₃ = 0): σ_vm = √(σ₁² - σ₁σ₂ + σ₂²)

## Columnas

### Esfuerzo crítico de Euler
- P_cr = π²EI/(KL)²
- K = factor de extremo:
  - Empotrado-libre: K = 2
  - Articulado-articulado: K = 1
  - Empotrado-articulado: K = 0,7
  - Empotrado-empotrado: K = 0,5
- **Longitud efectiva**: L_e = KL
- **Esbeltez**: λ = L_e/r (r = radio de giro = √(I/A))

### Fórmula de secante
- σ_max = (P/A)[1 + (ec/r²)·sec(π/2·√(P/P_cr))]
- e = excentricidad, c = distancia al borde

### Columnas cortas vs esbeltas
- **Corta**: λ < λ_c → fallo por fluencia
- **Esbelta**: λ > λ_c → fallo por pandeo
- **λ_c** = √(2π²E/σ_y)

## Errores comunes / Pitfalls

- **Esfuerzo cortante en vigas**: τ_max está en el eje neutro, NO en la fibra extrema
- **Círculo de Mohr**: τ_xy se toma negativo en el punto A (convención: cortante que gira en sentido horario es negativo)
- **Flechas**: verificar la condición de apoyo. Viga empotrada-libre tiene 16× más flecha que simplemente apoyada con la misma carga
- **Columnas**: usar K correcto según condiciones de extremo. K = 2 (empotrado-libre) es el más desfavorable
- **Von Mises**: para esfuerzo plano, σ₃ = 0. No olvidar esto

## Verificación

- [ ] Hooke: σ = Eε. Verificar unidades: [Pa] = [Pa]·[adimensional] ✓
- [ ] Torsión: τ = Tr/J. Verificar: [N·m]·[m]/[m⁴] = [N/m²] ✓
- [ ] Flecha viga centro: δ = PL³/(48EI). Verificar: [N]·[m³]/([N/m²]·[m⁴]) = [m] ✓
- [ ] Euler: P_cr = π²EI/(KL)². Verificar: [N/m²]·[m⁴]/[m²] = [N] ✓
- [ ] Mohr: σ₁ ≥ σ₂ ≥ σ₃. τ_max = (σ₁ - σ₃)/2
