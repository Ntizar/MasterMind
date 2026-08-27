---
name: nap-dgt
version: "1.0.0"
description: >
  NAP DGT — Punto de Acceso Nacional de Tráfico y Movilidad de la DGT.
  Catálogo CKAN con datos de tráfico, paneles, cámaras, incidencias, radares,
  zonas de bajas emisiones, Camino de Santiago y más. Formato DATEX2.
---

# NAP DGT — Punto de Acceso Nacional de Tráfico y Movilidad

## Qué es

Portal de datos abiertos de la Dirección General de Tráfico (DGT).
Catálogo CKAN con conjuntos de datos de tráfico, movilidad e infraestructura viaria.
Formato principal: DATEX2 (estándar europeo de datos de tráfico).

## URLs

- **Portal:** https://nap.dgt.es/
- **Catálogo datasets:** https://nap.dgt.es/dataset
- **API CKAN:** https://nap.dgt.es/api/3/action/ (puede requerir auth)
- **Mapa de Movilidad:** http://mapamovilidad.dgt.es/
- **Mapa de Tráfico:** (web integrada)

## Organizaciones del catálogo

- **DGT** — Dirección General de Tráfico (principal)
- **SCT** — Serveis Catalans de Trànsit
- **DT-GV** — Dirección de Tráfico Gobierno Vasco
- **Ayuntamiento de Madrid**
- **112 Comunidad Valenciana**
- **112 Galicia**
- **DGT via HERE**
- **DGT via TomTom**
- **DGT via MITMA** (Dirección General de Carreteras)
- **Diputación de Valencia**

## Datasets disponibles

### Tiempo real (DATEX2 v3.7 — NUEVO)
- **Paneles DGT - Tiempo Real** — Estado de paneles de información al viajero
- **Paneles DGT - Localizaciones** — Ubicación de paneles
- **Cámaras DGT** — Cámaras de vigilancia de tráfico
- **Incidencias DGT** — Accidentes, obras, cortes, eventos

### Tiempo real (DATEX2 legacy — a extinguir 30/09/2026)
- Paneles y localizaciones en formato DATEX2 anterior

### Infraestructura
- **Radares fijos DGT** — Localización de radares de velocidad
- **Tramos INVIVE** — Tramos de interés para la seguridad vial
- **Tramos de elevado riesgo para motocicletas**
- **Límites de velocidad** — Formato ROSATTE XML
- **Señalización vertical** — Red de carreteras (ej: Diputación Valencia, formato TNITS)

### Movilidad
- **Mapa de Movilidad** — Aplicación web: carreteras, PKs, tramos de concentración de accidentes
- **Mapa de Tráfico** — Visualización del estado del tráfico

### Zonas de bajas emisiones
- **ZBE** — Zonas de Bajas Emisiones (DATEX2 v3)

### Seguridad vial
- **Camino de Santiago - Tramos paralelos de riesgo**
- **Camino de Santiago - Puntos de intersección de riesgo**
- **TEFIVA** — Tramos de elevada siniestralidad

### Otros
- **Conos conectados** — Formato JSON
- **Posiciones de vehículos lentos** — JSON
- **Localización de conos para pruebas deportivas** — JSON

## Formato DATEX2

Estándar europeo para intercambio de datos de tráfico.
- Basado en XML
- API: HTTPS endpoints con datos en tiempo real
- Documentación: https://www.datex2.eu/
- Versiones: v3 (actual) y v2 (legacy, a extinguir sept 2026)

## Cómo acceder a un dataset

```bash
# Ver detalles de un dataset
curl -sL "https://nap.dgt.es/dataset/radares-fijos-dgt"

# Descargar recurso (ejemplo radares)
curl -sL "https://nap.dgt.es/dataset/radares-fijos-dgt/resource/<resource-id>"
```

## Relación con otros datasets

- **OpenData Movilidad MITMA** → Datos de movilidad basados en móviles (Orange)
  - `opendata-movilidad-mitma` skill
- **VisorHermes Fomento** → Visor cartográfico de infraestructura de transporte
  - `visor-hermes-fomento` skill
- **ESIOS/REE** → Datos energéticos
  - `esios-complete` skill

## Nota

Guardado 2026-06-30. Catálogo extenso, formato DATEX2 requiere parser dedicado.
Los datasets de tiempo real son ideales para dashboards de tráfico en vivo.
