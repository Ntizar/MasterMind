---
name: business-model-canvas
description: Business Model Canvas interactivo en HTML — los 9 bloques clásicos del BMC con layout grid, zonas por color, bloques editables, timeline de fases y visión de futuro ERA. Template reutilizable para cualquier proyecto.
version: "1.0.0"
author: Hermes Agent
tags: [canvas, business-model, Osterwalder, estrategia, editable, interactivo]
---

# Business Model Canvas — Template Interactivo

Genera Business Model Canvases interactivos en HTML para presentar modelos de negocio de cualquier proyecto. Basado en el framework de Alexander Osterwalder con los 9 bloques clásicos.

## Cuándo usarlo

- Usuario pide un **Business Model Canvas**, **modelo de negocio**, **lienzo estratégico** o presentación del modelo de un proyecto
- Necesitas visualizar y documentar un modelo de negocio completo en una sola página
- Quieres un **template editable** que David pueda modificar directamente en el navegador
- Se enfoca en el **futuro/ERA** del proyecto, no solo el estado actual

## Estructura del Canvas

Los 9 bloques se disponen en el grid clásico del BMC:

| Posición | Bloque | Zona | Color |
|----------|--------|------|-------|
| Arriba izq. | Socios Clave | Infraestructura | Índigo (#6366f1) |
| Arriba izq. | Recursos Clave | Infraestructura | Índigo (#6366f1) |
| Centro superior | Actividades Clave | Infraestructura | Índigo (#6366f1) |
| Centro | Propuesta de Valor | Oferta | Naranja (#f97316) |
| Arriba der. | Segmentos de Clientes | Clientes | Azul (#2563eb) |
| Arriba der. | Canales | Clientes | Azul (#2563eb) |
| Lado der. | Relación con Clientes | Clientes | Azul (#2563eb) |
| Abajo izq. | Estructura de Costes | Finanzas | Verde (#16a34a) |
| Abajo izq. | Fuentes de Ingresos | Finanzas | Verde (#16a34a) |

## Layout CSS Grid

El canvas usa un grid de 5 columnas × 4 filas:

```
[socios] [recursos] [actividades] [propuesta] [clientes]
         [costes]                    [propuesta] [canales]
         [ingresos]                  [propuesta] [relacion]
```

- **Socios** + **Recursos**: columnas 1-2, filas 1-2 (alto 2)
- **Actividades**: columna 3, fila 1 (alto 1)
- **Propuesta de Valor**: columna 4, filas 1-2 (alto 2, más grande)
- **Clientes**: columna 5, filas 1-2 (alto 2)
- **Canales**: columna 5, fila 2
- **Relación**: columna 5, filas 3-4 (alto 2)
- **Costes**: columna 2, filas 3-4 (alto 2)
- **Ingresos**: columna 1, filas 3-4 (alto 2)

## Bloques editables

Cada bloque `<div class="bmc-block">` tiene `contenteditable="true"` — David puede hacer clic y modificar cualquier texto directamente en el navegador. Al hacer focus, se muestra un outline azul.

## Tags temporales

Cada ítem dentro de los bloques lleva una etiqueta:
- 🔵 `<span class="future-tag current">HOY</span>` — lo que ya existe
- 🟢 `<span class="future-tag future">ERA</span>` — visión de futuro

## Secciones extra (obligatorias)

Todo BMC generado debe incluir:

1. **Stats bar** — KPIs principales del proyecto (4 stats alternando azul/naranja/verde)
2. **Legenda** — Muestra los colores por área (Clientes, Oferta, Infraestructura, Finanzas)
3. **Sección Visión de Futuro** — Grid de cards con initiatives futuras, cada una con título, descripción y prioridad
4. **Timeline / Hoja de Ruta** — 4 fases en horizontal con flechas (→) entre ellas
5. **Footer** — "Hecho con ❤️ por David Antizar"

## Prioridades de la sección futura

Usar 3 niveles de prioridad:
- `alta` — Rojo (#dc2626) — imprescindible
- `media` — Amarillo (#d97706) — importante pero no crítico
- `estrategica` — Azul (#2563eb) — impacto transformador a largo plazo

## Responsive

- Desktop (>900px): grid de 5 columnas como definido arriba
- Móvil (≤900px): todos los bloques en 1 columna apilados verticalmente
- Las flechas del timeline cambian de → a ↓

## Template mínimo

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PROYECTO — Business Model Canvas</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.nucleo.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.data.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.ui.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.motion.css">
</head>
<body class="nz" data-nz-skin="aurora" data-nz-theme="light">
  <!-- Header con badge ERA -->
  <!-- Stats bar -->
  <!-- Canvas grid con 9 bloques contenteditable -->
  <!-- Sección Visión de Futuro ERA -->
  <!-- Timeline de fases -->
  <!-- Footer -->
</body>
</html>
```

## Pitfalls

- **No usar gradientes azul→naranja** — colores sólidos puros del Núcleo Aurora
- **body class="nz" obligatorio** — sin `.nz` en el body, nada funciona
- **No inventar clases Aurora** — el grid del BMC requiere CSS custom propio, es normal y justificado
- **Cada bloque debe tener contenteditable** — es la clave interactiva del canvas
- **Usar 4 stats en la stats bar** — alternando colores, no todos iguales
- **Timeline siempre con 4 fases** — mínimo 4 fases en la hoja de ruta

## Referencias

- Ver `references/ciaf-bmc-template.md` para la implementación completa y verificada del template.
