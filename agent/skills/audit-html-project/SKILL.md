---
name: audit-html-project
description: "Procedimiento sistemático para auditar proyectos HTML masivos: detectar errores de navegación rota, atribuciones incorrectas, páginas huérfanas, inconsistencias de diseño y consistencia de contenido. Incluye formato de salida estructurado con severidades."
version: 2.2.0
author: Hermes Agent
tags: [html, audit, quality, static-site, education]
---

# Audit HTML Project — Auditoría Sistemática de Proyectos HTML

Procedimiento para auditar proyectos HTML grandes (10+ archivos) de forma sistemática y eficiente.

## Cuándo usar

- Proyecto HTML con 10+ archivos y el usuario reporta errores
- Antes de hacer commit/push a un repositorio de contenido educativo
- Cuando se genera contenido HTML masivamente y se necesita QA
- Cuando un sitio estático muestra errores de navegación
- **SPA con backend (Express + Chart.js + Three.js)** — auditoría de endpoints, sync de datos, responsive de componentes JS, estado de DB

## Pasos

### 1. Inventario del proyecto

```python
import os
base = "/path/to/project"
html_files = [f for f in os.listdir(base) if f.endswith('.html')]
# Clasificar por tipo: páginas de contenido, páginas índice, archivos de navegación
```

### 2. Detección de errores sistemáticos

Escanear cada archivo por estos problemas:

**Críticos (❌):**
- Sin atribución correcta (`David Antizar` + `❤️`)
- Navegación rota: `href="#">` con texto "Anterior" o "Siguiente"
- Enlaces rotos internos: referencias a archivos que no existen

**Advertencias (⚠️):**
- Sin ejercicios interactivos (en contenido educativo)
- Sin resumen final
- Sin sección de teoría
- Sin ejemplos
- Sin caja de error frecuente o idea clave
- Sin barra de progreso
- Contenido inexistente (páginas de volumen vacías)

### 3. Clasificar por severidad

1. **Bloqueantes** — navegación rota, enlaces rotos, contenido inexistente
2. **Importantes** — atribuciones incorrectas, sin resumen
3. **Mejora** — sin ejercicios, sin ejemplos

### 4. Estrategia de escaneo para proyectos grandes (30+ archivos)

Para proyectos con 30+ archivos HTML, **NO usar `read_file` por cada archivo** — es lento y consume el límite de tool calls. Usar `grep` vía terminal para el escaneo inicial:

```bash
# Escaneo masivo de atribución
grep -c 'David Antizar' *.html | grep ':0$'

# Escaneo de KaTeX
grep -c 'katex' *.html | grep ':0$'

# Enlaces a archivos que no existen
for f in *.html; do
  grep -oP 'href="[^"]*\.html"' "$f" | while read -r href; do
    target=$(echo "$href" | sed 's/href="//;s/"//')
    [ ! -f "$target" ] && echo "ROTO: $f → $target"
  done
done
```

Luego, para las fases de corrección y verificación profunda, usar `execute_code` con Python y un solo script que procese todos los archivos.

### 5. Corrección en lotes

Usar `execute_code` con Python para batch-fix:

```python
from hermes_tools import read_file, write_file, patch
import os

base = "/path/to/project"
html_files = sorted([f for f in os.listdir(base) if f.endswith('.html')])
all_set = set(html_files)

# Ejemplo: corregir todas las atribuciones
files = ['s09-3-bachiller.html', 's10-1-carrera.html', ...]
for f in files:
    content = read_file(path=os.path.join(base, f)).get('content', '')
    content = content.replace("corazón", "❤️")
    write_file(path=os.path.join(base, f), content=content)
```

#### 5.1 Añadir CDN faltante (KaTeX, Plotly.js, etc.)

Para proyectos educativos con contenido matemático, verificar si KaTeX está presente y añadirlo si falta:

```python
katex_cdn = '''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{delimiters:[{left:'\\\\[',right:'\\\\]',display:true},{left:'\\\\\\(',right:'\\\\)',display:false}]})"></script>'''

for fname in archivos_sin_katex:
    content = read_file(path=join(base, fname)).get('content', '')
    new_content = content.replace('</title>', f'</title>\n{katex_cdn}', 1)
    write_file(path=join(base, fname), content=new_content)
```

**Regla:** KaTeX SOLO para niveles donde haya fórmulas (ESO, Bachiller, Universidad). Primaria usa emojis y texto plano — no necesita KaTeX.

#### 5.2 Crear índices de nivel faltantes

Cuando un nivel (ej: 1º Primaria) carece de índice, y otros niveles (4º+) sí tienen, crear el índice replicando el diseño visual y estructural de los existentes:

```python
# 1. Identificar un índice de referencia (ej: s04-4primaria.html)
# 2. Extraer su estructura: header, grid de tarjetas, colores, footer
# 3. Mapear las sesiones reales del nivel
# 4. Generar el nuevo índice con ese mismo diseño
```

El nuevo índice debe incluir:
- Header con título y descripción del nivel
- Grid de tarjetas, UNA por sesión, con: título, descripción corta, tag/tema
- Cada tarjeta enlaza a su sesión correspondiente
- Footer con atribución y enlace "Volver al índice general"
- Misma paleta de colores y glassmorphism que los índices existentes

**Regla:** NO reutilizar nombres de archivo existentes. Si `s01-1primaria.html` ya existe y es una sesión, crear `s01-1primaria-index.html` como índice.

### 6. Verificación post-corrección

Re-ejecutar el escáner para confirmar que todos los errores se resolvieron. Usar un script de verificación único que cubra **8 checks**:

```python
print('1. ENLACES ROTOS:')    # 0 = perfecto
print('2. ATRIBUCION:')       # 0 = perfecto
print('3. KATEX:')            # 0 en niveles que lo necesitan
print('4. NUEVOS INDICES:')   # existen los que creamos
print('5. INDEX.HTML ENLACES:')  # apuntan a los nuevos índices
print('6. ENLACES CORREGIDOS:')  # los targets rotos ya no aparecen
print('7. CONEXION CADENAS:')    # cadenas paralelas conectadas
print('8. INDEX.HTML ATRIBUCION:') # tiene footer
```

## Formato de salida (preferido por el usuario)

El usuario pide auditorías "estrictas y críticas" que "expliquen todo bien". Usar este formato:

```markdown
# 🔍 AUDITORÍA COMPLETA — [Nombre del Proyecto]

**Proyecto:** [Descripción]
**Archivos HTML:** [N]

---

## 📊 RESUMEN EJECUTIVO

| Severidad | Encontrados | Estado |
|-----------|------------|--------|
| ❌ **Críticos** | N | [resumen] |
| ⚠️ **Importantes** | N | [resumen] |
| 💡 **Mejoras** | N | [resumen] |

---

## ❌ ERRORES CRÍTICOS

### 1. [Descripción del error]
[Tabla con archivos afectados y detalle del error]

**Impacto:** [Qué le pasa al usuario/alumno]

---

## ⚠️ PROBLEMAS IMPORTANTES

[Similar formato]

---

## 💡 MEJORAS SUGERIDAS

[Similar formato]

---

## ✅ LO QUE FUNCIONA BIEN

[Bullet points positivos]

---

## 📋 PLAN DE CORRECCIÓN

Si quieres que arregle todo, el orden sería:
1. **Fase 1 (Crítico):** [Acción]
2. **Fase 2 (Crítico):** [Acción]
...
```

**Regla:** SIEMPRE terminar con "¿Quieres que empiece a corregir?" — el usuario quiere acción, no solo diagnóstico.

## Reglas

- **NUNCA modificar la estructura de navegación** de sesiones individuales (eso es responsabilidad del generador)
- **Las páginas de volumen** (nivel educativo completo) deben ser índices funcionales con: título, descripción, lista de sesiones con enlaces, objetivos de aprendizaje y resumen
- **El INDEX.html** debe reflejar correctamente el contenido real (niveles, etiquetas, descripciones)
- **Siempre verificar** que los archivos referenciados existen antes de corregir enlaces
- **Commit y push** tras las correcciones
- **RITMO: no parar entre pasos** — El usuario frustración = "¿por qué has parado?". Flujo: terminar un fix → siguiente inmediatamente. Mostrar progreso en vivo, no esperar a tener todo perfecto para comunicar. Si hay 3+ fixes, hacerlos secuencialmente sin preguntar entre cada uno.

## Flujo post-auditoría: fix → generate → deploy

Cuando el usuario pide "arreglar y completar" tras una auditoría, el flujo natural es:

