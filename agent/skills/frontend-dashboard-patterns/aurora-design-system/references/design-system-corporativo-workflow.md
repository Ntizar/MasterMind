# Workflow: Design System Corporativo (no Aurora)

Cuando el usuario pide un CSS compartido para un equipo corporativo con colores oficiales propios, NO usar Aurora. Crear o usar un design system dedicado.

## Señales de que NO es Aurora
- "Queremos un CSS que usen todos del equipo"
- "Que se parezca al intranet de la empresa"
- "Colores de [Empresa]"
- Hay un manual de marca oficial con colores propios
- "Usa el Kaizen" / "estilo Ineco"

## Design systems corporativos existentes

### Kaizen Design System v4.0 (Ineco)
- **Repo local:** `/root/workspace/kaizen-design-system/`
- **CSS:** `kaizen.css` (1479 líneas)
- **CDN:** `cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css`
- **Colores oficiales:** Azul #1A4488 (Pantone 7687 C), Rojo #CB1823 (Pantone 485 C), Azul Medio #3463AC, Azul Claro #6B96CF
- **Estilo:** Flat corporativo, sin sombras, sin gradientes, bordes sutiles (1px), sin cards bordeadas pesadas
- **Clases:** `.kz-*` (sidebar, header, tiles, btns, table, forms, chips, slider, progress, tabs, etc.)
- **Tokens:** `--kz-azul`, `--kz-rojo`, `--kz-gris-*`, `--kz-font`, `--kz-gap-*`, `--kz-radius-*`
- **Uso:** `<link rel="stylesheet" href="path/to/kaizen.css">` + clases `kz-*`
- **AGENTS.md:** `/root/workspace/kaizen-design-system/AGENTS.md`

## Flujo para crear nuevo DS corporativo
1. Buscar manual de marca del equipo (colores, tipografía, estilo)
2. Crear CSS con variables `--<prefix>-*` y clases `<prefix>-*`
3. Publicar en repo + CDN (jsDelivr)
4. Documentar en AGENTS.md para agentes IA
5. NO mezclar con Aurora

## Conversión de proyecto existente a DS corporativo
Ver `rebranding-proyecto-web` skill → sección "Conversión a Design System corporativo"
