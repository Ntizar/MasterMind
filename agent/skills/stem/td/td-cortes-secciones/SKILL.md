---
name: td-cortes-secciones
description: Cortes y secciones según ISO 128-4: cortes totales, parciales, escalados, semicortes, secciones, roturas y representaciones normalizadas.
tags: [stem, td, intermediate]
---

# Cortes y Secciones

## Referencias de autoridad

- **ISO 128-4**: Technical products documentation — General principles of representation — Section views
- **UNE-EN ISO 128-4**: Adaptación española
- **Barron-Bravo**: Dibujo Técnico, Editorial Paraninfo

## Corte total

### Definición
- Secciona completamente la pieza mediante un plano de corte
- Se representa la parte INTERIOR visible y la parte posterior eliminada
- **Línea de corte**: línea a trazos y puntos fina (o gruesa si se prefiere)
- **Flechas**: indican la dirección de visión
- **Hachuras**: relleno con líneas finas a 45° (o ángulo conveniente)

### Representación
- **Sección**: la parte cortada se rellena con hachuras
- **Parte posterior**: se representa con líneas continuas finas (lo que se ve detrás)
- **Hachuras**: 45° respecto a la horizontal, separación uniforme (7-10 mm)
- **Dirección de hachuras**: misma en todas las vistas de la misma pieza

### Reglas de hachuras
- **Ángulo**: 45° (o 30°/60° si 45° no es conveniente)
- **Separación**: uniforme, 7-10 mm (proporcional al tamaño de la pieza)
- **Pieza maciza**: NO se hachura (tornillos, ejes, pernos, pasadores NO se cortan longitudinalmente)
- **Materiales diferentes**: diferentes patrones de hachura

## Corte parcial (alma)

### Definición
- Solo se corta una parte de la pieza
- Se usa para mostrar detalles internos sin cortar toda la pieza
- **Límite del corte**: línea de rotura continua fina (a mano alzada) o ondulada

### Aplicaciones
- Piezas simétricas: cortar solo la mitad
- Mostrar detalles internos de una zona concreta
- Evitar hachurar zonas que no aportan información

## Semicorte

### Definición
- Mitad de la pieza en corte, mitad en vista exterior
- Se usa para piezas simétricas
- **Línea de separación**: eje de simetría (línea a trazos y puntos fina)

### Reglas
- La parte cortada se representa con hachuras
- La parte sin cortar se representa en vista exterior
- La línea de separación es siempre el eje de simetría

## Corte escalonado (en escalera)

### Definición
- El plano de corte cambia de dirección (varios planos paralelos)
- Se usa para piezas con elementos alineados en diferentes profundidades
- **No se representan las líneas de cambio de plano** en el corte

### Representación
- Flechas en cada dirección de corte
- Se representa como si todo estuviera en un solo plano
- Las líneas de cambio NO se dibujan

## Corte roturado

### Definición
- Sección mostrada directamente sobre la vista, sin desplazar
- Se usa para secciones pequeñas
- **Contorno**: línea continua gruesa
- **Hachuras**: como en cualquier sección

## Sección

### Definición
- Solo se representa la parte cortada, sin la parte posterior
- Se coloca fuera de la vista o roturada sobre ella
- **Contorno**: línea continua gruesa
- **Hachuras**: relleno con líneas finas

### Tipos de sección
- **Sección fuera de vista**: colocada junto a la vista, con línea de corte
- **Sección roturada**: sobre la vista misma
- **Sección interrumpida**: la vista se interrumpe para mostrar la sección

## Roturas

### Definición
- Se representa solo la parte interesante de la pieza, omitiendo la parte intermedia
- Se usa para piezas largas con sección constante

### Tipos de rotura
- **Rotura continua fina**: línea ondulada o a mano alzada
- **Rotura con líneas rectas**: para piezas prismáticas largas
- **Rotura en ejes**: para ejes largos con elementos repetidos

## Línea de corte

### Representación
- **Línea a trazos y puntos fina** (o gruesa): indica el plano de corte
- **Flechas**: indican la dirección de visión del corte
- **Letra**: identifica el corte (A-A, B-B, etc.)
- **Leyenda**: "Corte A-A" junto a la vista del corte

### Posición de la línea de corte
- Debe pasar por los elementos que se quieren mostrar
- Preferiblemente por ejes de simetría
- Evitar pasar por elementos que no aporten información

## Errores comunes / Pitfalls

- **Hachurar piezas macizas**: tornillos, ejes, pernos NO se hachuran si se cortan longitudinalmente
- **Hachuras**: ángulo 45° estándar, separación uniforme
- **Corte escalonado**: NO dibujar las líneas de cambio de plano
- **Semicorte**: la línea de separación es SIEMPRE el eje de simetría (trazos y puntos)
- **Sección**: solo se representa la parte cortada, no la parte posterior
- **Piezas macizas**: verificar la norma UNE sobre qué elementos NO se hachuran

## Verificación

- [ ] ¿Las hachuras son a 45° con separación uniforme?
- [ ] ¿Los ejes/tornillos se hachuran si se cortan longitudinalmente? (NO)
- [ ] ¿La línea de corte tiene flechas indicando la dirección de visión?
- [ ] ¿El semicorte tiene el eje de simetría como línea de separación?
- [ ] ¿El corte escalonado NO muestra las líneas de cambio de plano?
- [ ] ¿La sección solo muestra la parte cortada?
