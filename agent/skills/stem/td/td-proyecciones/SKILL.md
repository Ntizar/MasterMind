---
name: td-proyecciones
description: Sistema diédrico básico: proyección ortogonal, vistas principales (alzado, planta, perfil), correspondencia entre vistas, perspectivas axonométricas.
tags: [stem, td, basics]
---

# Proyecciones y Sistema Diédrico

## Proyección ortogonal

- **Proyección ortogonal**: rayos proyectantes perpendiculares al plano de proyección
- **Proyección cónica**: rayos proyectantes convergentes en un punto (centro de proyección)
- En dibujo técnico: SIEMPRE proyección ortogonal (a menos que se indique lo contrario)

## Sistema de tres planos de proyección

- **Plano vertical (PV)**: alzado (vista frontal)
- **Plano horizontal (PH)**: planta (vista superior)
- **Plano lateral (PL)**: perfil (vista lateral)

### Abatimiento
- PV se mantiene fijo
- PH se rota 90° hacia abajo (gira alrededor del LT = Línea de Tierra)
- PL se rota 90° hacia la derecha (gira alrededor de la LT del PV)

## Vistas principales

### Alzado (vista frontal)
- Se observa desde el frente
- Muestra: ancho (X) y altura (Z)
- Es la vista de referencia para las demás

### Planta (vista superior)
- Se observa desde arriba
- Muestra: ancho (X) y profundidad (Y)
- Se situa DEBAJO del alzado (1º diedro)

### Perfil (vista lateral)
- Se observa desde el lateral derecho (perfil izquierdo) o izquierdo (perfil derecho)
- Muestra: profundidad (Y) y altura (Z)
- Se situa AL LADO del alzado

## Correspondencia entre vistas

- **Alzado ↔ Planta**: mismas coordenadas X (ancho). Se alinean verticalmente
- **Alzado ↔ Perfil**: mismas coordenadas Z (altura). Se alinean horizontalmente
- **Planta ↔ Perfil**: mismas coordenadas Y (profundidad). Se transportan con escuadra/compás o línea de 45°

### Regla mnemotécnica
- **Ancho**: Alzado y Planta comparten X
- **Alto**: Alzado y Perfil comparten Z
- **Profundidad**: Planta y Perfil comparten Y

## Sistema diédrico

### Elementos
- **Punto**: se representa con dos proyecciones (al menos)
  - A(x, y, z) → A'(x, z) en PV (alzado), A(x, y) en PH (planta)
- **Recta**: definida por dos puntos o un punto y su dirección
- **Plano**: definido por:
  - Tres puntos no alineados
  - Un punto y una recta
  - Dos rectas concurrentes o paralelas
  - Una recta y un punto exterior
  - Tres rectas concurrentes
  - Dos rectas paralelas
  - Un triángulo

### Planos en el diédrico
- **Plano vertical**: perpendicular a PV, paralelo a PL
- **Plano horizontal**: paralelo a PH
- **Plano de perfil**: paralelo a PL
- **Plano oblicuo**: inclinado respecto a los tres planos

###abatimiento del plano horizontal
- PH gira 90° hacia abajo alrededor de la Línea de Tierra
- El eje Y de la planta queda debajo de la LT
- El eje Y del perfil queda a la derecha de la LT

## Perspectivas axonométricas

### Isométrica (cabañera)
- Ejes: X, Y, Z a 120° entre sí
- En papel: X e Y a 30° de la horizontal, Z vertical
- **Reducción isométrica**: 0,82 (teórica). En la práctica se usa 1 (isométrica reducida)
- Los círculos se representan como elipses con ejes 0,56·D (isométrica) o D (reducida)

### Dimétrica
- Dos ejes con la misma escala, el tercero diferente
- Ángulos: típicamente 7° y 42° respecto a la horizontal

### Monométrica (cavalier / caballera)
- Un eje perpendicular (normal al plano de dibujo)
- Ángulo del eje oblicuo: 30°, 45° o 60°
- Reducción del eje oblicuo: 0,5 (caballera normal) o 1 (caballera simplificada)

## Representación de piezas

### Principios
- Elegir la vista principal que mejor represente la forma
- Número mínimo de vistas necesario
- Usar cortes y secciones cuando sea necesario
- No duplicar información

### Vista auxiliar
- Se obtiene proyectando sobre un plano auxiliar paralelo a una cara inclinada
- Muestra la verdadera magnitud de la cara inclinada

### Vista parcial
- Se representa solo una parte de la pieza (cuando la pieza es grande y la zona de interés es pequeña)
- Límite con línea ondulada o de rotura

## Errores comunes / Pitfalls

- **Abatimiento**: PH gira hacia ABAJO, no hacia ARRIBA. PL gira hacia la DERECHA
- **Correspondencia**: confundir qué dimensión comparten las vistas. Alzado-Planta = ancho (X). Alzado-Perfil = alto (Z). Planta-Perfil = profundidad (Y)
- **1º diedro vs 3º diedro**: en 1º diedro (Europa), la planta está DEBAJO del alzado. En 3º diedro (EE.UU.), la planta está ENCIMA
- **Perfil izquierdo vs derecho**: perfil izquierdo = se observa desde la izquierda. Se dibuja a la derecha del alzado (1º diedro)
- **Perspectiva isométrica**: los ejes están a 120° entre sí, NO a 90°. En papel se dibujan a 30° de la horizontal

## Verificación

- [ ] Correspondencia: ¿Alzado y Planta tienen el mismo ancho?
- [ ] Correspondencia: ¿Alzado y Perfil tienen la misma altura?
- [ ] Abatimiento: ¿la planta está debajo del alzado?
- [ ] Perspectiva isométrica: ¿los tres ejes forman 120°?
- [ ] Símbolo de proyección: ¿está presente?
