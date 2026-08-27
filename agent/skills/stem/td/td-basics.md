---
name: td-basics
description: Normalización ISO (128, 129), sistemas de representación básicos, proyección ortogonal, acotación, escalas, rotulación, tipos de línea.
tags: [stem, td, basics]
---

# Dibujo Técnico Básico

## Referencias de autoridad

- ISO 128: *Technical drawings — Presentation of views* (todas las partes)
- ISO 129-1: *Technical drawings — Dimensioning — Principles*
- ISO 9001: *Document management — Folded and bound drawing sizes*
- UNE-EN ISO 128-1:2021: *Norma española equivalente a ISO 128*
- Barrón-Bravo, J. — *Dibujo Técnico*, Paraninfo
- Esquiroz, A. — *Dibujo Geométrico*, Reverté

## Contenido clave

### Normalización de líneas (ISO 128)

**Tipos de línea y grosores**:
- **Línea continua gruesa** (ancho b): contornos visibles, aristas visibles. b = 0.13, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0 mm
- **Línea continua fina** (b/3): cotas, líneas de referencia, hachuras, contornos de secciones desplazadas.
- **Línea discontinua fina** (b/3): aristas NO visibles (ocultas). Segmentos ~6 mm, huecos ~1 mm.
- **Línea de trazas y puntos** (fine/heavy): ejes de simetría, trayectorias. Trazo largo ~30 mm, puntos ~1 mm, huecos ~1 mm.
- **Línea a dos trazos y puntos** (fine): superficies de corte.
- **Línea continua fina en zigzag**: rotura manual.
- **Línea continua fina en onda**: rotura parcial.

**Jerarquía de líneas** (cuando se superponen):
1. Contornos visibles (continua gruesa)
2. Contornos ocultos (discontinua fina)
3. Ejes y simetría (trazos y puntos)
4. Líneas de cota y referencia (continua fina)

### Sistemas de representación

**Proyección ortogonal** (sistema mongiano):
- Proyecciones perpendicularmente sobre planos de proyección.
- **Primer diedro** (europeo): objeto entre observador y plano. Vistas: alzado (frontal), planta (superior), perfil (lateral).
- **Tercer diedro** (americano): plano entre observador y objeto. Misma vista frontal, pero disposición diferente.
- Norma UNE-EN ISO 128-30 define los símbolos de diedro.

**Vistas principales** (primer diedro):
- **Alzado** (vista frontal): se observa desde delante. Muestra altura y anchura.
- **Planta** (vista superior): se observa desde arriba. Muestra anchura y profundidad.
- **Perfil izquierdo** (vista lateral izquierda): se observa desde la izquierda. Muestra altura y profundidad.
- **Perfil derecho**: se observa desde la derecha.
- **Vista inferior**: se observa desde abajo.
- **Vista posterior**: se observa desde detrás.

**Perspectivas**:
- **Cabaliera**: eje vertical (y) en vertical, ejes horizontales (x, z) a 45°. Factor de reducción en eje oblicuo: 0.5 (caballera normal) o 1.0 (caballera simplificada).
- **Isométrica**: tres ejes se separan 120°. Dos ejes horizontales a 30° de la horizontal. Factor de reducción teórico: 0.82 (usualmente se usa 1.0 sin reducción).

### Acotación (ISO 129-1)

**Elementos de cota**:
- **Línea de cota**: fina, paralela a la dimensión acotada. Termina en flechas (o puntos/trazos en某些 casos).
- **Línea de referencia (de llamada)**: fina, une la cota con el elemento acotado.
- **Línea de referencia (de dimensión)**: fina, paralela al elemento acotado, desde donde se mide.
- **Límite de cota**: pequeño trazo oblicuo (45°) o punto, en los extremos de la línea de cota.

**Principios de acotación**:
- Acotar la tamaño REAL (no la escala del dibujo).
- Cada dimensión se acota UNA SOLA VEZ, en la vista más representativa.
- Las cotas van fuera del dibujo, entre vistas si es necesario.
- Las cotas se leen desde abajo o desde la derecha.
- Agrupar cotas relacionadas.
- Evitar cruzar líneas de cota entre sí.

