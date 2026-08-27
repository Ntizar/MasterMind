---
name: td-intermediate
description: Geometría descriptiva (sistema diédrico), perspectivas (cabañero/isométrica, caballera), intersecciones, desarrollo de superficies.
tags: [stem, td, intermediate]
---

# Dibujo Técnico Intermedio

## Referencias de autoridad

- Ogura, Y. — *Geometría Morfológica*, Omega
- Esquiroz, A. — *Dibujo Geométrico*, Reverté
- Llagostera, J. — *Geometría Descriptiva*, Gustavo Gili
- ISO 128: *Technical drawings — Presentation of views* (partes 2, 3, 4)
- UNE-EN ISO 128-4:2021: *Cortes y secciones*

## Contenido clave

### Sistema diédrico

**Fundamentos**:
- Dos planos de proyección perpendiculares: plano vertical (PV) y plano horizontal (PH).
- Línea de tierra (LT): intersección de PV y PH.
- Cuatro cuadrantes (diedros): Q1 (↑→), Q2 (↑←), Q3 (↓←), Q4 (↓→).
- Abatimiento: rotar PH 90° hacia abajo (sentido horario) para representar en 2D.

**Punto**:
- Proyección vertical (v): distancia al PH (altura/cota).
- Proyección horizontal (h): distancia al PV (alejamiento).
- En el dibujo: v está sobre LT, h debajo (Q1). O viceversa según diedro.
- Coordenadas: (x, y, z) = (a lo largo de LT, alejamiento, cota).

**Recta** (definida por dos puntos o un punto y dirección):
- Traza vertical (Tv): intersección con PV. h' = LT, v' ≠ LT.
- Traza horizontal (Th): intersección con PH. v' = LT, h' ≠ LT.
- Pendiente: ángulo con PH. Tangente de pendiente = cota / alejamiento.
- Veracidad de magnitud: una recta es paralela a un plano de proyección cuando su proyección en ese plano muestra la longitud real.
- Recta horizontal: paralela a PH. v' paralela a LT.
- Recta frontal: paralela a PV. h' paralela a LT.
- Recta de punta: perpendicular a PV. v' es un punto.
- Recta vertical: perpendicular a PH. h' es un punto.

**Plano** (definido por tres puntos, recta+punto, dos rectas paralelas/que se cortan, o tres rectas no concurrentes):
- Traza vertical (α'): intersección con PV.
- Traza horizontal (α''): intersección con PH.
- Plano horizontal: paralelo a PH. α' paralela a LT, α'' paralela a LT.
- Plano frontal: paralelo a PV. α' paralela a LT, α'' paralela a LT.
- Plano vertical: perpendicular a PH, paralelo a LT. α'' perpendicular a LT.
- Plano de perfil: perpendicular a PV y PH. α' y α'' perpendiculares a LT.
- Plano oblicuo: α' y α'' cortan a LT en el mismo punto (línea de llamada).

**Incidencia**:
- Punto en recta: v ∈ v', h ∈ h'.
- Punto en plano: pertenece a una recta del plano.
- Recta en plano: pasa por dos puntos del plano, o por un punto y es paralela a una recta del plano.
- Recta perpendicular a plano: v' ⊥ α' y h' ⊥ α'' (regla de los tres perpendiculares).

**Paralelismo**:
- Rectas paralelas: v₁' ∥ v₂' y h₁' ∥ h₂'.
- Plano paralelo a recta: plano contiene una recta paralela a la recta dada.
- Planos paralelos: α₁' ∥ α₂' y α₁'' ∥ α₂''.

**Perpendicularidad**:
- Recta ⊥ plano: v' ⊥ α' y h' ⊥ α''
- Plano ⊥ plano: un plano contiene una recta perpendicular al otro.
- Plano ⊥ PV: α'' perpendicular a LT.
- Plano ⊥ PH: α' perpendicular a LT.

### Abatimientos

**Concepto**: llevar un elemento de un plano abatido (rotado) alrededor de su traza hasta coincidir con el plano de proyección.

**Abatimiento de punto P en plano α**:
1. Llevar P a una recta del plano α (normalmente una recta de máximo pendiente o horizontal del plano).
2. Abatir esa recta alrededor de su traza.
3. P abatido (P₀) está en la recta abatida, a la misma distancia del plano de abatimiento que P original.
4. Radio de abatimiento: hipotenusa del triángulo rectángulo formado por la proyección y la cota/alejamiento.

**Abatimiento de recta**: abatir dos puntos de la recta y unirlos.

**Abatimiento de ángulo**: abatir los dos lados del ángulo.

**Planos de proyección auxiliares**:
- Para ver magnitudes verdaderas de figuras inclinadas.
- Nuevo plano paralelo a la figura inclinada.
- Nueva línea de tierra paralela a la proyección de la figura.

### Giros

**Giro alrededor de eje vertical**:
- La proyección horizontal describe un arco de circunferencia.
- La proyección vertical se desplaza paralelamente a LT.
- Cota (z) se mantiene constante.

**Giro alrededor de eje frontal**:
- La proyección vertical describe un arco de circunferencia.
- La proyección horizontal se desplaza paralelamente a LT.
- Alejamiento se mantiene constante.

**Giro alrededor de eje de punta**:
- La recta que contiene el eje se ve como punto en una de las proyecciones.
- El giro se ve como rotación en esa proyección.

### Perspectiva cabañera / isométrica

**Perspectiva isométrica (cabañera)**:
- Tres ejes: x, y, z. Ángulos entre ejes: 120° cada uno.
- Dos ejes horizontales a 30° de la horizontal del papel.
- Eje vertical (z) en vertical.
- **Factores de reducción teóricos**: k = cos(30°) = √3/2 ≈ 0.866 para cada eje.
  - En la práctica se usa k = 1.0 (isométrica simplificada) para mayor claridad.
- Círculos en planos isométricos se representan como **elipses**:
  - Eje mayor: perpendicular al eje isométrico del plano.
  - Eje menor: paralelo al eje isométrico del plano.
  - Aproximación en 4 centros (para ángulos de 30°).

**Perspectiva caballera**:
- Eje vertical (y) en vertical.
- Ejes horizontal (x) y oblicuo (z) a 45° (o 30°, 60° según preferencia).
- **Factor de reducción en eje oblicuo**:
  - Caballera normal: k = 0.5 (reducción al 50%)
  - Caballera simplificada: k = 1.0 (sin reducción)
- Círculos en plano xOy: se representan como círculos (no se deforman).
- Círculos en plano xOz o yOz: se representan como elipses.

### Intersecciones

**Recta con plano**:
1. Contener la recta en un plano proyectante (perpendicular a un plano de proyección).
2. Hallar la intersección del plano proyectante con el plano dado (recta de intersección).
3. La intersección de esta recta con la recta dada es el punto de intersección.
4. **No visibilidad**: usar puntos competidores (dos puntos con misma proyección en un plano, diferentes en el otro).

**Plano con plano**:
1. Tomar dos rectas del primer plano.
2. Hallar la intersección de cada recta con el segundo plano.
3. La recta que une ambos puntos es la recta de intersección.
4. O usar un plano proyectante como auxiliar.

**No visibilidad**:
- Competidores en vertical: dos puntos con misma h' (misma proyección horizontal). El que tiene mayor cota (v') tapa al otro.
- Competidores en horizontal: dos puntos con misma v'. El que tiene mayor alejamiento (h') tapa al otro.