1. **Fix crítico** → corregir enlaces rotos, atribuciones, navegación (usar `execute_code` + `patch` para fixes simples, `write_file` para HTML completo)
2. **Fix importante** → actualizar trackers (progress.json, README, etc.) — **⚠️ NO usar `read_file` para JSON** (prependea números de línea), usar `terminal("cat ...")` + `json.loads()`
3. **Generar contenido faltante** → cargar skill del dominio, generar HTML con template, verificar calidad (>12KB, SVG, ejercicios)
4. **Actualizar índice** → INDEX.html con todos los temas
5. **Deploy** → git push (Pages se activa automático si repo es público)

### Cada fase → commit separado
- `🔧 Fix: <descripción>` para correcciones
- `📝 <bloque>: <temas generados>` para contenido nuevo
- `INDEX: actualizado con N temas` para actualización del índice

## Pitfalls

- **🔴 CSS CON DOBLES LLAVES `{{}}` DE TEMPLATE ENGINE** — Algunos archivos HTML generados por scripts Python/Jinja pueden contener `{{` y `}}` en lugar de `{` y `}` en bloques `<style>`. Esto rompe TODOS los estilos CSS del archivo. **Detección:** `grep -n '{{' *.html` dentro de bloques `<style>`. **Corrección:** reemplazar `{{` → `{` y `}}` → `}` SOLO dentro de `<style>` tags (nunca en HTML content). **Prioridad:** ❌ Crítico — el archivo se ve sin estilos. Ver `references/css-double-braces-fix.md` para patrón de corrección batch.
- **🔴 PREFIJOS DE LÍNEA `N|` EN HTML** — Archivos HTML contienen prefijos tipo `1|`, `     2|` al inicio de cada línea. Causa CSS destruido + texto basura visible. Origen: output de tools de visualización de código guardado como archivo real. **Detección:** `grep -rlP '^\s*\d+\|' *.html`. **Corrección:** `re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)`. **Trampa:** `read_file` de Hermes SIEMPRE prependea `N|` — no confundir con corrupción real. Usar `terminal("head -5 file")` para verificar contenido real. Ver `references/line-number-prefix-corruption.md`.
- **🔴 NÚMEROS DE LÍNEA INCORPORADOS EN HTML (`N|` PREFIX)** — Archivos HTML pueden contener prefijos tipo `52|` o `     3|` al inicio de cada línea. Causa: una herramienta escribe el output de `read_file()` (que prependea números de línea) de vuelta al archivo. **Síntomas:** números como texto visible en la página, CSS roto (números dentro de `<style>`), contenido renderizado con basura. **Detección:** `grep -cP '^\s*\d+\|' *.html | grep -:0$` — si algún archivo tiene matches, está corrompido. **Corrección:** `re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)` para eliminar todos los prefijos. **Prioridad:** ❌ Crítico — el archivo se ve completamente roto. Ver `references/line-number-corruption-fix.md` para patrón de detección y corrección.
- **🔴 `write_file` DOBLE-ESCAPA BACKSLASHES EN REGEX** — Cuando `write_file` escribe código que contiene patrones regex como `new RegExp('[\\s\\S]*?')` o `/\\d+/g`, el tool puede duplicar los backslashes (escritura: `[\\s\\S]` → archivo: `[\\\\s\\\\S]`). El regex queda roto silenciosamente — el código pasa `node --check` pero no funciona en runtime. **Detección:** `grep -n '\\\\\\\\' file.js` — si hay resultados sospechosos, hay doble-escape. **Prevención:** Usar `indexOf`/`substring` en vez de regex para patrones simples (limpiar tags, extraer JSON). Si se necesita regex, verificar el contenido real con `cat -n file | grep 'pattern'` tras escribir. **Trampa:** `read_file` de Hermes también puede mostrar doble-escape — usar `terminal("cat -n file")` para verificar el contenido real del archivo. Ver `pdf-to-landing/references/server-2-endpoint-pattern.md` para ejemplo completo.
- **🔴 `write_file` CORROMPE CONTENIDO COMPLEJO (NO solo prefijos de línea)** — Cuando se usa `read_file` dentro de `execute_code` para leer HTML/JS y luego `write_file` para escribir de vuelta (incluso después de procesar), el contenido puede corromperse: strings truncados, secuencias de escape rotas, caracteres UTF-8 mangled. Esto ES DIFERENTE al pitfall de prefijos `N|` — aquí el problema es que `write_file` dentro de `execute_code` puede truncar o corromper datos dentro de strings JavaScript complejos (arrays de objetos, datos con caracteres especiales). **Síntomas:** `SyntaxError: Invalid or unexpected token` en Node.js, navegador no ejecuta inline scripts, datos de referencia (como `_contractTypes`) truncados. **Detección:** `node --check` falla. **Corrección:** Restaurar desde el último commit funcional (`git show COMMIT:index.html`). **Prevención:** NUNCA usar `write_file` para reescribir archivos completos con contenido JS/CSS complejo extraído de `read_file` dentro de `execute_code`. Usar `patch` con `old_string`/`new_string` para ediciones específicas. Ver `references/write-file-corruption-pattern.md` para el caso completo.
- **🔴 BATCH FIX SOBRESCRIBE CORRECCIONES ANTERIORES** — Si haces múltiples fases de corrección (ej: Fase 2 añade transiciones, Fase 5 reconstruye navegación), la Fase 5 puede sobrescribir lo que hiciste en Fase 2. **SOLUCIÓN:** Al hacer batch-fix de navegación, PRESERVAR los enlaces de transición entre niveles que ya existían. Marcarlos antes del batch y re-insertarlos después. Verificar con test específico post-fix.
- **🔴 FÓRMULAS KATEX COMO TEXTO PLANO** — Las fórmulas pueden estar escritas como texto (`R²`, `{(1,0), (0,1)}`) en lugar de KaTeX (`$R^2$`, `$\\{(1,0), (0,1)\\}$`). El CDN de KaTeX puede estar cargado pero las fórmulas no se renderizan porque no tienen delimitadores `$`. **SIEMPRE** verificar: (1) KaTeX CDN presente, (2) script auto-render con delimiters, (3) fórmulas envueltas en `$...$` o `$$...$$`. Detectar con: `re.findall(r'(?<!\\$)R[²³](?!\\$)', content)`.
- **🔴 Plotly/KaTeX en contexto de ejecución equivocado** — El código JavaScript puede terminar en ubicaciones que impiden su ejecución: (1) dentro de `<script src="...">` (el navegador ignora el inline content), (2) flotante sin tag `<script>`, (3) en un `<script>` separado que ejecuta ANTES de DOMContentLoaded (el div aún no existe). **SIEMPRE** verificar: Plotly.newPlot y renderMathInElement deben estar dentro de un handler `DOMContentLoaded`. Ver `references/plotly-chart-verification.md` para patrones de detección y corrección.
- **🔴 CONVERSIÓN KATEX: SOLO en HTML, NO en scripts** — Al convertir símbolos unicode a KaTeX, los símbolos dentro de `<script>` tags son código JavaScript válido (títulos de gráficos, strings). Convertirlos rompe el JS. **Patrón seguro:** Dividir contenido por tags `<script>`, procesar solo partes HTML. Ver `references/katex-formula-conversion.md` para el script de corrección batch.
- **GitHub Pages case sensitivity** — `INDEX.html` no se sirve como raíz, necesita `index.html`
- **🔴 Navegación Siguiente → #** — patrón común en contenido generado automáticamente
- **🔴 Atribución con emoji corrupto** — "corazón" en texto plano en vez de `❤️`
- **🔴 Páginas de volumen como índices** — no confundir con sesiones individuales; son páginas de navegación entre sesiones
- **🔴 Archivo nombrado como índice pero que es sesión** — `s01-1primaria.html` puede sonar a "índice de 1º Primaria" pero ser en realidad una sesión individual. Verificar siempre contando enlaces a otras sesiones (< 3 = es sesión, no índice).
- **🔴 Dos cadenas paralelas sin conexión** — un nivel puede tener archivos `sXX-YYprimaria.html` (sesiones resumen) Y archivos `sXX-YY-tema.html` (sesiones detalladas) sin que ninguna enlace a la otra. Los alumnos que entren por una cadena nunca verán la otra.
- **🔴 Transición entre niveles rota por naming inconsistente** — `s02-7primaria.html` (última de 2º) puede enlazar a `s03-1primaria.html` que no existe porque el índice real de 3º se llama `s03-3primaria.html`. El naming numérico no es fiable entre niveles.
- **🔴 KaTeX version pinning** — usar siempre una versión concreta (`@0.16.9`), nunca `@latest`, para evitar roturas por cambios en CDN.
- **🔴 CDN en índices de nivel** — los índices (ej: `s09-bachiller.html`) no tienen fórmulas, pero es buena práctica añadir KaTeX para que cualquier preview/snippet de sesión se renderice bien.
- **🔴 ORDEN ALFABÉTICO vs NUMÉRICO rompe navegación** — `sorted()` pone `s01-10` ANTES de `s01-2` (porque "1" < "2"). Si se genera navegación con orden alfabético, TODOS los enlaces Anterior/Siguiente apuntan al archivo incorrecto. **SIEMPRE** usar sorting numérico explícito: `sorted(files, key=lambda x: int(re.match(r's\\d+-(\\d+)', x).group(1)))`. Verificar con prueba: ¿`s01-10` viene después de `s01-9`?
- **🔴 Navegación rota sistemáticamente → reconstruir, no parchear** — Si la mayoría de enlaces de navegación apuntan a archivos incorrectos (ej: 73/73 sesiones con links rotos), NO intentar corregir uno por uno. En su lugar: (1) construir mapa de navegación correcto con orden numérico, (2) usar `execute_code` para batch-reemplazar todas las secciones `<div class="nav">` de una vez. Más eficiente y menos propenso a errores.
- **🔴 REGEX TRAP: extraer navegación de `<div class="nav">` completo** — No usar regex parciales como `r'(?:Anterior|Siguiente).*?href="([^"]+\\.html)"'` para identificar qué enlace es Anterior y cuál es Siguiente. El orden de `<a>` dentro del div puede no coincidir con el orden textual, y el texto "Anterior" puede aparecer DESPUÉS del href en algunos generadores. **SOLUCIÓN:** Extraer el bloque completo `<div class="nav">...</div>` y analizarlo: el primer `<a>` con `←` es Anterior, el segundo con `→` es Siguiente. Patrón seguro: `r'<div class="nav">\\s*<a href="([^"]+)".*?</a>\\s*<a href="([^"]+)".*?</a>\\s*</div>'` y luego verificar con `←`/`→` qué es cuál. Ver `references/navegacion-nav-div-extraction.md`.
- **🔴 NOMBRES DE ARCHIVO INCORRECTOS EN NAVEGACIÓN** — Un generador puede crear enlaces con nombres de archivo que NO coinciden con los archivos reales. Ejemplo: `b03-05-piezas-caballera.html` en vez de `b03-05-perspectivas-piezas.html`. Esto es más sutil que `href="#"` porque el enlace está bien formado pero apunta al archivo equivocado. **SOLUCIÓN:** Escanear TODOS los `href="*.html"` y verificar que cada target existe como archivo físico. No confiar en que "suena bien" — verificar con `os.path.exists()`.
- **🔴 NOMBRES DE ARCHIVO EN progress.json ≠ archivos reales**: El tracker puede referenciar `b06-04-reglas-acotacion-iso-129.html` pero el archivo real se llama `b06-04-reglas-acotacion.html`. **SOLUCIÓN:** Antes de cualquier operación, verificar `os.path.exists()` para cada archivo referenced en progress.json. Si hay discrepancia, corregir inmediatamente.
- **🔴 LÍNEAS CORROMPIDAS POR MERGE/PATCH** — Cuando se aplica un `patch` o se resuelve un merge conflict sobre un archivo HTML grande con inline JS, dos líneas pueden fusionarse en una sola. Patrones reconocibles: (1) `const         // ===== SECTION =====` — un `const` suelto antes de un comentario, (2) `});getElementById('xxx');` — cierre de callback pegado a nueva declaración, (3) `// ===== NAME =====getElementById('xxx');` — comentario pegado a código. **Detección:** `grep -n "// ====.*[a-zA-Z]('". index.html` y `grep -n "const.*// ====" index.html`. **Corrección:** Restaurar línea desde commit anterior con `git show HEAD~1:index.html`. **Prevención:** Verificar con `vm.Script` después de cada patch/merge. **Decisión revert vs fix:** Si el diff de brace balance entre versiones es ≥ 2 y >5 líneas afectadas, revert es más seguro que fix manual. Ver `references/inline-js-syntax-validation.md` para técnicas completas de diagnóstico (vm.Script, brace balance comparison, binary search).
- **🔴 INLINE JS ESCAPING EN ONCLICK HANDLERS** — Los `<script>` inline en HTML usan comillas simples `'` para strings JS, pero los atributos `onclick="..."` necesitan comillas simples en el OUTPUT HTML. Patrón roto: `onclick="fn('' + id + '')"` — el primer `'` cierra el string JS, rompiendo todo. Patrón correcto: `onclick="fn(\x27" + id + "\x27)"` o usar template literals (backticks) para el string externo. **Detección:** `node --check` del script inline falla con `SyntaxError: Unexpected string`. **⚠️ Trampa:** `node --check` NO puede validar scripts inline porque su escaping está diseñado para contexto HTML, no JS standalone — el test puede dar falsos positivos. **Corrección:** Cambiar delimiters del string externo de `'` a `` ` `` (template literal), donde `'` es solo un carácter regular. Ver `references/inline-js-escaping-patterns.md` para patrones completos. Ver `references/write-file-corruption-pattern.md` para la restauración desde git.
- **🔴 EXTRAER SCRIPTS INLINE A ARCHIVOS EXTERNOS CAMBIA EL CONTEXTO DE ESCAPING** — Cuando mueves contenido de `<script>` inline a `<script src="...">` externo, los requerimientos de escaping CAMBIAN. En HTML inline, `\\\\'` (4 backslashes + quote) se interpreta como: HTML parser → `\\\\'` → JS parser → `\'` (escaped quote). En archivo JS standalone, `\\\\'` se interpreta como: JS parser → `\\` (literal backslash) + `'` (cierra string). **Resultado:** El script que funcionaba inline ROMPE al extraerlo a archivo externo. **SOLUCIÓN:** Al extraer scripts inline a archivos externos, reescribir el escaping: (1) usar template literals (backticks) para strings que construyen HTML, (2) o usar `\x27` para comillas simples en output, (3) o usar concatenación con `+ "'" +`. **NUNCA** simplemente copiar el contenido inline a un archivo .js y asumir que funciona. Ver `references/inline-js-escaping-patterns.md` para la tabla completa de conversión.
- **🔴 Duplicados temáticos** — Dos archivos pueden tratar el mismo tema con nombres ligeramente distintos (ej: `s04-1-fracciones-equivalentes.html` y `s04-4-fracciones-equivalentes.html`). No son idénticos pero uno es redundante. **SOLUCIÓN:** Comparar títulos, contenido y referencias cruzadas. Eliminar el redundante y actualizar todos los índices que lo referencian.

