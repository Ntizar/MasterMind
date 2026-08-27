# Anti-AI Design Rules — David Antizar

## Señales de "Look IA" que EVITAR
- ❌ **Border-left colored cards** (azul/rojo/naranja a la izquierda) — "se nota mucho que es IA"
- ❌ **Liquid glass effects** — rechazados explícitamente
- ❌ **Dark themes** para dashboards de datos
- ❌ **Font sizes grandes** en KPIs (17px+ es demasiado)
- ❌ **Gradientes llamativos** en fondos de cards
- ❌ **Tablas con demasiado padding** — David prefiere datos compactos

## Lo que SÍ funciona (estilo David)
- ✅ Fondo blanco, sombras sutiles (`box-shadow: 0 1px 3px rgba(0,0,0,0.08)`)
- ✅ Hover con elevación (`transform: translateY(-1px)`, sombra crece)
- ✅ Fuentes compactas (10-12px labels, 14-17px values)
- ✅ Colores sólidos en bordes sutiles (`border: 1px solid #e2e8f0`)
- ✅ Bordes redondeados pequeños (`border-radius: 8px`)
- ✅ Espaciado generoso entre elementos pero compacto en cards
- ✅ Botones tipo pill/badge (`border-radius: 14-16px`)
- ✅ Scroll horizontal para muchas opciones (no pestañas verticales)

## Tabs Responsive (15+ pestañas)
```css
.tabs-row { display: flex; flex-wrap: wrap; gap: 4px; }
.tab-btn { font-size: 10px; padding: 3px 8px; flex-shrink: 0; }
```

## Data Density
David quiere VER MUCHOS DATOS en cada pantalla:
- KPIs compactos en grid (no cards grandes)
- Charts pequeños pero informativos
- Selectores de ciudad/región por pestaña
- Autogeneración de datos por CCAA/provincia
- Datos en tiempo real (fetch on click)
