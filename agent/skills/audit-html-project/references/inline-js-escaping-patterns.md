# Inline JS Escaping Patterns — Guía de Escaping en Scripts Inline vs Externos

## Problema central

Los `<script>` inline en HTML y los archivos `.js` externos tienen reglas de escaping DIFERENTES para el mismo código JavaScript. Mover código de uno a otro sin ajustar el escaping causa bugs silenciosos.

## Por qué son diferentes

En HTML inline, el navegador procesa el contenido en dos fases:
1. **HTML parser** lee el attribute value y el contenido del `<script>`
2. **JS parser** interpreta el JavaScript resultante

En un archivo `.js` externo, solo hay una fase:
1. **JS parser** interpreta el JavaScript directamente

Esto significa que `\\` en HTML inline (procesado por HTML parser primero) produce un resultado diferente que `\\` en un archivo .js standalone.

## Tabla de conversión: HTML inline → Archivo JS externo

| En HTML inline | En archivo .js | Output HTML resultante | Notas |
|---|---|---|---|
| `onclick="fn('' + id + '')"` | ❌ BROKEN | N/A | Primer `'` cierra el string JS |
| `onclick="fn(\\x27' + id + '\\x27)"` | `onclick="fn(\\x27' + id + '\\x27)"` | `onclick="fn('123')"` | `\x27` = hex escape para `'` |
| `html += '...\\'...` | `html += '...\\'...` | `...`...' | `\\'` = literal `\` + cierra string |
| `style="background=\\\\'rgba(...)"` | `style="background=\\'rgba(...)"` | `background='rgba(...)` | Reducir `\\\\` a `\\` |

## Patrón 1: onclick con comillas simples en output

### ❌ Roto (el patrón más común)
```javascript
// En HTML inline — el primer ' cierra el string JS
html += '<div onclick="showContractDetail('' + ct.id + '')">';
//                                                      ^^ estos rompen todo
```

### ✅ Correcto con \x27
```javascript
// Funciona tanto inline como externo
html += '<div onclick="showContractDetail(\\x27' + ct.id + '\\x27)">';
```

### ✅ Correcto con template literal (RECOMENDADO)
```javascript
// Usar backticks — las comillas simples son solo caracteres regulares
html += `<div onclick="showContractDetail('${ct.id}')">`;
```

### ✅ Correcto con concatenación explícita
```javascript
// Separar las comillas en tokens concatenados
html += '<div onclick="showContractDetail(' + "'" + ct.id + "'" + ')">';
```

## Patrón 2: onmouseover/onmouseout con comillas en CSS

### ❌ Roto al extraer a archivo externo
```javascript
// En HTML inline: \\\\' = 4 backslashes en archivo
onmouseover="this.style.background=\\\\'rgba(26,82,118,0.08)\\\\'"
// En archivo .js standalone: \\\\ = 2 backslashes literales + ' cierra string
```

### ✅ Correcto con template literal
```javascript
onmouseover="this.style.background='rgba(26,82,118,0.08)'"
```

### ✅ Correcto con \x27
```javascript
onmouseover="this.style.background=\\x27rgba(26,82,118,0.08)\\x27"
```

## Patrón 3: onclick que llama a función con argumento string

### ❌ Roto
```javascript
html += '<a onclick="verArticulo(\\\\'' + art.numero + '\\\\')">';
```

### ✅ Correcto
```javascript
html += `<a onclick="verArticulo('${art.numero}')">`;
```

## Flujo de trabajo: extraer inline scripts a archivos externos

Cuando necesites mover `<script>` inline a `<script src="...">`:

### Paso 1: Extraer el contenido
```python
import re
with open('index.html') as f:
    html = f.read()

scripts = []
for m in re.finditer(r'<script>((?:(?!</script>).)+)</script>', html, re.DOTALL):
    content = m.group(1).strip()
    if len(content) > 100:  # solo scripts con contenido real
        scripts.append(content)
```

### Paso 2: NO usar node --check para validar
`node --check` no puede validar scripts que usan escaping de HTML inline — dará falsos positivos. En su lugar, validaaaa en el navegador:
```bash
# En vez de:
node --check extracted.js  # ❌ Puede fallar con escaping HTML válido

# Usar:
# 1. Añadir <script src="extracted.js"></script> al HTML
# 2. Abrir en navegador
# 3. Verificar en consola que las funciones existen
```

### Paso 3: Reescribir escaping
Buscar y reemplazar estos patrones:
```python
# Patrón 1: comillas simples en onclick
content = content.replace("fn('' + ", "fn(\\x27' + ")
content = content.replace(" + '')\"", " + '\\x27)\"")

# Patrón 2: backslashes antes de comillas en atributos HTML
content = re.sub(r"=\\\\+'", "='", content)  # \\\\' -> '
content = re.sub(r"=\\\\+\\'", "='", content)  # \\\\\\' -> '

# O mejor: convertir a template literals (ver patrón 4)
```

### Paso 4 (RECOMENDADO): Convertir a template literals
```python
# Para cada línea que construye HTML con onclick:
# Cambiar delimitador de ' a ` y eliminar escaping de '
lines = content.split('\n')
fixed = []
for line in lines:
    if 'html +=' in line and ('onclick=' in line or 'onmouseover=' in line):
        # Cambiar ' a ` como delimitador del string
        line = re.sub(r"^(\s*html \+= )'", r"\1`", line, count=1)
        line = re.sub(r"';\s*$", "`;", line)
        # Eliminar backslashes antes de comillas (ya no son necesarios en template literals)
        line = line.replace("\\'", "'")
    fixed.append(line)
content = '\n'.join(fixed)
```

### Paso 5: Verificar en navegador
```javascript
// En la consola del navegador:
typeof switchTab  // debería ser "function"
typeof renderMapa  // debería ser "function"
// Clickear cada pestaña y verificar que funciona
```

## Caso de estudio: ContrataPúblico (2026-06-16)

### Situación
- 2 scripts inline en `index.html` (9,631 y 18,088 chars)
- Script 0: `_contractTypes` array + `renderTiposContrato()` + `showContractDetail()`
- Script 1: `switchTab()`, `renderMapa()`, `renderTextoCompleto()`, toast system, DOMContentLoaded
- El patrón `''` en onclick handlers estaba roto DESDE LA CREACIÓN del proyecto
- `node --check` reportaba `SyntaxError: Unexpected string` pero se atribuyó a "corrupción de write_file"
- La corrupción real era pre-existente: el escaping nunca fue correcto

### Error original
```javascript
// Línea 581 del HTML original:
html += '<div ... onclick="showContractDetail('' + ct.id + '')">';
//                                                      ^^ siempre estuvo mal
```

### Corrección aplicada
```javascript
// Template literal (lo que se aplicó):
html += `<div ... onclick="showContractDetail('${ct.id}')">`;
```

### Lecciones
1. `node --check` falla en scripts inline con escaping HTML válido — no es un indicador fiable
2. El bug existía desde la primera sesión del proyecto — nunca fue "corrompido" por write_file
3. La solución correcta es template literals, no intentar arreglar el escaping con backslashes
4. Al extraer a archivo externo, el bug se vuelve más visible (node --check lo detecta)

## Prevención

1. **Siempre usar template literals** para strings que construyen HTML con atributos que contienen JS
2. **Nunca usar `''` vacío** para comillas simples en output — usar `\x27` o template literals
3. **Antes de extraer scripts inline**, verificar que el escaping funciona en contexto standalone
4. **Usar `browser_console`** para verificar que las funciones existen después de cualquier cambio
