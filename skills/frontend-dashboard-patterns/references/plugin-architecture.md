# Sistema de Plugins Extensible — Referencia

Arquitectura de plugins para proyectos con múltiples fuentes de datos intercambiables.

## Patrón

```javascript
// plugins.js
const PLUGINS = {
    ors: ORSRouter,    // OpenRouteService
    otp: OTPRouter,    // OpenTripPlanner
    nap: GTFSNapRouter // NAP/GTFS
};

export function registerPlugin(name, plugin) {
    PLUGINS[name] = plugin;
}

export async function orchestratePlugins(action, params) {
    const results = {};
    const errors = {};
    
    await Promise.allSettled(
        Object.entries(PLUGINS).map(async ([name, plugin]) => {
            try { results[name] = await plugin[action](params); }
            catch (err) { errors[name] = err.message; }
        })
    );
    
    return { results, errors };
}
```

## Interfaz IRouter

```javascript
class IRouter {
    async resolve(origin, dest, mode) { ... }
    async getIsochrones(point, time, mode) { ... }
}
```

## Para añadir un nuevo plugin

1. Crear `js/routing-{name}.js`
2. Implementar `resolve()` y `getIsochrones()`
3. Registrar: `registerPlugin('name', router)`
4. El orquestador lo llama automáticamente

## Caso real: TimeIneco

- **ors.js** — OpenRouteService (isocronas + routing para coche/bici/peatón)
- **gtfs.js** — Parser GTFS + motor de horarios laborales
- **plugins.js** — Sistema de registro y orquestación
- **main.js** — Orquestador principal que llama a los plugins