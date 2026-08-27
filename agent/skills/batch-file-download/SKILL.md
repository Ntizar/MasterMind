---
name: batch-file-download
version: "1.0.0"
description: "Patrón para descargar masivamente archivos (PDFs, imágenes, etc.) de sitios web con rate limiting, retries, y verificación de integridad. Diseñado para 100+ archivos con delays anti-429."
tags: [batch, download, pdf, rate-limiting, resilience, background]
---

# Batch File Download — Patrón de descarga masiva resiliente

## Resumen

Patrón genérico para descargar cientos de archivos (PDFs, imágenes, etc.) de sitios web con rate limiting agresivo, retries con backoff, y verificación de integridad. Optimizado para Drupal/WordPress y sitios gubernamentales.

## Cuándo usarlo

- 100+ archivos a descargar de un sitio con rate limiting
- Sitios que devuelven 429 tras ~50 requests
- Descargas que tardan más de 5 minutos (no apto para cron con timeout corto)
- Necesidad de verificar integridad (archivos corruptos, HTML en vez de PDF)

## Arquitectura

### Conexión nueva por archivo (CRÍTICO)

```python
def descargar_archivo(url, dest_path):
    """Conexión nueva cada vez — sin session keep-alive."""
    for intento in range(8):
        try:
            # requests.get() directo — sin Session()
            resp = requests.get(url, timeout=120, allow_redirects=True)
            if resp.status_code == 200 and resp.content[:5] == b"%PDF-":
                return True
            elif resp.status_code == 429:
                delay = 30 * (intento + 1)  # 30, 60, 90...
                time.sleep(delay)
            else:
                return False  # error no reintentable
        except requests.exceptions.ConnectionError:
            time.sleep(10 * (intento + 1))
        except requests.exceptions.Timeout:
            time.sleep(15 * (intento + 1))
    return False
```

**Por qué NO usar Session():** Las conexiones keep-alive pueden romperse tras tiempos largos (segundos de inactividad, cambios de ruta, etc.). Nueva conexión = menos errores silenciosos.

### Delays y batches

```python
# Delay entre descargas (ajustar según el sitio)
DELAY = 1.0  # segundos

# Para sitios muy agresivos con rate limiting:
DELAY = 2.0

# Para sitios permisivos:
DELAY = 0.3
```

### Verificación de integridad

```python
# PDFs: verificar magic bytes
if resp.content[:5] == b"%PDF-":
    # archivo válido
else:
    # HTML en vez de PDF, o archivo corrupto

# Archivos genéricos: verificar tamaño mínimo
if path.exists() and path.stat().st_size > 2000:
    # ya existe y no es un error page
```

### Estructura del script

```python
#!/usr/bin/env python3
"""
batch-download.py — Descarga masiva de archivos
Uso: python3 batch-download.py --delay 1 [--dry-run]
"""
import json, sys, time, requests
from pathlib import Path

BASE = Path("/ruta/al/proyecto")
DELAY = 1.0
DRY_RUN = False

# Parse args
for arg in sys.argv[1:]:
    if arg == "--dry-run": DRY_RUN = True
    elif arg.startswith("--delay"):
        DELAY = float(arg.split("=")[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1])

# Cargar índices (JSON pre-cacheados)
indices = cargar_indices()

# Contar pendientes
total_pendientes = contar_pendientes(indices)

# Descargar
stats = {"exitosos": 0, "fallidos": 0, "saltados": 0}
for pais, reports in indices.items():
    for r in reports:
        fname = f"{pais}_{r['year']}_{r['title']}"
        path = BASE / "downloads" / pais / fname
        
        if path.exists() and path.stat().st_size > 2000:
            stats["saltados"] += 1
            continue
        
        if descargar_archivo(r["pdf_url"], path):
            stats["exitosos"] += 1
        else:
            stats["fallidos"] += 1
        
        time.sleep(DELAY)

# Resumen
print(f"✅ {stats['exitosos']} ❌ {stats['fallidos']} ⏭️ {stats['saltados']}")
```

## Pitfalls

- **NO usar `tee` en background:** `python3 script.py | tee log.txt` en background puede truncar la salida. Ejecutar SIN pipe.
- **Timeout de cron:** No ejecutar en cron con timeout < 300s para tareas que tardan horas. Usar `nohup`, `&`, o background process.
- **Session keep-alive rompe conexiones:** Tras tiempos largos, las conexiones de `requests.Session()` pueden quedar huérfanas. Usar `requests.get()` directo.
- **429 con backoff exponencial:** No usar delay fijo — progresivo (30s, 60s, 90s...) es más efectivo.
- **Verificar magic bytes:** HTTP 200 no significa archivo válido. Verificar `content[:5]` para PDFs.
- **Nombres de archivo inconsistentes:** Verificar que el formato de nombre generado coincide con los existentes en disco. Un bug de naming puede hacer que el script re-descargue todo.

## Pitfalls de naming

Los nombres de archivo generados pueden NO coincidir con los del índice:
- Minúsculas vs mayúsculas (`de-10413` vs `DE-10413`)
- Doble extensión (`.pdf.` al final)
- Caracteres especiales no escapados
- Espacios en títulos del índice

**Verificar siempre:** listar archivos en disco y comparar con el índice. Si hay discrepancia, los archivos pueden existir con nombres ligeramente distintos.

## Ejemplo: ERAVisor

Script completo en `/root/workspace/ERAVisor/scripts/descargar_todos.py`

Estado a 2026-07-07: 1380 informes, ~1300 descargados, ~80 pendientes (DE/UK con nombres inconsistentes), 3GB en disco.

## Alternativas

- **`wget -c -i urls.txt`:** Para listas simples de URLs, sin verificación de integridad
- **`curl -O`:** Similar a wget, pero sin reintentos automáticos
- **`axel`/`aria2c`:** Descarga multi-hilo, pero no maneja 429 bien
