---
name: ineapy-ine-espana
version: 1.0.0
category: devops
description: >
  Librería Python para acceder a datos del INE (Instituto Nacional de Estadística) de España.
  Dos interfaces: INEWrapper (bajo nivel, HTTP directo) y INEConsultor (alto nivel, DataFrame-ready).
  API oficial: https://servicios.ine.es/wstempus/js/{lang}/{funcion}/{input}
  Repo: https://github.com/Angel-RC/ineapy
---

# INEapy — Acceso a datos del INE de España

## Instalación

```bash
pip install ineapy pandas
```

Dependencias: `dlt`, `pydantic`, `pandas`. No requiere API key (API pública del INE).

## Arquitectura

```
INEapy
├── INEWrapper (bajo nivel) → requests a servicios.ine.es, JSON crudo
│   └── Usa dlt RESTClient + PageNumberPaginator
└── INEConsultor (alto nivel) → métodos simples, salidas listas para pandas
    └── Parsea respuestas, devuelve dicts con timestamps y metadata
```

## APIs base

- **Wrapper:** `https://servicios.ine.es/wstempus/js/{ES|EN}/`
- **Catálogo:** https://www.ine.es/dyngs/INEbase/en/listaoperaciones.htm
- **Doc API:** https://www.ine.es/dyngs/DAB/index.htm?cid=1099

## INEConsultor — Interfaz recomendada

```python
from ineapy import INEConsultor
c = INEConsultor()          # Español (default)
c_en = INEConsultor(language="EN")  # Inglés
```

### Listar operaciones disponibles

```python
ops = c.list_operations()           # Todas
ops = c.list_operations(filter_geo=0)  # Solo nacional
ops = c.list_operations(filter_geo=1)  # Solo CCAA
# → [{'id_operation': 25, 'cod_operation': 'IPC', 'name_operation': '...'}]
```

### Operaciones estadísticas más útiles

| Código | Nombre | Variables comunes |
|--------|--------|-------------------|
| `IPC` | Índice de Precios de Consumo | 349=Total Nacional, 762=Grupos ECOICOP, 3=Tipo dato |
| `IPCA` | IPC Armonizado | Mismas que IPC |
| `EPA` | Encuesta de Población Activa | Desempleo, empleo |
| `PIB` / `CNTR` | Contabilidad Nacional | PIB nominal/real |
| `IPI` | Índice de Producción Industrial | Por sector |
| `IPRI` | Índices de Precios Industriales | Por sector |
| `EPOBA` | Población actual | Provincias, sexo |
| `CP` | Cifras de Población | Provincias, sexo |
| `EEE:IND` | Estadística Empresas Industriales | Sector |
| `ICN` | Cifras de Negocios Industria | Por sector |

### Obtener info de una operación

```python
info = c.get_operation_info("IPC")
# → {'id_operation': 25, 'cod_operation': 'IPC', 'name_operation': 'Índice de Precios de Consumo (IPC)'}
```

### Listar variables de una operación

```python
variables = c.list_variables("IPC")
# → [{'id_variable': 349, 'name_variable': 'Total Nacional'}, ...]
```

### Listar filtros disponibles

```python
# Todos los filtros de una operación
filters = c.list_filters_from_operation("IPC")
# → [{'id_variable': 3, 'name_variable': 'Tipo de dato', 'id_value': 74, 'name_value': 'Variación anual'}]

# Valores de una variable específica
vals = c.list_filters_from_variable_operation("IPC", "349")
# → [{'id_variable': 349, 'id_value': 16473, 'name_value': 'Total Nacional'}]

# Todas las variables del sistema
all_vars = c.list_variables()
```

### Periodicidades conocidas

```python
p = c.list_periodicities()
# → [{'id': 1, 'name': 'Mensual'}, {'id': 12, 'name': 'Anual'}, ...]
```

| ID | Nombre |
|----|--------|
| 0 | Al Detalle |
| 1 | Mensual |
| 2 | Bimestral |
| 3 | Trimestral |
| 4 | Cuatrimestral |
| 6 | Semestral |
| 7 | Semanal |
| 12 | Anual |
| 30 | Diario |
| 100 | Sin periodicidad |

### Obtener datos — get_series_data (serie conocida)

