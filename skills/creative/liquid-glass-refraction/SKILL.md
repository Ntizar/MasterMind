---
name: liquid-glass-refraction
version: "1.0.0"
description: "Efecto Liquid Glass con refracción SVG — design system CSS + React con refracción, specular highlights y blur. Inspirado en Z1Code/glass-refraction (⭐36)."
tags: [liquid-glass, css, svg, refraction, design, ui, glassmorphism]
---

# Liquid Glass con Refracción SVG

## Resumen

Efecto de vidrio líquido (Liquid Glass) con refracción real usando SVG filters. Combina feDisplacementMap para refracción, feGaussianBlur para blur y specular highlights para brillo. CSS + React components.

## Cuándo usar

- UI con efecto glassmorphism avanzado (más allá de backdrop-filter)
- Componentes con refracción real del contenido detrás
- Design system con glass panels premium
- Hero sections con efecto cristal dinámico

## Patrón de uso

```html
<!-- SVG filter para refracción -->
<svg style="position:absolute;width:0;height:0">
  <filter id="glass-refraction">
    <!-- Blur del contenido detrás -->
    <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>
    <!-- Refracción con displacement map -->
    <feDisplacementMap in="blur" in2="SourceGraphic" scale="15" 
      xChannelSelector="R" yChannelSelector="G" result="refract"/>
    <!-- Specular highlight -->
    <feSpecularLighting in="refract" surfaceScale="2" 
      specularConstant="0.8" specularExponent="20" result="spec">
      <fePointLight x="100" y="50" z="200"/>
    </feSpecularLighting>
    <feComposite in="spec" in2="refract" operator="in" result="specMask"/>
    <feComposite in="refract" in2="specMask" operator="arithmetic" 
      k1="0" k2="1" k3="1" k4="0"/>
  </filter>
</svg>

<!-- Glass panel con refracción -->
<div class="glass-panel" style="filter: url(#glass-refraction)">
  <h2>Contenido con efecto cristal</h2>
  <p>El contenido detrás se refracta a través del vidrio</p>
</div>
```

```css
/* CSS-only fallback con backdrop-filter */
.glass-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 4px 30px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* Specular highlight con pseudo-elemento */
.glass-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 50%;
  background: linear-gradient(180deg, 
    rgba(255,255,255,0.15) 0%, 
    transparent 100%);
  border-radius: 16px 16px 0 0;
  pointer-events: none;
}
```

## React component

```jsx
function GlassPanel({ children, blur = 10, opacity = 0.1 }) {
  return (
    <div 
      className="glass-panel"
      style={{
        background: `rgba(255,255,255,${opacity})`,
        backdropFilter: `blur(${blur}px) saturate(180%)`,
        border: '1px solid rgba(255,255,255,0.2)',
        borderRadius: 16,
        boxShadow: '0 4px 30px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.3)'
      }}
    >
      {children}
    </div>
  );
}
```

## Pitfalls

- **Performance:** SVG filters son costosos. Usar en pocos elementos, no en listas largas.
- **backdrop-filter:** Safari necesita `-webkit-backdrop-filter`. Firefox no soporta todos los valores.
- **Refraction real:** `feDisplacementMap` solo funciona con SVG, no con HTML estándar. Usar para elementos visuales clave.
- **Stacking context:** `backdrop-filter` crea stacking context. Puede romper z-index de hijos.
- **Mobile:** backdrop-filter es costoso en mobile. Considerar fallback sin blur en dispositivos lentos.

## Referencias

- glass-refraction: https://github.com/Z1Code/glass-refraction
- SVG Filters: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/filter
- backdrop-filter: https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter

---

**Hecho con ❤️ por David Antizar**
