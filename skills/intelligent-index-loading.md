---
name: intelligent-index-loading
description: Patrón de índice inteligente con carga bajo demanda. El orchestrator filtra learnings por señal de relevancia y decay R(t) sin abrir archivos individuales, reduciendo el 80% del trabajo de lectura.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [índice-inteligente, carga-bajo-demanda, decay, señal-relevancia, optimización]
---

# Patrón de Índice Inteligente con Carga Bajo Demanda

## Qué es

Patrón de gestión de contexto que permite al orchestrator leer un único archivo `_index.md` con una tabla de 32+ entradas para tomar decisiones sin abrir archivos individuales. Cada fila de la tabla contiene metadatos suficientes para filtrar y priorizar qué conocimiento es relevante para la tarea actual.

### Estructura de cada fila en el índice

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `fecha` | Fecha de creación del learning | `2026-06-03` |
| `tarea` | Qué se aprendió | `Implementar export PDF con manejo de errores` |
| `tipo` | Categoría del learning | `bugfix`, `feature`, `pattern`, `decision` |
| `clusters` | Clusters asociados | `dashboard, pdf, errores` |
| `proyecto` | Proyecto al que pertenece | `medvisit` |
| `patrón` | Patrón identificado | `manejo-errores-grupal` |
| `señal_de_relevancia` | Valor 0.0–1.0 de relevancia actual | `0.7` |
| `cuándo_cargar` | Condición para abrir el archivo | `si_tiene_pdf`, `si_errores`, `siempre` |
| `decay` | Función R(t) actual del learning | `0.65`, `1.0 (permanente)` |
| `archivo` | Ruta al learning individual | `agents/learnings/2026-03-25-...md` |

### Cómo funciona el filtro

El orchestrator aplica dos filtros en secuencia sobre el índice:

```
ÍNDICE COMPLETO (32+ entradas)
        │
        ▼
┌─────────────────────┐
│ Filtro por señal    │  → Elimina filas con señal_de_relevancia < umbral
│ de relevancia       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Filtro por decay    │  → Elimina filas con R(t) < umbral
│ R(t) > umbral       │
└─────────┬───────────┘
          │
          ▼
    SUBCONJUNTO
    de 2-5 archivos
    para abrir
```

### Umbrales

| Condición | Umbral señal | Umbral decay |
|-----------|-------------|-------------|
| Normal | ≥ 0.3 | ≥ 0.3 |
| Presión de tokens | ≥ 0.5 | ≥ 0.5 |
| Excepción permanente | — | decay = 1.0 (learnings con decay permanente) |

**Regla de la excepción permanente:** Los learnings marcados con `decay = 1.0 (permanente)` **nunca** se filtran, sin importar el umbral. Esto garantiza que patrones fundamentales del sistema siempre estén disponibles.

## Cuándo usar

- **Al inicio de cada sesión:** El orchestrator lee `_index.md` para decidir qué learnings cargar.
- **Antes de delegar a un subagente:** Filtrar qué contexto es relevante para esa tarea específica.
- **Bajo presión de tokens:** Subir umbrales a 0.5 para reducir el subconjunto.
- **Al reanudar un proyecto:** Filtrar por `proyecto` y `clusters` relevantes.
- **NUNCA:** Abrir archivos individuales sin antes filtrar por el índice.

### Ejemplo de decisión

```
Tarea: "Arreglar export PDF de MedVisit"

1. Filtrar índice por clusters CONTIENE "pdf": 3 filas
2. Filtrar por señal ≥ 0.3: 3 filas (todas pasan)
3. Filtrar por decay ≥ 0.3: 2 filas (1 queda en 0.15, se descarta)
4. Resultado: abrir solo 2 archivos en lugar de revisar los 32
```

## Pasos

### Paso 1 — Leer el índice

```
1. Abrir `skills/_index.md` (o ruta equivalente)
2. Leer TODA la tabla (es un solo archivo, coste mínimo)
3. Identificar columnas relevantes para la tarea
```

### Paso 2 — Aplicar filtro por señal

```
1. Identificar clusters, tipo o proyecto de la tarea
2. Seleccionar filas donde señal_de_relevancia ≥ umbral
3. Si no hay resultados, bajar umbral a 0.3 (nivel base)
```

### Paso 3 — Aplicar filtro por decay

```
1. Sobre el subconjunto del paso 2, filtrar decay R(t) ≥ umbral
2. Excepción: si decay = 1.0 (permanente), mantener siempre
3. Si el subconjunto tiene más de 5 archivos, subir umbral a 0.5
```

### Paso 4 — Decidir qué abrir

```
1. Los archivos filtrados se abren uno por uno
2. Cada uno se carga como contexto del subagente correspondiente
3. Si el subconjunto es vacío, proceder sin contexto adicional
```

### Paso 5 — Actualizar el índice

```
1. Tras completar la tarea, el orchestrator actualiza:
   - señal_de_relevancia de los archivos usados
   - decay de los learnings consultados
   - nuevas entradas si se generó un nuevo learning
```

## Pitfalls

| Pitfall | Síntoma | Solución |
|---------|---------|----------|
| Índice desactualizado | Se abren archivos irrelevantes | Actualizar índice tras cada sesión |
| Umbral demasiado bajo | Demasiados archivos para abrir | Subir a 0.5 bajo presión de tokens |
| Umbral demasiado alto | Se pierden learnings útiles | Bajar a 0.3, verificar manualmente |
| Decay permanente olvidado | Se filtran patrones fundamentales | Verificar que decay=1.0 siempre pasa |
| Señal estática | No refleja relevancia cambiante | Actualizar señal tras cada uso |
| No filtrar antes de abrir | Se cargan 32 archivos en contexto | SIEMPRE filtrar por índice primero |

## Verificación

Para verificar que el patrón se ejecuta correctamente:

1. **Conteo de archivos:** El orchestrator reporta cuántos archivos abrió tras el filtro. Debe ser ≤ 5 en condiciones normales, ≤ 3 bajo presión de tokens.
2. **Cobertura del filtro:** Al menos una fila con decay permanente debe estar siempre en el subconjunto.
3. **Actualización del índice:** Tras la sesión, el índice debe reflejar los cambios de señal y decay.
4. **Regla de excepción:** Verificar que ningún learning con `decay = 1.0` fue descartado por el filtro de decay.
5. **Tiempo de lectura:** Leer el índice completo debe tomar < 1 segundo (es un solo archivo).
