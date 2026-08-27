---
name: td-advanced
description: Normalización avanzada (tolerancias geométricas ISO 1101, dimensionales ISO 286), cortes y secciones (ISO 128-4), normalización industrial, planos de conjunto.
tags: [stem, td, advanced]
---

# Dibujo Técnico Avanzado

## Referencias de autoridad

- ISO 1101: *Geometrical product specifications (GPS) — Geometrical tolerancing — Tolerances of form, orientation, location and run-off*
- ISO 286-1: *Geometrical product specifications (GPS) — ISO code system for tolerances of linear sizes — Part 1: Tolerances for bits and holes*
- ISO 128-4:2020: *Technical drawings — Presentation of views — Part 4: Rules for the representation of sections and cuts*
- ISO 13715: *Welded joints — Geometrical product specifications (GPS) — Geometrical tolerances for seams*
- UNE-EN ISO 1101:2018: *Norma española de tolerancias geométricas*
- Manual de tolerancias ISO — *Geometrical Product Specifications (GPS) Guide*

## Contenido clave

### Tolerancias geométricas (ISO 1101)

**Concepto**: las tolerancias geométricas controlan la forma, orientación, ubicación y batido de los elementos geométricos, INDEPENDIENTEMENTE de las tolerancias dimensionales.

**Categorías de tolerancias**:

1. **Tolerancias de forma** (sin referencia):
   - **Planitud**: superficie plana dentro de dos planos paralelos. Símbolo: — (línea horizontal)
   - **Rectitud**: recta dentro de un cilindro o dos planos paralelos. Símbolo: | / (diagonal)
   - **Circularidad**: sección circular dentro de dos círculos concéntricos. Símbolo: ○
   - **Cilindricidad**: superficie cilíndrica dentro de dos cilindros concéntricos. Símbolo: /○/ (dos diagonales con círculo)
   - **Perfil de superficie**: superficie dentro de dos superficies paralelas. Símbolo: ⌒ (arco)
   - **Perfil de línea**: perfil dentro de dos líneas paralelas. Símbolo: ⌒ (arco)

2. **Tolerancias de orientación** (con referencia):
   - **Paralelismo**: símbolo: ∥
   - **Perpendicularidad**: símbolo: ⊥
   - **Inclinación**: símbolo: ∠
   - Controlan el ángulo entre elemento y referencia.

3. **Tolerancias de ubicación** (con referencia):
   - **Posición**: símbolo: ⊕ (círculo con cruz)
   - **Coaxialidad/concentricidad**: símbolo: ○⊕ (círculo con cruz)
   - **Simetría**: símbolo: —|— (tres líneas)
   - Controlan la posición exacta del elemento respecto a referencia.

4. **Tolerancias de batido** (con referencia):
   - **Batido circular**: símbolo: ↗ (flecha diagonal)
   - **Batido total**: símbolo: ↗↗ (dos flechas diagonales)
   - Controlan la variación radial y axial en rotación.

**Caja de tolerancia**:
```
┌─────────────────────────┐
│  tolerancia │ referencia │
│             │ secundaria │
│             │ terciaria  │
└─────────────────────────┘
```
- Primera casilla: símbolo de tolerancia + valor (± si aplica)
- Casillas siguientes: identificadores de referencias (A, B, C, ...)
- El valor puede ir precedido de ⌀ (cilíndrico) o S⌀ (esférico)

**Modificadores**:
- ⌀: zona de tolerancia cilíndrica
- S⌀: zona de tolerancia esférica
- Ⓜ: modo máximo (MMC — Maximum Material Condition)
- Ⓛ: modo mínimo (LMC — Least Material Condition)
- Ⓟ: proyectado (zona de tolerancia proyectada más allá de la superficie)

**Condiciones de material**:
- **MMC** (modo máximo): condición donde el elemento contiene MÁS material. Para eje: diámetro máximo. Para agujero: diámetro mínimo.
- **LMC** (modo mínimo): condición donde el elemento contiene MENOS material. Para eje: diámetro mínimo. Para agujero: diámetro máximo.
- Con Ⓜ: la toleranza geométrica se amplía cuando el tamaño se aleja del MMC (bonificación).

