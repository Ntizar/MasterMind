---
name: td-abatimientos-giros
description: Abatimiento, giros y cambio de plano en geometría descriptiva. Obtención de verdaderas magnitudes, distancias y ángulos.
tags: [stem, td, intermediate]
---

# Abatimientos, Giros y Cambio de Plano

## Referencias de autoridad

- **Ogura**: Geometría Morfológica, Editorial Reverté
- **Esquiroz**: Dibujo Geométrico, Editorial Paraninfo
- **Llagostera**: Geometría Descriptiva, Editorial Teide
- **Gili-Gau**: Geometría Descriptiva, Editorial UPC

## Abatimiento

### Concepto
- **Abatir** un plano es hacerlo coincidir con el plano de proyección girándolo alrededor de su traza
- Permite ver el plano en verdadera magnitud
- El abatimiento se hace sobre PH (abatimiento horizontal) o PV (abatimiento vertical)

### Abatimiento de un punto de un plano
1. **Identificar la traza de abatimiento (eje de giro)**: α₁ para abatimiento sobre PH, α₂ para abatimiento sobre PV
2. **Trazar la perpendicular** desde el punto a la traza de abatimiento
3. **Determinar la altura/desplazamiento** del punto respecto al plano de abatimiento
4. **Girar 90°** alrededor de la perpendicular hasta que el plano quede sobre el plano de proyección

### Regla práctica para abatimiento sobre PH
- **Punto A en el plano α**:
  1. Trazar por A una horizontal del plano (recta horizontal contenida en α)
  2. Abatir esa horizontal alrededor de α₁
  3. La perpendicular desde A' a α₁ se corta con la horizontal abatida en el punto abatido A₀

### Abatimiento de figuras planas
- Abatir el plano que contiene la figura
- Los puntos de la figura se abaten individualmente
- La figura abatida está en verdadera magnitud

### Aplicaciones del abatimiento
- Obtener VM de figuras planas
- Medir ángulos reales entre rectas de un plano
- Determinar distancias reales en un plano

## Giros

### Concepto
- **Giro**: rotación de un punto, recta o plano alrededor de un eje
- El eje de giro puede ser vertical, horizontal o de perfil
- En diédrico, el eje se representa por sus proyecciones

### Giro alrededor de eje vertical
- **Planta**: el punto gira en torno a la proyección del eje (un punto)
- **Alzado**: el punto se desplaza horizontalmente (misma altura)
- **Aplicación**: llevar una recta oblicua a frontal o horizontal

### Giro alrededor de eje horizontal
- **Alzado**: el punto gira en torno a la proyección del eje
- **Planta**: el punto se desplaza horizontalmente (misma profundidad)
- **Aplicación**: llevar una recta oblicua a frontal

### Giro para obtener VM
1. **Girar la recta** hasta que sea paralela a un plano de proyección
2. **Giro alrededor de eje vertical**: llevar la recta a frontal (paralela a PV)
3. **Giro alrededor de eje horizontal**: llevar la recta a horizontal (paralela a PH)
4. **VM**: la proyección en el plano paralelo muestra la VM

### Cambio de dirección del giro
- Si el giro no es suficiente, se puede cambiar de eje
- Se puede combinar giro vertical + giro horizontal

## Cambio de plano

### Concepto
- **Cambio de plano**: introducir un nuevo plano de proyección perpendicular a uno de los existentes
- Permite obtener nuevas proyecciones desde una perspectiva diferente
- El nuevo plano reemplaza al antiguo en la proyección

### Cambio de plano vertical
- **Nueva LT** (Línea de Tierra) se traza en posición conveniente
- **Nuevas proyecciones** se obtienen midiendo distancias desde la LT antigua
- **Regla**: la distancia del nuevo punto a la nueva LT = distancia del punto antiguo a la LT antigua (en la dirección perpendicular)

### Cambio de plano horizontal
- Similar al vertical, pero se cambia el plano horizontal
- **Nueva LT** se traza en posición conveniente
- **Nuevas proyecciones**: la distancia del nuevo punto a la nueva LT = distancia del punto antiguo a la LT antigua

### Aplicaciones del cambio de plano
- **Obtener VM de una recta**: nuevo plano paralelo a la recta
- **Obtener un punto de una recta**: nuevo plano perpendicular a la recta
- **Obtener un plano de canto**: nuevo plano perpendicular al plano
- **Obtener VM de un plano**: dos cambios de plano (primero de canto, luego paralelo)

### Reglas del cambio de plano
1. **Nuevo plano perpendicular** al existente
2. **Nueva LT** en posición conveniente
3. **Nueva proyección**: la distancia al nuevo plano se mide en la dirección perpendicular a la nueva LT
4. **La otra proyección** (la que no se cambia) se mantiene igual

## Combinación de métodos

### Abatimiento + Giro
- Abatir un plano y luego girar elementos del plano abatido
- Útil para figuras complejas

### Giro + Cambio de plano
- Girar una recta para hacerla paralela a un plano
- Cambiar de plano para obtener la VM
- Método más versátil que el giro solo

### Cambio de plano + Abatimiento
- Cambiar de plano para llevar un plano a posición de canto
- Abatir para ver en verdadera magnitud

## Errores comunes / Pitfalls

- **Abatimiento**: confundir la traza de abatimiento con la traza del plano. α₁ es la traza horizontal (eje de giro para abatimiento sobre PH)
- **Giros**: el eje de giro debe ser perpendicular al plano de proyección donde se gira
- **Cambio de plano**: el nuevo plano debe ser perpendicular al existente. Si no, no es un cambio de plano válido
- **Distancias en cambio de plano**: medir en dirección perpendicular a la nueva LT, no en cualquier dirección
- **VM**: verificar que la recta es realmente paralela al plano de proyección donde se mide

## Verificación

- [ ] Abatimiento: ¿el punto abatido está en la perpendicular a la traza?
- [ ] Giro: ¿el eje de giro es perpendicular al plano de proyección donde se gira?
- [ ] Cambio de plano: ¿el nuevo plano es perpendicular al existente?
- [ ] VM: ¿la recta es paralela al plano de proyección donde se mide?
- [ ] Distancia: ¿la perpendicular es realmente perpendicular a la recta/plano?
