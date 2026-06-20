---
name: budget-comparison
description: >
  Extraer, estructurar y comparar presupuestos de obra (PEMs) de construccion
  generados en PDFs (CYPE Arquimedes, Presto). Comparar oferta de constructora
  contra presupuesto base de ejecucion material. Generar informes y herramientas
  HTML interactivas.
version: "1.1.0"
tags: [presupuesto, construccion, CYPE, Presto, comparacion, PDF, obra]
---

# Budget Comparison — Extraccion y comparacion de presupuestos de obra

## Cuándo usarlo

- El usuario adjunta un PDF de presupuesto de obra (PEM) y quiere compararlo
- El usuario pide \"comparar presupuestos\", \"detectar diferencias entre ofertas\"
- Hay un presupuesto base (proyecto) y una/multiple ofertas de constructoras
- Se necesita extraer datos estructurados de PDFs de construccion (300+ paginas)

## No es para

- Informes institucionales/regulatorios (usar `documentos-institucionales`)
- Presupuestos de software/IT (usar `pdf-to-dashboard`)
- Analisis de facturas (usar `liteparse-rust-pdf-ocr`)

## Flujo de trabajo

### Paso 1: Extraer presupuesto base (referencia)

```python
import pdfplumber

# PDF CYPE Arquimedes — estructura fija:
# Pagina 1: resumen minimo
# Paginas 2-N-1: detalle de partidas
# Pagina N (ultima): resumen final con totales

with pdfplumber.open(pdf_path) as pdf:
    # Extraer resumen final (ultima pagina)
    page = pdf.pages[-1]
    text = page.extract_text()
    
    # Parsear capitulos: "1. MOVIMIENTO DE TIERRAS .............................… 873,19"
    pattern = r'(\d+)\.\s+(.+?)\.{2,}…?\s+([\d.,]+)'
    
    # Extraer detalle (paginas intermedias)
    for i in range(1, len(pdf.pages) - 1):
        page = pdf.pages[i]
        text = page.extract_text()
        tables = page.extract_tables()
```

### Paso 2: Extraer oferta de constructora

Los PDFs de ofertas suelen tener estructura diferente:

- **Pagina 1:** Portada (datos empresa, expediente, fecha)
- **Pagina 2-3:** Resumen con capitulos + totales + IVA + total contrata
- **Pagina 4-N:** Detalle de partidas

```python
# Resumen de oferta (pagina 2-3)
page2 = pdf.pages[1]
page3 = pdf.pages[2]
text2 = page2.extract_text()
text3 = page3.extract_text()

# Pattern: "01 MOVIMIENTO DE TIERRAS 1.863,37 0,17"
pattern = r'(\d{2})\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)'

# Totales
total_match = re.search(r'TOTAL EJECUCION MATERIAL\s+([\d.,]+)', text)
iva_match = re.search(r'%\s*I\.?V\.?A\.?\s+([\d.,]+)', text)
contrata_match = re.search(r'TOTAL PRESUPUESTO CONTRATA\s+([\d.,]+)', text)
```

### Paso 3: Normalizar y comparar

**⚠️ Normalizacion de claves:** CYPE usa `Cap-1`, `Cap-2`... ofertas Presto usan `Cap-01`, `Cap-02`.

```python
# Normalizar claves para matching
def normalize_key(key):
    # Extraer numero de capitulo
    num = re.search(r'(\d+)', key)
    if num:
        return f"Cap-{num.group(1).zfill(2)}"
    return key

# Comparar por capitulo
for ref_key, ref_data in referencia['capitulos'].items():
    offer_key = normalize_key(ref_key)
    if offer_key in oferta['capitulos']:
        diff = oferta['capitulos'][offer_key]['total'] - ref_data['total']
        diff_pct = (diff / ref_data['total'] * 100) if ref_data['total'] > 0 else 0
    else:
        diff = ref_data['total']  # capitulo eliminado en oferta
        diff_pct = -100
```

