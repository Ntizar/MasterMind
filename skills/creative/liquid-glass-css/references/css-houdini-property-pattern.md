# CSS Houdini @property — Patrón de gradientes animados en Aurora

Implementado en la mejora #12 del plan 9009 para Ntizar-Aurora (2026-05-31).

## Regla estructural crítica

Los `@property` declarations **DEBEN estar fuera de cualquier `@layer`** — el spec CSS lo exige. Las reglas CSS que usan esas propiedades van dentro de `@layer ntizar.components`.

## Implementación concreta en ntizar.next.css

### 1. Declaraciones @property (nivel global, fuera de @layer)

```css
@property --nz-gradient-angle {
  syntax: "<angle>";
  inherits: true;
  initial-value: 135deg;
}

@property --nz-gradient-pos {
  syntax: "<percentage>";
  inherits: true;
  initial-value: 0%;
}

@property --nz-gradient-pos-2 {
  syntax: "<percentage>";
  inherits: true;
  initial-value: 50%;
}

@property --nz-gradient-pos-3 {
  syntax: "<percentage>";
  inherits: true;
  initial-value: 100%;
}
```

### 2. Clases de gradiente animable (dentro de @layer ntizar.components)

```css
.nz-gradient-animated {
  --nz-gradient-angle: 135deg;
  --nz-gradient-pos: 0%;
  --nz-gradient-pos-2: 58%;
  --nz-gradient-pos-3: 100%;
  background: linear-gradient(
    var(--nz-gradient-angle),
    var(--nz-oklch-brand-soft, var(--nz-color-brand-soft))  var(var(--nz-gradient-pos)),
    var(--nz-oklch-brand, var(--nz-color-brand))            var(--nz-gradient-pos-2),
    var(--nz-oklch-brand-strong, var(--nz-color-brand-strong)) var(--nz-gradient-pos-3)
  );
}
```

Variante accent: `.nz-gradient-animated--accent`
Variante aurora: `.nz-gradient-animated--aurora`

### 3. Keyframes de animación

```css
@keyframes nz-gradient-rotate {
  from { --nz-gradient-angle: 135deg; }
  to   { --nz-gradient-angle: 495deg; }
}

@keyframes nz-gradient-drift {
  from { --nz-gradient-pos: 0%; --nz-gradient-pos-2: 58%; --nz-gradient-pos-3: 100%; }
  to   { --nz-gradient-pos: 10%; --nz-gradient-pos-2: 68%; --nz-gradient-pos-3: 110%; }
}
```

### 4. Clases utilidad

- `.nz-gradient-rotate` — animación de rotación (12s linear infinite)
- `.nz-gradient-drift` — animación de deriva (8s ease-in-out alternate)

### 5. Aurora Mesh Houdini

```css
.nz-aurora-mesh--houdini::before {
  animation-name: nz-mesh-drift-houdini;
  /* Si @property funciona, el navegador interpola las posiciones */
}
```

## Compatibilidad

| Navegador | @property | Degradación |
|-----------|-----------|-------------|
| Chrome/Edge | ✅ Soportado | — |
| Safari 16+ | ✅ Soportado | — |
| Firefox | ❌ No soportado | Gradiente funciona sin animación |

## Métricas de la implementación

- Líneas CSS añadidas: ~160
- Archivos modificados: 1 (`ntizar.next.css`)
- Tokens nuevos: 4 (`@property` declarations)
- Breaking changes: 0

## Referencias

- CSS Houdini Properties and Values API: https://www.w3.org/TR/css-variables-2/
- MDN: @property: https://developer.mozilla.org/en-US/docs/Web/CSS/@property
