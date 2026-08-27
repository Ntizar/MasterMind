# Checklist de Auditoría — 21 Componentes Premium Aurora

## Contexto

Cuando se pide auditar un HTML contra Aurora Design System, verificar estos 21 componentes premium. Si un proyecto tiene más de 3 categorías vacías → NO está usando Aurora correctamente.

## Script de auditoría

```bash
curl -s <url> | python3 agent/skills/frontend-dashboard-patterns/aurora-design-system/scripts/audit-aurora.py -
```

## Componentes premium (21)

### Fondo / atmósfera (2)
- [ ] `nz-aurora-mesh--animated` — fondo mesh animado
- [ ] `nz-orb` — orbs decorativos

### Animaciones (2)
- [ ] `nz-anim-fade-in` — animaciones de entrada
- [ ] `nz-hover-lift` — interacción hover en cards

### Datos / KPIs (4)
- [ ] `nz-kpi` (preferir `nz-kpi--accent`) — tiles de métricas
- [ ] `nz-chart--glass` — gráficos envueltos en glass
- [ ] `nz-progress` / `nz-meter` — barras de progreso
- [ ] `nz-data-card` — tarjetas de datos

### Layout (3)
- [ ] `nz-bento-grid` — layouts de datos
- [ ] `nz-table` — listas/tablas
- [ ] `nz-stack` — spacing consistente

### Interacción (4)
- [ ] `nz-modal` — modales (NO divs custom)
- [ ] `nz-tabs` — navegación por tabs
- [ ] `nz-nav--glass` — sidebar/nav glass
- [ ] `nz-search` — barra de búsqueda

### Feedback / estado (4)
- [ ] `nz-skeleton` — loading states
- [ ] `nz-badge` — badges glass
- [ ] `nz-spinner--accent` — spinner de carga
- [ ] `nz-callout` — callouts informativos

### Extras (4)
- [ ] `nz-stats-banner` — banner de estadísticas
- [ ] `nz-divider--label` — separadores con texto
- [ ] `nz-surface--glass` — superficies glass
- [ ] `nz-gradient-text` — títulos con gradiente

## Métricas de calidad

| Métrica | Umbral OK | Umbral Crítico |
|---|---|---|
| CSS custom líneas | <= 30 | > 50 |
| Clases custom | <= 5 | > 10 |
| Hex hardcodes | 0 | > 0 |
| Inline styles | <= 3 | > 5 |
| Clases Aurora únicas | >= 100 | < 50 |
| Packs cargados | >= 4 | < 2 |
| Componentes premium | >= 15/21 (70%) | < 11/21 (50%) |

## Veredictos

- **🔴 CRÍTICO:** CSS >50 líneas + >10 clases custom + <50% componentes premium
- **🟡 PARCIAL:** CSS 30-50 líneas + 5-10 clases custom + 50-70% componentes premium
- **🟢 OK:** CSS <=30 líneas + <=5 clases custom + >=70% componentes premium