### Tolerancias dimensionales (ISO 286)

**Sistema de ajustes**:
- **Agujero base**: el agujero tiene tolerancia fija (H), se varía el eje para obtener el ajuste deseado.
- **Eje base**: el eje tiene tolerancia fija (h), se varía el agujero.
- Norma UNE recomienda: agujero base como preferente.

**Tolerales y ajustes**:
- **H7/g6**: ajuste con juego (guía). H7 = agujero IT7, g6 = eje IT6 con desviación fundamental g.
- **H7/k6**: ajuste con transición (puede haber juego o interferencia leve).
- **H7/p6**: ajuste con interferencia (precisión). Requiere presión o calor para montar.

**IT (International Tolerance) grades**:
- IT01, IT0, IT1, IT2, ..., IT16, IT17 (IT01 es el más preciso, IT17 el menos)
- IT5-IT7: precisión alta (rodamientos, cilindros)
- IT8-IT11: precisión media (engranes, ejes)
- IT12-IT14: precisión baja (estructuras, chapa)

**Desviaciones fundamentales**:
- **Agujeros** (mayúsculas): A-ZC (desviación inferior), H (desviación inferior = 0)
- **Ejes** (minúsculas): a-zc (desviación superior), h (desviación superior = 0)

### Cortes y secciones (ISO 128-4)

**Corte total**:
- Plano de corte que atraviesa completamente la pieza.
- Sección: parte entre el observador y el plano de corte se SUPRIME.
- La parte posterior se representa con contornos visibles.
- Línea de corte: trazo y punto gruesa. Flechas indican dirección de vista.

**Corte parcial (medio corte)**:
- Solo se corta la mitad (o fracción) de la pieza.
- La línea de separación es una línea continua fina ondulada o a dos trazos y puntos.
- Útil para piezas simétricas: mitad vista exterior, mitad corte.

**Corte escalonado**:
- Múltiples planos de corte paralelos.
- Se representa como un solo corte.
- No se representan las líneas de intersección entre planos de corte.

**Corte rotado**:
- Plano de corte que gira alrededor de un eje para revelar interior.
- Se representa la vista girada en la posición del corte.

**Secciones**:
- **Sección desplazada**: secciona la pieza y muestra la sección en una posición distinta.
- **Sección integrada**: la sección se dibuja superpuesta a la vista (contorno continuo fino).
- **Sección de rotura**: para elementos largos de sección constante (ejes, tubos). Se representa un tramo y se indica que se repite.

**Hachuras**:
- Líneas continuas finas a 45° (preferiblemente) o 30°/60°.
- Separación: 1-2 mm para secciones pequeñas, 2-4 mm para medianas, 4-8 mm para grandes.
- Piezas macizas NO se hachuran en corte longitudinal (ejes, pernos, pasadores, esferas).
- Hachuras de piezas adyacentes: ángulos distintos (30° vs 45°) o separación distinta.

### Normalización industrial

**Tolerancias de soldadura (ISO 13715)**:
- Símbolos de soldadura normalizados:
  - Soldadura a tope: ⊥ (triángulo)
  - Soldadura de filete: ▽ (triángulo rectángulo)
  - Soldadura de角: L (ángulo)
  - Soldadura de tapón: ○
- Flecha señala el lado de la soldadura.
- Cota junto al símbolo: tamaño de la soldadura (a = throat, s = size).
- Cota junto a la flecha: lado de la soldadura. Cota junto al cuadrado: lado opuesto.

**Representación simplificada de elementos**:
- **Roscas**: hilo exterior visible (grueso), interior oculto (discontinuo). Diámetro del hilo menor = 0.85 × diámetro nominal.
- **Rodamientos**: representación simbólica normalizada.
- **Muelles**: representación simplificada con línea continua fina. Solo los extremos se representan con detalle.
- **Pernos/tornillos**: cabeza hexagonal simbólica. Rosca simbólica.

