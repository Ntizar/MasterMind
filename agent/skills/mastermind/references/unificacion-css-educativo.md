# Unificación CSS para contenido educativo

Patrón para unificar el CSS de un curso educativo multi-nivel (Primaria → Carrera) **sin perder la personalidad visual de cada nivel**.

## Principio

Cada nivel educativo mantiene su CSS inline con su propia paleta de colores. NO se unifica en un CSS externo. La unificación se limita a **valores cosméticos** que no afectan a la identidad visual.

## Qué unificar (seguro)

| Propiedad | Valor unificado | Motivo |
|-----------|----------------|--------|
| `line-height` | `1.7` | Más legible que 1.6 |
| `max-width` del container | `850px` | Más aire que 800px |
| Fondo `.interactive` y `.exercise` | `#f1f5f9` | Más claro que `var(--gris)` (#94a3b8) |
| Bordes `.nav` y `.footer` | `#e2e8f0` | Más sutil que `var(--gris)` |
| `box-shadow` en cajas | `0 1px 3px rgba(0,0,0,.04)` | Sutil profundidad |
| Fondo del body | Degradado sutil `#f8faff → #fffaf5` | Toque de calidez |
| Variables `:root` | Las 13 comunes (`--azul`, `--naranja`, etc.) | Base compartida |

## Qué NO unificar (mantener por nivel)

- **Paleta de colores** — Cada nivel tiene su propio color primario (1º azul, 2º morado, 3º rosa, 4º amarillo, etc.)
- **Clases específicas** — Juegos de contar (`.num-btn`, `.counting-game`) solo en primaria; gráficos Plotly (`.chart-container`) solo en bachiller/carrera
- **Estructura de índices** — Los índices de nivel tienen glass effect y grid; las sesiones tienen cajas didácticas

## Cómo aplicar

```python
# Para cada archivo HTML del proyecto:
for fname in html_files:
    with open(fpath) as f:
        content = f.read()
    
    # 1. Normalizar variables :root
    # 2. Reemplazar fondos oscuros por claros
    content = content.replace(
        '.interactive{background:var(--gris);...}',
        '.interactive{background:#f1f5f9;...}'
    )
    # 3. Reemplazar bordes grises por sutiles
    content = content.replace(
        'border-top:1px solid var(--gris);border-bottom:1px solid var(--gris)}',
        'border-top:1px solid #e2e8f0;border-bottom:1px solid #e2e8f0}'
    )
    # 4. Unificar line-height y container width
    content = content.replace('line-height:1.6}', 'line-height:1.7}')
    content = content.replace('max-width:800px;', 'max-width:850px;')
    # 5. Añadir sombra sutil a cajas
    content = content.replace(
        '.box{padding:1rem 1.2rem;border-radius:8px;...}',
        '.box{padding:1rem 1.2rem;border-radius:10px;...;box-shadow:0 1px 3px rgba(0,0,0,.04)}'
    )
    # 6. Añadir fondo degradado al body
    content = content.replace(
        'background:var(--fondo);',
        'background:linear-gradient(135deg,#f8faff 0%,#fffaf5 100%);'
    )
```

## Verificación post-unificación

```bash
# 1. Sin enlaces rotos
grep -rn 'href="[^"]*\.html"' *.html | grep -v 'INDEX.html' | while read line; do
  target=$(echo "$line" | grep -oP 'href="\K[^"]+\.html')
  [ -f "$target" ] || echo "BROKEN: $line"
done

# 2. Atribución en todas las páginas
for f in *.html; do
  grep -q 'David Antizar\|❤️' "$f" || echo "NO ATTR: $f"
done

# 3. KaTeX en ESO/Bachiller/Carrera
for f in eso*.html s09-*.html s10-*.html; do
  grep -q 'katex' "$f" || echo "NO KATEX: $f"
done
```