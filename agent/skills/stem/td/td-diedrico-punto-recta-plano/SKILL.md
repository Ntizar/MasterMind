---
name: td-diedrico-punto-recta-plano
description: Sistema diédrico: punto, recta y plano. Pertenencia, incidencia, paralelismo, perpendicularidad, verdaderas magnitudes.
tags: [stem, td, intermediate]
---

# Geometría Descriptiva: Punto, Recta y Plano

## Referencias de autoridad

- **Llagostera**: Geometría Descriptiva, Editorial Teide
- **Ogura**: Geometría Morfológica, Editorial Reverté
- **Esquiroz**: Dibujo Geométrico, Editorial Paraninfo
- **ISO 128-30**: Technical products documentation — Views — Representations on fixed views, section views, and detail views

## Punto en el sistema diédrico

### Representación
- A(x, y, z) → A' (alzado): (x, z) → arriba de la LT
- A(x, y, z) → A (planta): (x, y) → debajo de la LT
- La línea de unión A'-A es perpendicular a la LT

### Cuadrantes
- **1º cuadrante**: x > 0, y > 0, z > 0 (planta abajo, alzado arriba)
- **2º cuadrante**: x > 0, y < 0, z > 0 (planta arriba, alzado arriba)
- **3º cuadrante**: x > 0, y < 0, z < 0 (planta arriba, alzado abajo)
- **4º cuadrante**: x > 0, y > 0, z < 0 (planta abajo, alzado abajo)
- **En Europa se usa el 1º cuadrante** (método europeo)

### Puntos notables
- **En el primer bisector**: y = z (equidista de PV y PH)
- **En el segundo bisector**: y = -z
- **En el plano vertical**: y = 0 (A está sobre la LT)
- **En el plano horizontal**: z = 0 (A' está sobre la LT)
- **Sobre la LT**: y = z = 0 (punto en la intersección de PV y PH)

## Recta en el sistema diédrico

### Definición
- Dos puntos A y B definen una recta r
- r → r' (alzado) y r (planta)
- **Traza horizontal (Th)**: intersección de r con PH (z = 0)
- **Traza vertical (Tv)**: intersección de r con PV (y = 0)

### Posiciones de la recta
- **Horizontal**: paralela a PH (r' paralela a LT)
- **Frontal**: paralela a PV (r paralela a LT)
- **De punta**: perpendicular a PH (r' es un punto, r es perpendicular a LT)
- **De perfil**: paralela a PL (r' y r perpendiculares a LT)
- **Oblicua**: no paralela ni perpendicular a ningún plano

### Verdadera magnitud (VM)
- Una recta está en VM cuando es paralela al plano de proyección
- **Recta horizontal**: VM en planta
- **Recta frontal**: VM en alzado
- **Recta oblicua**: se obtiene VM por giro o cambio de plano

## Plano en el sistema diédrico

### Definición
- Un plano α se representa por sus **trazas**:
  - **Traza horizontal (α₁)**: intersección de α con PH
  - **Traza vertical (α₂)**: intersección de α con PV
  - Las trazas se cortan en la LT (punto de fuga)

### Posiciones del plano
- **Horizontal**: paralelo a PH (α₂ paralela a LT, α₁ es un punto o no existe)
- **Frontal**: paralelo a PV (α₁ paralela a LT, α₂ es un punto o no existe)
- **De canto**: perpendicular a PH y PV (α₁ y α₂ perpendiculares a LT)
- **Oblicuo**: inclinado respecto a los tres planos (trazas oblicuas a LT)
- **Paralelo a LT**: α₁ y α₂ paralelas a LT (o una de ellas es paralela a LT y la otra no existe)

### Rectas notables del plano
- **Recta horizontal del plano**: paralela a PH, está en el plano
  - Su alzado es paralelo a α₁ (traza horizontal)
- **Recta de máxima pendiente**: perpendicular a las horizontales del plano
  - Su planta es perpendicular a α₁
- **Recta de máxima inclinación**: perpendicular a α₁
  - Su alzado es perpendicular a α₂

### Pertenencia

#### Punto en una recta
- A ∈ r ↔ A' ∈ r' y A ∈ r

#### Punto en un plano
- A ∈ α ↔ existe una recta r ∈ α tal que A ∈ r
- **Método**: trazar una recta por A en el plano (usando horizontales o frontales del plano)

#### Recta en un plano
- r ∈ α ↔ Th ∈ α₁ y Tv ∈ α₂
- O: r pasa por dos puntos de α, o por un punto y es paralela a una recta de α

#### Recta paralela a un plano
- r ∥ α ↔ existe una recta s ∈ α tal que r ∥ s
- **Condición**: Th ∈ α₁ o Tv ∈ α₂ (o ambas paralelas)

#### Recta perpendicular a un plano
- r ⊥ α ↔ r ⊥ todas las rectas de α
- **Condición práctica**: r' ⊥ α₂ y r ⊥ α₁ (para recta oblicua)
- **Recta horizontal**: r ⊥ α → r ⊥ α₁ (horizontal del plano)
- **Recta frontal**: r ⊥ α → r' ⊥ α₂ (frontal del plano)

## Paralelismo y perpendicularidad

### Paralelismo
- Dos rectas: r ∥ s ↔ r' ∥ s' y r ∥ s
- Recta y plano: r ∥ α ↔ existe s ∈ α tal que r ∥ s
- Dos planos: α ∥ β ↔ α₁ ∥ β₁ y α₂ ∥ β₂

### Perpendicularidad
- Dos rectas: r ⊥ s (se cortan o se cruzan)
- Recta y plano: r ⊥ α → r' ⊥ α₂ y r ⊥ α₁
- Dos planos: α ⊥ β ↔ una traza de α es perpendicular a la otra traza de β

## Errores comunes / Pitfalls

- **Cuadrantes**: en Europa se usa el 1º cuadrante. Planta abajo, alzado arriba
- **Trazas**: α₁ es la traza horizontal (con PH), α₂ es la traza vertical (con PV). No confundir
- **Recta horizontal del plano**: su alzado es PARALELO a α₁, no perpendicular
- **Recta de máxima pendiente**: su planta es PERPENDICULAR a α₁
- **Pertenencia**: un punto pertenece a un plano si está en una recta del plano. No basta con que las proyecciones coincidan
- **Perpendicularidad recta-plano**: r' ⊥ α₂ Y r ⊥ α₁. Ambas condiciones son necesarias

## Verificación

- [ ] Punto: ¿A' y A están en la misma vertical?
- [ ] Recta: ¿las trazas están en los planos correctos? Th en PH (z=0), Tv en PV (y=0)
- [ ] Plano: ¿α₁ y α₂ se cortan en la LT?
- [ ] Pertenencia: ¿el punto está en una recta del plano?
- [ ] Perpendicularidad: ¿r' ⊥ α₂ y r ⊥ α₁?