## 🔴 CORRECCIÓN DE HTML COMPLEJO: ORDEN DE OPERACIONES (v2.1 — NUEVO)

Cuando un archivo HTML tiene **múltiples problemas simultáneos** (scripts rotos + divs desbalanceados + contenido faltante), el orden de corrección es CRÍTICO. Corregir en el orden incorrecto puede introducir nuevos bugs o hacer que los fixes anteriores se pierdan.

### Regla de oro: Scripts → Estructura → Contenido

```
1. 🔴 SCRIPTS (arreglar execution context)
   → Eliminar <script src="..."> con contenido inline
   → Consolidar scripts rotos en bloques válidos
   → Verificar balance <script> / </script>

2. 🟡 ESTRUCTURA (arreglar HTML balance)
   → Contar <div> y </div> — deben coincidir
   → Eliminar </div> extra o añadir divs faltantes
   → Verificar que no hay tags HTML desbalanceados

3. 🟢 CONTENIDO (añadir mejoras pedagógicas)
   → Añadir ejercicios, SVGs, badges, etc.
   → Cada mejora añade divs → verificar balance de nuevo
```

### ¿Por qué este orden?

- **Si corriges scripts primero**, los divs añadidos por el contenido nuevo no afectan la corrección de scripts.
- **Si corriges divs antes de scripts**, un script fix puede añadir/eliminar divs y romper el balance que ya arreglaste.
- **Si corriges contenido antes de scripts/divs**, el contenido nuevo puede añadir divs que desbalancean la estructura que ya arreglaste.

### Detección de compound failure

Un archivo tiene **compound failure** si cumple 2+ de:
- Scripts rotos (`<script src=...>` con inline content)
- Divs desbalanceados (diff != 0)
- Contenido faltante (ejercicios, SVGs, badges)
- Scripts flotantes sin `<script>` tags

### Checklist de verificación post-corrección

```python
def verify_html_integrity(content):
    checks = {}
    
    # 1. Scripts balance
    script_opens = content.count('<script')
    script_closes = content.count('</script>')
    checks['scripts'] = script_opens == script_closes
    
    # 2. Divs balance
    div_opens = content.count('<div')
    div_closes = content.count('</div>')
    checks['divs'] = div_opens == div_closes
    
    # 3. Structure
    checks['doctype'] = '<!DOCTYPE html>' in content
    checks['html_close'] = '</html>' in content
    
    # 4. No <script src=...> con inline content
    import re
    bad_scripts = re.findall(r'<script\\s+src="[^"]*">\\s*[^<]', content)
    checks['no_bad_scripts'] = len(bad_scripts) == 0
    
    return checks
```

## Revisión Visual y Modernización CSS (v2.0)

