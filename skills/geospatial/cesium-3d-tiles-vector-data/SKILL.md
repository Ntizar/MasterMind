---
name: cesium-3d-tiles-vector-data
version: "1.0.0"
description: "Conocimiento completo sobre el soporte de datos vectoriales nativos en 3D Tiles 2.0 de Cesium: especificación, glTF extensions, pipeline de tiling, integración con CesiumJS/Unreal."
---

# Cesium 3D Tiles — Soporte de Datos Vectoriales

**Fuente:** [Help Shape Vector Data Support in 3D Tiles](https://cesium.com/blog/2026/06/29/help-shape-vector-data-support-in-3d-tiles/) — Xuan Huang, Cesium, 29 Jun 2026

## Contexto

Cesium añade soporte 3D-native para **puntos, líneas y polígonos vectoriales** en 3D Tiles 2.0. Es la petición más longeva de la comunidad. Además añaden soporte runtime de **Mapbox Vector Tiles (MVT)** en CesiumJS y Cesium for Unreal.

## Problema actual

El ecosistema de datos vectoriales es **mayoritariamente 2D**: MVT, MapLibre Tiles (MLT), GeoJSON. Optimizados para tiles planos con proyección Web Mercator. No sirven para:

- Carreteras con precisión centimétrica sobre terreno 3D
- Torres de telecomunicaciones con datos vectoriales superpuestos
- POIs extraídos por IA a escala global con elevaciones precisas
- Ingeniería: diseños de construcción con anotaciones 3D, grietas en puentes (cara superior e inferior)

## Estrategia de Cesium (doble vía)

### 1. 3D Tiles 2.0 nativo para vector
- Extender el estándar 3D Tiles 2.0 (basado en glTF) para soportar vector data
- Los tiles vectoriales usan el mismo spatial indexing, attribute encoding y LOD que meshes y point clouds
- Compresión: Meshopt + Gzip

### 2. Soporte runtime de MVT
- Mapbox Vector Tiles en CesiumJS y Cesium for Unreal
- Reutiliza los mismos pipelines de rendering que 3D Tiles
- Complementa el soporte GeoJSON ya existente

## Especificación técnica

### Extensiones propuestas

| Extensión | Ámbito | Propósito |
|-----------|--------|-----------|
| `3DTILES_content_gltf_vector` | 3D Tiles extension | Identifica tile content como "vector data". Compatible con 3D Tiles 1.1. Equivalente planeado para 2.0 |
| `KHR_mesh_primitive_restart` | glTF extension | Codificación eficiente de `LINE_STRIP` y `LINE_LOOP` para líneas y polígonos |
| `EXT_mesh_polygon` | glTF extension | Representación backwards-compatible de polígonos preservando topología + triangulación runtime-ready |
| `EXT_mesh_features` + `EXT_structural_metadata` | glTF extensions | Feature IDs, propiedades y metadatos en tiles vectoriales |

### Requisitos de diseño (user-driven)

**Elementos fundamentales:**
- Puntos, líneas y polígonos
- Coordenadas 3D con manejo graceful de 2D/2.5D
- Querying y styling de propiedades por elemento

**Tiling flexible:**
- Streaming en tiempo real con LOD
- Coordenadas 3D no referenciadas a la Tierra (Marte, Luna)
- Esquemas: quadtrees, octrees, k-d-trees, Discrete Global Grid Systems (DGGS)
- Crítico para regiones polares o estructuras verticales (postes, presas) donde Web Mercator no funciona

**Visualización de alta fidelidad:**
- Deserialización runtime eficiente (formatos binarios, compresión GPU-ready)
- Precisión centímetro-milimétrica para alinear vector con no-vector (escaneados, fotogrametría)

## Pipeline completo

```
GeoJSON (input)
  → Optimized tiling pipeline (Cesium ion o self-hosted)
    → glTF encoding (con extensiones)
      → Streaming + LOD
        → Render en CesiumJS / Cesium for Unreal / Cesium Native
```

### Formatos de entrada (fase 1)
- **GeoJSON** — formato inicial soportado
- **GeoPackage** — según feedback comunidad
- **Shapefiles** — según feedback comunidad

### Formatos adicionales runtime
- **MVT (Mapbox Vector Tiles)** — soporte en CesiumJS

### Fases futuras
- Extender styling support
- 3D Tiles + terrain clamping
- Más formatos fuente
- Rendimiento y robustez

## Casos de uso documentados

1. **Tráfico regional** — 150.000 links (polylines) de OpenPaths, Atlanta Regional Council
2. **AEC (Arquitectura/Ingeniería/Construcción)** — modelos 3D con anotaciones, niveles, tags
3. **Puentes** — detección de grietas con drone photogrammetry (Robert Street bridge, St. Paul, MN) — solo 3D-native captura grietas bajo el puente
4. **Túneles** — vector data derivado de iTwin Capture AI Analysis desde LiDAR móvil
5. **Smart Construction** — EARTHBRAIN Dashboard, linework en proyectos complejos
6. **300K points** — detección por computer vision de Blyncsy en CesiumJS
7. **Carreteras 3D** — diseño hipotético en Coffs Harbour, NSW Australia (Bentley), 3 LODs con elevaciones reales
8. **Building footprints NYC** — 13 LODs, styling runtime (azul, dashed outlines)

## Relevancia para proyectos Ntizar

- **DataHubEspana** — potencial para integrar tiles vectoriales 3D (catastro, infraestructuras)
- **GTFSSpain** — rutas de transporte en 3D con precisión centimétrica sobre terreno
- **GBFSSpain** — estaciones de bicicletas como puntos 3D con elevación real
- **Visor Hermes Fomento** — superposición de datos vectoriales MITMA/NAP en 3D

## Recursos

- [Cesium Community Forum](https://community.cesium.com/) — dejar feedback sobre la especificación
- [3D Tiles Spec](https://github.com/CesiumGS/3d-tiles)
- [glTF Extensions](https://github.com/KhronosGroup/glTF/tree/main/extensions)
- Artículo original: Xuan Huang, Jun 29 2026