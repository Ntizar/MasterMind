---
name: micro-crons-pipeline
version: "1.0.0"
description: "Sistema de producción iterativa con micro-crons para proyectos grandes"
category: mastermind
---

# 🏭 Micro-Crons Pipeline - Línea de Montaje de Proyectos

## Visión General

Un sistema que divide proyectos grandes en tareas atómicas y las ejecuta automáticamente mediante una cadena de cron jobs, como una línea de montaje. Cada iteración mejora el proyecto hasta darlo por terminado.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CRON MAESTRO (cada 2h)                   │
│  • Lee estado del proyecto (pipeline-status.json)           │
│  • Determina siguiente tarea del backlog                    │
│  • Delega a cron de ejecución o ejecuta directamente        │
│  • Actualiza estado tras completar                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                CRON DE EJECUCIÓN (on-demand)                │
│  • Carga contexto del proyecto + tarea actual               │
│  • Ejecuta la tarea (código, docs, tests, etc.)             │
│  • Entrega resultado al maestro para validación             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 CRON DE VALIDACIÓN (after-execution)        │
│  • Revisa calidad del output                                │
│  • Aprueba o solicita correcciones                          │
│  • Actualiza métricas del proyecto                          │
└─────────────────────────────────────────────────────────────┘
```

## Flujo de Uso

### Paso 1: Definir el Proyecto

El usuario describe el proyecto. Mastermind crea la estructura:

```bash
# Estructura de un proyecto
/proyectos/{nombre-proyecto}/
├── pipeline-status.json    # Estado actual del pipeline
├── backlog.json           # Lista de tareas pendientes
├── README.md              # Descripción del proyecto
├── src/                   # Código fuente (según tipo)
└── ...                    # Resto de archivos del proyecto
```

### Paso 2: Pipeline Status Schema

```json
{
  "proyecto": "nombre-del-proyecto",
  "version": "1.0.0",
  "estado": "in-progress",  // planning | in-progress | review | done
  "fase_actual": "desarrollo",
  "tarea_actual": {
    "id": "task-001",
    "tipo": "feature",     // feature | fix | refactor | docs | test
    "descripcion": "Implementar sistema de autenticación",
    "estado": "in-progress",
    "intentos": 0,
    "max_intentos": 3
  },
  "metricas": {
    "tareas_totales": 15,
    "tareas_completadas": 3,
    "tareas_en_curso": 1,
    "tareas_pendientes": 11,
    "ultima_ejecucion": "2026-06-11T14:30:00Z",
    "proxima_ejecucion": "2026-06-11T16:30:00Z"
  },
  "historial": []
}
```

### Paso 3: Backlog Schema

```json
{
  "tareas": [
    {
      "id": "task-001",
      "tipo": "feature",
      "prioridad": "alta",
      "descripcion": "Sistema de autenticación básico",
      "criterios_aceptacion": [
        "Login/logout funcional",
        "Sesiones persistentes",
        "Roles básicos (admin/user)"
      ],
      "dependencias": [],
      "archivos_afectados": ["src/auth/", "src/middleware/"],
      "estado": "pending",  // pending | in-progress | review | done | blocked
      "intentos": 0
    },
    {
      "id": "task-002",
      "tipo": "feature",
      "prioridad": "media",
      "descripcion": "Dashboard principal con métricas",
      "criterios_aceptacion": [...],
      "dependencias": ["task-001"],
      "archivos_afectados": ["src/views/dashboard/"],
      "estado": "blocked"
    }
  ]
}
```

## Cron Jobs del Sistema

### 1. Cron Maestro (el orquestador)

**Frecuencia recomendada:** Cada 2 horas o diario según complejidad

```javascript
// Prompt del Cron Maestro
const promptMaestro = `
Eres el orquestador del pipeline de producción del proyecto [NOMBRE].

INSTRUCCIONES:
1. Lee /proyectos/[NOMBRE]/pipeline-status.json
2. Lee /proyectos/[NOMBRE]/backlog.json
3. Determina la siguiente tarea a ejecutar:
   - Priorizar por prioridad (alta > media > baja)
   - Respetar dependencias
   - No repetir tareas fallidas 3+ veces
4. Si hay tarea disponible:
   - Actualiza pipeline-status.json (estado: in-progress)
   - Ejecuta la tarea usando las herramientas apropiadas
   - Si éxito: actualiza a "done" y mueve al backlog
   - Si falla: incrementa intentos, si >=3 marca como "failed"
5. Actualiza métricas
6. Entrega resumen de progreso

REGLAS:
- Cada tarea debe ser ATÓMICA (máx 1 archivo o módulo)
- Si una tarea es compleja, divídela en subtareas
- Nunca dejes el proyecto en estado inconsistente
- Si el proyecto está completo, marca estado: "done"
`;
```

### 2. Cron de Validación (opcional, para calidad)

```javascript
const promptValidacion = `
Revisa el último cambio en el proyecto [NOMBRE]:

1. Lee pipeline-status.json para ver qué se hizo
2. Ejecuta validaciones:
   - ¿El código compila/sin errores?
   - ¿Los tests pasan?
   - ¿Cumple los criterios de aceptación?
   - ¿No rompe funcionalidad existente?
3. Si todo OK: aprueba y avanza
4. Si hay issues: crea tarea de corrección en backlog
5. Actualiza métricas de calidad
`;
```

## Templates por Tipo de Proyecto

### Proyecto Web (HTML/JS/CSS)

```json
{
  "fases": [
    {
      "nombre": "wireframe",
      "tareas": ["estructura-html", "css-basico", "layout-responsive"]
    },
    {
      "nombre": "desarrollo",
      "tareas": ["componentes-core", "interactividad", "estado-global"]
    },
    {
      "nombre": "optimizacion",
      "tareas": ["accesibilidad", "performance", "seo-basico"]
    }
  ]
}
```

### Proyecto Node.js/Backend

```json
{
  "fases": [
    {
      "nombre": "fundamentos",
      "tareas": ["setup-proyecto", "config-db", "modelos-base"]
    },
    {
      "nombre": "api",
      "tareas": ["endpoints-core", "validacion", "autenticacion"]
    },
    {
      "nombre": "integracion",
      "tareas": ["tests-unit", "tests-integracion", "docs-api"]
    }
  ]
}
```

### Documento/Artículo

```json
{
  "fases": [
    {
      "nombre": "estructura",
      "tareas": ["outline", "secciones-principales"]
    },
    {
      "nombre": "contenido",
      "tareas": ["desarrollo-seccion-1", "desarrollo-seccion-2", "ejemplos"]
    },
    {
      "nombre": "pulido",
      "tareas": ["edicion", "formato", "revision-final"]
    }
  ]
}
```

## Comandos de Uso

### Iniciar un nuevo proyecto
```bash
# Mastermind crea la estructura y cron maestro
"Mastermind, quiero crear un proyecto [DESCRIPCION]"
→ Ejecuta: crear-proyecto.sh [nombre] [tipo]
```

### Pausar pipeline
```bash
"Mastermind, pausa el pipeline de [proyecto]"
→ Pausa cron maestro
```

### Reanudar pipeline
```bash
"Mastermind, reanuda el pipeline de [proyecto]"
→ Reactiva cron maestro
```

### Forzar ejecución manual
```bash
"Mastermind, ejecuta ahora el pipeline de [proyecto]"
→ Ejecuta cron maestro una vez
```

### Ver estado del proyecto
```bash
"Mastermind, ¿cómo va el proyecto [nombre]?"
→ Lee pipeline-status.json y entrega resumen
```

## Métricas y Reporting

El pipeline genera un reporte semanal automático:

```markdown
# 📊 Reporte Semanal - [Nombre Proyecto]