Cuando un proyecto HTML tiene 50+ archivos y se necesita una revisión completa de diseño y calidad visual, seguir este procedimiento de 6 fases:

### Fase 1: Inventario y diagnóstico

```python
import os, re
from collections import Counter

project_dir = "/path/to/project"
html_files = [f for f in os.listdir(project_dir) if f.endswith('.html')]

# 1. Glassmorphism
glass_count = sum(1 for f in html_files if 'backdrop-filter' in open(os.path.join(project_dir, f)).read())
print(f"Glassmorphism: {glass_count}/{len(html_files)} archivos")

# 2. Estilos inline
inline_counts = []
for f in html_files:
    content = open(os.path.join(project_dir, f)).read()
    count = len(re.findall(r'style="[^"]*"', content))
    inline_counts.append((f, count))

total_inline = sum(c for _, c in inline_counts)
files_over_15 = [(f, c) for f, c in inline_counts if c > 15]
print(f"Total estilos inline: {total_inline}")
print(f"Archivos con >15 estilos inline: {len(files_over_15)}")

# 3. Plotly/KaTeX por nivel
for f in html_files:
    content = open(os.path.join(project_dir, f)).read()
    has_plotly = 'plotly' in content.lower()
    has_katex = 'katex' in content.lower()
    # Clasificar por nivel (eso, bachiller, carrera, primaria)
```

### Fase 2: Glassmorphism batch injection

Añadir glassmorphism a todos los archivos que lo necesitan:

```python
glass_css = """
/* Glassmorphism effect */
.glass{background:rgba(255,255,255,.75);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.box.glass{background:rgba(255,255,255,.75);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.interactive.glass{background:rgba(241,245,249,.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.summary.glass{background:rgba(239,246,255,.8);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.chart-container.glass{background:rgba(248,250,252,.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.3);box-shadow:0 4px 12px rgba(0,0,0,.06)}
"""

for fname in html_files:
    content = open(os.path.join(project_dir, fname)).read()
    if 'backdrop-filter' not in content:
        content = content.replace('</style>', glass_css + '\n</style>')
        open(os.path.join(project_dir, fname), 'w').write(content)
```

**Pitfall:** Algunos archivos pueden tener `</style` sin el `>` de cierre (corrupción de template engine). Detectar con `grep -c '</style' file` vs `grep -c '</style>' file`. Si hay diferencia, reparar primero el tag roto antes de inyectar CSS.

### Fase 3: Reducción de estilos inline

**Objetivo:** Reducir estilos inline moviendo patrones comunes a clases CSS reutilizables.

```python
# 1. Extraer todos los estilos inline y contar frecuencias
all_styles = []
for f in html_files:
    content = open(os.path.join(project_dir, f)).read()
    inline_styles = re.findall(r'style="([^"]*)"', content)
    all_styles.extend(inline_styles)

style_counts = Counter(all_styles)
top_styles = style_counts.most_common(50)

# 2. Crear clases CSS para los patrones más frecuentes
style_to_class = {
    'margin-top:.5rem': 'mt-1',
    'padding-left:1.2rem; margin-top:.5rem': 'pl-1-mt-1',
    'display: inline-flex; align-items: center; gap: 0.5rem; color: #2563eb; text-decoration: none; font-weight: 600; padding: 1rem 1rem; border-radius: 10px; background: rgba(255,255,255,0.6); border: 1px solid rgba(255,255,255,0.3); font-size: 1rem': 'nav-link',
    'color:#94a3b8; font-size: 1rem': 'text-muted',
    'text-align:center; margin: 1rem 0': 'text-center',
    # ... más patrones
}

# 3. Reemplazar inline styles con clases
for style, cls in style_to_class.items():
    escaped = re.escape(style)
    content = re.sub(f'style="{escaped}"', f'class="{cls}"', content)
```

**Regla:** No intentar eliminar TODOS los estilos inline. El objetivo es reducir los patrones más comunes (los que aparecen 10+ veces). Los estilos únicos de cada archivo se dejan como están — no merece la pena crear una clase CSS para un solo uso.

**Objetivo real:** Reducir de ~2000 a ~900 estilos inline (60% de reducción). Los que quedan son combinaciones muy específicas de cada archivo.

### Fase 4: Inyección de Plotly/KaTeX por nivel

Para proyectos educativos, añadir gráficos interactivos y fórmulas según el nivel:

```python
# Plotly para ESO (no para Primaria)
plotly_cdn = '''<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>'''

# Para cada archivo de ESO que no tenga Plotly:
# 1. Añadir CDN antes de </head>
# 2. Añadir div de gráfico con id="plot-tema"
# 3. Añadir script de renderizado antes de </body>

plot_div = f'''
<div class="chart-container glass">
    <h3>{titulo_grafico}</h3>
    <div id="{plot_id}" style="width:100%;max-width:600px;height:350px;margin:0 auto;"></div>
</div>'''

plot_script = f'''
<script>
const plotData = {data_json};
const layout = {layout_json};
const config = {{responsive: true, displayModeBar: false}};
if (typeof Plotly !== 'undefined') {{
    Plotly.newPlot('{plot_id}', plotData, layout, config);
}}
</script>'''
```

**Regla:** Plotly SOLO para ESO, Bachiller y Universidad. Primaria usa emojis y texto plano — no necesita gráficos interactivos.

**Regla:** Cada gráfico debe ser relevante al tema del archivo. No añadir un gráfico genérico — debe ilustrar el concepto que se está enseñando.

### Fase 5: Detección y eliminación de duplicados

```python
# Comparar archivos por título y contenido
for f1, f2 in combinations(html_files, 2):
    c1 = open(os.path.join(project_dir, f1)).read()
    c2 = open(os.path.join(project_dir, f2)).read()
    
    # Extraer títulos
    t1 = re.search(r'<title>(.*?)</title>', c1)
    t2 = re.search(r'<title>(.*?)</title>', c2)
    
    if t1 and t2 and t1.group(1) == t2.group(1):
        print(f"DUPLICADO EXACTO: {f1} == {f2}")
    
    # Comparar títulos similares (mismo tema)
    if t1 and t2 and t1.group(1).lower() == t2.group(1).lower():
        print(f"DUPLICADO TEMÁTICO: {f1} vs {f2}")
```

**Procedimiento de eliminación:**
1. Eliminar el archivo duplicado
2. Actualizar TODOS los índices que referencian el duplicado para que apunten al archivo principal
3. Verificar que no hay enlaces rotos post-eliminación

### Fase 6: Verificación visual por nivel

Navegar a un archivo representativo de cada nivel educativo y verificar visualmente con `browser_vision`:

