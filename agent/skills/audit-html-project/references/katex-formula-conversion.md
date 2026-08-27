# Fórmulas KaTeX — Patrones de Conversión

## Problema Común

Las fórmulas matemáticas se generan como texto plano en lugar de formato KaTeX:
- `R²` en vez de `$R^2$`
- `{(1,0), (0,1)}` en vez de `$\{(1,0), (0,1)\}$`
- `∈` en vez de `$\in$`

El CDN de KaTeX puede estar cargado correctamente, pero las fórmulas no se renderizan porque carecen de delimitadores `$`.

## Patrones de Conversión

### Espacios vectoriales
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `R²` | `$R^2$` |
| `R³` | `$R^3$` |
| `R^n` | `$R^n$` |
| `{(1,0), (0,1)}` | `$\{(1,0), (0,1)\}$` |
| `{v₁, v₂, v₃}` | `$\{v_1, v_2, v_3\}$` |

### Símbolos matemáticos
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `∈` | `$\in$` |
| `∉` | `$\notin$` |
| `≤` | `$\leq$` |
| `≥` | `$\geq$` |
| `≠` | `$\neq$` |
| `±` | `$\pm$` |
| `∞` | `$\infty$` |
| `∑` | `$\sum$` |
| `∫` | `$\int$` |
| `∂` | `$\partial$` |
| `∇` | `$\nabla$` |
| `→` (vector) | `$\vec{v}$` o `$\overrightarrow{AB}$` |

### Límites y cálculo
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `lim(x→∞)` | `$\lim_{x \to \infty}$` |
| `f'(x)` | `$f'(x)$` o `$\frac{df}{dx}$` |
| `∫₀¹ f(x)dx` | `$\int_0^1 f(x)dx$` |

### Raíces cuadradas
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `√240` | `$\sqrt{240}$` |
| `√n` | `$\sqrt{n}$` |
| `√(a+b)` | `$\sqrt{a+b}$` |
| `√s` | `$\sqrt{s}$` |

### Subscripts unicode
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `x₀` | `$x_0$` |
| `x₁` | `$x_1$` |
| `z₀.₀₅` | `$z_{0.05}$` |
| `t₀.₀₂₅,₂₄` | `$t_{0.025,24}$` |
| `g₁₀` | `$g_{10}$` |
| `l₁` | `$l_1$` |

### Operadores de comparación en contexto
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `π ≈ 3.14` | `$\pi \approx 3.14$` |
| `10 ≠ 9` | `$10 \neq 9$` |
| `P(X ≤ 1)` | `$P(X \leq 1)$` |
| `P(X ≥ 28)` | `$P(X \geq 28)$` |

### Símbolos ± en contexto
| Texto plano | KaTeX correcto |
|-------------|----------------|
| `10.2 ± 0.124` | `$10.2 \pm 0.124$` |
| `margen de ±0.1 mm` | `margen de $\pm 0.1$ mm` |

## Verificación Rápida

```python
import re

def check_katex_formulas(content):
    """Check for plain text math that should be in KaTeX"""
    issues = []
    
    # R²/R³ outside of $
    for match in re.finditer(r'(?<!\$)R[²³](?!\$)', content):
        issues.append(f'R²/R³ sin delimitador: position {match.start()}')
    
    # Sets outside of $
    for match in re.finditer(r'\{[^}]{5,}\}', content):
        if '$' not in content[max(0,match.start()-10):match.end()+10]:
            if not any(x in content[match.start()-50:match.start()] 
                      for x in ['class=', 'id=', 'style=']):
                issues.append(f'Conjunto sin delimitador: {match.group()[:30]}...')
    
    return issues
```

## Ejemplo de Corrección

**Antes (roto):**
```html
<h3>Bases en R²: {(1,0), (0,1)} vs {(1,1), (1,-1)}</h3>
```

**Después (funciona):**
```html
<h3>Bases en $R^2$: $\{(1,0), (0,1)\}$ vs $\{(1,1), (1,-1)\}$</h3>
```

## Notes

- Los `{` y `}` en LaTeX DEBEN ser escapados como `\\{` y `\\}`
- KaTeX auto-render solo procesa texto dentro de `$...$` o `$$...$$`
- El script `renderMathInElement` necesita configuración de delimiters
- No convertir `{` y `}` que son parte de HTML (clases, IDs, estilos)
- **NO convertir dentro de `<script>` tags** — Los símbolos unicode en código JavaScript (títulos de gráficos Plotly, strings de UI) son correctos como están. Por ejemplo, `'Bases en R²'` como título de Plotly es válido. Solo convertir en contenido HTML visible.
- **Estrategia de conversión segura:** Dividir el contenido por `<script>...<\/script>` y solo procesar las partes que NO están dentro de scripts. Usar `re.split(r'(<script[^>]*>.*?</script>)', content, flags=re.S)` y aplicar conversiones solo a partes impares (HTML).

## Patrón de Corrección Batch

```python
import re

def fix_formulas_in_file(filepath):
    """Fix math formulas in HTML content (not in <script> tags)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into HTML and script parts
    parts = re.split(r'(<script(?:\s[^>]*)?>.*?</script>)', content, flags=re.S)
    
    fixed_parts = []
    for part in parts:
        if part.startswith('<script'):
            fixed_parts.append(part)  # Don't touch scripts
            continue
        
        # √ followed by expression
        part = re.sub(r'√(\d+)', r'$\\sqrt{\1}$', part)
        part = re.sub(r'√\(([^)]+)\)', r'$\\sqrt{\\1}$', part)
        part = re.sub(r'√([a-zA-Z])', r'$\\sqrt{\1}$', part)
        
        # R² R³ R⁴
        part = part.replace('R²', '$R^2$')
        part = part.replace('R³', '$R^3$')
        
        # Unicode subscripts
        sub_map = {'₀':'_0','₁':'_1','₂':'_2','₃':'_3','₄':'_4',
                   '₅':'_5','₆':'_6','₇':'_7','₈':'_8','₉':'_9'}
        def repl(m):
            letter = m.group(1)
            subs = ''.join(sub_map.get(c, c) for c in m.group(2))
            return f'${letter}{subs}$'
        part = re.sub(r'([a-zA-Z])([₀₁₂₃₄₅₆₇₈₉]+)', repl, part)
        
        # ± → $\pm$
        part = part.replace('±', '$\\pm$')
        
        # Comparison operators (split by $ to avoid double-wrapping)
        op_map = {'≤':'\\leq','≥':'\\geq','≠':'\\neq','≈':'\\approx','∞':'\\infty'}
        dollar_parts = part.split('$')
        new_parts = []
        for i, dp in enumerate(dollar_parts):
            if i % 2 == 0:  # Outside KaTeX
                for uni, tex in op_map.items():
                    dp = dp.replace(uni, f'${tex}$')
            new_parts.append(dp)
        part = '$'.join(new_parts)
        
        fixed_parts.append(part)
    
    result = ''.join(fixed_parts)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
```
