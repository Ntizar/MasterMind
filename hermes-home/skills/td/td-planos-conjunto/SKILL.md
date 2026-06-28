---
name: td-planos-conjunto
description: Planos de conjunto: despiece, lista de piezas, marcas, vistas de montaje, vistas explosivas, normalización industrial y representación de piezas complejas.
tags: [stem, td, advanced]
---

# Planos de Conjunto

## Referencias de autoridad

- **ISO 128-31**: Technical products documentation — Section views — Details and detail views
- **ISO 10605**: Technical product documentation — General principles for assembly drawings
- **UNE 1-041-88**: Planos de conjunto
- **Barron-Bravo**: Dibujo Técnico, Editorial Paraninfo

## Plano de conjunto

### Definición
- Representación de un montaje con todas las piezas ensambladas
- Muestra cómo se relacionan las piezas entre sí
- Incluye: vistas del conjunto, cotas generales, lista de piezas, notas

### Vistas del conjunto
- **Vista principal**: la que mejor muestra el conjunto
- **Vistas adicionales**: las necesarias para entender el montaje
- **Cortes**: para mostrar elementos internos y su relación
- **Vistas explosivas**: para mostrar el orden de montaje/desmontaje

## Despiece

### Definición
- Representación individual de cada pieza del conjunto
- Cada pieza se representa con sus vistas, cotas y tolerancias
- Se numera cada pieza con una marca (referencia)

### Representación
- **Piezas estándar** (tornillos, tuercas, arandelas): no se representan en despiece (solo en lista)
- **Piezas especiales**: se representan con todas las vistas necesarias
- **Piezas fabricadas**: se cotan completamente

## Lista de piezas

### Estructura
| Nº | Marca | Descripción | Cantidad | Material | Observaciones |
|---|---|---|---|---|---|
| 1 | 001 | Eje principal | 1 | C45 | |
| 2 | 002 | Cojinete | 2 | 6205-2RS | |
| 3 | 003 | Tapa | 1 | Aluminio 6061 | |

### Elementos
- **Nº**: número de orden
- **Marca**: referencia única de la pieza
- **Descripción**: nombre de la pieza
- **Cantidad**: número de unidades
- **Material**: material de fabricación
- **Observaciones**: notas especiales

### Piezas estándar
- **Norma**: indicar la norma (ISO, DIN, UNE)
- **Ejemplo**: Tornillo ISO 4014-M6×20
- **Código**: indicar el código del fabricante si aplica

## Marcas de piezas

### Referencia
- **Número de orden**: 1, 2, 3, ...
- **Marca**: código único (001, 002, ...)
- **Indicación**: flecha desde la marca a la pieza
- **Línea de referencia**: horizontal con flecha en un extremo

### Representación de marcas
- **Flecha**: señala la pieza
- **Línea horizontal**: contiene el número de orden
- **Cajetín**: contiene la descripción (opcional)
- **Piezas agrupadas**: una sola marca para varias piezas iguales

## Vistas de montaje

### Vista isométrica del conjunto
- Muestra el ensamblaje completo
- Útil para entender la relación entre piezas
- Se pueden usar cortes parciales

### Vista explosiva
- Piezas separadas en el orden de montaje
- Muestra el orden de ensamblaje
- Líneas de guía desde cada pieza hasta su posición en el conjunto
- **Orden de montaje**: de dentro hacia fuera, de abajo hacia arriba

### Secciones del conjunto
- **Piezas macizas**: NO se hachuran (ejes, tornillos, pasadores)
- **Piezas cortadas transversalmente**: se hachuran
- **Piezas adyacentes**: hachuras con diferente ángulo o separación
- **Piezas del mismo tipo**: hachuras idénticas

## Representación de elementos normalizados

### Tornillería
- **Tornillo**: cabeza, rosca, longitud
- **Normas**: ISO 4014 (hexagonal), ISO 4017 (hexagonal corto), ISO 7045 (pan head)
- **Representación simplificada**: en conjunto, no se representa la rosca completa
- **Línea de rosca**: gruesa para el diámetro exterior, fina para el interior

### Rodamientos
- **Representación simplificada**: rectángulos con diagonales
- **Norma**: ISO 15 (rodamientos de bolas), ISO 15:1998
- **Datos**: código del rodamiento (6205, 6308, ...)

### Chavetas
- **Norma**: ISO 773 (cilíndrica), ISO 774 (cónica)
- **Representación**: rectángulo en la vista del eje

### Retenes y juntas
- **Retenes**: representación simplificada según norma
- **Juntas tóricas**: línea gruesa en la sección

## Normas de representación en conjunto

### Piezas adyacentes
- **Hachuras diferentes**: ángulo o separación distinta
- **Mismo material**: hachuras idénticas

### Piezas macizas
- **NO se hachuran** si se cortan longitudinalmente
- **Sí se hachuran** si se cortan transversalmente

### Elementos normalizados
- **NO se hachuran** si se cortan longitudinalmente
- **Sí se hachuran** si se cortan transversalmente

### Piezas del mismo tipo
- **Hachuras idénticas** para simplificar
- **Diferenciar** con ángulo o separación diferente

## Errores comunes / Pitfalls

- **Hachurar piezas macizas**: tornillos, ejes, pasadores NO se hachuran longitudinalmente
- **Lista de piezas**: olvidar piezas estándar (tornillos, tuercas, arandelas)
- **Marcas**: no indicar todas las piezas. Cada pieza debe tener su marca
- **Vista explosiva**: orden incorrecto de montaje (debe ser de dentro hacia fuera)
- **Hachuras adyacentes**: mismo ángulo para piezas diferentes. Deben ser distintos
- **Cotas del conjunto**: acotar dimensiones generales, no dimensiones de piezas individuales

## Verificación

- [ ] ¿Todas las piezas tienen marca?
- [ ] ¿La lista de piezas incluye todas las piezas?
- [ ] ¿Las piezas macizas se hachuran solo transversalmente?
- [ ] ¿Las hachuras de piezas adyacentes son diferentes?
- [ ] ¿La vista explosiva muestra el orden correcto de montaje?
- [ ] ¿Las cotas del conjunto son las dimensiones generales?