### Paso 4: Generar herramienta HTML

Crear un HTML autocontenido con:
- Tabla comparativa con filtros y ordenacion
- Grafico de barras (referencia vs oferta + diferencias)
- Ranking de capitulos por mayor diferencia
- Detalle de partidas

## Patrones de parsing por herramienta

### CYPE Arquimedes
- Cabeceras: "Presupuesto parcial nº X NOMBRE" o "CAPÍTULO X NOMBRE"
- Resumen final en la ÚLTIMA pagina del PDF
- Formato: `Cap-1`, `Cap-2`...
- Partidas con codigos alfanumericos largos (ej: `m23E02AM010`)
- Subpartidas con referencias de planos (VC.T-2.1 [P16-P15])

### Presto
- Cabeceras: "CAPÍTULO X NOMBRE" con ceros a la izquierda (01, 02...)
- Formato: `Cap-01`, `Cap-02`...
- Resumen en paginas 2-3

### Presto moderno (GLAM-style) — Tablas rotas + extract_words por coordenadas X

**Problema:** Algunos PDFs Presto modernos tienen tablas donde la fila del capítulo entero está en una sola celda. `extract_tables()` devuelve filas con todo el texto junto y las columnas vacías.

**Solución:** Usar `extract_words()` con coordenadas X para mapear columnas:

```python
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        words = page.extract_words()
        
        # Agrupar palabras por linea Y
        lines = {}
        for w in words:
            y_key = round(w['top'], 0)
            if y_key not in lines:
                lines[y_key] = []
            lines[y_key].append(w)
        
        for y_key in sorted(lines.keys()):
            line_words = sorted(lines[y_key], key=lambda w: w['x0'])
            
            # Detectar linea de capítulo (tiene "Capítulo")
            if 'Capítulo' not in [w['text'] for w in line_words]:
                continue
            
            # Columnas conocidas:
            # Código: x~52 | Nat: x~109 | Ud: x~129 | Resumen: x~258
            # CanPres: x~409 | PrPres: x~453 | ImpPres: x~501
            
            # Extraer código (primera palabra)
            code = line_words[0]['text']
            
            # Extraer nombre (entre "Capítulo" y x~400)
            name_words = [w['text'] for w in line_words 
                         if w['text'] != 'Capítulo' and w['x0'] < 400]
            name = ' '.join(name_words)
            
            # Extrair total (ImpPres: x >= 500)
            imp_words = [w for w in line_words 
                        if w['x0'] >= 500 and w['text'] != '€']
            if imp_words:
                imp_str = ''.join(w['text'] for w in imp_words)
                total = parse_es_amount(imp_str)
```

> **Pitfall:** Los números españoles "2.041,83" se extraen como una sola palabra. Pero números con más de 4 dígitos como "2 0.316,59" se separan en palabras distintas ("2", "0.316,59"). Hay que concatenar todas las palabras en la columna ImpPres ANTES de parsear.

### ⚡ CRÍTICO: Regex para extraer precios — el bug del split numérico

**Problema:** El regex `([\d\s.,]+)\s*€` captura partes incorrectas cuando el número tiene espacios internos. Ejemplo:

```
LÍNEA: "01 Capítulo MOVIMIENTO DE TIERRAS 1,00 2.041,83 € 2.041,83 €"
price_parts = [' 1,00 2.041,83 ', ' 2.041,83 ']
# Si concatenas las dos últimas partes: "1,00 2.041,832.041,83" → parse error
```

**Solución (PROMOVER):** Usar el ÚLTIMO valor antes del último `€`, no concatenar partes:

```python
# CORRECTO: encontrar el último € y tomar todo lo que hay antes
last_euro_idx = rest.rfind('€')
before_last_euro = rest[:last_euro_idx].strip()
num_match = re.search(r'([\d][\d\s.,]*)$', before_last_euro)
num_str = num_match.group(1).strip()
clean = num_str.replace(' ', '').replace('.', '').replace(',', '.')
total = float(clean)
```

