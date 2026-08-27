# Plantilla: Caso de Negocio Corporativo

> Estructura HTML para presentaciones de caso de negocio, propuestas internas y roadmaps.
> Basado en Kaizen Ineco v4 (commit bddb586).

## Estructura de secciones

```
1. HERO
   - Tag (ej: "Caso de Negocio · Empresa · 2025")
   - Título principal con palabra clave en color
   - Subtítulo explicativo
   - 4 KPI tiles (grid-4)

2. EL PROBLEMA
   - Comparación lado a lado: card-red (manual) vs card-green (automático)
   - Cada lado: steps numerados con tiempos
   - Callout con resultado

3. EJEMPLO REAL
   - Card con header de color (simula el producto)
   - KPIs del producto
   - Tabla de datos reales
   - Segunda tabla (escenarios)
   - Fuentes con links
   - Callout "dato clave"

4. MODELO DE NEGOCIO
   - Grid-2: Propuesta (invert-row) + Ejemplo numérico (card-green)
   - Tabla proyección 3 años

5. POR QUÉ ESTO VA A SER LA FORMA DE TRABAJAR
   - Grid-3 de 6 argument cards (icon + título + descripción)
   - Callout azul con frase potente

6. LA INVERSIÓN
   - Grid-2: Inversión inicial + Retorno
   - Roadmap 3 fases (grid-3)

7. CIERRE
   - Fondo blue-light
   - Título potente
   - 4 KPI tiles finales

8. FOOTER
   - "Hecho con ❤️ por David Antizar"
   - Links al repo
```

## CSS mínimo requerido

Incluir: variables CSS, secciones, container, kpi, card, table-wrap, table, step, callout, tag, invest-row, divider, fade-in animation.

## Datos que siempre incluir
- Números concretos (€, %, horas, personas)
- Comparación antes/después
- Ejemplo real del producto (no screenshots)
- Fuentes de datos
- Proyección temporal (1-3 años)
- ROI calculado

## Pitfalls
- NO inventar datos — usar los que el usuario proporciona o los del proyecto
- NO hacer tablas markdown en la presentación — usar HTML tables
- SIEMPRE footer con atribución a David
- Fondo blanco SIEMPRE para este tipo de presentación
