# WaveThree — Océano Espectral JONSWAP + FFT 2D

**Fecha de creación:** 2026-06-17  
**Proyecto:** WaveThree (Ntizar/WaveThree)  
**Contexto:** Implementar un océano espectral usando el espectro JONSWAP y FFT 2D en CPU para generar campos de alturas realistas de superficie oceánica.

## Arquitectura de archivos

```
src/ocean/
├── gerstner.js           — Ondas Gerstner (shader vertex/fragment)
├── fft.js                — FFT 2D CPU (Cooley-Tukey radix-2)
├── spectrum.js           — JONSWAP spectrum + angular spread + height field
├── spectral-ocean.js     — Malla Three.js animada con alturas FFT
└── index.js              — Re-exporta todos los submódulos
```

## 1. FFT 2D en CPU (`fft.js`)

Implementación Cooley-Tukey radix-2 butterfly, in-place. Datos complejos como `Float32Array` entrelazado `[r0, i0, r1, i1, ...]`.

### Funciones exportadas

- `fft2d(data, N, inverse=false)` — FFT 2D in-place (filas + columnas)
- `fftShift(data, N)` — Desplaza DC al centro de la imagen
- `ifftShift(data, N)` — Invierte fftShift (auto-inverso: aplica dos veces = identidad)

### Performance

- 128×128 FFT inversa: ~19 ms/frame en JavaScript moderno
- Viable para animación a 50+ FPS con regeneración cada ~100ms

## 2. Espectro JONSWAP (`spectrum.js`)

### Fórmula completa

```
S(f) = α · Hs² · fp⁴ · f⁻⁵ · exp(-1.25·(f/fp)⁻⁴) · γ^exp(-(f-fp)²/(2·σ²·fp²))

α = 0.076 · (g·Tp / 2π)⁻²
σ = 0.07 si f ≤ fp, 0.09 si f > fp
fp = 1 / Tp
```

### Distribución direccional

`angularSpread(freq, meanDir, spread)` — cos² con dispersión gaussiana. El spread efectivo aumenta con la frecuencia.

### Generación de campo de alturas

```javascript
generateHeightField({ Hs, Tp, dir, N, L, gamma, spread }) → Float32Array(N×N)
```

**Algoritmo:**
1. Crear malla de frecuencias 2D (kx, ky)
2. Calcular S(k) = S_f(f) · D(θ) para cada punto
3. Generar números aleatorios gaussianos (Box-Muller) para fase aleatoria
4. Construir campo complejo: A·exp(i·φ) donde A = √(2·S·Δk²)
5. Aplicar fftShift al espectro
6. FFT inversa 2D → campo de alturas en espacio real
7. Normalizar para que Hs = 4σ (Hs = 4 × desviación estándar de las alturas)

## 3. Malla Three.js (`spectral-ocean.js`)

### Interfaz compatible con gerstner.js

```javascript
const ocean = createSpectralOcean({
  hs: 3.2,      // Altura significativa (m)
  tp: 8.7,      // Periodo pico (s)
  dir: 245,     // Dirección media (grados)
  N: 128,       // Resolución FFT
  L: 64,        // Tamaño del dominio (m)
  windSpeed: 17.5,
  windDir: 240,
});
scene.add(ocean.mesh);
ocean.update(time);           // Animación
ocean.update(time, newParams); // Actualizar parámetros
```

### Actualización de vértices

- Cada frame: regenera campo de alturas cada ~100ms
- Interpolación lineal entre frames consecutivos
- Normals calculadas por diferencia finita
- **Smooth clip con `tanh(h/3)*3`** para evitar picos extremos (-18m → ~±3m)

## 4. Toggle Gerstner ↔ Espectral

### En main.js

```javascript
// Estado
const state = { oceanMode: 'gerstner' }; // 'gerstner' | 'spectral'

// Crear océano según modo
function createOcean(mode) {
  if (mode === 'spectral') {
    spectralOcean = createSpectralOcean({ hs, tp, dir, N: 128, L: 64, ... });
    scene.add(spectralOcean.mesh);
  } else {
    ocean = createGerstnerOcean(params);
    scene.add(ocean.mesh);
  }
}

// Toggle en UI
document.getElementById('ocean-mode-toggle').addEventListener('click', () => {
  state.oceanMode = state.oceanMode === 'gerstner' ? 'spectral' : 'gerstner';
  createOcean(state.oceanMode);
});
```

## Validación numérica

| Métrica | Valor |
|---|---|
| Pico del espectro | f = 0.115 Hz (fp = 1/8.7) |
| Hs calculado (4σ) | 3.200 m (0% error) |
| FFT 128×128 | 19.2 ms/frame |

## Pitfalls

- **`fftShift` vs `ifftShift`:** `fftShift` desplaza DC al centro. `ifftShift` es auto-inverso (aplicarlo dos veces = identidad). No confundir.
- **Hs = 4σ:** La altura significativa es 4 veces la desviación estándar del campo de alturas. Si el campo no se normaliza, Hs calculado será incorrecto.
- **Valores extremos:** Los campos espectrales tienen colas pesadas. Usar `tanh(h/3)*3` para suavizar picos extremos en la malla.
- **`type: "module"` en package.json:** Necesario para que Node.js/Esm puedan importar los módulos. Sin esto, warnings de parsing.
- **No usar WebGPU compute shaders aún:** La FFT en CPU para 128×128 es ~19ms/frame, totalmente viable. WebGPU compute shaders sería complejidad innecesaria por ahora.
- **Regeneración periódica:** No regenerar cada frame (demasiado costoso). Regenerar cada ~100ms + interpolar entre frames.
