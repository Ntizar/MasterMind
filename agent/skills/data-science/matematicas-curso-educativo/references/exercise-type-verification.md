# Verificación programática de variedad de ejercicios

## Cuándo usarlo

Antes de commitear una mejora de HTML en DeSumarIntegrar, verificar que los ejercicios tienen variedad suficiente.

## Patrón

```python
import re
from collections import Counter

with open(file) as f:
    content = f.read()

blocks = re.split(r'<div class="exercise">', content)
blocks = blocks[1:]  # skip before first exercise

types = {'quiz_botones': 0, 'ordenar': 0, 'completar_hueco': 0, 'vf': 0, 'problema': 0, 'input_numeric': 0}

for block in blocks:
    p_match = re.search(r'<p>\d+\.\s*(.*?)</p>', block, re.DOTALL)
    if p_match:
        question = p_match.group(1).strip()[:80]
        if 'Completa la suma repetida' in question:
            types['completar_hueco'] += 1
        elif 'Ordena' in question:
            types['ordenar'] += 1
        elif 'Verdadero o Falso' in question:
            types['vf'] += 1
        elif 'Problema' in question:
            types['problema'] += 1
        elif 'quiz-options' in block:
            types['quiz_botones'] += 1
        elif 'input type="number"' in block:
            types['input_numeric'] += 1

print(f"Total: {sum(types.values())} ejercicios")
for t, c in types.items():
    if c > 0:
        print(f"  {t}: {c}")

# Reglas de validación
total = sum(types.values())
max_count = max(types.values())
max_type = max(types, key=types.get)

if max_count > total * 0.5:
    print(f"WARNING: '{max_type}' tiene {max_count} ejercicios (>50% del total)")
else:
    print(f"OK: Buen distribution: ningun tipo supera 50%")

unique_types = sum(1 for c in types.values() if c > 0)
if unique_types >= 4:
    print(f"OK: {unique_types} tipos diferentes (minimo 4)")
else:
    print(f"WARNING: Solo {unique_types} tipos diferentes (necesitas >=4)")
```

## Reglas

- **Ningún tipo debe superar 50%** del total de ejercicios
- **Mínimo 4 tipos diferentes**
- **Ideal:** 6 tipos diferentes con distribución equilibrada (2-3 por tipo)

## Ejemplo real (s02-3-intro-multiplicacion.html, 2026-06-10)

```
Total: 12 ejercicios
  quiz_botones: 3
  ordenar: 2
  completar_hueco: 2
  vf: 1
  problema: 2
OK: Buena distribución: ningún tipo supera 50%
OK: 5 tipos diferentes (mínimo 4)
```

## Antes de añadir, verificar qué tipos YA existen

El propósito principal de este script es **evitar duplicar tipos**. Antes de decidir qué ejercicio añadir:
1. Ejecutar este script
2. Ver qué tipos tienen count=0
3. Añadir SOLO los tipos ausentes