> **Por qué funciona:** En Presto, la columna `ImpPres` (importe total) siempre es el último valor antes del último `€`. No necesitas concatenar partes — solo tomar el último número.

> **Pitfall alternativo:** Si usas `extract_words()` por coordenadas X, los números se extraen como palabras individuales. En ese caso sí necesitas concatenar palabras adyacentes en la columna ImpPres.

## ⚠️ CRÍTICO: Validación del total extraído

**Problema frecuente:** La suma de TODAS las líneas de "Capítulo" extraídas da un número MUY superior al Presupuesto General del documento. Esto ocurre porque:

1. **Padres e hijos duplicados:** Presto tiene capítulos padre (ej: `SAN.07.01`) que incluyen sus hijos (`SAN.07.01.01`, `.02`, `.03`). Si sumas todo, los duplicas.
2. **Complementos de materiales incluidos:** `CA` (Micropilotes), `EA` (Acero), `EH` (Hormigón armado) están incluidos en capítulos 03, 04, 05. No se suman aparte.
3. **Instalaciones dentro de capítulos:** ELE, FON, TEL, TER, VMC están DENTRO de los capítulos numéricos (13, 15, 14, 17, 18). No son capítulos independientes.

**Procedimiento de validación (PASO OBLIGATORIO):**

1. **Siempre leer el total del documento primero:**
   ```python
   # Última página del PDF — buscar "PRESUPUESTO_P" o "PRESUPUESTO GENERAL"
   last_page = pdf.pages[-1]
   text = last_page.extract_text()
   # Buscar línea con "PRESUPUESTO_P" o "PRESUPUESTO GENERAL"
   total_match = re.search(r'PRESUPUESTO[_\s]*(?:GENERAL)?[_\s]*P?\s+[\d\s.,]+\s*€', text)
   documento_total = extract_total_from_line(last_page, text)
   ```

2. **Extraer TODAS las líneas de "Capítulo"** (sin filtrar).

3. **Identificar padres e hijos:**
   - Un código es hijo si otro código en la lista empieza con `codigo + '.'`
   - Ej: `SAN.07.01.01` es hijo de `SAN.07.01`

4. **Para cada grupo padre-hijos, decidir cuál usar:**
   - Si `padre ≈ hijos` (ratio 0.9-1.1): usar padre (incluye hijos)
   - Si `hijos > padre * 1.1`: usar hijos (padre es sección, no total)
   - Si `padre < hijos < padre * 1.1`: usar padre (es resumen parcial)
   - **⚠️ Si `padre > hijos`: el padre puede incluir MÁS cosas no listadas** → usar padre

5. **Sumar solo los capítulos seleccionados** y comparar con `documento_total`.
   - Si la diferencia es < 1% → correcto.
   - Si no, revisar qué capítulos sobran o faltan.

**⚠️ Pitfall avanzado:** Algunos padres tienen ratio ~0.6 (ej: SAN.07.01 = 20.316 € vs hijos = 12.373 €). Esto significa que el padre es un resumen PARCIAL que no incluye todos los hijos. En este caso, usar el padre (es el valor oficial del capítulo).

**⚠️ Pitfall avanzado 2:** Algunos padres tienen ratio > 1.5 (ej: 25 = 3.589 € vs hijos = 36.906 €). Esto significa que el padre es un NOMBRE DE SECCIÓN, no un total. Los hijos son los capítulos reales. Usar hijos.

**⚠️ Pitfall avanzado 3:** En Presto moderno, TODOS los códigos pueden ser "hijos" de algún otro código (ej: "03.04.01" no es hijo de "01" aunque contiene "01"). La función `is_child()` debe verificar `code.startswith(other + '.')` EXACTO, no solo contiene.