**Métodos de acotación**:
- **Encadenada**: cotas en serie, una detrás de otra. Error acumulativo.
- **Paralela**: todas desde una línea de referencia común. Sin error acumulativo.
- **Combinada**: mezcla de encadenada y paralela.
- **Coordenadas**: cotas en forma de coordenadas X, Y (común en CNC).

### Escalas

**Definición**: Escala = dimensión_dibujo / dimensión_real

**Escala natural**: 1:1

**Escala de ampliación**: 2:1, 5:1, 10:1, 2×10ⁿ, 5×10ⁿ, 10ⁿ (n > 0)

**Escala de reducción**: 1:2, 1:5, 1:10, 1:20, 1:50, 1:100, 1:200, 1:500, 1:1000

**Formatos de papel (ISO 9001 / serie A)**:
- A0: 841 × 1189 mm (1 m²)
- A1: 594 × 841 mm (A0 doblado)
- A2: 420 × 594 mm
- A3: 297 × 420 mm
- A4: 210 × 297 mm
- Relación: cada formato es la mitad del anterior. Relación de lados: √2 ≈ 1.414

### Rotulación

- **Altura de letra** (h): 2.5, 3.5, 5, 7, 10, 14, 20 mm
- **Tipo A** (estrecho): b = h/14 (ancho de trazo)
- **Tipo B** (ancho): b = h/10
- **Letra inclinada**: 75° respecto a la horizontal (recomendada) o vertical
- **Mayúsculas, minúsculas, números, símbolos** normalizados
- **Marco y letra de formato**: en la esquina inferior derecha, lectura desde el borde inferior o derecho

## Unidades y sistema SI

- Todas las cotas en **milímetros (mm)** por defecto en dibujo técnico. No se escribe la unidad.
- Si se usa otra unidad (metros, pulgadas), se indica explícitamente en la cota o en la leyenda.
- Ángulos en **grados sexagesimales** (°) o radianes (rad).
- Raqueteras y ángulos pequeños: grados, minutos ('), segundos (").
- Ejemplo: 45° 30' 15"

## Errores comunes / Pitfalls

- **Confusión tipos de línea**: continua gruesa = lo que se VE. Discontinua fina = lo que NO se VE (oculto). Trazos y puntos = ejes/simetría. No confundir discontinua con trazos-puntos.
- **Errores en acotación**: duplicar cotas (mismo valor en dos sitios) u omitir cotas (dimensiones sin acotar). Cada dimensión se acota UNA VEZ.
- **Escala mal aplicada**: acotar según el tamaño del dibujo en vez del tamaño real. La cota SIEMPRE indica la medida real del objeto, independientemente de la escala.
- **Proyección equivocada**: en primer diedro, la planta VA DEBAJO del alzado. En tercer diedro, la planta VA ENCIMA. No mezclar sistemas.
- **Líneas de cota cruzando**: las líneas de cota no deben cruzar entre sí. Si es inevitable, romper una de ellas.
- **Símbolos de diedro**: verificar siempre qué diedro se usa. Los símbolos son distintos y no son intercambiables.

## Verificación

- [ ] Tipos de línea: verificar jerarquía (gruesa > discontinua > trazos-puntos > fina)
- [ ] Proyección ortogonal: verificar que alzado y planta comparten anchura; alzado y perfil comparten altura
- [ ] Acotación: verificar que cada dimensión aparece UNA SOLA VEZ
- [ ] Escala: verificar que cota = tamaño_real, NO tamaño_dibujo
- [ ] Formato papel: verificar que relación de lados = √2 (A0: 841/1189 ≈ 0.707 = 1/√2 ✓)
- [ ] Rotulación: verificar altura mínima h = 2.5 mm para legibilidad
- [ ] Primer diedro: planta DEBAJO del alzado, perfil izquierdo a la DERECHA del alzado
- [ ] Tercer diedro: planta ENCIMA del alzado, perfil izquierdo a la IZQUIERDA del alzado
