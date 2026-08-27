# Datos de Población por CP — Metodología Completa

## Problema
El INE (Instituto Nacional de Estadística de España) **NO publica población por código postal**. Solo publica por municipio (Padrón Municipal) y por provincia. Esto es una limitación conocida que afecta a cualquier proyecto que necesite datos demográficos granulares por CP.

## Solución implementada

### 1. Obtención de población municipal
**Fuente:** Wikipedia "Anexo:Municipios de España por población"
- Referencia: INE Padrón Municipal 1 de enero de 2025
- URL: `https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n`

**Por qué Wikipedia:**
- El INE web bloquea scraping (404 en endpoints)
- datos.gob.es devuelve 403 sin session
- Wikipedia referencia directamente datos del INE y tiene tablas bien estructuradas
- Actualizado regularmente con datos oficiales

**Parsing:**
```python
# 1. Descargar HTML
# 2. Buscar tablas sortable: re.finditer(r'<table[^>]*class="[^"]*sortable[^"]*"[^>]*>(.*?)</table>', content, re.DOTALL)
# 3. Para cada tabla, extraer filas: re.findall(r'<tr[^>]*>(.*?)</tr>', table_content, re.DOTALL)
# 4. Limpiar celdas: re.sub(r'<[^>]+>', '', cell).strip()
# 5. Parsear población: re.sub(r'[^\d]', '', pop_text) → int()
```

**Estructura de tablas Wikipedia:**
- Secciones por rango: >500k, 200-500k, 100-200k, 50-100k, 20-50k, 10-20k, 5-10k
- Columnas: #, Nombre, Población (fecha), Provincia, Comunidad autónoma
- Población en formato "3 506 730" (espacios como separadores de miles)

### 2. Distribución proporcional a CPs
Para cada municipio con N CPs:

```
peso_cp = 0.3 + 1.4 * (densidad_cp / densidad_max_municipio)
poblacion_cp = round(poblacion_municipio * peso_cp / suma_pesos)
```

**Rango de pesos [0.3, 1.7]:**
- 0.3 = CP menos denso del municipio (recibe al menos 30% del peso base)
- 1.7 = CP más denso del municipio (recibe hasta 1.7x del peso base)
- Esto evita que un solo CP concentre toda la población

**Verificación:** La suma de CPs por municipio coincide exactamente con la población municipal (±1 por redondeo).

### 3. Estimación de superficie por CP
Basada en la densidad relativa del CP:

| Densidad relativa | Superficie estimada |
|---|---|
| >= 10,000 | 0.8 km² (centro urbano) |
| >= 7,000 | 1.2 km² |
| >= 5,000 | 1.8 km² |
| >= 3,000 | 2.5 km² |
| >= 2,000 | 3.5 km² |
| >= 1,000 | 5.0 km² |
| < 1,000 | 8.0 km² (periferia/rural) |

### 4. Cálculo de densidad real
```
densidad_real = poblacion / superficie_km2
```

## Cobertura actual (299 CPs, 30 municipios)

| Municipio | Población | CPs |
|---|---|---|
| Madrid | 3,506,730 | 48 |
| Barcelona | 1,731,649 | 30 |
| Valencia | 840,792 | 20 |
| Zaragoza | 693,091 | 10 |
| Sevilla | 689,423 | 16 |
| Málaga | 599,063 | 10 |
| Murcia | 479,405 | — |
| Palma de Mallorca | 434,786 | 10 |
| Las Palmas de Gran Canaria | 381,868 | 10 |
| Alicante | 366,221 | 10 |
| Bilbao | 351,124 | 10 |
| Córdoba | 323,262 | 10 |
| Valladolid | 302,614 | 10 |
| Vigo | 294,489 | 10 |
| Gijón | 269,894 | 8 |
| La Coruña | 260,699 | 10 |
| Granada | 233,975 | 10 |
| Oviedo | 223,968 | 8 |
| Santa Cruz de Tenerife | 211,957 | 10 |
| Pamplona | 209,094 | 10 |
| Alcalá de Henares | 203,208 | 2 |
| San Sebastián | 189,866 | 10 |
| Santander | 175,425 | 10 |
| Alcobendas | 123,342 | 2 |
| Rivas-Vaciamadrid | 103,148 | 1 |
| San Sebastián de los Reyes | 97,983 | 1 |
| Getafe | 193,238 | 8 |
| Valdemoro | 85,972 | 1 |
| Aranjuez | 63,040 | 2 |
| San Martín de la Vega | 21,010 | 1 |
| San Lorenzo de El Escorial | 18,489 | 1 |

**Total población cubierta:** ~13.2M habitantes

## Fuentes alternativas (si falla Wikipedia)

1. **INE vía Nomenclátor:** `www.ine.es/daco/daco42/nomina/cp.htm` — solo lista de CPs, sin población
2. **Eurostat:** No tiene datos a nivel de CP para España
3. **WorldPop:** Requiere API key, datos por grilla 100m
4. **OpenStreetMap:** No tiene datos de población directa, pero se puede usar para estimar superficie habitada
5. **Padrón Municipal directo:** Descargar CSV del INE (requiere registro y navegación web)

## Actualización futura
Para actualizar los datos:
1. Re-scrapear Wikipedia (los datos se actualizan anualmente)
2. Re-aplicar distribución proporcional
3. Comparar con censo INE para verificar coherencia
