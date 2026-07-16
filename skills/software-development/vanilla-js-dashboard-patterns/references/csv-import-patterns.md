# CSV Import/Export Patterns — Detalle de sesión PLANDEMOVILIDAD

## Parser CSV completo

### Manejo de edge cases
- **BOM UTF-8**: Excel añade `\uFEFF` al inicio. Eliminar: `if (texto.charCodeAt(0) === 0xFEFF) texto = texto.substring(1);`
- **Comillas dobles**: `"campo con ""comillas"" escapadas"` → `campo con "comillas" escapadas`
- **Saltos de línea en campos**: `"campo\nmultilínea"` → se parsea como un solo campo
- **CSV vacío o con 1 línea**: Devolver error explícito

### Detección de formato
El parser detecta automáticamente el tipo de CSV:
- `encuesta_movilidad` — Tiene `modo_principal` + `distancia_km`
- `lista_empleados` — Tiene `departamento` pero no `modo_principal`
- `generico` — No matchea patrones conocidos

### Mapeo de columnas (30+ columnas)
```js
// Ejemplo de mapeo para PLANDEMOVILIDAD
'modo_principal': 'modo_principal',  // nombre exacto
'modo principal': 'modo_principal',  // con espacio
'distancia_km': 'distancia_km',     // nombre exacto
'distancia km': 'distancia_km',     // con espacio
'distancia': 'distancia_km',        // abreviado
```

### Normalización de modos de transporte
15+ aliases mapeados a valores canónicos:
- `coche`, `car`, `particular` → `coche_particular`
- `bus`, `autobus`, `metro`, `tren` → `transporte_publico`
- `bici`, `bike` → `bicicleta`
- `pie`, `caminando`, `walking` → `a_pie`

### Validación
- Columnas requeridas: `nombre`, `departamento`, `modo_principal`, `distancia_km`, `tiempo_viaje_min`
- Distancias fuera de rango (0-500 km): advertencia
- Filas sin nombre o sin modo: conteo de advertencias

### Export CSV con BOM
```js
const BOM = '\uFEFF';
const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
```
El BOM hace que Excel reconozca UTF-8 automáticamente.

## Test real: 15 empleados
- 21 columnas, 100% cobertura
- 10 departamentos detectados
- Reparto modal: coche=8, TP=4, bici=2, pie=1
- Cero errores de validación
