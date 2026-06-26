# INE API — Datos Económicos y Demográficos Reales

## API REST
`https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla_id}?tip=AM&nult=1`

## Tablas clave
| Tabla | Contenido | Registros |
|-------|-----------|-----------|
| 28201 | Salario bruto por CA, sexo, edad | 324 |
| 2852 | Población por provincia y sexo | 159 |
| 28200 | Salario bruto por provincia, contrato | 162 |

## Mapeo nombres INE ↔ cp_data
| cp_data | INE |
|---------|-----|
| "A Coruña" | "Coruña, A" |
| "Las Palmas" | "Palmas, Las" |
| "Vizcaya" | "Bizkaia" |
| "Guipúzcoa" | "Gipuzkoa" |
| "Baleares" | "Balears, Illes" |
| "Alicante" | "Alicante/Alacant" |
| "Valencia" | "Valencia/València" |
| "Castellón" | "Castellón/Castelló" |

## IRPF tramos (general estatal)
0-12.450€: 19% | 12.450-20.200€: 24% | 20.200-35.200€: 30% | 35.200-60.000€: 37% | >60.000€: 45%

## Salarios EAES 2024
| CA | Bruto |
|----|------:|
| País Vasco | 35.170€ |
| Madrid | 34.410€ |
| Navarra | 32.605€ |
| Cataluña | 31.730€ |
| Nacional | 29.540€ |

## Pitfalls
- INE web bloquea scraping → usar solo API REST
- Tabla 56934 NO es renta, es población
- Tabla 9683 NO sirve para provincias (solo CCAA)
- David insiste: SOLO datos REALES, nunca inventar
