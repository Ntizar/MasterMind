# InBody 3D + Entrenos por Zona — Implementación v3.1

## Implementación actual (v3.1)

### 3D Human — buildHuman3D()

Cada segmento del cuerpo se construye con DOS cilindros: interior (músculo azul) + exterior (grasa naranja). Las dimensiones se escalan según los datos reales de InBody.

**Materiales:**
- `muscleMat`: MeshPhysicalMaterial, color 0x3b82f6, clearcoat 0.2
- `muscleMatDark`: color 0x2563eb (para antebrazos/pantorrillas)
- `fatMat`: color 0xf97316, transparent 0.75, opacity 0.75
- `skinMat`: color 0xfcd9a6 (cabeza, manos)

**Referencias InBody (para un 78.5kg):**
```
brazo_izq_mmagro: 4.1kg, brazo_der_mmagro: 4.1kg
brazo_izq_grasa: 2.2kg, brazo_der_grasa: 2.2kg
pierna_izq_mmagro: 10.1kg, pierna_der_mmagro: 10.1kg
pierna_izq_grasa: 4.0kg, pierna_der_grasa: 4.1kg
tronco_mmagro: 31.1kg, tronco_grasa: 17.5kg
```

**Fórmula de escalado (createSegment helper):**
```javascript
var muscleRatio = muscleKg / ref.tronco_mmagro;
var fatRatio = fatKg / ref.tronco_grasa;
var baseMuscleR = height * 0.25;
var muscleR = baseMuscleR * Math.max(0.3, muscleRatio * 2);
var fatR = muscleR + baseMuscleR * 0.3 * Math.max(0, fatRatio * 2);
```

**Segmentos construidos:** cabeza, cuello, pecho, abdomen, cadera, hombros, brazos (izq/der × 2), manos, piernas (izq/der × 2), pies, sombra suelo.

**Labels HTML flotantes:** grasa%, MME kg, InBody Score, peso→objetivo, segmentos (brazos/piernas/tronco kg MME).

### Entrenos por zona muscular — renderEntrenos()

**Detección por descripción (regex):**
```
pecho: pecho|push|press|press banca|fondos|fly
espalda: espalda|pull|dominada|rem|fila|jalón
pierna: pierna|cuádriceps|sentadilla|squat|prensa|gemelo|hombro|delt|lateral
biceps: brazo|bíceps|biceps|curl|martillo
triceps: tríceps|triceps|extensión tríceps|roca|kickback
core: core|abdomen|plancha|crunch|oblicuo
gluteo: glúteo|gluteo|puente|hip thrust
cardio: cardio|cinta|elíptica|bici|ciclismo|running
full_body: full body|cuerpo completo|circuit|funcional
```

**Chart horizontal:** barras horizontales por zona con colores únicos, tooltip muestra entrenos + min + kcal por zona.

**Lista agrupada por fecha:** cada día muestra sus entrenos con badge de zona, icono emoji, duración, kcal, intensidad.

### Composición Corporal — renderComposicionChart()

Doughnut con 6 componentes: MME (azul), Grasa (naranja), Agua (celeste), Proteínas (verde), Minerales (gris), Otros (violeta). Cutout 55%, tooltips con kg + porcentaje.

## API Response /api/progreso

```javascript
{
  datos3D: {
    pesoActual, pesoObjetivo, kgPerdidos,
    grasaPctActual, mmeActual, inbodyScoreActual,
    grasaVisceralActual, imcActual, semanasRestantes, ritmoSemanal,
    segmentos: {
      brazo_izq_mmagro, brazo_izq_grasa, brazo_izq_mmagro_pct, brazo_izq_grasa_pct,
      brazo_der_mmagro, brazo_der_grasa, brazo_der_mmagro_pct, brazo_der_grasa_pct,
      pierna_izq_mmagro, pierna_izq_grasa, pierna_izq_mmagro_pct, pierna_izq_grasa_pct,
      pierna_der_mmagro, pierna_der_grasa, pierna_der_mmagro_pct, pierna_der_grasa_pct,
      tronco_mmagro, tronco_grasa, tronco_mmagro_pct, tronco_grasa_pct
    },
    historico: { peso: [...], inbody: [...] }
  },
  historialEntrenos: [{fecha, tipo, grupo, duracion, intensidad, series, kcal, notas}],
  resumenSemanal: { diasEntrenados, totalSeries, totalMinutos, fuerzaCount, cardioCount, ultimaSemaana }
}
```

## Pitfalls

- **InBody `porcentaje_grasa` puede ser null** si el dispositivo no lo reporta. fallback: estimar por IMC.
- **`masa_muscular_esquelética_kg` tiene acento** en la DB — usar exactamente ese nombre.
- **NaN no redeploya instantáneamente** — puede tardar 1-5 min en detectar cambios de git. Si el HTML no se actualiza, forzar con un commit vacío (push idéntico).
- **container3D debe definirse ANTES de buildHuman3D** — se usa para appendChild de labels HTML.
- **No usar `headMat`** — renombrar a `skinMat` para claridad.
