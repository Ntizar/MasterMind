# Cesium añade soporte vectorial nativo a 3D Tiles 2.0

**Fecha:** 30 Jun 2026
**Fuente:** https://cesium.com/blog/2026/06/29/help-shape-vector-data-support-in-3d-tiles/
**Autor:** Xuan Huang (Cesium)
**Skill creado:** `cesium-3d-tiles-vector-data`

## Resumen

Cesium anuncia soporte 3D-native para puntos, líneas y polígonos vectoriales en 3D Tiles 2.0. Estrategia doble:
1. **Extender 3D Tiles 2.0** con nuevas extensiones glTF (`3DTILES_content_gltf_vector`, `KHR_mesh_primitive_restart`, `EXT_mesh_polygon`)
2. **Soporte runtime de MVT** en CesiumJS y Cesium for Unreal

Pipeline: GeoJSON → tiling pipeline (ion/self-hosted) → glTF → streaming LOD → runtime

### Extensiones clave
- `3DTILES_content_gltf_vector` — identifica tile content como vector (compatible 1.1)
- `KHR_mesh_primitive_restart` — LINE_STRIP/LINE_LOOP eficientes
- `EXT_mesh_polygon` — polígonos con topología preservada + triangulación
- `EXT_mesh_features` + `EXT_structural_metadata` — metadatos y propiedades

### Relevancia para proyectos Ntizar
DataHubEspana, GTFSSpain, GBFSSpain, Visor Hermes — todos pueden beneficiarse de vector tiles en 3D con precisión real sobre terreno.

**Skill creado y re-indexado en ChromaDB.** El artículo se publicó ayer (29 Jun 2026), acabamos de pillar la primicia.
