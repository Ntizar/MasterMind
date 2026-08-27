---
name: gtfs-tidy
description: GTFS Tidy — limpieza y validación de feeds GTFS con herramientas CLI programables en Go.
category: geospatial
---

# GTFS Tidy — Limpieza de Feeds GTFS

## Qué es

GTFS Tidy es una herramienta CLI en Go para limpiar y validar feeds GTFS:
- **Limpieza automática** — normaliza IDs, remove duplicados
- **Validación** — detecta errores comunes en feeds GTFS
- **Programable** — crear reglas de validación custom
- **Rápido** — compilado en Go, muy eficiente

## Instalación

```bash
# Instalación desde source
go install github.com/patrickbr/gtfstidy@latest

# O descargar binario
# https://github.com/patrickbr/gtfstidy/releases
```

## Uso básico

```bash
# Limpiar un feed GTFS
gtfstidy --input feed.zip --output clean.zip

# Validar un feed
gtfstidy --validate feed.zip

# Ver info del feed
gtfstidy --info feed.zip
```

## Casos de uso para David

- **Limpieza de GTFS** — normalizar feeds antes de procesar
- **Validación** — verificar calidad de feeds de transporte
- **Pipeline** — integrar en pipeline de datos de transporte
- **Debug** — entender errores en feeds GTFS

## Pitfalls

- Requiere Go instalado para compilar desde source
- No modifica el formato GTFS, solo limpia datos
- Algunas reglas de validación son configurables
- Feed zip debe seguir formato GTFS estándar

## Referencias

- Repo: `github.com/patrickbr/gtfstidy` (148⭐)
