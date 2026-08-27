# Patrón: Migración Completa a Aurora Design System

**Sesión:** 2026-06-16 (ContrataPúblico)
**Tipo:** Auditoría → Migración completa de HTML existente a Aurora

## Contexto

Proyecto HTML existente con CSS custom propio (`cp-*` classes, 578 líneas de CSS) que necesita migrarse al Aurora Design System sin romper funcionalidad.

## Procedimiento en 5 fases

### Fase 1: Auditoría automática

Contar métricas del estado actual:
```python
import re

with open('index.html', 'r') as f:
    content = f.read()

# CSS custom
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
css_lines = [l for l in style_match.group(1).split('\n') if l.strip() and not l.strip().startswith('/*')]

# Clases custom vs Aurora
custom = re.findall(r'cp-[a-zA-Z0-9_-]+', content)
aurora = re.findall(r'nz-[a-zA-Z0-9_-]+', content)

# Packs cargados
packs = re.findall(r'ntizar\.[a-zA-Z0-9_-]+\.css', content)

# Hex hardcodes en CSS
hex_in_css = re.findall(r'#[0-9a-fA-F]{3,8}\b', style_match.group(1))

# Inline styles
inline = re.findall(r'style="[^"]*"', content)

print(f"CSS lines: {len(css_lines)}")
print(f"Custom classes: {len(set(custom))}")
print(f"Aurora classes: {len(set(aurora))}")
print(f"Packs loaded: {sorted(set(packs))}")
print(f"Hex colors in CSS: {len(hex_in_css)}")
print(f"Inline styles: {len(inline)}")
```

### Fase 2: Cargar packs Aurora faltantes

**Packs mínimos necesarios:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.next.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.data.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.charts.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.motion.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.ui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.forms.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.patterns.css">
```

**Nota:** Usar `@master` en vez de `@latest` para evitar cache de Cloudflare (4h).

**Verificar qué packs tienen qué clases:**
```bash
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.next.css | grep -c 'card--glass-liquid'
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.data.css | grep -c 'stat-grid'
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.motion.css | grep -c 'hover-lift'
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.ui.css | grep -c 'accordion'
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.forms.css | grep -c 'search--lg'
curl -s https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/ntizar.patterns.css | grep -c 'bento-grid'
```

### Fase 3: Reemplazar HTML con componentes Aurora

**Estructura base del body:**
```html
<body class="nz" data-nz-theme="light" data-nz-skin="aurora" data-nz-shape="default" data-nz-density="comfortable">
  <!-- Mesh y orbs DENTRO del app-shell (position:absolute, no fixed) -->
  <div class="nz-app-shell" style="position:relative;z-index:1;background:transparent;min-height:100vh;">
    <div class="nz-aurora-mesh nz-aurora-mesh--animated" style="position:absolute;inset:0;z-index:0;pointer-events:none;"></div>
    <div class="nz-orb nz-orb--aurora nz-orb--lg" style="position:absolute;top:5%;left:3%;z-index:0;pointer-events:none;opacity:0.9;"></div>
    <div class="nz-orb nz-orb--accent" style="position:absolute;bottom:10%;right:5%;z-index:0;pointer-events:none;opacity:0.7;"></div>
    <div class="nz-orb nz-orb--brand nz-orb--sm" style="position:absolute;top:50%;right:15%;z-index:0;pointer-events:none;opacity:0.6;"></div>
    
    <!-- Contenido real -->
    <aside class="nz-sidebar">...</aside>
    <main class="nz-main">...</main>
  </div>
