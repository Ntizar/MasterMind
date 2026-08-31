---
name: numba-jit-acceleration
version: "1.0.0"
description: "Use al acelerar código numérico Python con Numba JIT."
tags: [python, jit, compiler, numpy, performance, cuda, parallel, llvm]
---

# Numba — Aceleración JIT de código numérico Python

## Resumen

Numba (11.1k⭐, BSD-2, mantenido por Anaconda) es un compilador Just-In-Time que traduce un subconjunto de Python numérico (con NumPy) a máquina nativa vía LLVM. Acelera bucles y cálculo numérico 10-1000x sin salir de Python ni escribir C.

**Cuándo usarlo:** simulaciones Monte Carlo, física/cálculos por píxel, procesamiento de nubes de puntos (LiDAR), sombras solares, estadística sobre arrays grandes — todo lo CPU-bound en los proyectos de datos de David.

## Instalación

```bash
pip install numba
# Versiones de numba están casadas con versiones de Python y NumPy:
# comprobar tabla de compatibilidad si hay ImportError tras actualizar numpy
```

## Patrones principales

### 1. Compilar una función (`@njit`)

```python
from numba import njit
import numpy as np

@njit(fastmath=True)          # fastmath: reordena ops flotantes (más rápido, menos estricto)
def shadow_loop(sun_az, sun_el, grid):
    n = grid.shape[0]
    out = np.zeros(n)
    for i in range(n):
        out[i] = grid[i] * np.sin(sun_el) / np.tan(np.radians(sun_az + i))
    return out
```

- `@njit` = `@jit(nopython=True)`: si la función usa algo no soportado, **falla en tiempo de compilación** en vez de degradar a modo object lento. Siempre njit, nunca jit pelado.
- Primera llamada compila (~0.1-1s). Para producción: `cache=True`.

### 2. Paralelizar bucles (`parallel=True` + `prange`)

```python
from numba import prange

@njit(parallel=True)
def pairwise_distances(X, Y):
    n, m = X.shape[0], Y.shape[0]
    D = np.empty((n, m))
    for i in prange(n):                    # prange, NO range
        for j in range(m):
            D[i, j] = np.sqrt(((X[i] - Y[j]) ** 2).sum())
    return D
```

- Usa `prange` para el bucle exterior independiente. `NUMBA_NUM_THREADS` limita hilos.
- Reducciones (sumas, máx) soportadas; escrituras con índice derivado del bucle (`out[i] = ...`) soportadas; escrituras aleatorias = race condition.

### 3. UFuncs personalizados (`@vectorize` / `@guvectorize`)

```python
from numba import vectorize, int64

@vectorize([int64(int64, int64)])
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

gcd(np.array([12, 18]), np.array([8, 24]))   # funciona con broadcasting como ufunc NumPy
```

### 4. GPU CUDA

```python
from numba import cuda

@cuda.jit
def add_kernel(a, b, out):
    i = cuda.grid(1)
    if i < a.size:
        out[i] = a[i] + b[i]

d_a = cuda.to_device(a); d_out = cuda.device_array_like(a)
add_kernel[blocks, threads_per_block](d_a, d_b, d_out)
```

- Requiere NVIDIA GPU + driver CUDA. `@cuda.jit` no compila si hay objeto no soportado: mismo principio nopython.
- Alternativa más simple sin escribir kernels: `@jit(target_backend='cuda')` para bucles paralelizables.

## Pitfalls

- **No soporta casi nada del ecosistema:** nada de pandas, dicts heterogéneos, funciones lambda dentro, atributos de objetos arbitrarios. Solo NumPy, scalars, tuplas/listas homogéneas, arrays tipados.
- **`np.linalg` limitado**: `np.dot` sí; `svd`/`lstsq` solo en versiones recientes y con restricciones.
- **Compilación por signatura**: cada combinación de tipos de argumentos compila una variante. Pasar arrays no-contiguos (`A.T`) cambia la signatura y recompila → usar `np.ascontiguousarray`.
- **fastmath=True rompe IEEE**: `0*inf` y comparaciones con NaN pueden cambiar de resultado.
- **NumPy 2.x**: numba antiguos (<0.59) reventaban con numpy≥2. Actualizar numba si se actualiza numpy.
- **Medir siempre**: `time.perf_counter()` sobre 2ª llamada (la primera paga la compilación), o warmup antes de cronometrar.

## Verificación

```bash
python -c "import numba, numpy as np; from numba import njit; f = njit(lambda x: x.sum()); print('OK', f(np.arange(1000)), numba.__version__)"
```

## Cuándo NO usar Numba

- Código I/O-bound o con pandas en el hot path → vectorizar primero con NumPy/pandas.
- Necesitas depuración interactiva → separar el kernel numérico en su propia función `@njit`.
- Cálculo con tipos arbitrarios/objetos → Cython o Python puro.

## Referencia

- Repo: https://github.com/numba/numba
- Docs: https://numba.readthedocs.io/en/stable/
- Examples: https://github.com/numba/numba-examples (notebooks en Binder)
