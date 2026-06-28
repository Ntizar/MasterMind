---
name: design-system-scaffold
description: "Crear design systems CSS corporativos desde cero para equipos — análisis de imagen de referencia, extracción de tokens, CSS con variables, galería HTML, documentación AGENTS.md para IAs, y repo GitHub. Patrón extraído del Kaizen Design System para Equipo Kaizen Ineco."
version: "1.0.0"
author: Mastermind
tags: [design-system, css, corporate, team, scaffold, tokens, agents-md]
related_skills: [aurora-design-system, aurora-llm-optimization, popular-web-designs]
---

# Design System Scaffold

Crear un design system CSS completo y profesional para un equipo o empresa, partiendo de una imagen de referencia (intranet, app, mockup).

## Cuándo usar

- Un equipo pide un CSS compartido para unificar el estilo de sus herramientas
- Hay una imagen de referencia (intranet, app, mockup) de la que extraer el estilo
- Se necesita un repo con CSS + documentación + ejemplos para que las IAs lo usen
- Se quiere que todas las herramientas del equipo tengan aspecto coherente
- **Extender un design system existente** para cubrir un nuevo dominio (dashboards, datos, etc.)

## ⚠️ REGLA #0: EVOLUCIONAR PRIMERO, APLICAR DESPUÉS

**Señal del usuario:** "ME interesa más que mejores el kaizen design system para que en un futuro sea implementable en herramientas asi. El gtfs no me toques."

**Patrón:** Cuando un design system carece de componentes para un proyecto objetivo, el flujo correcto es:
1. **Auditar** qué componentes tiene vs. qué necesita el proyecto objetivo
2. **Extender** el design system con los componentes faltantes
3. **Actualizar** showcase (index.html), standalone, docs (README + AGENTS.md)
4. **Commit + push** del design system actualizado
5. **DESPUÉS** — aplicar al proyecto objetivo (en otra sesión)

**NUNCA** modificar el proyecto objetivo para encajar con un design system incompleto. Primero se arregla el DS, luego se aplica.

### Checklist de extensión

1. Analizar el proyecto objetivo → listar componentes CSS que usa
2. Auditar el DS existente → qué tiene, qué falta
3. Crear lista de componentes faltantes con prioridad
4. Implementar en el CSS principal (añadir al FINAL para no romper existente)
5. Añadir demos al index.html (nuevas secciones de nav + HTML de ejemplo)
6. Regenerar index-standalone.html (CSS inlined)
7. Actualizar README.md y AGENTS.md con los nuevos componentes
8. Commit + push
9. Verificar que nada existente se ha roto (abrir index.html, comprobar visualmente)

## ⛔ REGLA #1: NUNCA cards bordeadas (estilo IA)

**Señal del usuario:** "la card esa bordeada no la quiero para nada!!! Eso parece que es IA"

Las cards con bordes gruesos, sombras y esquinas redondeadas grandes son el **patrón #1 que delata que un diseño es generado por IA**. Los diseños corporativos reales (intranet Ineco, apps enterprise) usan:

- ✅ **Títulos de sección** en azul con línea de 2px debajo
- ✅ **Separadores sutiles** — líneas de 1px o whitespace
- ✅ **Tiles limpios** — borde de 1px sutil, sin sombra
- ✅ **Fondo blanco puro** — sin gradientes en componentes
- ❌ **NO** cards con bordes de 2px+ y border-radius grande
- ❌ **NO** sombras (box-shadow) en cards
- ❌ **NO** gradientes en fondos de cards
- ❌ **NO** icono + título + texto dentro de una card bordeada

**Referencia visual:** El intranet real de Ineco — sidebar plana, secciones con títulos azul+línea, tiles simples con 1px border, cero sombras.

## Flujo completo (7 pasos)

### Paso 0: Obtener colores oficiales de la marca (SI hay manual de PDF)

Si la empresa tiene un **manual de marca en PDF**, extraer los colores oficiales de ahí ANTES de analizar screenshots. Los PDFs de manuales de marca suelen incluir: HEX, RGB, CMYK, y Pantone.

**Flujo de extracción de colores desde PDF:**

```bash
# 1. Descargar el PDF
curl -sL -o manual-marca.pdf "URL_DEL_PDF"

# 2. Extraer texto con pdftotext (si está disponible)
pdftotext manual-marca.pdf - | grep -i -E "pantone|rgb|hex|cmyk|color"

# 3. Fallback: PyMuPDF via venv (si pdftotext falla)
/opt/hermes/.venv/bin/python3 -c "
import fitz
doc = fitz.open('manual-marca.pdf')
for page in doc:
    text = page.get_text()
    # Buscar líneas con códigos de color
    for line in text.split('\n'):
        if any(k in line.lower() for k in ['pantone', 'rgb', 'hex', 'cmyk', 'color']):
            print(line)
"

# 4. Si el PDF es imagen (escaneado), renderizar y usar visión
/opt/hermes/.venv/bin/python3 -c "
import fitz
doc = fitz.open('manual-marca.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    pix.save(f'page_{i+1}.png')
    print(f'Guardado page_{i+1}.png')
"
# Luego vision_analyze en cada imagen
```