```python
# Si ya conoces el código de serie
data = c.get_series_data("IPC318622", nult=12)
# → [{'cod_serie': 'IPC318622', 'name_serie': '...', 'timestamp': Timestamp, 'year': 2025, 'value': 2.7, ...}]

# Por rango de fechas
data = c.get_series_data("IPC318622", date="20240101:20241231")
```

### Obtener datos — get_operation_data (con filtros)

```python
# IPC: Variación anual, Total Nacional, Índice general, últimos 6 meses
data = c.get_operation_data(
    cod_operation='IPC',
    filters=['349:16473', '762:304092'],  # Total Nacional + Índice general
    p=1,         # Mensual
    nult=6
)
# → [{'cod_serie': 'IPC318622', 'name_serie': '...', 'timestamp': Timestamp, 'value': 2.7, ...}]
```

**Filtros IPC más usados:**
- `349:16473` → Total Nacional
- `762:304092` → Índice general (CPI total)
- `3:74` → Variación anual (índice de variación)
- `3:83` → Índice (valor absoluto)
- `3:84` → Variación mensual
- `3:85` → Media anual

### Obtener datos de una tabla

```python
# Listar tablas de una operación
tables = c.list_tables_from_operation("IPC")
# → [{'id_table': 24077, 'name_table': 'Índice general nacional...', ...}]

# Obtener datos de una tabla
data = c.get_table_data("24077", nult=12)

# Filtros de una tabla
filters = c.list_filters_from_table("24077")
```

### Obtener datos por metadata (método flexible)

```python
data = c.get_operation_data(
    cod_operation='IPC',
    filters=['349:16473', '762:304092'],  # Total Nacional + Índice general
    p=1,
    date="20240101:20241231"  # O nult=N
)
```

## INEWrapper — Acceso bajo nivel

```python
from ineapy import INEWrapper
wrapper = INEWrapper()       # ES
wrapper_en = INEWrapper(language="EN")
```

### Parámetros comunes

- `det` (int): Nivel de detalle — 0=básico, 1=intermedio, 2=completo
- `tip` (str): Tipo respuesta — ""=normal, "A"]=friendly, "M"]=metadata, "AM"]=friendly+metadata
- `nult` (int): Últimos N datos
- `date` (str): Rango fechas `"yyyymmdd:yyyymmdd"`
- `page` (int): Número de página
- `filters` (list): Filtros `["id_variable:id_value"]`
- `p` (int): Periodicidad (ver tabla arriba)

### Métodos Wrapper — Operaciones

```python
r = wrapper.get_available_operations(det=0, tip="")     # Lista operaciones
r = wrapper.get_operation("IPC", det=0, tip="M")        # Info operación
r = wrapper.get_operation_tables("IPC", det=2, tip="M") # Tablas de operación
```

### Métodos Wrapper — Series

```python
r = wrapper.get_series("IPC318622", det=1, tip="M")     # Info serie
r = wrapper.get_series_data("IPC318622", nult=12)        # Datos serie
r = wrapper.get_series_values("IPC318622", det=1)        # Valores serie
r = wrapper.get_operation_series("IPC", det=1, tip="M")  # Series de operación (página)
all_series = wrapper.get_operation_series_all_pages("IPC", det=0)  # Todas las series
```

### Métodos Wrapper — Metadata

```python
r = wrapper.get_operation_metadata_series("IPC", filters=["349:16473"], p=1, page=1)
all = wrapper.get_operation_metadata_series_all_pages("IPC", filters=["349:16473"], p=1)
r = wrapper.get_metadata_operation_data("IPC", filters=["349:16473"], p=1, nult=6)
```

### Métodos Wrapper — Variables

```python
r = wrapper.get_variables(det=0)                      # Todas las variables
r = wrapper.get_variable_values("115", det=1)         # Valores de variable
r = wrapper.get_operation_variables("IPC", det=1)     # Variables de operación
r = wrapper.get_operation_variable_values("115", "IPC")  # Valores variable en operación
```

### Métodos Wrapper — Tablas

