---
name: physics-optica
description: Óptica geométrica: reflexión, refracción, ley de Snell, lentes delgadas, espejos, instrumentos ópticos. Óptica ondulatoria: interferencia, difracción, polarización.
tags: [stem, physics, intermediate]
---

# Óptica

## Óptica geométrica

### Reflexión
- **Ley de reflexión**: θ_i = θ_r (ángulo de incidencia = ángulo de reflexión)
- θ medido respecto a la normal a la superficie
- Reflexión especular: superficie lisa. Difusa: superficie rugosa

### Refracción (Ley de Snell)
- n₁·sen(θ₁) = n₂·sen(θ₂)
- n = c/v = índice de refracción
- n_agua ≈ 1,33, n_vidrio ≈ 1,5, n_diamante ≈ 2,42, n_aire ≈ 1,0003
- La luz se desvía HACIA la normal al pasar a un medio más denso

### Reflexión total interna
- Se produce cuando θ₁ > θ_c (ángulo crítico)
- sen(θ_c) = n₂/n₁ (n₁ > n₂, de más denso a menos denso)
- Aplicación: fibras ópticas

### Espejos

#### Espejo plano
- Imagen virtual, del mismo tamaño, lateralmente invertida
- d_imagen = -d_objeto (virtual, detrás del espejo)

#### Espejo cóncavo (convergente)
- **Ecuación**: 1/f = 1/d_o + 1/d_i
- f > 0 (focal real, frente al espejo)
- R = 2f (radio de curvatura)
- Aumento: m = -d_i/d_o = h_i/h_o
- Si d_o > f: imagen real, invertida
- Si d_o < f: imagen virtual, derecha, ampliada

#### Espejo convexo (divergente)
- f < 0 (focal virtual, detrás del espejo)
- Imagen SIEMPRE virtual, derecha, reducida

### Lentes delgadas

#### Ecuación de lentes
- 1/f = 1/d_o + 1/d_i
- f > 0: lente convergente (biconvexa)
- f < 0: lente divergente (bicóncava)

#### Aumento
- m = h_i/h_o = -d_i/d_o
- m > 0: imagen derecha. m < 0: imagen invertida
- |m| > 1: ampliada. |m| < 1: reducida

#### Potencia de una lente
- P = 1/f (en dioptrías, D = 1/m)
- Lentes en contacto: P_total = P₁ + P₂

#### Combinación de lentes
- d_o₂ = d - d_i₁ (d = distancia entre lentes)
- m_total = m₁ · m₂

### Instrumentos ópticos

#### Ojo humano
- Distancia mínima de visión distinta: ~25 cm (punto próximo)
- Distancia mínima de visión nítida: ~25 cm
- Defectos: miopía (lente divergente), hipermetropía (lente convergente), astigmatismo (lente cilíndrica)

#### Lupa (lente simple)
- m ≈ 25/f + 1 (imagen en el punto próximo)
- m ≈ 25/f (imagen en el infinito)

#### Microscopio compuesto
- m_total = m_objetiva · m_ocular
- m_obj = -d_i_obj/f_obj (≈ -16 cm/f_obj)
- m_oc = 25/f_oc (cm)

#### Telescopio refractor
- m = -f_obj/f_oc (magnificación angular)
- Resolución: θ = 1,22·λ/D (criterio de Rayleigh)

## Óptica ondulatoria

### Interferencia

#### Doble rendija (Young)
- **Máximos**: d·sen(θ) = mλ (m = 0, ±1, ±2, ...)
- **Mínimos**: d·sen(θ) = (m + ½)λ
- En pantalla: y_m = mλL/d (si θ pequeño)
- Separación entre máximos: Δy = λL/d

#### Películas delgadas
- Máximo constructivo: 2nt = mλ (con reflexión de cambio de fase)
- Mínimo destructivo: 2nt = (m + ½)λ
- Cambio de fase de π al reflejarse en medio más denso

### Difracción

#### Rendija simple
- **Mínimos**: a·sen(θ) = mλ (m = ±1, ±2, ...)
- a = ancho de la rendija
- La luz se dispersa al pasar por una rendija estrecha

#### Red de difracción
- d·sen(θ) = mλ (máximos)
- d = distancia entre rendijas (1/N, N = líneas por unidad de longitud)
- Más líneas → mayor dispersión

### Polarización

- **Luz no polarizada**: vibraciones en todas las direcciones perpendiculares a la propagación
- **Luz polarizada linealmente**: vibraciones en un solo plano
- **Ley de Malus**: I = I₀·cos²(θ)
- Polarización por reflexión: ángulo de Brewster tan(θ_B) = n₂/n₁
- La luz reflejada está completamente polarizada perpendicularmente al plano de incidencia

## Errores comunes / Pitfalls

- **Snell**: n₁sen(θ₁) = n₂sen(θ₂). θ medido respecto a la NORMAL, no a la superficie
- **Ángulo crítico**: solo existe si n₁ > n₂ (de más denso a menos denso)
- **Espejo cóncavo**: f > 0. Si d_o < f, la imagen es virtual (d_i < 0)
- **Lentes**: convergente f > 0, divergente f < 0. Convención de signos CRÍTICA
- **Interferencia Young**: máximos en d·sen(θ) = mλ, mínimos en (m+½)λ. No confundir
- **Difracción**: mínimos en a·sen(θ) = mλ (NO máximos)
- **Resolución**: θ = 1,22λ/D. Mayor D → mejor resolución (menor θ)

## Verificación

- [ ] Snell: si n₂ > n₁, θ₂ < θ₁ (se acerca a la normal)
- [ ] Espejo cóncavo: si d_o = 2f, imagen real, invertida, del mismo tamaño
- [ ] Lente convergente: si d_o > f, imagen real. Si d_o < f, virtual
- [ ] Interferencia: máximos = mλ, mínimos = (m+½)λ
- [ ] Difracción: mínimo central más ancho que los laterales
- [ ] Polarización: I = I₀cos²(θ). Si θ = 90°, I = 0
