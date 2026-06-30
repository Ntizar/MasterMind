# write_file Content Corruption Pattern

## Caso de estudio: ContrataPúblico (2026-06-16)

### Contexto
Proyecto SPA vanilla HTML con inline JavaScript (2 bloques `<script>` en `index.html`):
- Script 0: `_contractTypes` array con 8 objetos de tipos de contrato (datos JSON-like con strings largos)
- Script 1: `switchTab()`, `renderMapa()`, todas las funciones core de renderizado

### Operación que causó la corrupción
1. `read_file(path="index.html")` dentro de `execute_code` → devuelve contenido con prefijos `N|`
2. Procesamiento para extraer CSS a archivo separado
3. `write_file(path="index.html", content=content)` para escribir el HTML resultante
4. **Resultado:** El contenido JS inline se corrompió (strings truncados, caracteres UTF-8 mangled)

### Síntomas
- `node --check` del script inline extraído: `SyntaxError: Invalid or unexpected token` línea 23
- Navegador: 10 errores JS en consola, todas las funciones `undefined`
- `cat -A` mostraba bytes mojibake: `M-bM-^@M-^T`, `M-pM-^_M-^TM-^D`, `M-bM-^BM-,`
- Ubicación: datos `_contractTypes` alrededor de `regimen: "Administrati"` (truncado)

### Diferencia con el pitfall de prefijos `N|`
- **Prefijos `N|`:** `read_file` prependea números de línea → fácil de detectar y limpiar con regex
- **Corrupción de contenido:** `write_file` trunca o corrompe strings complejos dentro del JS → no visible hasta que se ejecuta el código

### Corrupción observada
El `_contractTypes` array contenía strings con:
- Comillas simples y dobles anidadas
- Caracteres especiales (—, –, emojis)
- Escape sequences (`\"`, `\\'`)
- Datos de régimen, tipo, descripción larga

Estos elementos, combinados con el manejo de `read_file`/`write_file` dentro de `execute_code`, causaron truncamiento y corrupción.

### Recuperación
```bash
# Restaurar desde el último commit funcional
git log --oneline -5  # identificar commit limpio
git show 134c1e3:index.html > index.html  # restaurar
git add index.html && git commit -m "Fix: restore corrupted inline JS"
```

### Recuperación avanzada: merge desde git + reaplicar adiciones

Cuando el archivo corrupto tiene adiciones nuevas (módulos, funciones, CSS) que no existían en el commit funcional, NO basta con restaurar el commit antiguo. Patrón de merge:

```python
import subprocess, re

# 1. Obtener versión funcional desde git
good = subprocess.check_output(['git', 'show', 'COMMIT:index.html'], text=True)

# 2. Obtener versión corrupta actual
with open('index.html', 'r') as f:
    current = f.read()

# 3. Identificar qué se añadió (scripts CSS, módulos JS, etc.)
# Buscar tags que están en current pero no en good
new_tags = []
for tag_pattern in [r'<link[^>]*css/custom\.css[^>]*>', r'<script src="js/modules/[^"]*">',
                     r'<script src="js/app\.js">']:
    for m in re.finditer(tag_pattern, current):
        tag = m.group(0)
        if tag not in good:
            new_tags.append(tag)

# 4. Insertar tags nuevos en la versión buena
# Encontrar el punto de inserción (después del último script existente)
good = good.replace(
    '  <script src="js/modules/checklist-expediente.js"></script>',
    '  <script src="js/modules/checklist-expediente.js"></script>\n' + '\n'.join(new_tags)
)

# 5. Aplicar patches específicos (modal show/close, etc.)
good = good.replace("classList.add('active')", "show()")

# 6. Escribir resultado
with open('index.html', 'w') as f:
    f.write(good)
```

**Regla:** Siempre restaurar desde git primero, luego reaplicar adiciones una por una. Nunca intentar "arreglar" el contenido corrupto directamente — es más propenso a errores que empezar desde una base limpia.

### Prevención

1. **NUNCA** usar `write_file` para reescribir archivos completos que contengan JS/CSS complejo extraído de `read_file` dentro de `execute_code`
2. **Usar `patch`** con `old_string`/`new_string` para ediciones específicas sobre archivos con contenido complejo
3. **Si necesitas reescribir completamente:** usar `terminal` con `cat << 'EOF' > file` o `python3 -c "open(...).write(...)"` en vez de `write_file`
4. **Verificar después de cualquier escritura:**
   ```bash
   node --check archivo.js  # para JS
   python3 -c "c=open('file.html').read(); assert c.count('<script')==c.count('</script>')"  # para HTML
   ```
5. **Para extracción de CSS de HTML:** usar `terminal` con `sed` o `python3` directamente, no `read_file` → process → `write_file`

### Patrón seguro de extracción CSS
```python
# CORRECTO: usar terminal con python3 directamente
terminal("""python3 -c "
import re
html = open('index.html').read()
style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    css = style_match.group(1).strip()
    open('css/custom.css', 'w').write(css)
    html = html.replace('<style>' + style_match.group(0).split('<style>')[1], '')
    # ... rest of processing
    open('index.html', 'w').write(html)
" """)
```