**Patrón común en Presto/GLAM:**
- Capítulos principales: `01` a `27` (obra civil, acabados, instalaciones incluidas)
- SAN.07.01 puede estar fuera de los capítulos numéricos (saneamiento de red)
- ELE.03.01-07 están dentro del capítulo 13
- FON.02.01.01-05 están dentro del capítulo 15
- TEL.10.01-04 están dentro del capítulo 14
- TER.01.01-05 están dentro del capítulo 17
- VMC.09.01.01-03 + VMC09.02 están dentro del capítulo 18
- CA, EA, EH son complementos de materiales (excluir)

### Herramienta recomendada

**pdfplumber** (no PyMuPDF/fitz) — funciona mejor con CYPE:
```bash
/opt/hermes/.venv/bin/python3 -c "import pdfplumber; print('ok')"
```

> **Pitfall:** pdfplumber necesita el venv de Hermes (`/opt/hermes/.venv/bin/python3`). No funciona con el python3 del sistema.

## ⚠️ CRÍTICO: GLAM puede ser igual al CYPE/Dmarche

**Problema frecuente:** El presupuesto de GLAM (constructora) tiene los mismos importes base que el CYPE/Dmarche (proyecto básico). Esto ocurre porque GLAM usa los mismos precios base del proyecto.

**Solución:** NO asumir que GLAM siempre tiene importes diferentes al CYPE. Verificar siempre con la extracción real del PDF.

**Regla:** El comparador debe mostrar SIEMPRE las 3 columnas: Referencia (Dmarche/CYPE), Constructora 1 (GLAM), Constructora 2 (Trevicon/u otra). NO eliminar ninguna columna automáticamente. El usuario decide qué significa cada una.

## Flujo actualizado — Comparador tripartito (caso Nogal 9)

**Arquitectura de datos:** Un solo JSON unificado con las 3 fuentes:

```json
{
  "proyecto": "NOM PROYECTO",
  "localizacion": "Madrid",
  "referencia": {
    "nombre": "Dmarche (CYPE - Proyecto Base)",
    "tipo": "PEM",
    "total": 1218453.83,
    "capitulos": { "01": {"nombre": "...", "total": 2041.83}, ... }
  },
  "ofertas": {
    "glam": {
      "nombre": "GLAM (Constructora)",
      "total": 1218453.83,
      "capitulos": { "01": {"nombre": "...", "total": 2041.83}, ... }
    },
    "trevicon": {
      "nombre": "Trevicon (Constructora)",
      "total": 1098001.21,
      "capitulos": { "01": {"nombre": "...", "total": 1863.37}, ... }
    }
  }
}
```

**JSON de comparaciones (resumen capítulo a capítulo):**
```json
[
  {
    "codigo": "01",
    "nombre": "MOVIMIENTO DE TIERRAS",
    "referencia": 2041.83,
    "glam": 2041.83,
    "trevicon": 1863.37,
    "diff_glam_pct": 0.0,
    "diff_trevicon_pct": -8.7
  },
  ...
]
```

**HTML del comparador — 4 tabs obligatorias:**

1. **📊 Tabla Completa** — Tabla con todas las columnas + búsqueda + filtros (todos/subidas/bajadas)
2. **📈 Diferencias Constructora 1** — Gráfico de barras horizontal top 10 diferencias
3. **📈 Diferencias Constructora 2** — Igual para la segunda constructora
4. **📋 Resumen** — Stats por constructora (capítulos iguales/diferentes, totales, % diff)

**KPIs en hero (4 cards):**
- Referencia total
- Constructora 1 total + % vs Ref
- Constructora 2 total + % vs Ref
- Diferencia entre constructoras (€ y %)

**Diseño:** Aurora Design System con glass-liquid, mesh animado, orbs, responsive, fondo claro.

## ⚠️ CRÍTICO: El HTML del comparador — estructura de tabs

Cuando generes el HTML del comparador:

