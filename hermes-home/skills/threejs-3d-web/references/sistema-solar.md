# Gemelo Digital del Sistema Solar

Implementación de un sistema solar 3D interactivo con efemérides reales (junio 2026).

## Patrón Kepleriano

Posiciones reales usando ecuación de Kepler:

1. **Julian Date** desde `Date` actual
2. **Anomalía media**: `M = M0 + n * (JD - JD0)` donde `n = 2π/period`
3. **Ecuación de Kepler**: resolver `E - e*sin(E) = M` con Newton-Raphson (10 iteraciones)
4. **Anomalía verdadera**: `ν = 2*atan2(sqrt(1+e)*sin(E/2), sqrt(1-e)*cos(E/2))`
5. **Distancia**: `r = a*(1 - e*cos(E))`
6. **Posición 2D**: `x = r*cos(ν)`, `z = r*sin(ν)`
7. **Inclinación**: `y = z*sin(inclination)`, `z = z*cos(inclination)`

## Datos de planetas

Cada planeta tiene:
- `displayRadius`: radio visual (NO real, escalado para visibilidad)
- `semiMajorAxis`: semi-eje mayor en UA
- `eccentricity`: excentricidad orbital
- `inclination`: inclinación en grados
- `period`: período orbital en días
- `color`: color hexadecimal

## Escalado

- **Distancias**: 1 UA = ~30 unidades Three.js
- **Tamaños**: arbitrarios, NO proporcionales al Sol real
- **Sol**: radio 6, glow radio 10
- **Planetas**: 2.5–5.0 unidades

## Interacción

- **Click en planeta**: raycaster → cámara anima suavemente (cubic easing)
- **OrbitControls**: rotar, zoom, pan con ratón
- **Panel info**: click en nombre → muestra datos

## Deploy

GitHub Pages en branch `gh-pages`. Token HTTPS en `/hermes-home/.env`.
