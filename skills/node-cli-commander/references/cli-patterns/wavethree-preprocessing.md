# Caso de uso: WaveThree Preprocessing CLI

## Contexto

Proyecto WaveThree (visor marino 3D con Three.js) necesita un pipeline de preprocesamiento de datos oceanográficos reales.

## Implementación

### gebco-extract.js
- Lee tiles GEBCO en formato NetCDF (usando lib `netcdfjs`)
- Filtra por región geográfica (lat/lon)
- Convierte a heightmap binario: `[width: uint32][height: uint32][Float32LE data]`
- Exporta `extractGebco(opts)` + entry point standalone
- Maneja variables de batimetría genéricas (elevation, grid_values, bathymetry, z, depth)
- Genera coordenadas lineales como fallback si no hay lat/lon explícitas

### scenario-generator.js
- Parsea CSV de datos de boya/SWAN: fecha, hs, tp, dir, wind_speed, wind_dir
- Genera JSON compatible con formato de `data/scenarios/temporal_2026_01_17_1200.json`
- Soporta `--format single` (último registro) y `--format array` (todos)
- Conversión de dirección numérica → cardinal (N, NNE, NE, etc.)
- Exporta `generateScenarios(opts)` + entry point standalone

### index.js
- CLI principal con Commander.js
- Subcomandos: `gebco` y `scenario`
- Cada subcomando pasa opciones como objeto a la función exportada
- Error handling con try/catch + process.exit(1)

### package.json
```json
{
  "scripts": {
    "start": "node src/index.js",
    "gebco": "node src/index.js gebco",
    "scenario": "node src/index.js scenario"
  }
}
```

## Commit
`43feb1f` — 📦 Fase 1.3: Pipeline datos reales — GEBCO extract, scenario generator, CLI
