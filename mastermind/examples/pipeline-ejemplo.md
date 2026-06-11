# 🏭 Ejemplo: Configurar Pipeline para Proyecto "Mi Dashboard Web"

Este ejemplo muestra cómo configurar el sistema completo para un proyecto de dashboard web.

## Paso 1: Crear el Proyecto

```bash
# Ejecutar script de inicialización
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh crear mi-dashboard web "Dashboard interactivo con gráficos"
```

**Resultado:**
```
✅ Proyecto 'mi-dashboard' creado en /root/workspace/proyectos/mi-dashboard

Estructura:
mi-dashboard/
├── pipeline-status.json
├── backlog.json
├── README.md
├── src/
├── tests/
├── docs/
└── scripts/
```

## Paso 2: Agregar Tareas al Backlog

### Tarea 1: Estructura HTML base
```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh agregar mi-dashboard '{
  "id": "task-001",
  "tipo": "feature",
  "prioridad": "alta",
  "descripcion": "Crear estructura HTML con layout responsive",
  "criterios_aceptacion": [
    "HTML válido con semantic tags",
    "Layout flexbox/grid responsive",
    "Header, main, footer estructurados"
  ],
  "dependencias": [],
  "archivos_afectados": ["src/index.html"],
  "estado": "pending",
  "intentos": 0
}'
```

### Tarea 2: CSS base con variables
```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh agregar mi-dashboard '{
  "id": "task-002",
  "tipo": "feature",
  "prioridad": "alta",
  "descripcion": "Crear CSS base con variables y reset",
  "criterios_aceptacion": [
    "Variables CSS para colores/tipografía",
    "Reset CSS moderno",
    "Responsive breakpoints definidos"
  ],
  "dependencias": ["task-001"],
  "archivos_afectados": ["src/styles/main.css"],
  "estado": "pending",
  "intentos": 0
}'
```

### Tarea 3: Componente de gráfico
```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh agregar mi-dashboard '{
  "id": "task-003",
  "tipo": "feature",
  "prioridad": "media",
  "descripcion": "Implementar componente de gráfico con Chart.js",
  "criterios_aceptacion": [
    "Gráfico de línea funcional",
    "Datos de ejemplo cargados",
    "Responsive en mobile"
  ],
  "dependencias": ["task-002"],
  "archivos_afectados": ["src/js/charts.js", "src/index.html"],
  "estado": "pending",
  "intentos": 0
}'
```

## Paso 3: Ver Estado del Backlog

```bash
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh estado mi-dashboard
```

**Resultado:**
```
═══════════════════════════════════════════════════════════
📊 Estado del Pipeline: mi-dashboard
═══════════════════════════════════════════════════════════

{
  "proyecto": "mi-dashboard",
  "version": "1.0.0",
  "tipo": "web",
  "estado": "planning",
  "metricas": {
    "tareas_totales": 3,
    "tareas_completadas": 0,
    "tareas_pendientes": 3
  }
}

═══════════════════════════════════════════════════════════
📋 Backlog
═══════════════════════════════════════════════════════════

task-001 [pending] Crear estructura HTML con layout responsive
task-002 [pending] Crear CSS base con variables y reset
task-003 [pending] Implementar componente de gráfico con Chart.js
```

## Paso 4: Configurar Cron Maestro

```bash
# Crear cron job que ejecuta cada 2 horas
hermes cron create \
  --name "mi-dashboard-pipeline" \
  --schedule "0 */2 * * *" \
  --prompt "Eres el orquestador del pipeline del proyecto mi-dashboard.
  
INSTRUCCIONES:
1. Lee /root/workspace/proyectos/mi-dashboard/pipeline-status.json
2. Lee /root/workspace/proyectos/mi-dashboard/backlog.json
3. Busca la siguiente tarea con estado 'pending' y sin dependencias bloqueadas
4. Si hay tarea disponible:
   - Actualiza su estado a 'in-progress' en backlog.json
   - Ejecuta la tarea (crea/modifica archivos según sea necesario)
   - Si éxito: marca como 'done' y actualiza pipeline-status.json
   - Si falla: incrementa intentos, si >=3 marca como 'failed'
5. Actualiza métricas en pipeline-status.json
6. Entrega resumen del progreso

REGLAS:
- Cada tarea debe ser ATÓMICA (máx 1 archivo principal)
- Respeta las dependencias entre tareas
- Si el proyecto está completo, marca estado: 'done'
- Siempre entrega un resumen al final" \
  --deliver "telegram"
```

## Paso 5: Ejecutar Iteración Manual (Testing)

```bash
# Forzar una ejecución inmediata
bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh iterar mi-dashboard
```

**Resultado:**
```
ℹ️  Ejecutando iteración del pipeline 'mi-dashboard'
ℹ️  Tarea seleccionada: task-001
✅ Iteración iniciada. Tarea task-001 en progreso.
```

## Paso 6: Ejecutar el Cron Manualmente

```bash
# Ejecutar el cron una vez para probar
hermes cron run mi-dashboard-pipeline
```

**El agente ejecutará:**
1. Lee los archivos de estado
2. Encuentra task-001 como siguiente tarea
3. Crea el HTML base del dashboard
4. Actualiza el backlog: task-001 → done
5. Actualiza pipeline-status.json
6. Entrega resumen por Telegram

## Resultado Esperado

Después de varias ejecuciones del cron:

```json
// pipeline-status.json
{
  "proyecto": "mi-dashboard",
  "estado": "in-progress",
  "metricas": {
    "tareas_totales": 3,
    "tareas_completadas": 2,
    "tareas_en_curso": 1,
    "tareas_pendientes": 0
  }
}
```

```json
// backlog.json
{
  "tareas": [
    {"id": "task-001", "estado": "done"},
    {"id": "task-002", "estado": "done"},
    {"id": "task-003", "estado": "in-progress"}
  ]
}
```

## Comandos Útiles

### Ver progreso en tiempo real
```bash
watch -n 5 'bash /root/workspace/Mastermind/mastermind/scripts/pipeline-init.sh estado mi-dashboard'
```

### Pausar pipeline
```bash
hermes cron pause mi-dashboard-pipeline
```

### Reanudar pipeline
```bash
hermes cron resume mi-dashboard-pipeline
```

### Eliminar pipeline
```bash
hermes cron remove mi-dashboard-pipeline
rm -rf /root/workspace/proyectos/mi-dashboard
```

---

## Tips

1. **Tareas atómicas**: Cada tarea debe poder completarse en una sola ejecución del cron (~15 min max)

2. **Dependencias claras**: Define bien qué tareas dependen de otras

3. **Criterios de aceptación**: Especifica qué significa "hecho" para cada tarea

4. **Monitoreo**: Revisa el estado manualmente las primeras veces para ajustar la configuración

5. **Ajuste de frecuencia**: Si el proyecto avanza muy lento, aumenta la frecuencia del cron

---

**Autor:** David Antizar
**Versión:** 1.0.0