</body>
```

**Mapeo de componentes (custom → Aurora):**

| Custom | Aurora | Notas |
|--------|--------|-------|
| `cp-contract-grid` | `nz-bento-grid` | Grid responsive de cards |
| `cp-contract-card` | `nz-card nz-card--glass-liquid nz-hover-lift` | Card con glass + hover |
| `cp-contract-card__header` | `nz-card__header` | Header de card |
| `cp-contract-card__icon` | `nz-badge nz-badge--glass` | Badge con icono |
| `cp-contract-card__tag` | `nz-badge nz-badge--glass-brand` | Badge con color |
| `cp-article-card` | `nz-card nz-card--glass-liquid nz-hover-lift` | Card de artículo |
| `cp-article-num` | `nz-badge nz-badge--glass-brand` | Badge de número |
| `cp-article-title` | `nz-text-strong nz-text-sm` | Título de artículo |
| `cp-article-meta` | `nz-text-sm nz-text-muted` | Meta info |
| `cp-tree` | `nz-accordion` | Árbol jerárquico |
| `nz-surface nz-surface--glass-soft` | `nz-card nz-card--glass-liquid` | Reemplazar surface por card |
| `nz-surface__body` | `nz-card__body` | Body de card |
| `nz-surface__header` | `nz-card__header` | Header de card |
| Loading spinner | `nz-skeleton nz-skeleton--block` | Skeleton loading |
| `nz-modal` (custom) | `nz-modal` (Aurora) | Modal con backdrop blur |

**Sidebar:**
```html
<aside class="nz-sidebar">
  <div class="nz-sidebar__header">
    <div class="nz-sidebar__logo">⚖️</div>
    <div class="nz-sidebar__title">Nombre</div>
    <div class="nz-sidebar__subtitle">Subtítulo</div>
  </div>
  <nav class="nz-sidebar__nav">
    <a class="nz-sidebar__link" onclick="switchTab('modulo')" data-tab="modulo">
      <span class="nz-sidebar__icon">📊</span>
      <span class="nz-sidebar__label">Módulo</span>
    </a>
  </nav>
  <div class="nz-sidebar__footer">
    <div class="nz-sidebar__version">v0.1.0</div>
    <div class="nz-sidebar__credit">Hecho con ❤️ por David Antizar</div>
  </div>
</aside>
```

**Hero con KPIs:**
```html
<section class="nz-hero nz-hero--centered">
  <div class="nz-hero__inner">
    <div class="nz-hero__eyebrow">Descripción</div>
    <h1 class="nz-hero__title nz-gradient-text">⚖️ Título</h1>
    <p class="nz-hero__sub">Subtítulo</p>
    <div class="nz-stat-grid nz-stat-grid--4">
      <div class="nz-stat-tile">
        <div class="nz-stat-tile__value">100</div>
        <div class="nz-stat-tile__label">Items</div>
      </div>
    </div>
    <div class="u-nz-gap-2" style="display:flex;gap:10px;flex-wrap:wrap;">
      <a class="nz-btn nz-btn--glass-liquid-brand">Botón 1</a>
      <a class="nz-btn nz-btn--glass-liquid-accent">Botón 2</a>
    </div>
  </div>
</section>
```

**Modal:**
```html
<dialog class="nz-modal" id="myModal" onclick="if(event.target===this)closeModal()">
  <div class="nz-modal__panel">
    <div class="nz-modal__close" onclick="closeModal()">✕</div>
    <div class="nz-modal__header">
      <div class="nz-modal__icon">📊</div>
      <div>
        <div class="nz-modal__title">Título</div>
        <div class="nz-modal__art-ref nz-text-sm nz-text-muted">Referencia</div>
      </div>
    </div>
    <div class="nz-modal__body">
      <p class="nz-modal__desc nz-text--secondary">Descripción</p>
      <ul class="nz-modal__features nz-text-sm">...</ul>
    </div>
  </div>
