# Patrones de Shell CSS para Aurora

**Fecha:** 2026-06-22

Cuando generes HTML con Aurora, SIEMPRE incluye un CSS shell propio. Los componentes Aurora necesitan contexto visual para verse premium.

## Patrón 1: Login Shell

```css
.login-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}
.login-shell::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 20%, var(--nz-surface-glass-brand) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 80%, var(--nz-surface-glass-accent) 0%, transparent 60%);
  pointer-events: none;
}
.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 26rem;
}
```

**Estructura HTML:** Brand → Header → Social login → Divider → Form → Footer

## Patrón 2: Dashboard Shell

```css
.dash-shell {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  min-height: 100vh;
}
.dash-sidebar {
  position: sticky; top: 0; height: 100vh;
  overflow-y: auto;
  padding: 1.5rem 1rem;
  background: var(--nz-surface-soft);
  border-right: 1px solid var(--nz-border-soft);
  display: flex; flex-direction: column; gap: 1rem;
}
.dash-main { padding: 2rem clamp(1.5rem, 4vw, 3rem); overflow-y: auto; }
```

**Estructura HTML:** Sidebar (nav + brand + user) → Main (header → KPIs → Chart/Activity → Table)

## Patrón 3: Landing Shell

```css
.landing-shell {
  background: linear-gradient(180deg, #ffffff 0%, var(--nz-surface-page) 100%);
}
.landing-shell .nz-container {
  max-width: 72rem;
  margin: 0 auto;
  padding: 0 clamp(1.25rem, 4vw, 2.5rem);
}
.landing-hero {
  padding: clamp(4rem, 8vw, 7rem) 0 clamp(3rem, 6vw, 5rem);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.landing-hero::before {
  content: "";
  position: absolute;
  top: -30%; right: -10%;
  width: 30rem; height: 30rem;
  border-radius: 50%;
  background: radial-gradient(circle, var(--nz-surface-glass-brand) 0%, transparent 70%);
  pointer-events: none;
}
```

**Estructura HTML:** Nav → Hero (kicker → title → sub → CTA) → Logos → Features → Pricing → Footer

## Patrón 4: UI Catalog Shell

```css
.ui-shell {
  padding: 2rem clamp(1.5rem, 4vw, 3rem);
  max-width: 64rem;
  margin: 0 auto;
}
.ui-section { margin-bottom: 2.5rem; }
.ui-section__title {
  font-size: var(--nz-text-lg);
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--nz-border-soft);
}
.ui-demo-card {
  padding: 1.5rem;
  border: 1px solid var(--nz-border-soft);
  border-radius: var(--nz-radius-lg);
  background: var(--nz-surface-raised);
  box-shadow: var(--nz-shadow-sm);
}
```

**Estructura HTML:** Header (breadcrumbs + title) → Sections → Demo cards

## Patrón 5: Forms Shell

```css
.forms-shell {
  max-width: 48rem;
  margin: 0 auto;
  padding: 3rem clamp(1.5rem, 4vw, 3rem);
}
.forms-card {
  padding: 2rem;
  border: 1px solid var(--nz-border-soft);
  border-radius: var(--nz-radius-xl);
  background: var(--nz-surface-raised);
  box-shadow: var(--nz-shadow-sm);
}
.forms-grid {
  display: grid;
  gap: 1.25rem;
  grid-template-columns: 1fr 1fr;
}
```

**Estructura HTML:** Header → Sections → Cards → Fields → Actions

## Reglas generales del shell

1. **Máximo 100-200 líneas de CSS** en el `<style>` del shell
2. **Usar `var(--nz-*)`** para colores, bordes, sombras, radios
3. **Mobile-first** — base 1 col, tablet 2 col, desktop 3+ col
4. **Touch targets 44px** en móvil
5. **Hover states** en cards, botones, links del nav
6. **No hardcodear hex** — siempre tokens Aurora
7. **El shell proporciona estructura visual**, los componentes Aurora proporcionan identidad visual
