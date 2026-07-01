# Ejemplo: Pipeline para Proyecto "Mi Dashboard Web"

## Paso 1: Crear el Proyecto

```bash
bash pipeline-init.sh crear mi-dashboard web "Dashboard interactivo con gráficos"
```

Resultado: estructura en `/root/workspace/proyectos/mi-dashboard/`

## Paso 2: Agregar Tareas

```bash
# Tarea 1: HTML base
bash pipeline-init.sh agregar mi-dashboard '{
  "id": "task-001", "tipo": "feature", "prioridad": "alta",
  "descripcion": "Crear estructura HTML con layout responsive",
  "criterios_aceptacion": ["HTML válido semántico", "Layout flexbox/grid", "Header/main/footer"],
  "dependencias": [], "archivos_afectados": ["src/index.html"],
  "estado": "pending", "intentos": 0
}'

# Tarea 2: CSS base
bash pipeline-init.sh agregar mi-dashboard '{
  "id": "task-002", "tipo": "feature", "prioridad": "alta",
  "descripcion": "Crear CSS base con variables y reset",
  "criterios_aceptacion": ["Variables CSS colores/tipografía", "Reset moderno", "Responsive breakpoints"],
  "dependencias": ["task-001"], "archivos_afectados": ["src/styles/main.css"],
  "estado": "pending", "intentos": 0
}'

# Tarea 3: Gráfico
bash pipeline-init.sh agregar mi-dashboard '{
  "id": "task-003", "tipo": "feature", "prioridad": "media",
  "descripcion": "Implementar gráfico con Chart.js",
  "criterios_aceptacion": ["Gráfico de línea funcional", "Datos ejemplo", "Responsive mobile"],
  "dependencias": ["task-002"], "archivos_afectados": ["src/js/charts.js", "src/index.html"],
  "estado": "pending", "intentos": 0
}'
```

## Paso 3: Ver Estado

```bash
bash pipeline-init.sh estado mi-dashboard
```

## Paso 4: Generar Cron

```bash
bash pipeline-generar-cron.sh mi-dashboard telegram "0 */2 * * *"
```

Copia el comando impreso y pégalo en Hermes.

## Paso 5: Ejecutar Iteración Manual (Testing)

```bash
bash pipeline-init.sh iterar mi-dashboard
```

## Resultado Esperado

Tras varias ejecuciones del cron:
- task-001 → done (HTML creado)
- task-002 → done (CSS creado)
- task-003 → in-progress (gráfico en desarrollo)
- Progreso: 66%
