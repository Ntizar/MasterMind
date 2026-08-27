# INE API — Datos Económicos y Demográficos Reales

## API REST del INE

**Base URL:** `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla_id}?tip=AM&nult=1`

- `tip=AM` → Anual, Modalidad
- `nult=1` → Solo el último año disponible
- Retorna array de objetos con `Nombre`, `MetaData[]`, `Data[]`

## Tablas identificadas

| Tabla | Contenido | Unidad | Registros |
|-------|-----------|--------|-----------|
| 28201 | Salario medio bruto por CA, sexo, edad | €/año | 324 |
| 2852 | Población por provincia y sexo | Personas | 159 |
| 28200 | Salario medio bruto por provincia, contrato | €/año | 162 |

## Estructura de respuesta

```json
[
  {
    "Nombre": "Ambos sexos. Todas las edades. Dato base. Total Nacional. Salario medio bruto.",
    "MetaData": [
      { "T3_Variable": "Sexo", "Nombre": "Ambos sexos", "Codigo": "" },
      { "T3_Variable": "Totales de edad", "Nombre": "Todas las edades" },
      { "T3_Variable": "Tipo de dato", "Nombre": "Dato base" },
      { "T3_Variable": "Conceptos salariales/laborales", "Nombre": "Salario medio bruto" },
      { "T3_Variable": "Comunidades y Ciudades Autónomas", "Nombre": "Madrid, Comunidad de" }
    ],
    "Data": [{ "Anyo": 2024, "Valor": 34410.01, "T3_Periodo": "A" }]
  }
]
```

## Filtros para extraer datos útiles

**Salario bruto por CA (Tabla 28201):**
```
 Sexo = "Ambos sexos"
 Totales de edad = "Todas las edades"
 Tipo de dato = "Dato base"
 Conceptos salariales/laborales = "Salario medio bruto"
 Comunidades y Ciudades Autónomas ≠ "Total Nacional"
```

**Población por provincia (Tabla 2852):**
```
 Sexo = "Total"
 Tamaño de los municipios = "Total habitantes"
 Provincias ≠ "Total Nacional"
```

## Nombres de provincia — Mapeo INE ↔ codigos-postales-spain.json

**Pitfall:** Los nombres del INE usan formato oficial que NO coincide con cp_data.

| codigos-postales-spain.json | INE (Tabla 2852) | salarios-medios.json key |
|----------------------------|-------------------|--------------------------|
| "A Coruña" | "Coruña, A" | "Coruña, A" |
| "Las Palmas" | "Palmas, Las" | "Palmas, Las" |
| "Vizcaya" | "Bizkaia" | "Bizkaia" |
| "Guipúzcoa" | "Gipuzkoa" | "Gipuzkoa" |
| "Baleares" | "Balears, Illes" | "Balears, Illes" |
| "Alicante" | "Alicante/Alacant" | "Alicante/Alacant" |
| "Valencia" | "Valencia/València" | "Valencia/València" |
| "Castellón" | "Castellón/Castelló" | "Castellón/Castelló" |

## IRPF estimado por tramos (general estatal)

| Tramo | Tipo marginal |
|-------|:------------:|
| 0 – 12.450€ | 19% |
| 12.450 – 20.200€ | 24% |
| 20.200 – 35.200€ | 30% |
| 35.200 – 60.000€ | 37% |
| > 60.000€ | 45% |

**Nota:** Sin bonificaciones autonómicas ni circunstancias personales.

## Salarios EAES 2024 — Datos extraídos

| CA | Bruto | Neto est. |
|----|------:|----------:|
| País Vasco | 35.170€ | 26.454€ |
| Madrid | 34.410€ | 25.922€ |
| Navarra | 32.605€ | 24.739€ |
| Cataluña | 31.730€ | 24.046€ |
| Baleares | 29.075€ | 22.125€ |
| Nacional | 29.540€ | 22.513€ |

## Población por provincias (Tabla 2852) — 52 provincias

Ejemplos reales del Padrón Municipal 2025:
- Madrid: 6.751.251 hab.
- Barcelona: 5.714.730 hab.
- Valencia: 2.589.312 hab.
- Sevilla: 1.947.852 hab.
- Málaga: 1.695.651 hab.
- Bilbao (Bizkaia): 1.154.334 hab.

## Pitfalls

1. **NAP_API_KEY:** Configurar en `.env`. El endpoint `/api/v2/fichero/{id}/descarga` SÍ funciona (devuelve redirect a S3).
2. **ORS funciona sin prefijo `Key`:** El token se envía directamente en `Authorization: <token>`, NO como `Key <token>` ni `Bearer <token>`.
3. **INE web bloquea scraping:** No intentar scraping directo de ine.es. Usar la API REST.
4. **Tabla 56934 NO es renta:** Es población. Las tablas de renta están en otros IDs (28201 para salarios).
5. **Tabla 2852 tiene datos de provincia:** 52 provincias con población real del Padrón Municipal 2025. Usar filtro: `Total habitantes` + `Personas` + nombre de provincia.
6. **Tabla 9683 NO sirve para provincias:** Devuelve datos a nivel de CCAA, no de provincia. Usar 2852 en su lugar.
7. **Datos solo REALES:** David insiste en que no se inventen datos. Si no hay dato oficial disponible, indicar "No disponible" en el informe. Nunca usar estimaciones por proxy para variables económicas o demográficas.
