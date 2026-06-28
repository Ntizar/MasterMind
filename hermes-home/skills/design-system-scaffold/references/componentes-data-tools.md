# Componentes para Herramientas de Datos / Dashboards

Componentes que un design system corporativo necesita para soportar herramientas de datos (dashboards, visores, reportes). Extraído de la auditoría Kaizen v4.0.

## Componentes básicos (ya presentes en la mayoría de DS)

| Componente | Clases típicas | Uso |
|---|---|---|
| Tiles/KPIs | `*-tile`, `*-kpi` | Métricas resumen |
| Tablas | `*-table` | Datos tabulares |
| Forms | `*-input`, `*-select` | Filtros y configuración |
| Tabs | `*-tabs` | Navegación por secciones |
| Badges | `*-badge` | Estados (activo/error/ok) |
| Alerts | `*-alert` | Notificaciones inline |
| Buttons | `*-btn` | Acciones |
| Progress | `*-progress` | Carga de datos |

## Componentes que SUELEN FALTAR (añadir al extender)

### Interacción
- **Dropzone** — Arrastrar y soltar archivos (ZIPs, CSVs, PDFs). Borde punteado, estado hover, feedback visual.
- **Range Slider** — Seleccionar rango numérico (distancia, fecha, precio). Doble thumb para rango min-max.
- **Toggle/Switch** — Activar/desactivar opciones binarias. Más limpio que checkbox para on/off.
- **Checkbox/Radio** — Selección múltiple (checkbox) o única (radio). Estilo flat con label integrado.
- **Filter Chips** — Tags clickeables para filtrar. Seleccionados en color primario, deseleccionados en gris.

### Feedback / Carga
- **Skeleton screens** — Placeholder animado mientras carga contenido. Mejor percepción que spinner solo.
- **Loading states** — Spinner, barra de progreso indeterminada, overlay de carga.
- **Toast/Snackbar** — Notificaciones temporales que desaparecen. Posición fija (bottom-right).
- **Status indicator** — Punto de color + texto para estado de entidad (activo, pausado, error).
- **Empty state** — Mensaje cuando no hay datos. Icono + texto + CTA opcional.

### Layout / Navegación
- **Panel/Drawer** — Panel lateral deslizante para detalles o configuración. Se superpone al contenido.
- **Search dropdown** — Input con resultados filtrados en tiempo real. Autocompletado.
- **Stats row** — Fila de métricas resumen (3-5 KPIs en línea). Variación del tiles grid.

### Datos
- **Data table enhanced** — Tabla con: ordenación por columna, paginación, búsqueda inline, selección de filas.
- **JSON viewer** — Colapsar/expandir objetos JSON. Syntax highlighting básico.
- **Timestamp** — Formato relativo ("hace 3 min") + tooltip con fecha completa.

## Checklist de auditoría para extender un DS existente

```
1. ¿Tiene dropzone? → Si no, añadir
2. ¿Tiene range slider? → Si no, añadir
3. ¿Tiene toggle/switch? → Si no, añadir
4. ¿Tiene skeleton loading? → Si no, añadir
5. ¿Tiene toast/snackbar? → Si no, añadir
6. ¿Tiene panel/drawer? → Si no, añadir
7. ¿Tiene filter chips? → Si no, añadir
8. ¿Tiene empty state? → Si no, añadir
9. ¿Tiene search dropdown? → Si no, añadir
10. ¿Tiene stats row? → Si no, añadir
```

## Referencia: Kaizen v4.0 (14 componentes añadidos)

18 secciones CSS nuevas (18-31) añadidas a `kaizen.css`:
1. Dropzone (kz-dropzone)
2. Range Slider (kz-slider)
3. Progress Bar (kz-progress)
4. Loading States (kz-loading, kz-spinner)
5. Search Dropdown (kz-search)
6. Panel/Drawer (kz-panel)
7. Toggle/Switch (kz-toggle)
8. Filter Chips (kz-chips)
9. Toast/Snackbar (kz-toast)
10. Status Indicator (kz-status)
11. Stats Row (kz-stats)
12. Empty State (kz-empty)
13. Skeleton (kz-skeleton)
14. Checkbox/Radio (kz-check, kz-radio)