**Pitfall:** `pdftotext` del sistema puede no funcionar si faltan shared libraries (`libpoppler.so`). Usar PyMuPDF via el venv de Hermes: `/opt/hermes/.venv/bin/python3 -c "import fitz; ..."`.

**Pitfall:** `read_file()` de Hermes devuelve contenido CON números de línea (`1| contenido`). Si copias ese output a un archivo CSS, los números rompen el CSS. Solución: usar `open('archivo.css').read()` en Python directamente, o `cat` en terminal, NUNCA `read_file` para copiar contenido.

### Paso 1: Analizar imagen de referencia

Usar `vision_analyze` para extraer:
- **Colores exactos** (hex codes) — primarios, acento, neutros
- **Tipografía** — familias, tamaños, pesos
- **Layout** — sidebar, header, contenido, espaciados
- **Componentes** — tarjetas, botones, menús, tablas, badges
- **Bordes, sombras** — radio, elevation, separadores

```python
vision_analyze(
    image_url="path/to/screenshot.png",
    question="Analiza este intranet en detalle. Extrae: 1) Colores exactos (hex), 2) Tipografía, 3) Estructura de layout, 4) Estilo de componentes, 5) Bordes, sombras, espaciados."
)
```

**Regla:** Si hay manual de PDF → colores del PDF son fuente de verdad. La screenshot es solo para layout/componentes. NUNCA approximar colores de una screenshot — siempre extraer del PDF oficial si existe.

