# Aurora 7 — Receta completa del wow (validada por David, 2026-09-08)

Proyecto: `C:\Users\d_ant\Projects\Aurora-7\`. Caso real donde se aplicó el patrón anti "demasiado igual".

## Decisiones del usuario (aprobadas vía clarify)

- **Repo nuevo Aurora-7** (no carpeta v7 dentro de Ntizar-Aurora).
- **Dark mode desde el día 1 con toggle** (◐ en la topbar) — excepción puntual aprobada a la regla light-por-defecto de Aurora v6.
- **Cero glass TOTAL** — más estricto que v6: ni glass sutil. Solo sólidos + sombras multicapa.

## Arquitectura

```
Aurora-7/
├── index.html            ← portada con momento firma (constelación)
├── tokens.css            ← ÚNICA fuente de tokens (--nz-*)
├── packs/
│   ├── p0-catalog.css    ← shell compartido del catálogo (wow: vías 2-5)
│   └── p1..p12-*.css     ← un pack por categoría de objetos
└── paginas/
    └── 01-layout.html    ← demo de categoría 01 (50 objetos vivos)
```

## Tokens clave (tokens.css)

- Azul: `--nz-blue-600: #2563eb` (brand) · Naranja: `--nz-orange-500: #f97316` (acento). **Nunca fundidos en gradiente.**
- Tema oscuro: bloque `[data-nz-theme="dark"]` que redefin SOLO tokens temáticos (bg/surface/border/text/brand/accent/soft/shadows/focus-ring). Fondo `#0b1220`, brand `#4f8ef7`.
- Sombras multicapa: `--nz-shadow-sm: 0 1px 2px ..., 0 2px 6px ...` hasta `--nz-shadow-xl`. Sin bordes duros para separar.
- Movimiento: `--nz-ease-out: cubic-bezier(0.16, 1, 0.3, 1)` (expo-out, entradas) · `--nz-ease-in: cubic-bezier(0.7, 0, 0.84, 0)` (salidas, más cortas).
- `prefers-reduced-motion`: congelar (duración 0.01ms), no ralentizar.

## Shell del catálogo (clases p0-catalog.css)

- `.cat-brandmark` — logo de dos puntos (azul + naranja solapados).
- `.cat-pagehead` — cabecera display con eyebrow en mayúsculas azules y `em` naranja en el H1.
- `.cat-demo` — tarjeta demo con hover: `translateY(-3px)` + sombra sube de `--nz-shadow-sm` a `--nz-shadow-lg`.
- `.cat-demo__num` — numeración del objeto en naranja (el acento marca el índice).
- `.cat-cat--wide` — UNA celda doble de ancho en el grid de categorías (jerarquía); el resto "en obra" con opacity .55.
- `.nz-in` — entrada escalonada: `animation: nzIn .3s var(--ease-out) backwards; animation-delay: var(--d)`.
- `.nz-btn--primary/--accent/--ghost` — 44px, pill, hover translateY(-2px), shadow-brand/accent.
- `.live-*` — señales de vida: switch funcional, progreso con scaleX animado, contador con rAF + expo-out.

## Constelación (momento firma) — receta JS

```js
// Canvas fijo inset:0, z-index:0, pointer-events:none; contenido en DOM z-index:1.
// DPR ≤ 2 · pausa en visibilitychange · resize re-seed · reduced-motion → un solo frame.
seed(): n = W < 640 ? 42 : 90 puntos; v ±0.35; r 1.2–2.5; alpha 0.18–0.58; 8% "spark" (naranjas).
Líneas: para cada par con dist < 110 → strokeStyle rgba(line, (1 - d/110) * 0.16).
Paleta LEÍDA POR FRAME (reacciona al toggle sin recargar):
  light: dot "37,99,235"  line "37,99,235"  spark "249,115,22"
  dark:  dot "125,165,255" line "79,142,247" spark "251,146,60"
Explosión al clic (window pointerdown): 18 partículas; v = 1.5 + rnd*3.2;
  vy -= 1 (impulso arriba); gravedad +0.12/frame; decay 0.985; vida 40–65 frames;
  30% naranjas; radio 1.6 + (life/60)*1.4; alpha = life/60.
```

## QA que debe pasar antes de entregar

1. Sin gradientes · sin glass/backdrop-filter · sin orbs · sin bordes decorativos.
2. Sin hex hardcodeados en HTML — todo `var(--nz-*)`.
3. Dos pantallas NO intercambiables (jerarquía presente).
4. Reduced-motion → fotograma estático legible (canvas renderizado una vez, no vacío).
5. Dark toggle reacciona también en el canvas (paleta por frame).
6. Touch targets 44px · castellano · footer `Hecho con ❤️ por David Antizar`.
