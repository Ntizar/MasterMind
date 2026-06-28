# Mapeo progress.json → nombres reales de archivo

Las keys en `progress.json` NO corresponden a nombres de archivo reales.
Siempre verificar con `os.listdir()` antes de leer archivos.

## Patrón general

Los nombres reales pueden ser:
- `s01-1-contar-0-10.html` (descriptivo, con guión bajo)
- `s01-1primaria.html` (corto, sin guión)
- `eso1-1-numeros-enteros.html` (ESO, descriptivo)
- `s09-1-bachiller-limites.html` (Bachiller, descriptivo)
- `s01-10-patrones.html` (número de 2 cifras en nombre)

## Mapeo parcial (2026-06-09)

### 1º Primaria (s01)
| progress.json key | Archivo real |
|---|---|
| s01-1primaria.html | s01-1primaria.html |
| s01-2primaria.html | s01-2primaria.html |
| s01-3primaria.html | s01-3primaria.html |
| s01-4primaria.html | s01-4primaria.html |
| s01-5primaria.html | s01-5-restar-hasta-10.html |
| s01-6primaria.html | s01-6-restar-hasta-20.html |
| s01-7primaria.html | s01-7-figuras-basicas.html |
| s01-8primaria.html | s01-8-medidas-tamano-peso.html |
| s01-9primaria.html | s01-9-medidas-longitud.html |
| s01-10primaria.html | s01-10-patrones.html |

### 2º Primaria (s02)
| progress.json key | Archivo real |
|---|---|
| s02-1primaria.html | s02-1primaria.html |
| s02-2primaria.html | s02-2primaria.html |
| s02-3primaria.html | s02-3primaria.html |
| s02-4primaria.html | s02-4primaria.html |
| s02-5primaria.html | s02-5primaria.html |
| s02-6primaria.html | s02-6primaria.html |
| s02-7primaria.html | s02-7primaria.html |

### Nota
- **Los primeros 4 temas** usan nombres descriptivos (`s01-1-contar-0-10.html`, `s01-2-contar-10-100.html`, etc.)
- **Los temas de 1º Primaria posterior** usan nombres cortos (`s01-1primaria.html`, `s01-2primaria.html`)
- **Los temas de 2º Primaria en adelante** mezclan ambos patrones
- **Algunos temas de primaria en progress.json no tienen archivo** (ej. s01-7primaria.html → s01-7-figuras-basicas.html)

## Regla

**Nunca asumir que la key de progress.json = nombre de archivo.** Siempre listar el directorio primero.

## Código de verificación

```python
import os, json
with open("progress.json") as f:
    prog = json.load(f)
existing = set(os.listdir("."))
for fname, info in prog["topics"].items():
    exists = fname in existing
    print(f"{'✅' if exists else '❌'} {fname} → {fname if exists else 'NO EXISTE (buscar real)'}")
```