**Pitfall real:** En Kaizen Design System, los colores iniciales fueron approximados de la screenshot (#1a2c5c, #e2001a) en vez de extraerlos del PDF (#1A4488, #CB1823). El usuario notó la diferencia y pidió corregirlo.

### Paso 2: Definir paleta y tokens CSS

Crear `:root` con variables CSS organizadas por categoría:

```css
:root {
  /* Primarios */
  --ds-blue-900: #0d1b3e;
  --ds-blue-800: #1a2c5c;
  /* ...escala completa... */
  
  /* Acento */
  --ds-red-500: #e2001a;
  
  /* Neutros */
  --ds-gray-800: #333333;
  
  /* Superficies */
  --ds-surface: #ffffff;
  
  /* Bordes */
  --ds-border: #e6e6e6;
  
  /* Sombras */
  --ds-shadow: 0 1px 3px rgba(0,0,0,0.1);
  
  /* Tipografía */
  --ds-font-sans: 'Inter', sans-serif;
  
  /* Espaciado */
  --ds-space-4: 1rem;
  
  /* Bordes redondeados */
  --ds-radius: 0.375rem;
}
```

**Regla de naming:** Usar prefijo corto del proyecto (`--kz-` para Kaizen, `--ds-` genérico). NUNCA `--nz-` (eso es Aurora).

### Paso 3: Crear CSS con componentes

**Para herramientas de datos/dashboards**, consultar `references/componentes-data-tools.md` — checklist de 10 componentes que suelen faltar y que hay que añadir al extender un DS existente.

Estructura del archivo CSS:

```
1. Variables (tokens)
2. Reset & Base
3. Layout (container, grid, flex)
4. Sidebar
5. Header
6. Cards
7. Tiles/KPIs
8. Buttons
9. Forms
10. Tables
11. Badges
12. Alerts
13. Progress
14. Modal
15. Tabs
16. Dropdown
17. Tooltip
18. Utilities
19. App Shell (layout principal)
20. Footer
21. Print styles
```

**Componentes mínimos para un design system corporativo:**
- App shell (sidebar + main)
- Cards (básica, bordeada, con acento)
- Tiles/KPIs (con icono, label, value, change)
- Buttons (primary, secondary, accent, ghost, sm, lg)
- Forms (input, select, textarea, label, help, error)
- Tables (con filas alternas)
- Badges (primary, accent, success, warning, danger)
- Alerts (info, success, warning, danger)
- Progress bars
- Map container (para Leaflet/Mapbox)

### Paso 4: Crear index.html (galería de ejemplos)

HTML completo que muestre TODOS los componentes del design system:

- Paleta de colores con swatches
- Tipografía (todas las escalas)
- Botones (todas las variantes y tamaños)
- Cards y Tiles
- Formularios
- Tablas
- Badges y Alertas
- Progreso
- Contenedor de mapa
- Layout de dashboard completo (mini sidebar + contenido)
- Código de uso (CDN y estructura)

**Reglas del index.html:**
- Usar el CSS local: `<link rel="stylesheet" href="nombre.css">`
- Incluir Google Fonts (Inter recomendado)
- Secciones claras con títulos
- Ejemplos interactivos cuando sea posible
- Footer con atribución

### Paso 5: Crear AGENTS.md (crucial para IAs)

Archivo que las IAs leen ANTES de generar código. Debe incluir:

1. **Reglas obligatorias** — siempre enlazar CSS via CDN, nunca hardcodear
2. **Paleta de colores** — tabla con hex y uso
3. **Componentes principales** — ejemplos de código para cada uno
4. **Patrones de layout** — dashboard completo, visor de mapa
5. **Errores comunes** — qué NO hacer
6. **Prompt template** — listo para copiar y pegar
7. **Referencia rápida de clases** — tabla de todas las clases

**Tamaño objetivo:** 8-12 KB (~2500-3500 tokens). Suficiente para que la IA sepa todo, poco para no gastar contexto.

### Paso 6: Crear README.md

Documentación para humanos:
- Descripción del sistema
- Paleta de colores (tabla)
- Instalación (CDN, local, submodule)
- Uso con ejemplos de código
- Lista de componentes
- Guías de estilo para IA
- Changelog
- Licencia

### Paso 7: Crear repo GitHub y push

```bash
# Crear repo (privado por defecto para equipos)
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"name":"nombre-design-system","private":true}'

# Push
git remote add origin https://$GITHUB_TOKEN@github.com/ORG/repo.git
git push -u origin main
```

## ⚠️ Pitfall crítico: CSS no carga desde file:// 

**Problema:** Cuando el usuario abre `index.html` desde la máquina local (doble clic), el CSS externo (`href="nombre.css"`) **no carga** si el navegador tiene restricciones de seguridad con archivos locales.

**Solución:** SIEMPRE crear una versión standalone con CSS embebido:

```python
# Leer CSS
with open('nombre.css') as f: css = f.read()
# Leer HTML
with open('index.html') as f: html = f.read()
# Reemplazar enlace con style inline
standalone = html.replace(
    '<link rel="stylesheet" href="nombre.css">',
    f'<style>\n{css}\n</style>'
)
# Guardar
with open('index-standalone.html', 'w') as f: f.write(standalone)
```

**Resultado:** `index-standalone.html` funciona SIEMPRE, sin importar de dónde se abra.

## ⚠️ Pitfall crítico: read_file() corrompe CSS/HTML

**Problema:** `read_file()` de Hermes devuelve contenido CON números de línea al inicio de cada línea (`1| contenido`, `2| contenido`). Si se usa ese output para crear un archivo CSS o HTML, los números rompen el archivo.

**Síntomas:**
- CSS con `1| :root {` en vez de `:root {`
- HTML con `5| <html>` en vez de `<html>`
- El navegador no renderiza nada o muestra errores raros

**Solución:** NUNCA usar `read_file()` para copiar contenido entre archivos. Usar en su lugar:
- `open('archivo.css').read()` en Python
- `cat archivo.css` en terminal
- `patch()` para ediciones específicas

**Caso real:** Al actualizar colores en Kaizen Design System, el CSS quedó con 500 líneas numeradas. Se detectó porque el navegador mostraba números de línea como texto visible en la página.

## Estructura del repositorio

```
nombre-design-system/
├── nombre.css              # CSS principal (tokens + componentes)
├── index.html              # Galería de ejemplos (usa CSS externo)
├── index-standalone.html   # Versión con CSS embebido (funciona siempre)
├── AGENTS.md               # Guía para agentes de IA
├── README.md               # Documentación para humanos
├── LICENSE                  # MIT
└── .gitignore
```

## Prompt para usar el design system

Cuando un usuario pida crear una herramienta:

```
Usa el [Nombre] Design System para el estilo. Enlaza el CSS via CDN:
https://cdn.jsdelivr.net/gh/ORG/repo@master/nombre.css

Usa las clases [prefijo]-* para todos los componentes. Estilo profesional y limpio,
colores de [Empresa].
```

## CDN para equipos (share via jsDelivr)

Para que el equipo pueda usar el CSS sin clonar el repo:

```
https://cdn.jsdelivr.net/gh/ORG/repo@master/nombre.css
```

**Reglas:**
- Repo debe ser público para que jsDelivr funcione
- **Repos privados → jsDelivr retorna 404/502** — usar copia local del CSS
- Usar `@master` (no tag) hasta que se estabilice
- jsDelivr hace cache automático — cambios se propagan en ~1 min
- Para versionar: crear tag `v1.0.0` y usar `@v1.0.0`

**Pitfall real:** Kaizen Design System es privado → jsDelivr no puede servirlo. Solución: copiar `kaizen.css` directamente al proyecto y enlazarlo localmente.

**Prompt listo para pegar en herramientas del equipo:**
```
Enlaza el Kaizen Design System:
https://cdn.jsdelivr.net/gh/Ntizar/kaizen-design-system@master/kaizen.css

Estilo corporativo Ineco: azul #1A4488, rojo #CB1823. Usa clases kz-*.
```

## Personalización

Las variables CSS permiten cambiar la marca sin modificar componentes:

```css
:root {
  --ds-blue-800: #tu-color-oscuro;
  --ds-red-500: #tu-color-acento;
  --ds-font-sans: 'Tu Fuente', sans-serif;
}
```

## Relación con otras skills

- **`aurora-design-system`** → usa Aurora para dashboards personales/creativos. Para equipos/corporativo, crear design system propio con este skill.
- **`aurora-llm-optimization`** → optimiza un design system EXISTENTE para LLMs. Este skill CREA uno nuevo.
- **`popular-web-designs`** → 54 design systems de referencia para inspiración visual.
- **`liquid-glass-css`** → efecto glass para proyectos personales, no para corporativo.