</dialog>
```

### Fase 4: CSS custom mínimo (solo lo que no viene en packs)

Los packs de Aurora NO incluyen: `nz-gradient-text`, `nz-aurora-mesh`, `nz-orb`, `nz-toast-container`. Hay que definirlos en el `<style>` inline:

```css
/* nz-gradient-text */
.nz-gradient-text {
  background: linear-gradient(135deg, #1a5276 0%, #c0392b 50%, #1a5276 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* nz-aurora-mesh */
.nz-aurora-mesh {
  background: radial-gradient(ellipse at 20% 50%, rgba(37,99,235,0.25) 0%, transparent 50%),
              radial-gradient(ellipse at 80% 20%, rgba(249,115,22,0.2) 0%, transparent 50%),
              radial-gradient(ellipse at 50% 80%, rgba(124,58,237,0.18) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 60%, rgba(236,72,153,0.15) 0%, transparent 50%);
  background-size: 200% 200%;
  animation: auroraMesh 20s ease-in-out infinite;
}
@keyframes auroraMesh {
  0%, 100% { background-position: 0% 50%, 100% 0%, 50% 100%; }
  25% { background-position: 50% 0%, 0% 100%, 100% 50%; }
  50% { background-position: 100% 50%, 50% 0%, 0% 100%; }
  75% { background-position: 50% 100%, 100% 50%, 50% 0%; }
}

/* nz-orb */
.nz-orb { border-radius: 50%; filter: blur(80px); pointer-events: none; }
.nz-orb--lg { width: 500px; height: 500px; }
.nz-orb--sm { width: 300px; height: 300px; }
.nz-orb--brand { background: radial-gradient(circle, rgba(37,99,235,0.2) 0%, transparent 70%); }
.nz-orb--accent { background: radial-gradient(circle, rgba(249,115,22,0.18) 0%, transparent 70%); }
.nz-orb--aurora { background: radial-gradient(circle, rgba(37,99,235,0.15) 0%, rgba(124,58,237,0.08) 100%); }
```

**Meta de CSS custom:** < 200 líneas. Si se pasa, revisar si un pack tiene el componente.

### Fase 5: Actualizar JS dinámico

Las funciones JS que generan HTML dinámico (renderizado de artículos, contratos, modales) deben reemplazar clases `cp-*` por `nz-*`:

```javascript
// ANTES
html += '<div class="cp-article-card" onclick="verArticulo(' + num + ')">';
html += '<div class="cp-article-num">Artículo ' + num + '</div>';

// DESPUÉS
html += '<div class="nz-card nz-card--glass-liquid nz-hover-lift" onclick="verArticulo(' + num + ')">';
html += '<div class="nz-card__header">';
html += '<span class="nz-badge nz-badge--glass-brand">Art. ' + num + '</span>';
```

**Verificación post-migración:**
```python
# Debe ser 0
custom = re.findall(r'cp-[a-zA-Z0-9_-]+', content)
assert len(custom) == 0, f"Quedan {len(set(custom))} clases custom: {sorted(set(custom))}"

# Aurora classes debe ser alto
aurora = re.findall(r'nz-[a-zA-Z0-9_-]+', content)
assert len(set(aurora)) > 50, f"Solo {len(set(aurora))} clases Aurora — insuficiente"
```

## Pitfalls críticos

### Pitfall 1: Mesh y orbs detrás del app-shell

**Problema:** Si el mesh y los orbs están con `position:fixed` FUERA del app-shell, y el app-shell tiene `background: rgba(255,255,255,0.6)`, el mesh queda tapado.

**Solución:**
1. Mover mesh y orbs DENTRO del app-shell
2. Usar `position:absolute` en vez de `position:fixed`
3. App-shell con `background: transparent`
4. Cards con `nz-card--glass-liquid` (background: rgba(255,255,255,0.55)) para que se vea el mesh a través

### Pitfall 2: nz-gradient-text no viene en packs

**Problema:** `nz-gradient-text` no está en ningún pack de Aurora. Hay que definirlo en CSS custom.

**Solución:** Definir con `background-clip: text` + `linear-gradient`.

### Pitfall 3: nz-accordion sin animaciones

**Problema:** `nz-accordion` puede venir en `ntizar.ui.css` pero sin estilos de animación.

**Solución:** Definir animaciones de apertura/cierre con `details[open] summary::before { transform: rotate(90deg); }`.

### Pitfall 4: nz-modal no viene en packs

**Problema:** `nz-modal` no está en ningún pack. Hay que definirlo completo.

**Solución:** Definir con `position: fixed`, `backdrop-filter: blur`, `nz-modal__panel`, `nz-modal__close`, etc.

### Pitfall 5: nz-toast-container no viene en packs

**Problema:** `nz-toast-container` no está en packs.

**Solución:** Definir como contenedor de toasts con `position: fixed`, `z-index: 99999`.

### Pitfall 6: Cards con backdrop-filter tapando el mesh

**Problema:** `backdrop-filter: blur(12px)` en cards hace el mesh menos visible.

**Solución:** Ajustar opacidad del mesh a 0.25+ y usar `background: rgba(255,255,255,0.55)` en cards (no 0.75).

### Pitfall 7: Fondo del body invisible

**Problema:** Gradiente de fondo con opacidad 0.03 es prácticamente invisible.

**Solución:** Usar colores sólidos pastel en el gradiente del body:
```css
background: linear-gradient(135deg, #eef2ff 0%, #fef3c7 30%, #fdf2f8 60%, #eef2ff 100%);
```

## Métricas objetivo post-migración

| Métrica | Objetivo |
|---------|----------|
| Clases Aurora únicas | > 50 |
| CSS custom líneas | < 200 |
| Clases custom `cp-*` | 0 |
| Packs Aurora | 7+ |
| Features Aurora usadas | 30+ |

## Referencias

- Aurora Design System: https://github.com/Ntizar/Ntizar-Aurora
- Skill `frontend-dashboard-patterns` sección 11: Aurora Design System
