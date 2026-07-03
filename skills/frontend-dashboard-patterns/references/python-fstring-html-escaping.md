# Python f-string escaping: Generar HTML con template literals JS

## El problema

Cuando generas HTML con JavaScript template literals (`${...}`) dentro de un f-string de Python, PYthon interpreta `{...}` como expresión:

```python
# MAL — Python lanza KeyError
f"showToast(`📦 Cargando ${file.name}...`);"
```

## La solución: `${{...}}`

Escapar la llave duplicándola para que Python la trate como literal:

```python
# BIEN
f"showToast(`📦 Cargando ${{file.name}}...`);"
# → showToast(`📦 Cargando ${file.name}...`);
```

## Reglas de escape

| JS template literal | Python f-string |
|---|---|
| `${variable}` | `${{variable}}` |
| `${obj.prop}` | `${{obj.prop}}` |
| `${func()}` | `${{func()}}` |
| `${arr[i]}` | `${{arr[i]}}` |
| `${(expr)}` | `${{(expr)}}` |

Si el f-string tiene también llaves Python reales (`{}`), se mezclan:
```python
f"items={len(items)}, primer: ${{items[0] if items else 'N/A'}}"
# → items=43, primer: ${items[0] if items else 'N/A'}
```

## Verificación

1. **Lint automático:** Buscar `\$` seguido de `{` sin `{{` en f-strings de `file.py`:
   ```bash
   grep -n 'f".*\${[a-z_]' archivo.py
   ```
   Si encuentra matches con una sola llave (`{variable}` en vez de `{{variable}}`), está mal.

2. **Post-generación:** Si el HTML resultante contiene `$${` o llaves sueltas sin `$`, el escape está mal.

3. **Síntoma en navegador:** JavaScript no se ejecuta. La consola muestra errores de sintaxis tipo `SyntaxError: expected expression, got '}'`.

## Caso práctico: generador de visor HTML GTFS

En `/root/workspace/GTFStoCSV/gtfstocsv/templater.py` — template literals JS dentro de f-strings Python para:
- Nombres de archivo: `${{file.name}}`
- Nombres de ruta: `${{route.route_short_name}}`
- Valores dinámicos: `${{value.toFixed(2)}}`
- Transformaciones: `${{(parseFloat(maxLon) + parseFloat(minLon))/2}}`

## Aplica a

Cualquier código Python que genere HTML con template literals JS:
- Generadores de dashboards/visores
- Generadores de landings HTML
- Informes HTML autocontenidos
- Cualquier patrón donde Python emite JavaScript

## Ver también

- Skill `gtfs-browser-parser` — sección "Python GTFS Parser & Exporter (CLI tool)"
- Proyecto de referencia: `/root/workspace/GTFStoCSV/gtfstocsv/templater.py`
