# Patrón de compactación móvil para apps de uso frecuente

**Fecha:** 2026-06-13  
**Contexto:** MasterFit (dieta-masterfit) — David dice "el resumen superior se ve demasiado grande en el móvil"

## Regla general

En apps de uso frecuente/rápido (dieta, tracking, registro), el hero y los KPIs deben compactarse progresivamente en móvil. No usar el mismo tamaño que desktop.

## Escalado progresivo

| Elemento | Desktop | ≤768px | ≤480px |
|---|---|---|---|
| Hero title | `var(--nz-size-3xl)` | `var(--nz-size-2xl)` | `var(--nz-size-xl)` |
| Hero subtitle | `var(--nz-size-sm)` | `var(--nz-size-xs)` | `var(--nz-size-2xs)` |
| Hero eyebrow | `var(--nz-size-xs)` | `var(--nz-size-2xs)` | `var(--nz-size-2xs)` |
| KPI value | `var(--nz-size-2xl)` | `var(--nz-size-xl)` | `var(--nz-size-lg)` |
| KPI label | `var(--nz-size-2xs)` | `var(--nz-size-2xs)` | `var(--nz-size-2xs)` |
| KPI padding | `var(--nz-space-2) var(--nz-space-1)` | `var(--nz-space-1) var(--nz-space-0)` | `var(--nz-space-1) var(--nz-space-0)` |

## Ejemplo CSS

```css
/* Compactación base */
.nz-hero__title { font-size: var(--nz-size-3xl); }
.nz-hero__sub { font-size: var(--nz-size-sm); }
.nz-hero__eyebrow { font-size: var(--nz-size-xs); }
.nz-kpi__value { font-size: var(--nz-size-2xl); }
.nz-kpi__label { font-size: var(--nz-size-2xs); }
.nz-kpi { padding: var(--nz-space-2) var(--nz-space-1); }

@media (max-width:768px) {
  .nz-hero__title { font-size: var(--nz-size-2xl); }
  .nz-hero__sub { font-size: var(--nz-size-xs); }
  .nz-hero__eyebrow { font-size: var(--nz-size-2xs); }
  .nz-kpi__value { font-size: var(--nz-size-xl); }
  .nz-kpi { padding: var(--nz-space-1) var(--nz-space-0); }
}

@media (max-width:480px) {
  .nz-hero__title { font-size: var(--nz-size-xl); }
  .nz-hero__sub { font-size: var(--nz-size-2xs); }
  .nz-kpi__value { font-size: var(--nz-size-lg); }
}
```

## Acciones: principal primero, secundaria abajo

- **Acción principal** (la que más se usa) → primer tab, tab activo por defecto
- **Acción secundaria** (exportar, config, ayuda) → footer como botón ghost

## Verificación

En móvil, el hero debe tener máximo 2 elementos interactivos. Nada más.
