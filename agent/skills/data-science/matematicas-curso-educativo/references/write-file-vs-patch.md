# write_file vs patch para HTML de DeSumarIntegrar

## Regla general

| Archivo | Método | Por qué |
|---------|--------|---------|
| > 20KB | `patch()` | Menos riesgo de perder contenido |
| ≤ 20KB + 1-2 cambios | `patch()` | Rápido y seguro |
| ≤ 20KB + 3+ cambios estructurales | `write_file` | Más limpio, evita patches encadenados |

## Cuándo usar write_file

- Nuevas secciones completas (ej: añadir "Línea de longitudes")
- Nuevos tipos de ejercicio (completar hueco, V/F, ordenar)
- Nuevo CSS necesario (nuevas clases)
- Nuevas funciones JS
- **Cualquier combinación de 3+ cambios anteriores**

## Cuándo usar patch

- Añadir 1-2 ejercicios del mismo tipo
- Corregir texto en una caja existente
- Añadir una sola función JS
- Modificar un ejercicio existente

## Ejemplo: write_file (run 13, s01-9-medidas-longitud)

El archivo tenía 10KB y necesitaba:
1. Nueva sección "Línea de longitudes" con CSS nuevo
2. 5 ejercicios nuevos de 5 tipos diferentes
3. 2 nuevas funciones JS (`checkFill1`, `checkFill2`, `checkVF`, `selectSort`, `checkSort`, `resetSort`)
4. Nueva caja de error común

Usar `patch()` hubiera requerido 6+ patches encadenados, con riesgo de conflictos.
`write_file` fue más limpio y seguro.

## Cuidado

- `write_file` SOBREScribe TODO el archivo. Antes de usar, leer el contenido completo con `read_file`.
- Verificar el resultado con `read_file` tras `write_file` para asegurar que nada se perdió.