1. **Primaria** → verificar: diseño child-friendly, emojis, colores vivos, sin KaTeX
2. **ESO** → verificar: glassmorphism, Plotly renderizado, colores Aurora (#2563eb + #f97316)
3. **Bachiller** → verificar: KaTeX fórmulas renderizadas, Plotly graphs, diseño profesional
4. **Universidad** → verificar: LaTeX complejo, gráficos avanzados, coherencia visual

**Regla:** NO verificar todos los archivos visualmente. Uno representativo por nivel es suficiente. El escaneo automático (Fases 1-5) cubre la consistencia técnica.

### Flujo de trabajo recomendado

```
1. Inventario → 2. Glassmorphism → 3. Inline styles → 4. Plotly/KaTeX → 5. Duplicados → 6. Verificación visual → 7. Commit/Push
```

**Ritmo:** No parar entre fases. El usuario quiere acción, no diagnósticos intermedios. Cada fase → commit separado.

**Objetivos de calidad por proyecto:**
- Glassmorphism: 100% de archivos
- Estilos inline: reducir >60%
- Plotly: 100% de ESO/Bachiller/Universidad
- KaTeX: 100% de Bachiller/Universidad
- Duplicados: 0
- Navegación: 0 enlaces rotos

## Verificación de fórmulas KaTeX (nuevo en v1.6)

Cuando el proyecto tiene contenido matemático (ESO, Bachiller, Universidad), verificar que las fórmulas están correctamente formateadas para KaTeX:

### 12. Verificar delimitadores KaTeX

Las fórmulas DEBEN estar envueltas en `$...$` (inline) o `$$...$$` (display). KaTeX CDN puede estar cargado pero si las fórmulas son texto plano, no se renderizan.

```python
# Detectar fórmulas como texto plano (fuera de $ delimiters)
def find_plain_math(content):
    """Find math symbols not wrapped in $ delimiters"""
    issues = []
    lines = content.split('\n')
    in_script = False
    
    for i, line in enumerate(lines):
        if '<script' in line: in_script = True
        if '</script' in line: in_script = False
        if in_script or '<style' in line: continue
        
        # Check for R², R³ outside of $
        if re.search(r'(?<!\$)R[²³](?!\$)', line):
            issues.append((i+1, 'R²/R³ sin delimitador $'))
        
        # Check for {sets} outside of $
        if re.search(r'\{[^}]{5,}\}', line) and '$' not in line:
            if not any(x in line for x in ['class=', 'id=', 'style=']):
                issues.append((i+1, 'Conjunto { } sin delimitador $'))
    
    return issues
```

**Criterio:** Si hay >0 fórmulas sin delimitador, es ⚠️ Importante.

### 13. Convertir fórmulas de texto plano a KaTeX

Cuando se detectan fórmulas sin delimitores, convertirlas:

```python
def convert_math_to_latex(content):
    """Convert plain text math to proper LaTeX with $ delimiters"""
    
    # R² → $R^2$
    content = re.sub(r'(?<!\$)(?<!\\)R²(?!\$)', r'$R^2$', content)
    content = re.sub(r'(?<!\$)(?<!\\)R³(?!\$)', r'$R^3$', content)
    
    # {(a,b), (c,d)} → $\{(a,b), (c,d)\}$  (sets need escaping)
    content = re.sub(r'\{(\([^)]+\)(?:\s*,\s*\([^)]+\))*)\}', r'$\\{\1\\}$', content)
    
    # Standalone sets {1, 2, 3}
    content = re.sub(r'\{(\d+(?:\s*,\s*\d+)*)\}', r'$\\{\1\\}$', content)
    
    # Math symbols
    content = re.sub(r'(?<!\$)∈(?!\$)', r'$\\in$', content)
    content = re.sub(r'(?<!\$)≤(?!\$)', r'$\\leq$', content)
    content = re.sub(r'(?<!\$)≥(?!\$)', r'$\\geq$', content)
    content = re.sub(r'(?<!\$)≠(?!\$)', r'$\\neq$', content)
    content = re.sub(r'(?<!\$)±(?!\$)', r'$\\pm$', content)
    
    return content
```

**Pitfall:** Los `{` y `}` en LaTeX necesitan ser escapados como `\{` y `\}` para mostrarse. Si no se escapan, KaTeX los interpreta como grupos de agrupación.

### 14. Verificar script auto-render

El script de KaTeX debe tener los delimiters correctos:

```python
# Verificar que el script de renderizado existe y tiene delimiters
has_render_script = 'renderMathInElement' in content
has_delimiters = 'delimiters' in content

if has_render_script and not has_delimiters:
    print(f'⚠️ {fname}: renderMathInElement sin delimiters configurados')
```

**Formato esperado:**
```javascript
renderMathInElement(document.body, {
    delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
    ],
    throwOnError: false
});
```

## Verificación de ejercicios interactivos (nuevo en v1.8)

### 15. Ejercicios con onclick que llaman funciones inexistentes

**Problema:** Los scripts generadores crean HTML con `onclick="checkExercise(1, 3)"` pero NO definen la función JavaScript. El ejercicio se ve pero al pulsar "Comprobar" sale error en consola.

**Detección:**

```python
def check_exercise_functions(content):
    """Find onclick handlers calling functions that aren't defined"""
    # Find all function calls in onclick
    onclick_fns = set(re.findall(r'onclick="([a-zA-Z_$]+)\(', content))
    # Find all function definitions
    defined_fns = set(re.findall(r'function\s+([a-zA-Z_$]+)\s*\(', content))
    
    missing = onclick_fns - defined_fns
    if missing:
        return f'❌ Funciones onclick no definidas: {missing}'
    return None
```

**Patrón mínimo de función `checkExercise`:**

```javascript
function checkExercise(num, correct) {
  const input = document.getElementById('e' + num);
  const feedback = document.getElementById('e' + num + '-fb');
  if (!input || !feedback) return;
  const val = input.value.trim();
  const isCorrect = parseFloat(val) === correct;
  feedback.textContent = isCorrect ? '¡Correcto! ✓' : 'Incorrecto. La respuesta es ' + correct;
  feedback.className = 'feedback ' + (isCorrect ? 'correct' : 'incorrect');
}
```

**Patrón para select (multiple choice):**

```javascript
function checkE1() {
  const sel = document.getElementById('e1');
  const fb = document.getElementById('e1-fb');
  if (!sel || !fb) return;
  const isCorrect = sel.value === 'correcta';
  fb.textContent = isCorrect ? '¡Correcto! ✓' : 'Incorrecto.';
  fb.className = 'feedback ' + (isCorrect ? 'correct' : 'incorrect');
}
```

**Criterio:** Si hay >0 funciones onclick sin definición, es ❌ Crítico — el ejercicio no funciona.

**Pitfall:** Las funciones `setDerivPoint(x)`, `setPotencia(n)` para gráficos interactivos necesitan que Plotly esté cargado. Añadir check de que Plotly está disponible antes de llamar a funciones que usan `Plotly.newPlot`.

## Verificación post-escritura obligatoria

Después de CUALQUIER operación `write_file` sobre archivos de código (HTML con inline JS, módulos JS, archivos CSS), ejecutar verificación antes de continuar:

```bash
# 1. JS syntax check (si hay archivos .js o inline scripts extraídos)
node --check archivo.js 2>&1 | head -5

# 2. HTML structure check (balance de tags)
python3 -c "
content = open('index.html').read()
assert content.count('<script') == content.count('</script>'), 'Scripts desbalanceados'
assert content.count('<div') == content.count('</div>'), 'Divs desbalanceados'
assert '<!DOCTYPE html>' in content, 'Sin DOCTYPE'
assert '</html>' in content, 'Sin cierre HTML'
print('✅ HTML structure OK')
"

# 3. Verificar elementos críticos no eliminados
python3 -c "
content = open('index.html').read()
for term in ['switchTab', 'function render', 'DOMContentLoaded']:
    assert term in content, f'CRÍTICO: {term} eliminado por write_file'
print('✅ Critical elements OK')
"
```

**Regla de oro:** Si `write_file` corrompió algo, el `node --check` lo detecta ANTES de que el usuario lo vea. Nunca asumir que `write_file` preservó el contenido correctamente — siempre verificar.

## Linked Files

- `references/line-number-prefix-corruption.md` — Patrón de corrupción: prefijos `N|` incrustados en HTML por tools de visualización. Rompe CSS y muestra texto basura. Incluye diferenciación con `read_file` de Hermes.
- `scripts/audit-quick.py` — Script de auditoría rápida: ejecutar desde la raíz del proyecto. Detecta: corrupción de números de línea, enlaces rotos, CSS desbalanceado, navegación rota, divs desbalanceados.
- `references/css-double-braces-fix.md` — Patrón de detección y corrección batch de `{{}}` en CSS (template engine artifacts)
- `references/escaneo-html-error-pattern.md` — Scripts reutilizables para escaneo y corrección automática
- `references/escaneo-navegacion-curso.md` — Escaneo específico de navegación de cursos educativos: cadenas paralelas, transiciones entre niveles, consistencia README, clasificación de páginas
- `references/verificacion-ruta-completa.md` — Verificación de ruta completa de navegación: INDEX → índice → sesión → vuelta al índice → INDEX, detección de enlaces malformados, navegación entre niveles
- `references/rebuild-navigation-batch.md` — Técnica batch para reconstruir navegación rota sistemáticamente (sorting numérico + execute_code)
- `references/plotly-chart-verification.md` — Verificación de gráficos Plotly: contenedores vacíos, código de inicialización faltante, patrones de chart containers
- `references/navegacion-nav-div-extraction.md` — Patrón seguro para extraer Anterior/Siguiente de `<div class="nav">` con regex completo, casos especiales (3 enlaces, disabled, INDEX) y casos reales
- `references/visual-audit-css-modernization.md` — Procedimiento de revisión visual y modernización CSS: glassmorphism, inline styles a clases, Plotly/KaTeX batch injection, verificación visual por nivel educativo
- `references/write-file-corruption-pattern.md` — Patrón de corrupción por `write_file` dentro de `execute_code`: contenido JS complejo truncado/mangled, casos reales (ContrataPúblico 2026-06-16), prevención y recuperación
- `references/inline-js-syntax-validation.md` — Técnicas de diagnóstico para scripts inline en HTML grandes: vm.Script validation, brace/paren balance comparison between versions, binary search for syntax errors, corrupted merge line detection, revert vs fix decision matrix
- `references/single-file-interactive-audit.md` — Procedimiento para auditar aplicaciones web monolíticas (1 archivo HTML+CSS+JS inline): visores interactivos, Leaflet, etc. Incluye: (a) auditoría de debugging (variables, comillas, lecturas duplicadas, estado global, UX), (b) data-driven visor audit (JSON backend, consistencia, enlaces no usados), y (c) **single-file dashboard post-fix audit** — verificación de integridad estructural post-oleadas de fixes: balance de tags, tab buttons ↔ panels mapping, funciones definidas vs llamadas, panel sizes/features, errores JS comunes, duplicados.

## Static SPA Mobile Responsive Audit

Auditoría de responsive móvil para SPAs estáticas (sin backend, un solo HTML+CSS+JS inline, deploy en GitHub Pages). Ver `references/single-file-interactive-audit.md` → sección "Mobile Responsive Audit" para el procedimiento completo.

### Checks rápidos
1. **Flex height chain** — trazar `html(100%) → body(100%) → #app(100vh) → #main-area(flex:1) → #map-container(flex:1) → #map(height:100%)`. Si cualquier eslabón no tiene altura computada, el mapa queda con 0px.
2. **position:fixed rompe flex flow** — cuando un hijo flex pasa a `position:fixed` en @media, se saca del flujo. Los hijos restantes deben llenar el espacio. Verificar que `#map-container` se estira correctamente.
3. **@media coverage** — verificar que TODO contenedor crítico (#map-container, #map, #sidebar) tiene reglas explícitas en @media. Un contenedor sin reglas mobile = depende del flex default que puede fallar.
4. **Sidebar-tapa-contenido** — panel `position:fixed; bottom:0` con `height:45vh` tapa 45% del mapa. Auto-collapse en móvil o UI de toggle clara.
5. **invalidateSize en orientación** — `screen.orientation.addEventListener('change')` además del `resize` handler.

### Patrón de corrección típico
```css
@media (max-width: 768px) {
    #map-container { height: calc(100vh - 84px); } /* 100vh - topbar - footer */
    #map { height: 100%; }
    #sidebar { /* ya tiene position:fixed */ }
    #sidebar:not(.collapsed) ~ #map-container { height: calc(55vh - 52px); }
}
```

## SPA con Backend Propio (Express + Node.js)

Procedimiento específico para auditar Single Page Applications con backend. Ver `single-page-app-audit` para el procedimiento detallado de auditoría de aplicaciones web individuales.

## Visores con JSON Backend (data-driven)

Visores que cargan datos desde múltiples archivos JSON (reports, memorias, index) — patrones de auditoría distintos al SPA-backend. Ver `references/single-file-interactive-audit.md` → sección "Data-Driven Visor Audit" para checks de: consistencia entre fuentes JSON, enlaces no utilizados, existencia de archivos referenciados, claridad de títulos, y vistas ausentes.

### Checklist SPA
1. Comparar rutas frontend vs backend (`grep -oP "fetch.*'/api/" dashboard.html` vs `grep -oP "app\.(get|post|put|delete)" server.js`)
2. Verificar syncGitHub en cada endpoint mutador
3. Verificar responsive de Chart.js/Three.js
4. Detectar funciones onclick sin definición
5. Verificar flujo CRUD completo con curl
6. Comparar SHA local vs remoto

### Pitfalls SPA
- Frontend usa nombre de endpoint distinto al backend (bug más común)
- `indexOf` con duplicados tras `reverse()`
- Charts declarados con `const` local (pérdida de referencia al recargar tab)
- Dos clones del mismo repo en local con diferente estado
- **🔴 Kaizen sidebar override incompleto** — Si el proyecto usa `kaizen.css` + custom CSS para el sidebar, Kaizen define `display:flex; justify-content:space-between; cursor:pointer; border-bottom` en `.kz-sidebar-category` y `.kz-sidebar-item` pensado para listas de navegación. Si el sidebar contiene formularios (inputs, chips, botones), estos estilos heredados rompen el layout. Ver `references/kaizen-sidebar-override-pattern.md` para fix pattern y detection checklist.

## HTML Structural Audit — Integridad Estructural

Procedimiento para auditar integridad estructural de archivos HTML en batch: CSS braces, div balance, style tags. Ver `html-structural-audit` para el script completo.

### Quick audit
```bash
cp /hermes-home/skills/devops/html-structural-audit/scripts/audit.py .
python3 audit.py /path/to/html-dir
python3 audit.py /path/to/html-dir --fix   # auto-fix
```

### Qué detecta
1. **CSS braces mismatch** — `{` vs `}` en `<style>` blocks
2. **Unbalanced `<div>` tags** — imbalance > 3 = layout breakage
3. **Unclosed `<style>` tags**

### Pitfalls
- No fix divs con imbalance > 6 — es un problema estructural
- Archivos > 20KB no deben reescribirse con `write_file` — usar `patch()`

Procedimiento específico para auditar Single Page Applications que tienen su propio servidor backend (Express, datos en JSON/SQLite, Chart.js, Three.js).

### 1. Inventario del stack

Identificar backend, frontend y persistencia:

```bash
# Stack completo
grep -c 'app\\.\\(get\\|post\\|put\\|delete\\)' server.js  # Endpoints REST
grep -c 'Chart\\.\\(register\\|new Chart\\)' dashboard.html  # Chart.js
grep -c 'THREE\\|Three' dashboard.html  # Three.js
grep -c 'fetch\\|axios' dashboard.html   # Llamadas a API
ls data/ 2>/dev/null || echo "Sin directorio data/"
```

### 1.1 Verificar dependencias CDN (post-extracción de JS)

**Si el JS fue extraído de inline a archivo separado**, verificar que las dependencias CDN no se perdieron:

```bash
# Detectar constructores de librerías externas en JS
grep -oP '\bnew\s+(Chart|THREE|Plotly|D3|L)\b' dashboard.js | sort -u
# Verificar que los CDN correspondientes están en el HTML
grep -i 'cdn.jsdelivr\|unpkg\|cdnjs' dashboard.html
```

**Pitfall conocido:** Extraer `<script>` inline a `<script src="...">` puede causar que se pierdan los CDN del `<head>`. El JS carga pero falla silenciosamente. Siempre verificar después de cualquier reestructuración de archivos.

### 2. Verificar endpoints REST

Para cada endpoint CRUD (`POST`, `PUT`, `DELETE`), verificar que:

- **El frontend llama al endpoint correcto.** Error común: el frontend usa un nombre (`'deporte'`) que el backend no reconoce (`'entrenamientos'`). Detectar con `grep -n "fetch.*'/api/" dashboard.html` y comparar con `app.[method]('/api/'` en server.js.
- **El endpoint acepta el formato de datos que envía el frontend.** El body de `fetch()` debe coincidir con `req.body` esperado.
- **El endpoint existe en el servidor.** Si el frontend hace `DELETE /api/entrenamientos/:idx`, el server debe tener `app.delete('/api/entrenamientos/:idx', ...)`.

```bash
# Comparar rutas de frontend vs backend
echo "=== FRONTEND ==="
grep -oP "fetch\\(['\"]/api/[^'\"]+" dashboard.html | sort -u
echo "=== BACKEND ==="
grep -oP "app\.(get|post|put|delete)\\(['\"]/api/[^'\"]+" server.js | sort -u
```

### 3. Verificar sincronización de datos con GitHub

Si el backend usa GitHub Contents API para persistencia (NaN containers pierden filesystem en redeploy):

1. **Identificar función sync**: buscar `syncGitHub` o `syncToGithub` en server.js
2. **Verificar llamada desde cada endpoint**: cada `POST / PUT / DELETE` debe llamar al sync
3. **Verificar tokens**: `GITHUB_TOKEN` debe estar configurado (NaN Env o .env)
4. **Comparar datos locales vs GitHub**:
   ```bash
   # SHA local
   sha256sum data/database.json
   # SHA remoto
   curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
     https://api.github.com/repos/OWNER/REPO/contents/data/database.json | \
     grep -o '"sha":"[^"]*"' | head -1
   ```
5. **Verificar conteo de registros** (pesos, comidas, entrenos, etc.) coinciden entre local y remoto

### 4. Verificar responsive de componentes JS

Los componentes renderizados por JavaScript (Chart.js, Three.js, tablas dinámicas) necesitan verificación específica:

- **Chart.js**: `responsive: true` en config, `maintainAspectRatio: false`, canvas con contenedor que tenga altura definida
- **Three.js**: `renderer.setSize()` debe ajustarse en resize event. Canvas con altura adaptable. Verificar que hay loading state mientras carga.
- **Tablas dinámicas**: grids de KPIs deben usar CSS Grid/Flexbox con `grid-template-columns: repeat(auto-fit, minmax(XXXpx, 1fr))`
- **Tabs**: contenedor de tabs debe tener `overflow-x: auto` + `flex-wrap: nowrap` en móvil. Verificar con:
  ```bash
  grep -oP '(overflow-x|flex-wrap|white-space).*(auto|nowrap)' dashboard.html
  ```
- **Loading states**: cada componente que hace fetch debe tener estado de carga (spinner/skeleton). Verificar que el loading se oculta tanto en éxito como en error.

### 5. Verificar DOM references y funciones

Errores comunes en SPAs con JavaScript vanilla:

- **Funciones definidas después de onclick**: `onclick="editarEntreno(0)"` pero `function editarEntreno(){}` no existe
- **Variables en scope incorrecto**: `const charts = window.charts = {}` (NO `const charts = {}` solo)
- **indexOf con duplicados**: Si se usa `list.indexOf(item)` en listas que pueden tener duplicados (tras reverse(), el índice devuelto es del primer match, no del seleccionado)

```bash
# Detectar funciones onclick sin definición
echo "=== FUNCIONES onclick ==="
grep -oP 'onclick="([a-zA-Z_]+)\(' dashboard.html | sort -u
echo "=== FUNCIONES DEFINIDAS ==="
grep -oP 'function\s+([a-zA-Z_]+)\s*\(' dashboard.html | sort -u
# Comparar — las que están en la primera lista pero no en la segunda son errores
```

### 6. Verificar flujo de datos completo

Una vez identificados los endpoints, probar el flujo completo de al menos un CRUD:

1. **GET** `/api/datos` → datos actuales
2. **POST** `/api/entrenamientos` → crear nuevo registro
3. **GET** `/api/datos` → confirmar que aparece
4. **DELETE** `/api/entrenamientos/:idx` → eliminar
5. **GET** `/api/datos` → confirmar que desaparece
6. **curl** la URL de producción para verificar que el HTML deployado tiene el fix

### 7. Verificar estado de deploy

- **URL de producción**: `https://<app>-<owner>-<owner>.apps.nan.builders/`
- **Health check**: `curl https://.../healthz` debe responder 200 `{"status":"ok"}`
- **Contenido del HTML**: `curl https://.../dashboard.html | grep -o "entrenamientos"` — confirmar que el HTML deployado contiene el fix
- **Git commit SHA**: `curl -s https://.../dashboard.html | md5sum` vs `md5sum dashboard.html` — si coinciden, el deploying está actualizado

### 8. Buscar carpetas huérfanas

Verificar que no hay carpetas locales del mismo proyecto que no estén actualizadas:

```bash
# Buscar directorios con package.json similares
find /root/workspace -maxdepth 2 -name 'package.json' | while read f; do
  echo "=== $(dirname $f) ==="
  cd "$(dirname $f)" && git log --oneline -3 2>/dev/null || echo "  No es repo git"
done
```

Si hay dos carpetas apuntando al mismo remoto pero con diferentes commits, la más antigua es huérfana. Preguntar al usuario si quiere limpiarla.

## Pitfalls de auditoría SPA-backend

- **🔴 Frontend usa nombre de endpoint distinto al backend** — El bug más común. El frontend llama a `'/api/deporte'` pero el backend tiene `app.delete('/api/entrenamientos/:idx')`. Detectar con la comparación de rutas del paso 2.
- **🔴 indexOf con duplicados tras reverse()** — Cuando se revierte un array y se usa `indexOf` para encontrar un elemento duplicado (dos entrenamientos con el mismo nombre), `indexOf` devuelve el índice del PRIMER match, no del seleccionado. Usar `findIndex()` en su lugar, o trabajar con índices explícitos.
- **🔴 Charts declarados con `const` local** — Si los charts se inicializan con `const chart = new Chart(...)` dentro de una función y no se asignan a un objeto global, al recargar la tab se pierde la referencia y no se puede destruir el canvas anterior. Patrón correcto: `window.charts = window.charts || {}; window.charts['peso'] = new Chart(...)`.
- **🔴 Tab lazy-rendered: no marcar tabs en renderTab** — Si los tabs son lazy (solo se renderizan cuando se activan), NO llamar a funciones de marcado/responsive dentro de `renderTab()`. Esperar a que el fetch termine y el DOM esté listo.
- **🔴 NaN containers: sync no bloqueante falla silenciosamente** — `syncGitHub()` con `await` pero sin catch visible puede fallar sin que el usuario lo sepa. Siempre loggear errores de sync.
- **🔴 Dos clones del mismo repo en local** — `dieta-masterfit/` y `dieta/` pueden apuntar ambos al mismo remoto pero con diferente estado. El servidor en NaN usa el remoto, no el local, así que la inconsistencia local no afecta producción pero confunde al desarrollador.

## Verificación de contenido educativo (nuevo en v1.1)

Cuando el proyecto es un curso educativo, añadir estas verificaciones al escaneo:

```python
# Verificar componentes educativos
has_katex = 'katex' in content.lower()
has_plotly = 'plotly' in content.lower()
has_attr = 'David Antizar' in content
has_summary = 'summary' in content.lower()
has_exercise = 'exercise' in content.lower()
has_feedback = 'feedback' in content.lower()
```

**Criterios mínimos por sesión:**
- KaTeX: para Bachiller/Carrera (NO para Primaria)
- Plotly.js: mínimo 1 gráfico interactivo por sesión
- Atribución: siempre presente
- Resumen: sección `.summary` con puntos clave
- Ejercicios: mínimo 3 con feedback

### 🔴 GRÁFICOS PLOTLY SIN INICIALIZACIÓN

**Problema:** Un script generador puede crear el CDN de Plotly Y el contenedor HTML (`<div id="plot-xxx" class="chart-plot">`) SIN añadir el código JavaScript que llama a `Plotly.newPlot()`. El gráfico aparece vacío — solo se ve un recuadro blanco.

**Detección:** Buscar contenedores `<div id="plot-*">` sin correspondiente `Plotly.newPlot`:

```python
import re

def check_plotly_init(content):
    """Find chart containers without Plotly.newPlot initialization"""
    containers = re.findall(r'<div\s+id="(plot-[^"]+)"', content)
    initializations = re.findall(r'Plotly\.newPlot\(', content)
    
    issues = []
    if containers and len(containers) > len(initializations):
        missing = containers[len(initializations):]
        issues.append(f'{len(missing)} contenedores Plotly sin inicializar: {missing}')
    elif containers and not initializations:
        issues.append(f'{len(containers)} contenedores Plotly sin código Plotly.newPlot')
    return issues
```

**Criterio:** Si hay contenedores `plot-*` sin `Plotly.newPlot`, es **❌ Crítico** — el gráfico no se ve.

**Patrón de corrección:** Para cada contenedor, añadir script de inicialización:

```javascript
Plotly.newPlot('plot-nombre', [{
    x: [...], y: [...],
    type: 'scatter', mode: 'lines+markers',
    name: 'Leyenda',
    line: {color: '#2563eb', width: 2}
}], {
    title: 'Título del gráfico',
    xaxis: {title: 'Eje X'},
    yaxis: {title: 'Eje Y'}
}, {responsive: true});
```

**Regla:** El CDN `<script src="plotly.js">` NO es suficiente — siempre verificar que hay `Plotly.newPlot()` o `Plotly.react()` para cada contenedor.

## Verificación de navegación de curso educativo (nuevo en v1.2)

### 6. Verificar ruta completa de navegación (nuevo en v1.4)

No basta con que los enlaces existan — hay que verificar que la **ruta de navegación completa** funciona:

```
INDEX.html → índice de nivel → sesión → vuelta al índice → INDEX
```

```python
# Mapa: cada sesión → su índice de nivel
level_index_map = {
    's01-1-contar-0-10.html': 's01-1primaria-index.html',
    's02-1-sumas-llevadas.html': 's02-2primaria-index.html',
    # ... todas las sesiones mapeadas a su índice
}

# Verificar que cada sesión enlaza a su índice
for session, level_idx in level_index_map.items():
    with open(session) as f:
        content = f.read()
    if level_idx not in content:
        print(f'❌ {session}: sin enlace a su índice {level_idx}')

# Verificar que cada índice enlaza a INDEX
for idx_file in level_index_map.values():
    with open(idx_file) as f:
        content = f.read()
    if 'INDEX.html' not in content:
        print(f'❌ {idx_file}: sin enlace a INDEX.html')
```

### 7. Verificar que INDEX.html enlaza a índices, no a sesiones (nuevo en v1.4)

```python
# INDEX.html debe enlazar a índices de nivel, NO a sesiones individuales
level_indexes = {'s01-1primaria-index.html', 's02-2primaria-index.html', ...}
session_files = {'s09-1-bachiller-limites.html', 's10-1-carrera-limites-multivariable.html'}

with open('INDEX.html') as f:
    content = f.read()
index_links = set(re.findall(r'href="([^"]*\.html)"', content))

if session_files & index_links:
    print(f'❌ INDEX.html enlaza a sesiones directas: {session_files & index_links}')
```

**Regla:** INDEX.html SIEMPRE debe enlazar a índices de nivel, nunca a sesiones individuales. Un alumno que pulse "Bachillerato" debe ver el índice del nivel, no la sesión 1 directamente.

### 8. Añadir navegación entre niveles en índices (nuevo en v1.4)

Los índices de nivel deben tener enlaces al nivel anterior y siguiente:

```python
level_chain = [
    ('s01-1primaria-index.html', None, 's02-2primaria-index.html', '1º Primaria', '2º Primaria'),
    ('s02-2primaria-index.html', 's01-1primaria-index.html', 's03-3primaria-index.html', '1º Primaria', '3º Primaria'),
    # ...
    ('s10-1carrera.html', 's09-bachiller.html', None, 'Bachiller', None),
]

for level_file, prev, next_level, prev_name, next_name in level_chain:
    with open(level_file) as f:
        content = f.read()
    
    # Añadir navegación entre niveles si no existe
    nav_html = '<div style="display:flex;justify-content:center;gap:1rem;margin-top:1.5rem;flex-wrap:wrap">\n'
    if prev:
        nav_html += f'  <a href="{prev}" style="color:#64748b;...">← {prev_name}</a>\n'
    if next_level:
        nav_html += f'  <a href="{next_level}" style="color:#2563eb;...">{next_name} →</a>\n'
    nav_html += '</div>\n'
```

### 9. Detectar enlaces HTML malformados (nuevo en v1.4)

Un error común es que el atributo `href` no tenga su `>` de cierre, quedando texto pegado:

```html
<!-- MAL: falta ">" antes de "Siguiente" -->
<a href="s04-4primaria.html"Siguiente: 5º Primaria →</a>

<!-- BIEN -->
<a href="s04-4primaria.html">Siguiente: 5º Primaria →</a>
```

```python
# Detectar hrefs malformados
bad_links = re.findall(r'href="([^"]*\.html)"[^>\s]', content)
if bad_links:
    print(f'❌ Enlaces malformados: {bad_links}')
```

## Verificación de navegación de curso educativo (nuevo en v1.2)

Cuando el proyecto es un **curso estructurado por niveles** (Primaria → ESO → Bachiller → Universidad), añadir estas verificaciones específicas de navegación:

### 1. Detectar cadenas de navegación paralelas

Un curso puede tener DOS cadenas de navegación independientes que deberían conectarse:
- **Cadena A (índices de nivel):** `s01-1primaria → s01-2primaria → ...` (sesiones resumen)
- **Cadena B (detallada):** `s01-1-contar-0-10 → s01-2-contar-10-100 → ...` (sesiones detalladas)

**Verificar:** ¿Hay algún enlace entre la Cadena A y la Cadena B? Si no, los alumnos que entren por una cadena nunca verán la otra.

```python
# Detectar cadenas paralelas
chain_a = [f for f in html_files if re.match(r's\d+-\d+primaria\.html', f)]
chain_b = [f for f in html_files if re.match(r's\d+-\d+-[a-z]', f)]

for src in chain_a:
    with open(src) as f:
        content = f.read()
    for target in chain_b:
        if target in content:
            print(f'✅ {src} → {target}')
# Si no hay output, las cadenas están desconectadas
```

### 2. Verificar índices de nivel por nivel

No todos los niveles tienen por qué tener índice, pero la experiencia debe ser uniforme:

| Nivel | ¿Tiene índice? | ¿Qué enlaza INDEX.html? |
|-------|---------------|------------------------|
| 1º Primaria | ❌ Sin índice | Enlaza a sesión individual |
| 2º Primaria | ❌ Sin índice | Enlaza a sesión individual |
| 3º Primaria | ❌ Sin índice | Enlaza a sesión individual |
| 4º Primaria | ✅ Con índice | Enlaza al índice |
| 5º+ | ✅ Con índice | Enlaza al índice |

**Regla:** Si INDEX.html enlaza a una sesión individual en lugar de un índice de nivel, el alumno no ve la estructura completa del nivel.

```python
# Clasificar cada archivo como índice o sesión
def classify_page(fname, content):
    hrefs = re.findall(r'href="([^"]+\.html)"', content)
    session_links = [h for h in hrefs if h not in ('INDEX.html', fname, 'index.html')]
    if len(session_links) >= 5:
        return 'indice'
    elif len(session_links) <= 3:
        return 'sesion'
    return 'indefinido'
```

### 3. Verificar transiciones entre niveles

La última sesión de cada nivel debe enlazar a la primera del siguiente:

```python
# Mapa de transiciones esperadas
transitions = {
    's01-4primaria.html': 's02-1primaria.html',  # 1ºP última → 2ºP primera
    's02-7primaria.html': 's03-3primaria.html',  # 2ºP última → 3ºP primera
    's03-3primaria.html': 's04-4primaria.html',  # 3ºP última → 4ºP índice
    's04-4primaria.html': 's05-5primaria.html',  # 4ºP última → 5ºP índice
    # ...
}
```

### 4. Verificar consistencia README vs. realidad

El README.md suele describir la estructura del proyecto. Verificar que:
- Los archivos que describe como "índices de nivel" realmente LO SEAN (tengan múltiples enlaces a sesiones)
- Los archivos que describe como "sesiones" realmente lo sean
- El conteo de sesiones por nivel coincida con los archivos reales

### 5. Detectar enlaces a archivos inexistentes en navegación secuencial

No basta con buscar `href="#"` — también hay que verificar que los targets de Anterior/Siguiente existen:

```python
for fname in html_files:
    with open(fname) as f:
        content = f.read()
    # Buscar hrefs en contexto de navegación
    for match in re.finditer(r'(?:Anterior|Siguiente).*?href="([^"]+\.html)"', content):
        target = match.group(1)
        if target not in all_existing_files:
            print(f'❌ {fname} → {target} (NO EXISTE)')
```

## Verificación de diseño y consistencia estructural (nuevo en v1.5)

### 10. Detectar inconsistencias en estructura HTML

Un proyecto puede tener dos "tipos" de archivos con estructura HTML diferente. Esto crea una experiencia inconsistente para el usuario.

```python
# Detectar qué archivos usan elementos semánticos
estructura = defaultdict(list)
for f in html_files:
    with open(os.path.join(base, f)) as fh:
        content = fh.read()
    
    has_nav = '<nav' in content
    has_header = '<header' in content
    has_footer = '<footer' in content
    has_main = '<main' in content
    
    key = f"nav={'✅' if has_nav else '❌'} header={'✅' if has_header else '❌'} footer={'✅' if has_footer else '❌'} main={'✅' if has_main else '❌'}"
    estructura[key].append(f)

print("📐 Estructuras HTML:")
for key, files in estructura.items():
    print(f"   {key}: {len(files)} archivos")
```

**Problema común:** Índices usan `<div class="header">` mientras sesiones usan `<header class="header">`. Ambos funcionan visualmente pero la estructura semántica es diferente.

**Regla:** Si hay más de 2 estructuras diferentes, reportarlo como ⚠️ Importante.

### 11. Verificar que README claims vs realidad

El README puede afirmar cosas que no son ciertas. Verificar:

```python
# Ejemplo: README dice "HTML semántico" pero muchos archivos no lo son
with open(os.path.join(base, 'README.md')) as f:
    readme = f.read()

if 'HTML semántico' in readme or 'header' in readme.lower():
    # Contar archivos con elementos semánticos
    con_semantica = sum(1 for f in html_files 
                       if has_header_element(f) and has_footer_element(f))
    total = len(html_files)
    porcentaje = con_semantica / total * 100
    
    if porcentaje < 80:
        print(f"⚠️ README dice 'HTML semántico' pero solo {porcentaje:.0f}% lo cumple")
```

## Pitfalls específicos de cursos educativos

- **Cadenas paralelas desconectadas:** El patrón más común y más difícil de detectar. Dos cadenas de navegación que coexisten sin enlazarse entre sí. Síntoma: un nivel tiene archivos `sXX-YYprimaria.html` (sesiones resumen) Y archivos `sXX-YY-tema.html` (sesiones detalladas) sin que ninguna enlace a la otra.
- **Índices que son sesiones:** Un archivo nombrado como índice de nivel (ej: `s01-1primaria.html`) que en realidad es una sesión individual con solo 1-2 enlaces a otras sesiones.
- **Transiciones entre niveles inconsistentes:** La última sesión del nivel N enlaza a una sesión que no es la primera del nivel N+1, o enlaza a un archivo que no existe.
- **README desactualizado
- **Enlaces HTML malformados (falta >):** Patrón de generación automática donde el > de cierre del atributo href se pierde, pegando el texto "Siguiente" al atributo. Ejemplo: `<a href="file.html"Siguiente: ...` en vez de `<a href="file.html">Siguiente: ...`. Detectar con regex: `href="([^"]*\.html)"[^\s>]`.
- **Estructura HTML inconsistente:** Algunos archivos usan `<div class="header">` y otros `<header class="header">`. Ambos funcionan visualmente pero crean experiencia inconsistente. Verificar que todos los archivos del mismo tipo tengan la misma estructura semántica.:** Describe archivos como "índices" que en realidad son sesiones, o viceversa. Siempre verificar contra el contenido real.