1. **4 tabs:** Tabla completa, diffs Constructora 1, diffs Constructora 2, Resumen
2. **Tabla con filtros:** búsqueda por texto, filtros por tipo de diferencia (subidas/bajadas/todos)
3. **Gráficos de barras:** Top 10 diferencias por constructora, barras horizontales con colores (verde=bajada, roja=subida)
4. **KPIs glass-liquid:** 4 cards en hero con totales y porcentajes
5. **Alertas automáticas:** Detectar GLAM=Referencia, diferencias >10%, constructora más barata
6. **Hash navigation:** `#tabla`, `#glam`, `#trev`, `#resumen` para deep-linking
7. **Responsive:** KPIs grid 4→2→1 columnas, tabla con scroll horizontal

### Multiplicador uniforme
Si todos los capitulos de instalaciones suben un ~142%, es probablemente un **recargo estandar** (indirectos + generales + beneficio).

### Diferencias por tipo de capitulo
| Tipo | Incremento tipico | Causa |
|------|-------------------|-------|
| Instalaciones (fontaneria, electricidad) | ~142% | Multiplicador indirectos |
| Estructurales (albañileria, cimentacion) | ~109-128% | Precios de mercado |
| Acabados (revestimientos, pinturas) | ~16-38% | Diferentes calidades |

### Alertas a detectar
- Capitulos completos que faltan en la oferta
- Partidas con diferencia > 50% (revisar mediciones)
- Oferta significativamente menor al PEM base (< 90%)
- Partidas que han sido eliminadas o divididas

## Conversion de importes espanoles

```python
# \"1.234,56\" → 1234.56
def parse_es_amount(s):
    return float(str(s).replace('.', '').replace(',', '.'))

# 1234.56 → \"1.234,56\"
def format_es_amount(n):
    return f\"{n:,.2f}\".replace(',', 'X').replace('.', ',').replace('X', '.')
```

## ⚠️ Post-extracción: Verificación y limpieza de JSON

Después de extraer los datos del PDF y generar los JSON derivados, SIEMPRE ejecutar verificación antes de dar por bueno el resultado. Los JSON derivados son propensos a errores acumulados.

### Problemas comunes detectados

1. **Floating point artifacts**: `921275.5999999999` en vez de `1098001.21`. Solución: `round(value, 2)` en todos los totales al escribir.
2. **Nombres con cantidades embebidas**: `"CIMENTACION 108.327,64 €"` en vez de `"CIMENTACION"`. Solución: regex para limpiar `re.sub(r'\s+[\d]{1,3}(?:\.[\d]{3})*,[\d]{2}\s*€?\s*$', '', name)`.
3. **Mapeo de capítulos inconsistente**: GLAM tiene `SAN.07.01` pero Trevicon tiene `02` para el mismo saneamiento. Solución: establecer mapeo explícito y usar la referencia como canonical.
4. **Totales que no cuadran**: La suma de capítulos difiere del total declarado. Solución: SIEMPRE verificar `sum(chapters) ≈ total` con tolerancia < 1€.
5. **Referencia vieja**: Se compara contra un presupuesto anterior (ej: 523.705€ de CYPE viejo) en vez del actual (1.218.453,83€ de GLAM). Solución: verificar que la referencia es la correcta antes de generar comparaciones.
6. **Capítulos duplicados**: Cap.02 y SAN.07.01 cuentan el mismo saneamiento dos veces. Solución: unificar en un solo registro usando la clave de la referencia.
7. **Capítulos con total=0**: Parsing falló para ciertos capítulos. Solución: reconstruir desde el JSON fuente (`presupuesto_referencia.json`) que tiene la fuente de verdad.

### Procedimiento de verificación (PASO OBLIGATORIO)

