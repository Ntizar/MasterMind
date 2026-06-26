---
name: td-tolerancias
description: Tolerancias dimensionales (ISO 286), tolerancias geométricas (ISO 1101), GPS (ISO 8015), ajustes, sistemas agujero/eje y representación en planos.
tags: [stem, td, advanced]
---

# Tolerancias en Dibujo Técnico

## Referencias de autoridad

- **ISO 1101**: Geometrical product specifications (GPS) — Geometrical tolerancing — Tolerances for form, orientation, location and run-out
- **ISO 286-1**: ISO system of limits and fits — Part 1: Bases of limits and fits
- **ISO 8015**: GPS — General principles — Tolerance principles
- **UNE-EN ISO 1101**: Adaptación española
- **ISO 286-2**: Tolerances for linear sizes
- **ISO 286-3**: Tolerances for angles

## Tolerancias dimensionales (ISO 286)

### Sistema de agujero base y eje base
- **Agujero base**: la tolerancia del agujero es H (tolerancia inferior = 0)
- **Eje base**: la tolerancia del eje es h (tolerancia superior = 0)
- **Europa**: agujero base (H)
- **EE.UU.**: eje base (h)

### Tolerancias estándar (IT)
- **IT01, IT0, IT1, ..., IT18**: 20 grados de tolerancia
- IT01: más precisa (micras)
- IT18: menos precisa (milímetros)
- **Grados habituales**: IT5-IT7 para rodamientos, IT6-IT8 para ajustes generales

### Desviaciones fundamentales
- **Agujeros**: A, B, C, ..., H, ..., ZC (H = desviación inferior = 0)
- **Ejes**: a, b, c, ..., h, ..., zc (h = desviación superior = 0)

### Ajustes

#### Ajuste con juego (clearance)
- El agujero SIEMPRE es mayor que el eje
- Ejemplo: H7/g6, H7/f6
- **Juego mínimo**: D_min - d_max
- **Juego máximo**: D_max - d_min

#### Ajuste con interferencia (interference)
- El eje SIEMPRE es mayor que el agujero
- Ejemplo: H7/p6, H7/s6
- **Interferencia mínima**: d_min - D_max
- **Interferencia máxima**: d_max - D_min

#### Ajuste incierto/transición (transition)
- Puede haber juego o interferencia
- Ejemplo: H7/k6, H7/n6
- **Máximo juego**: D_max - d_min
- **Máxima interferencia**: d_max - D_min

### Representación en plano
- **Dimensión con tolerancia**: Φ30 H7 o Φ30 +0,021/0
- **Tolerancia numérica**: Φ30 ±0,01
- **Tabla de tolerancias**: para múltiples dimensiones

## Tolerancias geométricas (ISO 1101)

### Marco de tolerancia
```
┌───┬──────┬───────┬──────┬──────┐
│ T │ M/R/P│  Valor│ Ref A│ Ref B│
└───┴──────┴───────┴──────┴──────┘
```
- **Caja 1**: símbolo de la tolerancia
- **Caja 2**: valor de la tolerancia (con o sin módulo M/R/P)
- **Caja 3+**: referencia(s) de datum

### Símbolos de tolerancias geométricas

#### Forma (sin referencia de datum)
- **Rectitud** (—): línea recta
- **Planitud** (▱): plano
- **Circularidad** (○): círculo
- **Cilindricidad** (⌭): cilindro

#### Orientación (con referencia de datum)
- **Paralelismo** (∥): paralelo al datum
- **Perpendicularidad** (⊥): perpendicular al datum
- **Inclinación** (∠): ángulo determinado respecto al datum

#### Localización (con referencia de datum)
- **Posición** (⊕): centro/ eje/ plano medio
- **Concentricidad** (◎): eje coaxial con datum
- **Simetría** (⊖): plano medio simétrico respecto al datum

#### Batida (con referencia de datum)
- **Batida circular** (↗): en un plano circular
- **Batida total** (↗↗): en toda la superficie

### Criterio de requisito (M/R/P)
- **M (Max material)**: requisito de material máximo. La tolerancia se aplica cuando la pieza está en su material máximo
- **R (Recuadrado)**: zona de tolerancia rectangular/cilíndrica
- **P (Free state)**: sin restricción (piezas flexibles)

### Datum

#### Concepto
- **Datum**: superficie/linea/punto de referencia teórica
- Se identifica con una letra mayúscula (A, B, C, ...)
- Se representa con un triángulo en la superficie de referencia

#### Sistema de datums
- **Datum primario (A)**: superficie de apoyo principal
- **Datum secundario (B)**: superficie de referencia secundaria (perpendicular a A)
- **Datum terciario (C)**: tercera referencia (perpendicular a A y B)
- **Orden de contacto**: A primero, B segundo, C tercero

## GPS (ISO 8015)

### Principio general
- Las tolerancias geométricas son independientes de las dimensionales
- **Principio de independiencia**: las tolerancias geométricas no afectan a las dimensionales (salvo que se indique lo contrario)
- **Principio de límite local**: cada dimensión individual debe estar dentro de los límites especificados

### Reglas de aplicación
- **Regla 1**: la superficie debe estar dentro de los límites de tamaño
- **Requisito encaje perfecto**: la superficie debe encajar en una caja de dimensiones máximas
- **Requisito de material máximo (MMC)**: la tolerancia geométrica se aplica en MMC

## Errores comunes / Pitfalls

- **Concentricidad vs excentricidad**: concentricidad se refiere al eje, no a la superficie. Para superficies, usar posición
- **Planitud vs paralelismo**: planitud no requiere datum, paralelismo sí
- **Marco de tolerancia**: el símbolo va primero, luego el valor, luego las referencias de datum
- **Datum**: el orden importa. A es el primario, B el secundario, C el terciario
- **Ajuste H7/g6**: H7 es el agujero (base), g6 es el eje. Verificar que es ajuste con juego
- **MMC**: el requisito M se indica en la segunda caja del marco, no como un símbolo aparte

## Verificación

- [ ] Marco de tolerancia: ¿símbolo → valor → datum?
- [ ] Datum: ¿el orden es A (primario), B (secundario), C (terciario)?
- [ ] Ajuste: ¿H7/g6 es con juego? ¿H7/p6 es con interferencia?
- [ ] Tolerancia geométrica: ¿el símbolo es el correcto para la característica?
- [ ] Regla 1: ¿cada dimensión individual está dentro de los límites?
