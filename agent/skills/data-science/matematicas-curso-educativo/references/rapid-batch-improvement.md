# MODO RÁPIDO — Mejora batch de 4-6 temas por sesión

## Cuándo usarlo

Cuando el cron de mejora continua o un agente manual tiene tiempo/recursos para mejorar varios temas en una sola ejecución, en vez de uno por uno.

## Procedimiento

### 1. Leer estado
```
read_file("/root/workspace/DeSumarIntegrar/progress.json")
read_file("/root/workspace/DeSumarIntegrar/MEGA-PLAN2.md")
```

### 2. Selección rápida (CRÍTICO)

Elegir 4-6 temas con esta prioridad:
1. **Rotar niveles:** Si los últimos fueron Primaria, coger ESO o Bachiller. Si los últimos fueron Bachiller, coger Primaria.
2. **Prioridad más baja** (1 antes que 3)
3. **Menos improvement_count** (los menos mejorados primero)
4. **Scores más bajos** (los que más necesitan mejora)

**Fórmula de selección:**
```python
# Ordenar por: (nivel_rotado, priority ASC, improvement_count ASC, score_total ASC)
# nivel_rotado = 0 si es diferente al nivel de los últimos 2 temas, 1 si es igual
```

**Regla de oro:** Nunca mejorar 2 temas del mismo nivel seguidos. Alternar P → ESO → B → P → ESO → B.

### 3. Mejora de cada tema (plantilla uniforme)

Para CADA tema seleccionado, aplicar exactamente este patrón:

1. **Leer el HTML** del tema
2. **Identificar las 2 dimensiones más débiles** (scores más bajos en progress.json)
3. **Aplicar mejoras:**
   - **Texto:** Añadir 1 explicación 4 pasos (qué es → para qué → cómo → error común)
   - **Ejercicios:** Añadir 2-3 de tipos DIFERENTES (completar, V/F, ordenar, problema contextual, quiz). NO repetir tipo.
   - **Visual:** Añadir 1 visualización SOLO si aporta (línea numérica, gráfico, canvas)
   - **Caso real:** Añadir 1 caso cotidiano que enganche (caramelos, pizza, notas, dinero)
   - **CSS:** Verificar clases del template base. Si falta, añadir.
4. **Actualizar progress.json** (scores, improvements, status)
5. **Git commit:** `git add -A && git commit -m "rapid: [tema] - [dimensiones]"`

### 4. Reglas de MODO RÁPIDO

- **NO** más de 3 ejercicios nuevos por tema
- **NO** visualizaciones decorativas
- **SÍ** rotar niveles obligatoriamente
- **SÍ** git commit por tema (uno por uno, no al final)
- **NO** mejorar más de 6 temas por sesión (límite de tokens/timeout)

### 5. Actualizar progress.json

Tras mejorar cada tema, actualizar en progress.json:
- `status`: `"improved_N"` donde N = improvement_count
- `scores`: actualizar con los valores reales tras la mejora
- `improvements`: añadir descripción de lo mejorado
- `last_improved`: fecha actual

## Ejemplo de ejecución

Sesión mejora 6 temas con rotación:
1. `s04-3-division-2-cifras.html` (4º Primaria)
2. `s05-3-mult-decimales.html` (5º Primaria)
3. `eso1-3-proporcionalidad.html` (1º ESO) ← rotó a ESO
4. `s04-6-areas.html` (4º Primaria)
5. `s09-1-bachiller-limites.html` (Bachiller) ← rotó a Bachiller
6. `s05-7-porcentajes.html` (5º Primaria)

## Diferencias con mejora individual

| Aspecto | Individual | Rápido (batch) |
|---------|-----------|----------------|
| Temas por sesión | 1 | 4-6 |
| Rotación de niveles | No explícita | OBLIGATORIA |
| Selección | Menor score primero | Menor score + nivel rotado |
| Git commit | Al final | Uno por tema |
| Profundidad | Más detallada | Template uniforme |
| Riesgo | Bajo | Medio (más cambios) |
