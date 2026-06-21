---
name: cron-batch-orchestration
version: "1.0.0"
description: "Crear y orquestar un batch de crons one-shot secuenciales que mejoran un repositorio iterativamente — cada cron clona, modifica, y push, el siguiente coge la versión mejorada."
tags: [cron, batch, orchestration, fork, iterative-improvement, automation]
---

# Cron Batch Orchestration — Mejora iterativa de repos via crons

Crear un batch de crons one-shot secuenciales que mejoran un repositorio paso a paso. Cada cron es autocontenido, clona el repo, hace su trabajo, y push. El siguiente cron coge la versión mejorada.

## Cuándo usar

- Tienes un repositorio base y quieres evolucionarlo rápidamente (24h) con mejoras secuenciales
- Cada mejora depende de la anterior (ej: primero GTFS real, luego routing con ese GTFS)
- Quieres parallelizar trabajo en sesiones independientes (cada cron es una sesión aislada)
- El usuario quiere ver progreso incremental sin intervención manual

## Flujo estándar (5 pasos)

### Paso 1: Analizar el repo base

```bash
# Explorar estructura
cd /root/workspace/<repo-base>
find . -type f -not -path '*/.git/*' | head -50
# Leer archivos clave para entender dependencias
```

### Paso 2: Crear el fork del repo

```bash
# Clonar el repo base a /tmp para referencia
git clone https://TOKEN@github.com/<user>/<repo-base>.git /tmp/<repo-base>-source

# Crear nuevo repo en GitHub via API
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"<repo-new>","description":"<desc>","private":true}'

# Clonar el nuevo repo vacío
git clone https://TOKEN@github.com/<user>/<repo-new>.git /tmp/<repo-new>

# Copiar todo el contenido (sin .git)
rsync -a /tmp/<repo-base>-source/ /tmp/<repo-new>/
# O manualmente:
cd /tmp/<repo-new>
git init && git remote add origin https://TOKEN@github.com/<user>/<repo-new>.git
git add . && git commit -m "Initial copy" && git push -u origin main
```

**IMPORTANTE:** El repo base NUNCA se modifica. Todo el trabajo va al fork.

### Paso 3: Planificar los crons

Diseñar una secuencia lógica donde cada cron depende del anterior:

```
Cron 1: Configuración base (API keys, config)
Cron 2: Datos fuente A (GTFS Madrid)
Cron 3: Datos fuente B (GTFS Barcelona)
Cron 4: Integración datos (multi-ciudad)
Cron 5: Motor de lógica (routing con GTFS)
Cron 6-N: Mejoras incrementales...
Cron N: Auditoría final
```

**Reglas de planificación:**
- Cada cron debe ser **autocontenido** (no depende de chat history)
- Cada cron debe tener un **prompt completo** con contexto del repo, archivos a modificar, y objetivos
- Horarios escalonados (cada hora) para que el siguiente coge la versión mejorada
- El último cron SIEMPRE es auditoría + corrección

### Paso 4: Crear los crons

Usar `cronjob(action='create')` para cada cron:

```python
# Cada cron tiene:
# - name: timeineco2-NN-descripcion
# - schedule: 0 HH * * * (horario escalonado)
# - repeat: 1 (one-shot)
# - deliver: origin
# - workdir: /root/workspace
# - prompt: instrucciones completas y autocontenidas
```

**El prompt de cada cron debe incluir:**
1. Qué repo clonar y dónde trabajar
2. Objetivo específico
3. Pasos detallados
4. Qué archivos crear/modificar
5. Qué datos buscar (URLs, fuentes)
6. Fallback si no se puede hacer lo principal
7. Recordatorio de no tocar el repo original

### Paso 5: Verificar y documentar

```bash
# Verificar que todos los crons están creados
cronjob(action='list')

# Crear plan de crons en el repo
write_file("CRONS-PLAN.md", plan_content)

# Commit al fork
git add CRONS-PLAN.md && git commit -m "docs: plan de crons" && git push
```

## Estructura de los crons

```
timeineco2-01-ors-api-config          [18:00] Configurar API ORS
timeineco2-02-nap-gtfs-madrid         [19:00] GTFS Madrid real
timeineco2-03-nap-gtfs-barcelona      [20:00] GTFS Barcelona real
timeineco2-04-nap-gtfs-multi-ciudad   [21:00] 5 ciudades más
timeineco2-05-routing-transit-gtfs    [22:00] Motor routing transit
timeineco2-06-datos-ine-poblacion     [23:00] Datos INE población
timeineco2-07-datos-economicos-ine    [00:00] Renta/salario/desempleo
timeineco2-08-precios-vivienda-mejora [01:00] Precios m² mejorados
timeineco2-09-motor-isocronas-mejora  [02:00] Simulación orgánica
timeineco2-10-geocodificacion-mejora  [03:00] Nominatim mejorada
timeineco2-11-dashboard-interactivo   [04:00] Dashboard web
timeineco2-12-informe-docx-mejora     [05:00] DOCX profesional
timeineco2-13-export-shp-mejora       [06:00] SHP + GeoJSON + CSV
timeineco2-14-ui-ux-mejora            [07:00] UI/UX responsive
timeineco2-15-testing-suite           [08:00] Tests unitarios
timeineco2-16-auditoria-final         [09:00] Auditoría + correcciones
```

## Pitfalls

- **Token truncado:** El token de GitHub puede aparecer truncado en logs. Leer siempre desde `/hermes-home/.env` la variable `GITHUB_TOKEN` completa.
- **gh CLI no instalado:** No usar `gh` para crear repos. Usar la GitHub API via `curl` o `urllib.request` en Python.
- **Directorio ya existe:** Si el destino del clone ya existe, borrarlo primero con `shutil.rmtree()` antes de clonar.
- **Crons comparten horario:** Verificar que ningún par de crons comparte el mismo horario (`schedule`). Si es así, escalarlos.
- **Prompt demasiado largo:** Los prompts de cron tienen límite de longitud. Si un cron es muy complejo, dividirlo en 2+ crons.
- **Dependencias circulares:** Asegurar que la secuencia de crons es lineal (A→B→C), no circular (A→B→A).
- **Cron de auditoría último:** Siempre dejar el cron de auditoría para el final, después de todas las mejoras.
- **No clonar en workspace activo:** Si el workspace ya tiene el repo, clonar a `/tmp/` primero, copiar, y luego crear el repo vacío en el destino.

## Variables de entorno

- `GITHUB_TOKEN`: Leer desde `/hermes-home/.env`, variable `GITHUB_TOKEN` (40 chars, formato `ghp_...`)
