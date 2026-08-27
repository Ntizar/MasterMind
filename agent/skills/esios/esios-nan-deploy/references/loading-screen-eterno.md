# Pantalla de carga eterna en SPAs (MapLibre / Leaflet / WebGL)

## Problema

La app se queda en "Inicializando motor WebGL 3D ..." o mensaje similar para siempre.
El servidor responde 200, pero el loading nunca se oculta.

## Causa raíz

El `hideLoading()` (o equivalente) solo se llama en un evento que nunca se dispara:

```javascript
// ❌ Si el mapa falla al cargar, NUNCA se dispara 'load'
map.on('load', () => { hideLoading(); });
```

Cuando el proveedor de tiles falla (CORS, API key inválida, 403, 503, etc.),
el evento `load` nunca se dispara y el loading se queda eterno.

## Solución: doble capa de resiliencia

### 1. Fallback automático en error

```javascript
map.on('error', (e) => {
  console.warn('MapLibre error:', e.error?.status, e.error?.message);
  // Cambiar a estilo fallback (ej: CartoDB)
  map.setStyle('https://basemaps.cartocdn.com/gl/positron-gl-style/style.json');
  map.once('load', () => {
    setupBuildingsLayer();
    setupTerrain();
    setupPOIMarkers();
    applySolarCycle();
    hideLoading();
  });
});
```

**Importante:** No filtrar por status code. Cualquier error (401, CORS, 503) debe triggerear fallback.

### 2. Timeout de seguridad

```javascript
// Si el mapa no carga en 12s, ocultar loading y crear fallback
setTimeout(() => {
  const loading = document.getElementById('loading');
  if (loading && !loading.classList.contains('hidden')) {
    console.warn('Timeout de carga — mostrando mapa sin tiles');
    loading.classList.add('hidden');
    if (!state.map) {
      // Crear mapa fallback con CartoDB
      state.map = new maplibregl.Map({
        container: 'map',
        style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
        center: [-3.7038, 40.4168],
        zoom: 13,
        pitch: 55,
        bearing: -15,
        antialias: true,
        attributionControl: false,
        maxPitch: 85,
      });
      state.map.on('load', () => {
        setupBuildingsLayer();
        setupTerrain();
        setupPOIMarkers();
        applySolarCycle();
      });
    }
  }
}, 12000);
```

## Checklist de debugging

1. Abrir DevTools → Console → ¿hay errores de MapLibre?
2. Verificar que las URLs de tiles son accesibles desde el dominio de deploy
3. Verificar que la API key funciona (no expirada, no restringida por dominio)
4. Comprobar CORS: `curl -I https://tiles.stadiamaps.com/styles/...`
5. Si el estilo falla, el fallback debe funcionar inmediatamente
6. Si NADA funciona, el timeout de 12s es la red de seguridad

## Casos reales

- **NapMaps (junio 2026):** Tiles de Stadia Maps no accesibles desde dominio NaN → loading eterno. Fix: fallback a CartoDB + timeout 12s.
- **MapLibre GL JS:** El estilo JSON se descarga primero, luego los tiles. Si el JSON falla, nunca llega al evento `load`.