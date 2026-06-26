# Pitfall: Contenido Duplicado tras Patch

## Problema

Al patchear un bloque inline (ej: `<div class="comparison">...</div>` en una sola línea), el patch puede insertar la versión mejorada PERO dejar la versión original inline. Resultado: **dos versiones del mismo contenido** en el archivo.

## Causa

El `old_string` del patch no incluye la versión original completa, o el patch tool no la encuentra por diferencias mínimas (espacios, saltos de línea).

## Detección

```bash
# Contar elementos duplicados
grep -c 'class="comparison"' file.html
grep -c 'class="box box-ejemplo"' file.html
grep -c 'class="box box-teoria"' file.html
```

Si el conteo subió después de un patch → verificar duplicados.

## Fix

```bash
# Encontrar la versión inline antigua (suele estar en una sola línea)
grep -n 'class="comparison" style="margin:1.5rem 0"' file.html
# Eliminar manualmente con patch o sed
```

## Regla

**Siempre verificar** después de un patch grande:
1. Contar elementos clave con `grep -c`
2. Si el conteo es mayor que antes → buscar duplicados
3. Eliminar la versión duplicada (suele ser la inline, en una sola línea)

## Ejemplo real

- `b07-04-verdadera-magnitud.html`: Al añadir la comparación interactiva mejorada, la versión inline original (`<div class="comparison" style="margin:1.5rem 0"><div class="comparison-side">...`) quedó duplicada. Se eliminó con un script de reemplazo.