### Planos de conjunto

**Vistas y cortes**:
- Mínimo de vistas necesario para definir completamente el conjunto.
- Cortes para mostrar interior y relaciones entre piezas.
- Vista爆炸 (exploded view) opcional para mostrar montaje.

**Balones (identificación de piezas)**:
- Círculo con número de pieza, conectado con línea al elemento.
- Lista de piezas (BOM — Bill of Materials) con:
  - Número de pieza
  - Nombre/descripción
  - Cantidad
  - Material
  - Observaciones

**Acotación de conjunto**:
- Cotas de instalación (dimensiones generales, puntos de fijación).
- Cotas de ajuste (entre piezas que se acoplan).
- Cotas de recorrido (espacios libres, holguras).
- NO cotear todas las piezas individualmente (eso va en planos de detalle).

**Notas técnicas**:
- Tratamientos térmicos (temple, revenido, normalizado).
- Acabados superficiales (rugosidad Ra, Rz).
- Pintura, pasivación, galvanizado.
- Par de apriete de tornillos.
- Observaciones especiales.

## Unidades y sistema SI

- Todas las cotas en **milímetros (mm)** por defecto.
- Rugosidad: **micrómetros (μm)**. Ra = rugosidad media aritmética.
- Par de apriete: **newton-metro (N·m)** o **newton-centímetro (N·cm)**.
- Tolerancias geométricas: mismas unidades que las cotas (mm).
- Ángulos de hachuras: grados (°).

## Errores comunes / Pitfalls

- **Interpretación símbolos tolerancias geométricas**: cada símbolo tiene un significado específico. Planitud (—) NO es lo mismo que rectitud (/). Perpendicularidad (⊥) requiere referencia. No confundir coaxialidad (○⊕) con concentricidad.
- **Confusión corte/sección**: en corte se representa TODO lo que hay detrás del plano de corte. En sección solo se muestra la superficie cortada. No representar contornos visibles detrás del plano en una sección.
- **Ajuste juego/interferencia/transición**: H7/g6 = juego (guía), H7/k6 = transición, H7/p6 = interferencia (precisión). No intercambiar.
- **Piezas macizas en corte**: ejes, pernos, pasadores, esferas, nervios NO se hachuran en corte longitudinal. Sí se hachuran en corte transversal.
- **Modo máximo (Ⓜ)**: la toleranza geométrica se amplía con la bonificación de material. Si el eje está por debajo del MMC, la toleranza de posición se amplía. No aplicar bonificación si no hay Ⓜ.
- **Hachuras en piezas adyacentes**: usar ángulos distintos (30° vs 45°) o separaciones distintas. No usar el mismo ángulo y separación para dos piezas diferentes.
- **Balones**: los números deben ser consecutivos y la lista de piezas debe coincidir exactamente con los balones. No omitir piezas.

## Verificación

- [ ] Caja de tolerancia: verificar símbolo + valor + referencias en el orden correcto
- [ ] MMC/LMC: verificar que la bonificación se aplica solo cuando se indica Ⓜ o Ⓛ
- [ ] Ajuste: verificar que H7/g6 da juego, H7/k6 da transición, H7/p6 da interferencia
- [ ] IT grade: verificar que IT5-7 es alta precisión, IT8-11 media, IT12-14 baja
- [ ] Corte total: verificar que la parte entre observador y plano se suprime
- [ ] Sección: verificar que solo se muestra la superficie cortada, no lo que hay detrás
- [ ] Hachuras: verificar ángulo 45° preferente, separación proporcional al tamaño
- [ ] Piezas macizas: verificar que NO se hachuran en corte longitudinal
- [ ] Balones: verificar que cada pieza tiene un balón y aparece en la lista
- [ ] Roscas: verificar que hilo exterior = gruesa visible, hilo interior = discontinua
