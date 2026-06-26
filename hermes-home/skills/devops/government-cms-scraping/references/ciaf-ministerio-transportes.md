# CIAF — Ministerio de Transportes (caso concreto)

## Estructura de URLs

| Año | Patrón principal | Patrón subpáginas | Estado |
|---|---|---|---|
| 2007-2014 | `/informes-finales/AÑO` → 404 | `/informes-finales/AÑO/informes-accidentes-ferroviarios-AÑO` | ✅ 157 PDFs |
| 2015-2016 | `/informes-finales/AÑO` | — | ✅ 21 PDFs |
| 2017-2025 | `/informes-finales/infofin-AÑO` | — | ✅ 38 PDFs |

**Total:** 270 PDFs, 263 MB

## Patrón de subpáginas (2007-2014)

```
# Página principal: solo menú, sin contenido
curl -s "https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/2008"
# → 73KB de menú, 0 PDFs

# Subpágina con PDFs:
curl -s "https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/2008/informes-accidentes-ferroviarios-2008"
# → 53 PDFs encontrados
```

## Patrones de path de PDFs (cambian según año)

```
# 2007-2014 (UUID-based)
/recursos_mfom/pdf/UUID/NOMBRE/ARCHIVO.pdf

# 2015-2016 (viejo)
/recursos_mfom/160927-151022-if-ciaf.pdf
/recursos_mfom/comodin/recursos/170919160123ifsn_ciaf.pdf

# 2015-2016 (medio)
/recursos_mfom/pdf/UUID/138417/160531150318IFCIAF.pdf

# 2017-2025 (nuevo)
/recursos_mfom/paginabasica/recursos/2025-41-0522-if.pdf
```

## Regex para extraer PDFs

```bash
# Patrón UUID (2007-2014) — cuidado con títulos con espacios
grep -oP "href=(['\"])(/recursos_mfom/pdf/[^'\"]+?\.pdf)\1"

# Patrón paginabasica (2017-2025)
grep -oP '/recursos_mfom/paginabasica/recursos/[^"<\s]+\.pdf'

# Patrón genérico
grep -oP '/recursos_mfom/[^"<\s]+\.pdf'
```

## Distribución por año

| Año | PDFs |
|---|---|
| 2007 | 4 |
| 2008 | 53 |
| 2009 | 43 |
| 2010 | 28 |
| 2011 | 24 |
| 2012 | 22 |
| 2013 | 23 |
| 2014 | 14 |
| 2015 | 10 |
| 2016 | 11 |
| 2017 | 12 |
| 2018 | 2 |
| 2019 | 3 |
| 2020 | 3 |
| 2021 | 6 |
| 2022 | 5 |
| 2023 | 3 |
| 2024 | 3 |
| 2025 | 1 |

## Script de referencia

Ver SKILL.md para el procedimiento genérico.