# Revisión Visual y Modernización CSS — DeSumarIntegrar

**Fecha:** 2026-06-14  
**Proyecto:** DeSumarIntegrar (github.com/Ntizar/DeSumarIntegrar)  
**Archivos:** 106 HTML (8 índices + 98 sesiones)  
**Niveles:** Primaria (57), ESO (9), Bachiller (11), Universidad (10)

## Resultados

| Métrica | Antes | Después | Cambio |
|---------|-------|---------|--------|
| Glassmorphism | ~20 | 106/106 | +86 archivos |
| Estilos inline | 2287 | 907 | -60% |
| ESO con Plotly | 0/9 | 9/9 | +9 |
| Duplicados | 1 | 0 | -1 |

## Glassmorphism

Clases CSS añadidas a todos los archivos:
- `.glass` — fondo blanco translúcido con blur
- `.box.glass` — cajas con glass
- `.interactive.glass` — elementos interactivos
- `.summary.glass` — resúmenes
- `.chart-container.glass` — contenedores de gráficos

**Pitfall crítico:** Algunos archivos tienen `</style` sin el `>` de cierre (corrupción). Detectar con `grep -c '</style' file` vs `grep -c '</style>' file`. Reparar tag roto antes de inyectar CSS.

## Reducción de Estilos Inline

### Método
1. Extraer todos los estilos inline con `re.findall(r'style="([^"]*)"', content)`
2. Contar frecuencias con `collections.Counter`
3. Mapear patrones comunes → clases CSS
4. Reemplazar con `re.sub(pattern, replacement, content)`
5. Iterar con regex flexibles para colores hexadecimales variables

### Patrones más frecuentes reemplazados
- `margin-top:.5rem` → `.mt-1` (220x)
- `padding-left:1.2rem; margin-top:.5rem` → `.pl-1-mt-1` (104x)
- `display: inline-flex; align-items: center; ...` → `.nav-link` (83x)
- `color:#94a3b8; font-size: 1rem` → `.text-muted` (77x)
- `text-align:center; margin: 1rem 0` → `.text-center` (55x)

### Regla
No eliminar TODOS los estilos inline. Objetivo: reducir patrones comunes (>10 apariciones). Los estilos únicos de cada archivo se dejan. Meta: 60% de reducción.

## Plotly en ESO

Cada archivo de ESO recibe:
1. CDN Plotly 2.27.0 antes de `</head>`
2. Div `#plot-tema` con `.chart-container glass`
3. Script de renderizado con datos relevantes al tema

**Regla:** Plotly SOLO para ESO+, NO Primaria. Cada gráfico debe ilustrar el concepto específico del tema.

## Duplicados

`s04-4-fracciones-equivalentes.html` eliminado (tema redundante con `s04-1-fracciones-equivalentes.html`). Índice `s04-4primaria.html` actualizado para apuntar a `s04-1`.
