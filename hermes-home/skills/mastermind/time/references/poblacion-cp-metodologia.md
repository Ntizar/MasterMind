# Datos de Población por CP — Metodología

## Problema
INE NO publica población por código postal, solo por municipio (Padrón Municipal).

## Solución
1. **Fuente:** Wikipedia "Anexo:Municipios de España por población" (ref INE Padrón 2025)
2. **Distribución proporcional:**
   ```
   peso_cp = 0.3 + 1.4 * (densidad_cp / densidad_max_municipio)
   poblacion_cp = round(poblacion_municipio * peso_cp / suma_pesos)
   ```
   Rango pesos [0.3, 1.7] — evita que un CP concentre toda la población.

## Cobertura: 299 CPs, 30 municipios, ~13.2M habitantes

Principales: Madrid(48 CPs), Barcelona(30), Valencia(20), Zaragoza(10), Sevilla(16), Málaga(10), Bilbao(10), Palma(10), Las Palmas(10), Alicante(10)

## Superficie estimada por densidad relativa
- >=10k densidad → 0.8 km² (centro)
- >=5k → 1.8 km²
- >=1k → 5.0 km²
- <1k → 8.0 km² (periferia/rural)

## Actualización
Re-scrapear Wikipedia anualmente → re-aplicar distribución → verificar con censo INE.