```python
r = wrapper.get_table("24077", det=2)
r = wrapper.get_table_data("24077", nult=12)
r = wrapper.get_table_series("24077", det=0, tip="M")
r = wrapper.get_table_groups("24077", det=2)
r = wrapper.get_table_group_values("24077", "1", det=1)
```

### Métodos Wrapper — Publicaciones

```python
r = wrapper.get_publications(det=0)
r = wrapper.get_operation_publications("IPC", det=0)
r = wrapper.get_publication_date("1", det=0)
```

### Métodos Wrapper — Periodicidades

```python
r = wrapper.get_periodicities()  # Se llama en __init__, caché en self.periodicities
```

## Errores comunes y pitfalls

1. **Periodicidad inválida**: `p` debe ser uno de los IDs de periodicidad (0,1,2,3,4,6,7,12,13,14,30,31,100,103-113). El error indica las válidas.

2. **Sin `nult` ni `date`**: `get_series_data` y `get_operation_data` requieren al menos uno. Siempre pasar `nult=N` o `date="yyyymmdd:yyyymmdd"`.

3. **Filtros formato**: Deben ser `"id_variable:id_value"` (strings). Ej: `"349:16473"`. Los IDs son numéricos pero se pasan como strings.

4. **Respuesta truncada del INE**: La API del INE a veces devuelve arrays JSON incompletos (sin cerrar `]`). El wrapper lo corrige automáticamente con `__solve_errors_in_response`.

5. **Serie completa sin filtros puede ser masiva**: `list_series_from_operation("IPC")` sin filtros puede tardar o agotar memoria. Usar filtros siempre que sea posible.

6. **`get_operation_data` vs `get_series_data`**: 
   - `get_series_data(cod_serie)` → cuando ya conoces el código de serie
   - `get_operation_data(cod_op, filters, p)` → cuando quieres datos filtrados por variables

7. **Metadata de variable**: Los IDs de variables y valores cambian entre operaciones. Siempre consultar `list_filters_from_variable_operation(op, var)` primero.

8. **El INEWrapper retorna objetos `Response` de requests**. Hay que hacer `.json()` para obtener los datos.

9. **El INEConsultor retorna listas de dicts parseados**. Ya incluye `pd.to_datetime()` en timestamps.

10. **Multi-idioma**: INEWrapper e INEConsultor soportan `language="ES"` (default) y `language="EN"`.

## Ejemplo completo: IPC mensual España

```python
from ineapy import INEConsultor
import pandas as pd

c = INEConsultor()

# 1. Verificar operación existe
info = c.get_operation_info("IPC")
print(f"Operación: {info['name_operation']}")

# 2. Ver variables disponibles
variables = c.list_variables("IPC")
print("Variables:", [v['name_variable'] for v in variables])

# 3. Ver valores de Total Nacional
vals = c.list_filters_from_variable_operation("IPC", "349")
print("Valores:", vals)

# 4. Obtener datos IPC variación anual, total nacional, índice general, mensual, últimos 12
data = c.get_operation_data(
    cod_operation='IPC',
    filters=['349:16473', '762:304092'],
    p=1,  # Mensual
    nult=12
)

# 5. Convertir a DataFrame
df = pd.DataFrame(data)
print(df[['timestamp', 'year', 'period', 'value', 'name_serie']].head(10))

# 6. Filtrar solo variación anual
df_anual = df[df['name_serie'].str.contains('Variación anual')]
print(df_anual[['timestamp', 'value']])
```

## Ejemplo completo: datos de tabla

```python
from ineapy import INEConsultor

c = INEConsultor()

# Listar tablas de IPC
tables = c.list_tables_from_operation("IPC")
print(f"Tablas IPC: {len(tables)}")
for t in tables[:5]:
    print(f"  {t['id_table']}: {t['name_table']}")

# Obtener datos de una tabla específica
data = c.get_table_data("24077", nult=12)
print(f"Datos tabla: {len(data)} puntos")
```

## Nota sobre la API directa del INE

Si se necesita más control o la librería no cubre algún endpoint, se puede usar la API REST directa:

```
GET https://servicios.ine.es/wstempus/js/ES/{FUNCION}/{INPUT}?parametros
```

Ejemplo:
```bash
curl "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC318622?nult=5"
```

La librería `ineapy` encapsula esta API con validación, paginación y manejo de errores.
