---
name: td-perspectivas
description: Perspectivas axonométricas: isométrica (cabañera), caballera (oblicua), dimétrica, monométrica. Círculos como elipses, reducción de ejes, representación de piezas.
tags: [stem, td, intermediate]
---

# Perspectivas Axonométricas

## Referencias de autoridad

- **Ogura**: Geometría Morfológica, Editorial Reverté
- **Esquiroz**: Dibujo Geométrico, Editorial Paraninfo
- **ISO 5456**: Technical drawings — Axonometric views
- **Llagostera**: Geometría Descriptiva, Editorial Teide

## Perspectiva isométrica (cabañera)

### Ejes
- Los tres ejes forman 120° entre sí
- En papel: X e Y a 30° de la horizontal, Z vertical
- **Reducción isométrica teórica**: 0,82 (factor de reducción √(2/3))
- **En la práctica**: se usa reducción 1 (isométrica reducida). Las cotas son las reales
- **Error común**: usar 0,82 en vez de 1. Solo se usa 0,82 si se exige rigor geométrico

### Representación de círculos
- En isométrica, los círculos se representan como **elipses**
- **Eje mayor**: perpendicular al plano isométrico correspondiente
- **Eje menor**: paralelo al plano isométrico correspondiente
- **Eje mayor ≈ 1,22·D** (isométrica reducida)
- **Eje menor ≈ 0,7·D** (isométrica reducida)
- **Método de los 4 centros**: aproximar la elipse con 4 arcos de circunferencia

### Círculos en las caras
- **Cara XY** (horizontal): eje mayor a 30° de la horizontal
- **Cara XZ** (vertical frontal): eje mayor vertical
- **Cara YZ** (vertical lateral): eje mayor a 150° de la horizontal

## Perspectiva caballera

### Ejes
- Un eje perpendicular al plano de dibujo (eje Z, vertical)
- Dos ejes en el plano: X horizontal, Y oblicuo
- **Ángulo del eje Y**: 30°, 45° o 60° (45° es más común)
- **Reducción del eje Y**:
  - **Caballera normal**: 0,5 (la más usada en la práctica)
  - **Caballera simplificada**: 1 (más fácil de dibujar)
- **Z**: siempre vertical, sin reducción

### Representación de círculos
- Los círculos en el plano perpendicular (XY o XZ) se representan como elipses
- Los círculos en el plano paralelo (YZ) se representan en verdadera magnitud
- **Elipse en plano paralelo**: eje mayor ≈ 1,29·D, eje menor ≈ 0,55·D (caballera normal)

## Perspectiva dimétrica

### Ejes
- Dos ejes con la misma escala, el tercero diferente
- **Ángulos típicos**: 7° y 42° respecto a la horizontal
- **Reducciones típicas**: 1, 1, 0,5 o 1, 1, 0,75
- Menos común que isométrica y caballera

## Perspectiva monométrica

### Ejes
- Solo un eje perpendicular al plano de dibujo
- Los otros dos en el plano (X horizontal, Y vertical)
- Muy poco usada en la práctica

## Perspectiva caballera con cara frontal verdadera

### Principio
- La cara frontal (YZ) se representa en verdadera magnitud
- Se usa mucho en dibujo industrial
- Los ejes X e Y salen de la cara frontal con ángulo de 45° y reducción 0,5

## Representación de piezas

### Principios
- Elegir la dirección de observación que mejor muestre la forma
- Colocar la cara más característica en la posición frontal
- No dibujar líneas ocultas (salvo que sean esenciales)
- Usar líneas de cota para dimensiones importantes

### Piezas con elementos cilíndricos
- Los cilindros se representan como elipses en la vista isométrica/caballera
- Los taladros: dibujar el círculo en la cara frontal, elipses en las caras laterales
- **Pitfall**: no olvidar dibujar las líneas de intersección entre cilindros

## Errores comunes / Pitfalls

- **Reducción isométrica**: usar 0,82 solo si se exige rigor. En la práctica se usa 1
- **Ejes isométricos**: los tres ejes forman 120° entre sí, NO 90°
- **Elipses isométricas**: el eje mayor es PERPENDICULAR al plano isométrico, no paralelo
- **Caballera**: el eje oblicuo suele ser 45°, no 30° ni 60° (aunque se pueden usar)
- **Líneas ocultas**: NO se dibujan en perspectiva (salvo que sean esenciales para la comprensión)
- **Círculos en YZ (caballera)**: se representan en verdadera magnitud, NO como elipses

## Verificación

- [ ] Isométrica: ¿los tres ejes forman 120°?
- [ ] Isométrica: ¿la reducción es 1 (práctica) o 0,82 (rigor)?
- [ ] Caballera: ¿el eje oblicuo es 45°? ¿la reducción es 0,5?
- [ ] Elipses: ¿el eje mayor es perpendicular al plano isométrico?
- [ ] Círculos en YZ (caballera): ¿se representan en verdadera magnitud?