## Progreso
- Tareas completadas: 12/20 (60%)
- En progreso: 2
- Pendientes: 6

## Últimas 24h
- ✅ task-012: API de usuarios (2.3h)
- ✅ task-013: Tests de integración (1.1h)
- 🔄 task-014: Dashboard admin (en curso)

## Calidad
- Tasa de éxito: 94% (16/17)
- Reintentos promedio: 1.2

## Próximas tareas
1. task-014: Dashboard admin
2. task-015: Sistema de notificaciones
3. task-016: Exportar a PDF
```

## Pitfalls y Soluciones

### ⚠️ Problema 1: Cron job no tiene contexto entre sesiones
**Solución:** Todo el estado vive en archivos JSON. El cron SIEMPRE lee los archivos antes de actuar.

### ⚠️ Problema 2: Tarea demasiado grande para un solo cron
**Solución:** Dividir en subtareas atómicas. Máximo ~15 minutos de ejecución por tarea.

### ⚠️ Problema 3: Errores de red/API
**Solución:** Sistema de reintentos con backoff. Si falla 3 veces, marca tarea como "failed" y continúa.

### ⚠️ Problema 4: Permisos de escritura
**Solución:** Verificar que /proyectos/ existe y es escribible antes de ejecutar.

### ⚠️ Problema 5: Múltiples crons compitiendo
**Solución:** Lock file en /proyectos/[nombre]/.pipeline.lock. Solo un cron ejecuta a la vez.

## Configuración Recomendada

### Para proyectos pequeños (1-2 días)
- Frecuencia: Cada 1 hora
- Tareas: 5-10
- Sin validación separada

### Para proyectos medianos (1 semana)
- Frecuencia: Cada 2 horas
- Tareas: 10-30
- Validación después de cada feature

### Para proyectos grandes (1+ mes)
- Frecuencia: Diaria o cada 4 horas
- Tareas: 30-100+
- Validación + reporte semanal

---

**Autor:** David Antizar
**Versión:** 1.0.0
**Licencia:** MIT
