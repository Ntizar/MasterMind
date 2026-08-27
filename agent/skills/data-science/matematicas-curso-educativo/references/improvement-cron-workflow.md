# Workflow: encontrar el primer tema pending que existe

Cuando el cron de mejora continua selecciona un tema de `progress.json`, las keys NO son nombres de archivo reales.
El workflow correcto es:

## Paso a paso

1. **Leer progress.json** → filtrar temas con `status: "pending"`
2. **Ordenar por priority** (1 primero, luego 2, luego 3)
3. **Listar directorio** con `os.listdir()` para obtener los archivos reales
4. **Verificar existencia** de cada tema pending en orden de prioridad
5. **Seleccionar el primero** que tenga archivo real

## Código Python de referencia

```python
import os, json

with open("progress.json") as f:
    prog = json.load(f)

existing = set(os.listdir("."))

pending = []
for fname, info in prog["topics"].items():
    if info["status"] == "pending":
        exists = fname in existing
        pending.append((fname, info["priority"], info["level"], exists))

pending.sort(key=lambda x: x[1])  # ordenar por priority

# Primer pending que existe
first = [(f,p,l,e) for f,p,l,e in pending if e][0]
print(f"Seleccionado: {f} (P{p}, {l})")
```

## Regla

Nunca asumir que la key de progress.json = nombre de archivo.
Los nombres reales pueden ser:
- `s01-5-restar-hasta-10.html` (descriptivo)
- `s01-1primaria.html` (corto)
- `eso1-1-numeros-enteros.html` (ESO)
- `s09-1-bachiller-limites.html` (Bachiller)

## Historial

- **2026-06-09:** Primera ejecución de este workflow. Los 4 primeros pending (s01-7 a s01-10) no existían como keys. El primero existente fue `s02-1primaria.html`.
- **2026-06-09 (run 13):** `s01-9primaria.html` era una key que NO existe en el filesystem. El archivo real es `s01-9-medidas-longitud.html`. **Solución:** cuando una key no existe, saltar a la siguiente key pending. Además, corregir progress.json para que la key apunte al nombre real.
