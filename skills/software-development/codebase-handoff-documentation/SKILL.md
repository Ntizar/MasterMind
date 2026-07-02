---
name: codebase-handoff-documentation
version: "1.0.0"
description: "Crear guías de mantenimiento para que cualquier persona pueda entender y trabajar en un código existente. Documentación de traspaso: leer el codebase completo, explicar qué hace cada bloque de código, esquemas de datos, scripts, despliegue y errores conocidos."
tags: [documentation, handoff, maintenance, codebase, guide]
---

# Codebase Handoff Documentation — Guías de Mantenimiento

## Resumen

Procedimiento para crear una guía completa de mantenimiento de un proyecto: leer el codebase, entender su arquitectura, y producir un `.md` que explique **qué hace cada bloque de código** de forma que cualquier persona sin contexto previo pueda mantenerlo.

## Cuándo usar

- Usuario pide "guía de mantenimiento", "documentación para que cualquiera pueda usarlo", "handoff", "traspaso de conocimiento"
- Proyecto que va a cambiar de responsable
- Documentación para un equipo que no conoce el código
- Antes de que alguien se vaya de una empresa/proyecto

## Diferencia con system-audit

| | system-audit | codebase-handoff-documentation |
|---|---|---|
| **Objetivo** | Encontrar problemas y proponer mejoras | Explicar QUÉ HACE el código que ya existe |
| **Output** | Informe de calidad + plan de mejoras | Guía de mantenimiento paso a paso |
| **Tono** | Crítico, constructivo | Didáctico, explicativo |
| **Líneas** | Señala líneas problemáticas | Explica qué hace cada bloque |

## Flujo de 6 pasos

### Paso 1: Inventario del proyecto

```bash
# Estructura
find . -maxdepth 3 -type f | grep -v '.git/' | head -100
# Conteo por tipo
find . -name '*.html' -o -name '*.js' -o -name '*.py' -o -name '*.json' | grep -v '.git/' | wc -l
# Archivos más grandes (por donde empezar)
find . -type f -not -path '*/.git/*' -exec wc -c {} + | sort -rn | head -20
```

**Objetivo:** Saber qué archivos son clave, cuáles son grandes, y por dónde empezar a leer.

### Paso 2: Leer TODO el código fuente

**Regla crítica:** Leer TODOS los archivos de código, no solo los grandes. Un archivo de 50 líneas puede contener lógica crucial.

Orden de lectura recomendado:
1. **README** — Contexto del proyecto
2. **Archivo principal** (index.html, main.py, etc.) — El corazón del sistema
3. **Scripts/pipelines** — Cómo se generan los datos
4. **Archivos de datos** (JSON, CSV) — Esquemas y ejemplos
5. **Configuración** (workflows, configs) — Cómo se despliega

### Paso 3: Identificar bloques de código

Para cada archivo grande (>200 líneas), dividir en bloques funcionales:

```
Líneas 1-12: Cabecera y dependencias externas
Líneas 13-331: Estilos CSS (variables, layout, responsive)
Líneas 336-558: Estructura HTML (header, tabs, sidebar, contenido)
Líneas 565-1735: Lógica JavaScript (init, datos, filtros, mapa, gráficos)
```

**Criterios para separar bloques:**
- Cambio de sección marcado con comentario (`/* ===== HEADER ===== */`)
- Cambio de tipo de contenido (HTML → CSS → JS)
- Función o módulo nuevo
- Grupo de funciones relacionadas

### Paso 4: Explicar cada bloque

Para cada bloque, responder:
1. **Qué hace** — Función en lenguaje natural (1-3 frases)
2. **Dependencias** — Qué necesita para funcionar (archivos, APIs, librerías)
3. **Datos de entrada/salida** — Qué consume y qué produce
4. **Pitfalls** — Errores comunes o cosas no obvias

**Regla de estilo:** Explicar como si el lector supiera programar pero NO conoce este proyecto específico. No asumir conocimiento del dominio (ej: si es un visor ferroviario, explicar qué es la CIAF).

### Paso 5: Documentar esquemas de datos

Incluir ejemplos reales de los JSON/CSV que alimentan el sistema:

```json
{
  "id": "2024-64/2024",
  "tipo": "incidente",
  "gravedad": "menor",
  "ubicacion": { "estacion": "...", "lat": 40.03, "lng": -2.14 }
}
```

Explicar:
- Qué significa cada campo
- Valores posibles (enum)
- Relaciones entre archivos (un JSON referencia a otro)

### Paso 6: Documentar mantenimiento y errores conocidos

Incluir secciones prácticas:
- **Cómo añadir datos nuevos** — Pasos concretos
- **Cómo modificar el diseño** — Qué archivo tocar
- **Errores conocidos** — Bugs documentados con workaround
- **Despliegue** — Cómo se publica (GitHub Pages, etc.)

## Formato del output

```markdown
# 📋 [Nombre del Proyecto] — Guía del código para mantenimiento

## 1. Qué es [Proyecto]
[Explicación no técnica, 1 párrafo]

## 2. Estructura del proyecto
[Árbol de directorios comentado]

## 3. Esquema de datos
[Ejemplos reales de JSON/CSV con campos explicados]

## 4. [Archivo principal] — Explicación por bloques
### 4.1 [Nombre del bloque] (líneas X-Y)
[Código relevante + explicación]

## 5. Scripts/Pipelines
[Cada script explicado]

## 6. Despliegue y mantenimiento
[Cómo añadir datos, modificar diseño, publicar]

## 7. Errores conocidos
[Bugs documentados con workaround]
```

## Ejemplo real

Ver `references/ciaf-visor-handoff-guide.md` — Guía completa del CIAF Visor (1735 líneas de HTML + 4 scripts Python documentados bloque por bloque).

## Pitfalls

- **No leer solo el README** — El README es marketing, no documentación técnica. Leer TODO el código.
- **No explicar QUÉ hace el código, sino PARA QUÉ** — "Línea 572: llama a loadData()" es inútil. "Línea 572: inicia la carga de datos desde JSONs remotos, que es lo primero que necesita el sistema para funcionar" es útil.
- **No asumir que el lector conoce el dominio** — Si el proyecto es de ferrocarriles, explicar qué es la CIAF. Si es de medicina, explicar qué es un EHR.
- **Incluir ejemplos reales de datos** — Un esquema JSON vacío no enseña nada. Un ejemplo con datos reales del proyecto sí.
- **Documentar errores conocidos** — Los bugs que ya se encontraron y tienen workaround son el conocimiento más valioso para el siguiente mantenedor.
- **No olvidar los scripts de pipeline** — Muchos proyectos dependen de scripts Python que generan los datos. Si nadie sabe cómo ejecutarlos, el proyecto muere.
- **Separar por bloques funcionales, no por líneas exactas** — "Líneas 100-150" es mejor que "línea 100 hace X, línea 101 hace Y". Agrupar por función/propósito.
