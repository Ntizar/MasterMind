# Análisis de peso y proyección de pérdida de grasa

## Framework de análisis

Cuando el usuario pregunta "¿es lógico que baje tanto?" o "¿dónde me pone X fecha?", seguir este proceso:

### 1. Calcular TMB (Mifflin-St Jeor, hombre)
```
TMB = 10 × peso(kg) + 6.25 × altura(cm) - 5 × edad(años) + 5
```
- Si no se sabe la edad, usar 45 como referencia (rango 40-50)
- Para David: ~1840 kcal/día a 97 kg, 174 cm, 45 años

### 2. Calcular TDEE
- Sedentario (x1.2): ~2200 kcal
- Ligero (x1.375): ~2530 kcal
- Moderado (x1.55): ~2850 kcal

### 3. Balance día por día
- Sumar todas las kcal ingeridas por día desde SEGUIMIENTO.md
- Restar TMB + ejercicio estimado
- Calcular déficit/superávit por día

### 4. Descomposición de la bajada de peso
- **Grasa real:** déficit total acumulado / 7700 kcal por kg
- **Agua/glicógeno/intestino:** resto de la bajada
- Primera semana: mayor caída por vaciado de glicógeno (1g glucógeno = 3g agua)

### 5. Proyección
- 0,3-0,5 kg/semana = ritmo natural/sostenible
- 0,7 kg/semana = acelerado pero viable (déficit ~550 kcal/día)
- 1,0 kg/semana = agresivo (déficit ~770 kcal/día, riesgo músculo)
- >1,3 kg/semana = peligroso (déficit >1000 kcal/día)

## Reglas de interpretación

- **NO confundir agua con grasa:** la báscula fluctúa ±1-2 kg por agua
- **Primera semana siempre es la de mayor caída:** vacío de glicógeno + retenciones post-copatrona
- **La tendencia semanal es lo que importa,** no el día a día
- **Comer por debajo de TMB todos los días = déficit real,** aunque haya días de copatrona
- **Beber mucha agua = menos retención:** paradoja, más agua = menos agua retenida

## Proyección de fechas

Para calcular peso en fecha X:
```
semanas = (fecha_X - fecha_actual).days / 7
peso_X = peso_actual - (semanas × kg_por_semana)
```

Ritmos de referencia:
- 0,3 kg/semana → ~26 semanas para bajar 8 kg
- 0,5 kg/semana → ~16 semanas para bajar 8 kg
- 0,7 kg/semana → ~11 semanas para bajar 8 kg
- 1,0 kg/semana → ~8 semanas para bajar 8 kg (agresivo)

### Ritmo real de últimos 7 días

Para proyecciones basadas en datos reales (no teóricos), calcular el ritmo de los últimos 7 días de peso:

```
peso_7d = peso.slice(-7)
p_inicio = peso_7d[0].peso_kg
p_fin = peso_7d[-1].peso_kg
dias = (fecha(p_fin) - fecha(p_inicio)) / 86400000
ritmo_real = max(0, (p_inicio - p_fin) / dias * 7)  # en kg/semana
```

**Cuándo usar:**
- El usuario pide "cuándo llego si sigo así" → usar ritmo real, no teórico
- El ritmo real suele ser menor que el acelerado (0,7) porque incluye días de alcohol, comidas sociales, y fluctuaciones
- Si el usuario tuvo una semana de copatrona/cenas especiales, el ritmo real baja → advertir que ese ritmo es el "real con desvíos", no el "real optimizado"

**Dashboard:** se muestra como primera línea morada en el chart de proyecciones y como primer escenario en la tabla.

## Plan óptimo para acelerar

Para pasar de 0,5 a 0,7 kg/semana:
1. Mantener ~1700 kcal/día (consistente, sin picos ni valles extremos)
2. 10.000 pasos/día mínimo (+300 kcal)
3. Gimnasio 4x/semana: 3 días fuerza + 1 día cardio HIIT (+300-400 kcal)
4. Proteína alta: 140-160g/día (proteger músculo)
5. Dormir 7-8 horas (regula cortisol y hambre)

## Pitfalls

- **NO promediar días con datos faltantes sin marcarlos como estimados**
- **NO asumir que la copatrona arruina todo:** un día de 3800 kcal se compensa con 2-3 días de déficit
- **NO dar miedo con números:** explicar siempre que la fluctuación de agua es normal
- **SIEMPRE aclarar la proporción grasa vs agua** cuando el usuario se sorprende con la báscula
