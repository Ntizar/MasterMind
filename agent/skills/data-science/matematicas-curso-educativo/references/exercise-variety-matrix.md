# Matriz de Variedad de Ejercicios para Archivos con 0 Ejercicios

## Cuándo usarlo

Cuando un archivo HTML tiene TODOS los scores a 0 en progress.json:
- `scores.exercises = 0`
- `scores.real_world = 0`
- `scores.text = 0` (o muy bajo)

Esto significa que el archivo es solo teoría + sliders interactivos, sin NINGÚN ejercicio de evaluación.

## Enfoque: 2-3 ejercicios por capítulo, tipo diferente cada vez

### Regla de oro
**Máximo 2-3 ejercicios por capítulo.** Cada uno debe ser de tipo DIFERENTE.
No añadir más — la variedad > cantidad.

### Matriz de tipos por capítulo

| # | Capítulo | Tipo 1 | Tipo 2 | Tipo 3 |
|---|----------|--------|--------|--------|
| 1 | Multiplicación | Completar hueco | V/F | Problema contextualizado |
| 2 | División | V/F | Completar divisor | Problema inverso |
| 3 | Fracciones | Problema vida real | Completar numerador/denominador | — |
| 4 | Comparar fracciones | Ordenar | Completar > < = | — |
| 5 | Perímetro | Problema contexto | Completar fórmula | V/F |
| 6 | Estadística | Quiz moda | Interpretar datos | — |

### Contenido adicional por capítulo (obligatorio)

Para CADA capítulo, añadir:
1. **1 caso real** — formato `<div class="teoria" style="border-left-color:var(--naranja)">` con `🌍 <strong>Caso real:</strong>`
2. **1 caja error común** — formato `<div class="ejemplo" style="border-left-color:var(--rojo)">` con `⚠️ <strong>Error común:</strong>`

### Ejemplos de casos reales que enganchan

| Tema | Caso real |
|------|-----------|
| Multiplicación | Packs de latas en supermercado |
| División | Repartir galletas entre personas |
| Fracciones | Trozos de pizza, lápices en caja |
| Comparar fracciones | Carrera (quién recorrió más) |
| Perímetro | Valla de jardín, guirnaldas de mesa |
| Estadística | Voto para excursión de clase |

### Ejemplos de errores comunes

| Tema | Error |
|------|-------|
| Multiplicación | Confundir × con + (5×3 ≠ 5+3) |
| División | Confundir cociente con resto |
| Fracciones | Creer que 1/4 > 1/2 |
| Comparar | No aplicar regla del denominador |
| Perímetro | Confundir perímetro con área (cm vs cm²) |
| Estadística | Confundir media con moda |

## Patrón de inserción

Usar `execute_code` con Python `.replace()` (ver `bulk-html-insert-pattern.md`).
Cada bloque se inserta DESPUÉS del `resumen-card` y ANTES del cierre `</div>` del capítulo.

## Verificación post-mejora

Contar en el HTML resultante:
- `Ejercicio` → debe ser 2-3 × número de capítulos
- `Caso real` → debe ser = número de capítulos
- `Error común` → debe ser = número de capítulos
- Tipos únicos → mínimo 4 tipos diferentes en total
