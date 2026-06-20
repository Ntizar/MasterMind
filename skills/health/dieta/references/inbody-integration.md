# Integración de datos InBody en la DB de dieta

## Qué es InBody

InBody120 es una báscula analítica que mide composición corporal mediante impedancia bioeléctrica. Genera informes con:
- Masa grasa, masa muscular esquelética, agua corporal, proteínas, minerales
- % grasa corporal, IMC
- Puntuación InBody (0-100+)
- Grasa visceral, TMB, relación cintura-cadera
- Análisis segmental (brazos, piernas, tronco)

## Flujo de integración

1. **Recibir informe InBody** (imagen o texto)
2. **Extraer todos los valores** del informe
3. **Verificar edad** — si InBody reporta edad diferente a la DB, preguntar al usuario
4. **Actualizar DB** añadiendo entrada en `inbody_history[]`
5. **Recalcular TMB** con edad correcta (Mifflin-St Jeor)
6. **Crear nota** en `/hermes-home/notes/YYYY-MM-DD-inbody-*.md`
7. **Commit + push** al repo dieta

## Estructura de entrada InBody en DB

```json
{
  "inbody": [
    {
      "fecha": "2026-06-04",
      "hora": "17:18",
      "tipo": "inbody",
      "dispositivo": "InBody120",
      "peso_kg": 98.1,
      "masa_grasa_kg": 31.4,
      "porcentaje_grasa": 32.0,
      "masa_muscular_esquelética_kg": 38.3,
      "agua_corporal_L": 48.9,
      "proteinas_kg": 13.4,
      "minerales_kg": 4.40,
      "imc": 32.4,
      "inbody_score": 70,
      "peso_objetivo_kg": 78.5,
      "control_grasa_kg": -19.6,
      "control_muscular_kg": 0.0,
      "tmb_kcal": 1810,
      "relacion_cintura_cadera": 0.98,
      "grasa_visceral": 14,
      "grado_obesidad": 147,
      "notas": "Primer test InBody — Día 1 de dieta."
    }
  ]
}
```

## Cálculo de TMB con edad correcta

**Fórmula Mifflin-St Jeor (hombre):**
```
TMB = 10 × peso(kg) + 6.25 × altura(cm) - 5 × edad + 5
```

**Ejemplo David (98 kg, 174 cm, 36 años):**
```
TMB = 10×98 + 6.25×174 - 5×36 + 5 = 1892 kcal/día
```

**Si InBody reporta edad diferente:**
- InBody dijo 36, DB tenía 45 → TMB real 1892 vs ~1840 (edad 45)
- Diferencia: ~52 kcal TMB, ~83 kcal TDEE (nivel moderado)
- **Siempre preguntar al usuario** si hay discrepancia de edad

## Interpretación rápida de métricas InBody

| Métrica | Normal (hombre) | Alerta | Peligro |
|---|---|---|---|
| % Grasa | 10-20% | 21-25% | >25% |
| IMC | 18.5-24.9 | 25-29.9 | ≥30 |
| Grasa visceral | 1-9 | 10-14 | >14 |
| InBody Score | 80-100+ | 60-79 | <60 |
| Rel. Cintura-Cadera | <0.90 | 0.90-0.95 | >0.95 |

## TDEE según nivel de actividad

| Nivel | Factor | David a 36 años (TMB 1892) |
|---|---|---|
| Sedentario | ×1.2 | ~2.270 kcal |
| Ligero (1-3 días) | ×1.375 | ~2.602 kcal |
| Moderado (3-5 días) | ×1.55 | ~2.933 kcal |
| Activo (6-7 días) | ×1.725 | ~3.265 kcal |

## Objetivo de pérdida

El InBody recomienda:
- **Control de grasa** = kg a perder de grasa (ej: -19.6 kg)
- **Control muscular** = kg a ganar/perder de músculo (ej: 0.0 = mantener)
- **Peso objetivo** = peso ideal según composición

**Ritmos de pérdida:**
- 0.7 kg/sem → déficit ~550 kcal/día → ideal
- 0.9 kg/sem → déficit ~700 kcal/día → agresivo pero viable
- 1.0 kg/sem → déficit ~770 kcal/día → riesgo músculo

## Frecuencia de tests

- **Primer test:** día 1 de dieta (baseline)
- **Seguimiento:** cada 4 semanas
- **Métricas a comparar:** % grasa, masa muscular, grasa visceral, InBody score
- **No medir más de 1 vez/semana** — la impedancia varía mucho por hidratación

## Pitfalls

- **Edad incorrecta en dispositivo:** los dispositivos pueden tener edad hardcodeada o antigua. SIEMPRE verificar con usuario.
- **Hidratación afecta impedancia:** medir siempre en mismo estado (mañana, ayuno, sin ejercicio previo)
- **No comparar TMB de InBody con Mifflin directamente:** cada fabricante usa su propia fórmula. Usar Mifflin como referencia independiente.
- **Grasa segmental estimada:** el InBody120 estima grasa por segmento, no la mide directamente. Los valores de % vs ideal pueden ser imprecisos.
- **InBody score no es absoluto:** una persona muy musculosa puede superar 100. Un 70 con buena base muscular es mejor que un 70 con poca masa.
