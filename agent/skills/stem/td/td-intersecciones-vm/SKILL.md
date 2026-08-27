---
name: td-intersecciones-vm
description: Intersecciones en geometría descriptiva: recta-plano, plano-plano, recta-recta. Verdadera magnitud de segmentos y ángulos.
tags: [stem, td, intermediate]
---

# Intersecciones y Verdadera Magnitud

## Referencias de autoridad

- **Ogura**: Geometría Morfológica, Editorial Reverté
- **Esquiroz**: Dibujo Geométrico, Editorial Paraninfo
- **Llagostera**: Geometría Descriptiva, Editorial Teide

## Intersección recta-plano

### Método general
1. **Plano de corte**: tomar un plano auxiliar β que contenga a la recta r
   - Lo más sencillo: plano de canto (perpendicular a PH o PV)
2. **Intersección β con α**: encontrar la recta i = α ∩ β
   - Encontrar las trazas de i (Th_i ∈ α₁ ∩ β₁ y Tv_i ∈ α₂ ∩ β₂)
3. **Intersección r con i**: el punto I = r ∩ i es la intersección buscada
   - I' = r' ∩ i' e I = r ∩ i

### Casos particulares
- **Plano oblicuo**: usar plano de corte de canto
- **Plano de canto**: la intersección es directa (α₁ es una línea)
- **Plana horizontal**: la intersección se encuentra por proyección directa

## Intersección plano-plano

### Método general
1. **Punto A = α ∩ β**: intersección con un plano auxiliar
   - Usar un plano de corte γ
   - i₁ = α ∩ γ y i₂ = β ∩ γ
   - A = i₁ ∩ i₂
2. **Punto B = α ∩ β**: repetir con otro plano de corte δ
3. **Recta de intersección**: r = AB

### Casos particulares
- **Dos planos paralelos a LT**: sus trazas son paralelas entre sí
- **Un plano horizontal y uno frontal**: la intersección es una recta de perfil
- **Dos planos de canto**: la intersección es una recta horizontal o frontal

## Intersección recta-recta

### Rectas que se cortan
- I' = r₁' ∩ r₂' e I = r₁ ∩ r₂
- Las proyecciones deben coincidir en la misma vertical

### Rectas que se cruzan (no se cortan)
- I' = r₁' ∩ r₂' pero I ≠ r₁ ∩ r₂ (no están en la misma vertical)
- **Puntos cruzados**: dos puntos que tienen la misma proyección en un plano pero distinta en el otro
  - **Cruzados horizontales**: misma proyección en planta, distinta en alzado
  - **Cruzados verticales**: misma proyección en alzado, distinta en planta

## Verdadera Magnitud (VM)

### Segmento en VM
- Un segmento está en VM cuando la recta que lo contiene es paralela al plano de proyección
- **Recta horizontal**: VM en planta
- **Recta frontal**: VM en alzado
- **Recta oblicua**: se obtiene VM por giro o cambio de plano

### Método del giro
1. **Girar la recta** hasta que sea horizontal o frontal
2. **Centro de giro**: la proyección donde la recta es visible (planta si se quiere VM en planta)
3. **Giro**: girar la proyección hasta que sea paralela a la LT
4. **VM**: la otra proyección muestra la verdadera magnitud

### Método del cambio de plano
1. **Nuevo plano de proyección** paralelo a la recta
2. **Nueva línea de tierra** paralela a la proyección de la recta
3. **Nueva proyección**: muestra la VM

### Ángulo de una recta con los planos
- **Ángulo con PH (α)**: ángulo que forma la recta con su proyección en PH
  - Se obtiene en VM de la recta
- **Ángulo con PV (β)**: ángulo que forma la recta con su proyección en PV
  - Se obtiene en VM de la recta

### Ángulo entre dos rectas
- **Se cortan**: llevar ambas a VM (giro o cambio de plano)
- **Se cruzan**: tomar un punto de una y trazar una paralela a la otra
  - Luego llevar a VM

### Ángulo entre dos planos
- **Plano secante**: tomar un plano perpendicular a la recta de intersección
- **Plano de canto**: si uno de los planos es de canto, el ángulo se ve directamente
- **VM del ángulo**: se obtiene por cambio de plano perpendicular a la recta de intersección

### Distancia de un punto a una recta
1. **VM de la recta**: llevar la recta a VM
2. **Distancia perpendicular**: trazar la perpendicular desde el punto a la recta en VM
3. **La VM de esta perpendicular** es la distancia real

### Distancia de un punto a un plano
1. **Plano de canto**: llevar el plano a posición de canto (cambio de plano)
2. **Distancia**: la distancia del punto a la traza del plano en esa posición
3. **La distancia es perpendicular al plano**

## Errores comunes / Pitfalls

- **Plano de corte**: debe contener a la recta y ser de canto (para simplificar)
- **Puntos cruzados**: no confundir con puntos que se cortan. Verificar que estén en la misma vertical
- **VM**: solo se obtiene cuando la recta es paralela al plano de proyección
- **Giros**: el centro de giro está en la proyección donde se gira (planta para VM en planta)
- **Ángulo entre planos**: se mide en un plano perpendicular a la recta de intersección
- **Distancia punto-recta**: la perpendicular debe trazarse en VM

## Verificación

- [ ] Intersección recta-plano: ¿el punto I está en r y en α?
- [ ] Intersección plano-plano: ¿la recta de intersección está en ambos planos?
- [ ] VM: ¿la recta es paralela al plano de proyección donde se mide?
- [ ] Ángulo entre planos: ¿se mide en un plano perpendicular a la recta de intersección?
- [ ] Distancia: ¿la perpendicular es realmente perpendicular?
