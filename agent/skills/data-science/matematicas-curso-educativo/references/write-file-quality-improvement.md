# Patrón write_file para mejora de calidad — DeSumarIntegrar

## Cuándo usarlo

Cuando el archivo HTML es **≤ 20KB** y necesita **3+ cambios estructurales**:
- Nuevos tipos de ejercicio (completar hueco, V/F, ordenar, quiz botones, problema inverso)
- Nueva CSS (clases nuevas como `.quiz-btn`, `.order-item`, `.fill-blank`)
- Nuevas funciones JS
- Nuevas secciones pedagógicas (explicación 4 pasos, error común, conexión)

## Procedimiento

### 1. Leer progress.json → seleccionar tema
```python
# Buscar: priority=1, improvement_count < 4, scores más bajos primero
```

### 2. Leer HTML completo con read_file
```
read_file("/root/workspace/DeSumarIntegrar/{archivo}")
```

### 3. Analizar QUÉ FALTA (NO asumir)
Contar en el HTML existente:
- Tipos de ejercicio: ¿cuántos son quiz? ¿cuántos completar hueco? ¿cuántos V/F?
- ¿Hay caja error común? ¿caja conexión?
- ¿Explicación estructurada 4 pasos?
- ¿Casos reales genéricos o cotidianos?

### 4. Planificar mejoras (solo lo que falta)
**Regla de oro: Si un ejercicio no aporta conocimiento nuevo, NO lo añadas.**

| Lo que ya existe | Lo que se añade |
|-------------------|-----------------|
| 10 ejercicios "X×Y=?" (todos iguales) | 7 ejercicios de 7 tipos diferentes |
| Sin explicación estructurada | Explicación 4 pasos (qué/para qué/cómo/error) |
| Sin error común | 1 caja box-error |
| Sin conexión | 1 caja box-idea con conexión |
| Resumen 6 puntos | Resumen 8 puntos |

### 5. Escribir versión completa con write_file
- Mantener CSS existente + añadir clases nuevas
- Mantener canvas/visualizaciones existentes
- Reemplazar ejercicios repetitivos por variados
- Insertar nuevas secciones pedagógicas
- Unificar funciones JS

### 6. Commit + push + actualizar progress.json

## Ejemplo real: s01-3primaria.html (multiplicar)

**Antes:** 10 ejercicios TODOS "X × Y = ?" con input numérico
**Después:** 7 ejercicios de 7 tipos diferentes:
1. Completar hueco: "3 × 5 = 5 + 5 + ___ = ?"
2. Verdadero/Falso: "4 × 3 = 12"
3. Problema contextual: "5 bancos × 3 niños = ?"
4. Ordenar: "Ordena 2×3, 3×3, 4×3, 5×3 de menor a mayor"
5. Quiz botones: "¿Cuánto es 6×2?" con 4 opciones
6. Problema inverso: "4 × ___ = 20"
7. Completar grupo: "___ × 4 = 16"

**Además:**
- Explicación estructurada 4 pasos
- Caso real: panadería del barrio
- Caja error común: no confundir × con +
- Caja conexión: multiplicación = suma rápida
- Resumen ampliado a 8 puntos

## Decisiones clave

1. **write_file > patch** cuando hay 3+ cambios estructurales
2. **Eliminar > añadir** cuando hay ejercicios repetitivos
3. **Variedad > cantidad** — 7 ejercicios de 7 tipos > 10 del mismo tipo
4. **Feedback rico** — cada ejercicio explica el "por qué" del resultado
5. **Verificar post-write** con read_file para asegurar nada se perdió