### Desarrollo de superficies

**Poliedros**:
- **Prisma**: desarrollar base + caras laterales (rectángulos). Las caras laterales se despliegan en línea.
- **Pirámide**: desarrollar base + caras laterales (triángulos). Cada cara se desarrolla en verdadera magnitud.
- **Tetraedro regular**: 4 caras triangulares equiláteras. Se desarrollan 4 triángulos unidos por un vértice.

**Cuerpos de revolución**:
- **Cilindro**: desarrollar base (círculo) + superficie lateral (rectángulo: base = 2πr, altura = h).
- **Cono**: desarrollar base (círculo) + superficie lateral (sector circular: radio = generatriz g, arco = 2πr).
  - Ángulo del sector: α = 360° × r/g = 360° × r/√(r² + h²)
- **Trompo/cono truncado**: desarrollar anillo circular.
  - Radio exterior = generatriz total. Radio interior = generatriz del truncado.
  - Ángulo: α = 360° × r₁/g₁ (r₁ = radio menor, g₁ = generatriz correspondiente)

**Intersecciones de cuerpos**:
- **Cilindro-cilindro** (diámetros iguales, ejes perpendiculares): las intersecciones son elipses que se ven como rectas en proyección.
- **Cilindro-cono**: usar planos cortantes que pasen por el vértice del cono.

## Unidades y sistema SI

- Todas las cotas en **milímetros (mm)** por defecto.
- Ángulos en **grados sexagesimales** (°) o radianes (rad).
- Factores de reducción: adimensionales (números puros).
- Coeficientes de proyección: adimensionales.

## Errores comunes / Pitfalls

- **Confusión diédrico/mongiano**: son lo MISMO. "Sistema diédrico" y "sistema mongiano" son sinónimos. No confundir con perspectiva cónica o axonométrica.
- **Abatimiento mal ejecutado**: el radio de abatimiento es la HIPOTENUSA del triángulo formado por la proyección y la cota/alejamiento. No usar la cota/alejamiento como radio directamente.
- **Ejes perspectiva cabañero**: los ejes x e z forman 30° con la HORIZONTAL, NO con la vertical. El eje y es vertical. Los ángulos entre ejes son 120°.
- **Reducción en perspectiva caballera**: en caballera normal, el eje oblicuo se reduce a la MITAD (k = 0.5). En caballera simplificada, k = 1.0. No confundir.
- **Círculos en isométrica**: SIEMPRE se representan como elipses, NUNCA como círculos. El eje mayor de la elipse es perpendicular al eje isométrico correspondiente.
- **Planos proyectantes**: un plano proyectante vertical tiene α'' perpendicular a LT. Un plano proyectante horizontal tiene α' perpendicular a LT. No confundir.
- **Competidores**: un competidor en vertical tiene la misma proyección horizontal (h' igual) pero diferente cota (v' diferente). El que tiene MAYOR cota es el que tapa.

## Verificación

- [ ] Sistema diédrico: verificar que un punto en LT tiene cota = 0 o alejamiento = 0
- [ ] Recta en plano: verificar que ambos puntos de la recta están en rectas del plano
- [ ] Plano perpendicular: verificar que α' ⊥ LT (plano vertical) o α'' ⊥ LT (plano horizontal)
- [ ] Abatimiento: verificar que P₀ está en la recta abatida y la distancia al abatimiento es correcta
- [ ] Giros: verificar que la cota se mantiene en giro vertical y el alejamiento en giro frontal
- [ ] Isométrica: verificar que ángulos entre ejes = 120° y que x, z = 30° de horizontal
- [ ] Caballera: verificar que eje oblicuo tiene factor 0.5 (normal) o 1.0 (simplificada)
- [ ] Desarrollo cono: verificar que ángulo del sector α = 360° × r/g < 360°
- [ ] Desarrollo cilindro: verificar que base del rectángulo = 2πr (longitud de la circunferencia)
- [ ] No visibilidad: verificar con competidores en ambas proyecciones