```python
import json

# 1. Cargar fuente de verdad
with open('presupuesto_referencia.json') as f:
    src = json.load(f)

ref = src['referencia']
glam = src['ofertas']['glam']
trev = src['ofertas']['trevicon']

# 2. Verificar sumas
for name, data in [('Ref', ref), ('GLAM', glam), ('Trevicon', trev)]:
    chapters_sum = sum(ch['total'] for ch in data['capitulos'].values())
    diff = abs(chapters_sum - data['total'])
    status = "✅" if diff < 1.0 else f"❌ diff={diff:.2f}"
    print(f"{name}: sum={chapters_sum:.2f} total={data['total']:.2f} {status}")

# 3. Detectar capítulos con total=0
for name, data in [('GLAM', glam), ('Trevicon', trev)]:
    zeros = [k for k, v in data['capitulos'].items() if v['total'] == 0]
    if zeros:
        print(f"⚠️  {name} chapters with total=0: {zeros}")

# 4. Reconstruir comparaciones desde fuente de verdad
all_caps = list(ref['capitulos'].keys())  # canonical order
comparaciones = []
for cap in all_caps:
    ref_val = ref['capitulos'][cap]['total']
    glam_val = glam['capitulos'].get(cap, {}).get('total', 0)
    # Mapeo explícito: SAN.07.01 ↔ 02
    if cap == 'SAN.07.01':
        trev_val = trev['capitulos'].get('02', {}).get('total', 0)
    else:
        trev_val = trev['capitulos'].get(cap, {}).get('total', 0)
    
    comparaciones.append({
        'codigo': cap,
        'nombre': ref['capitulos'][cap]['nombre'],
        'referencia': ref_val,
        'glam': glam_val,
        'trevicon': trev_val,
        'diff_glam_pct': round((glam_val - ref_val) / ref_val * 100, 1) if ref_val else None,
        'diff_trevicon_pct': round((trev_val - ref_val) / ref_val * 100, 1) if ref_val else None
    })

# 5. Verificar que las comparaciones suman correctamente
ref_s = sum(c['referencia'] for c in comparaciones)
glam_s = sum(c['glam'] for c in comparaciones)
trev_s = sum(c['trevicon'] for c in comparaciones)
assert abs(ref_s - ref['total']) < 0.01, f"Ref mismatch: {ref_s} vs {ref['total']}"
assert abs(glam_s - glam['total']) < 0.01, f"GLAM mismatch: {glam_s} vs {glam['total']}"
assert abs(trev_s - trev['total']) < 0.01, f"Trev mismatch: {trev_s} vs {trev['total']}"
```

### Regla de oro: un solo JSON fuente

Cuando existen múltiples JSON derivados (comparaciones, comparacion_final, comparacion_triptica, etc.), NUNCA arreglar cada uno por separado. En su lugar:

1. Verificar y limpiar SOLO el JSON fuente (`presupuesto_referencia.json`)
2. Reconstruir todos los derivados programáticamente desde la fuente
3. Verificar sumas en todos los derivados
4. Commitear todo junto

Esto garantiza consistencia y evita el "drift" entre archivos.

## Referencias

- `references/budget-parsing-patterns.md` — Patrones de parsing para presupuestos de construccion españoles (CYPE, Presto)
- `references/budget-comparison-workflow.md` — Flujo de comparacion de ofertas con caso real Nogal 9
- `references/presto-word-extraction.md` — Patrón para extraer tablas Presto rotas con coordenadas X
- `references/presto-total-validation.md` — Validación del total extraído: padres/hijos, complementos materiales, instalaciones incluidas (caso GLAM Nogal9)
- `references/github-pages-private-workaround.md` — Workaround para GitHub Pages en repos privados (cuenta free)
- `references/estructura-datos-unificada.md` — Estructura JSON unificada con 3 fuentes (referencia + 2 constructoras) y comparaciones capítulo a capítulo
- `references/json-verification-patterns.md` — Problemas comunes en JSON derivados de presupuestos y procedimiento de verificación/limpieza
- `pdf-to-dashboard` — Extraccion general de PDFs y generacion de dashboards HTML
