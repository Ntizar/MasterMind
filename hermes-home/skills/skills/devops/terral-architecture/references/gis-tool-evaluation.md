# Evaluación de Herramientas GIS para TerrAn

## GeoLibre (opengeos/GeoLibre) — Análisis 2026-06-11

### Qué es
GIS de escritorio/web completo. 622⭐, MIT, TypeScript + React + Tauri.
Stack: deck.gl 9.3, MapLibre GL 5.24, DuckDB-WASM, 3D Tiles.

### Qué hace bien (y podemos借鉴)
| Componente | Uso en TerrAn | Acción |
|---|---|---|
| MapLibre GL | Base del mapa 2D (mejor que Leaflet para miles de polígonos) | Considerar como tile layer |
| deck.gl | Capas 3D geoespacial (puntos, líneas, meshes) | Alternativa a Three.js para datos en mapa |
| 3D Tiles | Edificios OSM como tiles 3D estandarizados | Más eficiente que extruir cada building |
| DuckDB-WASM | Queries espaciales SQL en el navegador | Para dashboard interactivo |
| Plugin system | Modelo de arquitectura modular | Referencia para módulos TerrAn |

### Qué NO tiene (y TerrAn SÍ necesita)
- ❌ Auth / RBAC / multi-tenant
- ❌ CRUD de activos / inventarios
- ❌ Audit trail
- ❌ Gestión documental (PDFs)
- ❌ Búsqueda semántica (RAG)
- ❌ Personal / turnos / vacaciones
- ❌ Mantenimientos / inspecciones
- ❌ WebSocket real-time
- ❌ Stock / almacén
- ❌ Facturación / contratos

### Veredicto
**NO construir TerrAn encima de GeoLibre.** Razones:
1. GeoLibre es GIS, TerrAn es ERP — productos diferentes
2. React + TS vs vanilla JS — stack incompatible con preferencia de David
3. El 80% de TerrAn (lógica de negocio) hay que construirlo desde cero
4. Añadir GeoLibre = dependencia pesada (monorepo 20+ workspaces, Tauri, Rust)

**SÍ tomar prestados patrones:**
- MapLibre GL para tile layer 2D
- 3D Tiles para edificios (formato estándar)
- Plugin architecture (registro dinámico)
- Docker deployment pattern

### Patrón de evaluación (reutilizable)
Para evaluar cualquier herramienta externa:
1. **¿Qué hace?** — Features principales
2. **¿Qué necesito que NO hace?** — Gap analysis
3. **¿Qué componentes SÍ puedo reutilizar?** — Componentes modulares
4. **¿Construir encima aporta o complica?** — Coste/beneficio de integración
5. **¿Stack compatible?** — React vs vanilla, TypeScript vs JS, etc.
