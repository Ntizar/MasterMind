# Patrones de parsing para presupuestos de construccion españoles (Presto/CYPE)

## Contexto de la sesion (2026-06-17)

Proyecto Nogal 9: 9 viviendas + trasteros, Calle Nogal 9, 28039 Madrid.
PDF de 336 paginas generado por CYPE Ingenieros - Arquímedes.

## Estructura del PDF CYPE Arquímedes

- **Pagina 1:** "Presupuesto y medición" (resumen minimo)
- **Paginas 2-335:** Detalle de cada presupuesto parcial
- **Pagina 336:** Resumen final con totales por capitulo

### Cabeceras de capitulo (reconocimiento)
```
Presupuesto parcial nº 1 MOVIMIENTO DE TIERRAS
Presupuesto parcial nº 2 INSTALACION DE SANEAMIENTO
...
```

### Formato de partidas
```
1.1  m23E02AM010  m2  Desbroce y limpieza superficial...
Uds.  Largo  Ancho  Alto  Subtotal
197,80          197,80
Total m2 ............:  197,80  0,48  94,94
```

### Resumen final (pagina 336)
```
1. MOVIMIENTO DE TIERRAS .............................… 873,19
2. INSTALACION DE SANEAMIENTO ........................… 8.687,36
...
Total: 523.705,00
Asciende el presupuesto de ejecución material a la expresada cantidad de
QUINIENTOS VEINTITRES MIL SETECIENTOS CINCO 2.
```

## Regex para parsing

### Resumen de capitulos (pagina final)
```python
import re
# "1. MOVIMIENTO DE TIERRAS .............................… 873,19"
pattern = r'(\d+)\.\s+(.+?)\.{2,}…?\s+([\d.,]+)'
```

### Cabecera de capitulo
```python
pattern = r'Presupuesto parcial nº\s+(\d+)\s+(.+)'
```

### Conversion de importes espanoles
```python
# "1.234,56" → 1234.56
amount = float(str.replace('.', '').replace(',', '.'))
```

## Herramienta recomendada

**pdfplumber** (no PyMuPDF/fitz) — funciona mejor con CYPE:
```bash
/opt/hermes/.venv/bin/python3 -c "
import pdfplumber
with pdfplumber.open('archivo.pdf') as pdf:
## Herramienta recomendada

**pdfplumber** (no PyMuPDF/fitz) — funciona mejor con CYPE:
```bash
# pdfplumber ya instalado en /opt/hermes/.venv (NO requiere pip)
/opt/hermes/.venv/bin/python3 -c "import pdfplumber; print('ok')"
```

> **Pitfall:** pdfplumber necesita el venv de Hermes (`/opt/hermes/.venv/bin/python3`). No funciona con el python3 del sistema porque no tiene pip instalado.

## Patrones de ofertas de constructoras (Trevicon, etc.)

Los PDFs de ofertas suelen tener estructura diferente al PEM base:

### Estructura tipo Trevicon
- **Pagina 1:** Portada (datos empresa, expediente, fecha)
- **Pagina 2-3:** Resumen con capitulos + totales + IVA + total contrata
- **Pagina 4-N:** Detalle de partidas

### Parsing de resumen de oferta
```python
# "01 MOVIMIENTO DE TIERRAS 1.863,37 0,17"
pattern = r'(\d{2})\s+(.+?)\s+([\d.,]+)\s+([\d.,]+)'
# Captura: codigo(2 dig), nombre, importe, porcentaje

# Totales
total_match = re.search(r'TOTAL EJECUCIÓN MATERIAL\s+([\d.,]+)', text)
iva_match = re.search(r'%\s*I\.?V\.?A\.?\s+([\d.,]+)', text)
contrata_match = re.search(r'TOTAL PRESUPUESTO CONTRATA\s+([\d.,]+)', text)
```

### Diferencias clave CYPE vs ofertas constructoras
| Caracteristica | CYPE PEM | Oferta constructora |
|---|---|---|
| Cabecera capitulo | "Presupuesto parcial nº X" | "CAPÍTULO X" |
| Resumen | Ultima pagina | Pagina 2-3 |
| Formato codigo cap | `Cap-1`, `Cap-2` | `Cap-01`, `Cap-02` |
| Indirectos/Generales/Beneficio | No incluidos | A veces separados (28, 29, 30) |
| IVA | No incluido | Incluido en total |

## Referencia: Nogal 9

- Repo: github.com/Ntizar/nogal9
- JSON referencia: presupuesto_referencia.json
- Total: 523.705,00 €
- 27 capitulos, 1153 lineas de JSON
- Oferta Trevicon: 1.098.001,21€ (+109,7%)
