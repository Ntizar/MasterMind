---
name: plateau-3d-city-mcp
version: "1.0.0"
description: "MCP server para datos 3D city de Project PLATEAU — scene-editing y glTF export de modelos 3D de ciudades japonesas. Inspirado en pixelx-jp/plateau-creative-mcp (⭐30)."
tags: [mcp, 3d, city, plateau, gltf, scene-editing, japan]
---

# PLATEAU 3D City MCP

## Resumen

MCP server que expone datos 3D city de [Project PLATEAU](https://www.mlit.go.jp/plateau/) (gobierno japonés) como herramientas para agentes IA. Permite scene-editing y export glTF de modelos 3D de ciudades.

## Cuándo usar

- Integrar datos 3D de ciudades en un agente IA via MCP
- Editar escenas 3D de ciudades con comandos naturales
- Exportar modelos 3D de ciudades a glTF para three.js/WebGL
- Análisis urbano con modelos 3D reales

## Patrón de uso

```python
# Configurar MCP server en Hermes
# config.yaml:
# mcp:
#   servers:
#     plateau:
#       command: npx
#       args: ["-y", "@pixelx/plateau-mcp"]

# Usar desde el agente
# El agente puede usar las herramientas del MCP server:

# 1. Load city model
city = await mcp_plateau.load_city("Tokyo", area="Shibuya")

# 2. Edit scene — añadir/editar edificios
await mcp_plateau.add_building(
    position=[139.7, 35.65],
    height=50,
    type="office"
)

# 3. Export to glTF
gltf_data = await mcp_plateau.export_gltf(
    area="Shibuya",
    format="glTF",
    draco_compression=True
)

# 4. Query city data
buildings = await mcp_plateau.query_buildings(
    bbox=[139.69, 35.65, 139.70, 35.66],
    filter={"height_min": 30}
)
```

## Herramientas MCP del server

| Herramienta | Función |
|------------|---------|
| `load_city` | Cargar modelo 3D de ciudad por nombre/área |
| `query_buildings` | Consultar edificios por bbox, altura, tipo |
| `add_building` | Añadir edificio a la escena |
| `edit_building` | Editar propiedades de edificio |
| `remove_building` | Eliminar edificio |
| `export_gltf` | Exportar escena a glTF |
| `export_obj` | Exportar escena a OBJ |
| `get_terrain` | Obtener terreno 3D del área |
| `get_roads` | Obtener red de carreteras 3D |

## Pitfalls

- **Datos PLATEAU:** Solo cubre ciudades de Japón. Para otras ciudades, usar OSM Buildings.
- **glTF size:** Modelos de ciudades completas pueden ser muy grandes. Usar Draco compression.
- **MCP setup:** Configurar en config.yaml bajo `mcp.servers`. Requiere reinicio de Hermes.
- **Coordinate system:** PLATEAU usa JGD2011 (sistema japonés). Convertir a WGS84 para interoperabilidad.

## Referencias

- plateau-creative-mcp: https://github.com/pixelx-jp/plateau-creative-mcp
- Project PLATEAU: https://www.mlit.go.jp/plateau/
- MCP: https://modelcontextprotocol.io/

---

**Hecho con ❤️ por David Antizar**
