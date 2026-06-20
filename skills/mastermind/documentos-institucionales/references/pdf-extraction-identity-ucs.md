# PDF Extraction — Identity-UCS & Custom Font Encodings

## Problem

PDFs con fuentes embebidas (TTF CIDFonts) que usan CMaps personalizados o corruptos. PyMuPDF no disponible.

## Técnica: Identity-UCS con shift detection

### Paso 1 — Buscar ToUnicode CMap

```python
import re, zlib

data = open(pdf_path, 'rb').read()

# Encontrar referencias ToUnicode
to_unicode_refs = re.findall(rb'/ToUnicode\s+(\d+)\s+(\d+)\s+R', data)

# Extraer y leer cada ToUnicode stream
for ref_num, ref_gen in to_unicode_refs:
    obj_pattern = ref_num + rb'\s+' + ref_gen + rb'\s+obj'
    obj_match = re.search(obj_pattern, data)
    if obj_match:
        stream_match = re.search(rb'stream\n', data[obj_match.start():])
        if stream_match:
            stream_start = obj_match.start() + stream_match.end()
            end = data.find(b'\nendstream', stream_start)
            if end == -1: end = data.find(b'endstream', stream_start)
            if end == -1: continue
            raw = data[stream_start:end]
            try:
                decoded = zlib.decompress(raw)
            except:
                decoded = raw  # no comprimido
            print(decoded.decode('latin-1', errors='replace'))
```

### Paso 2 — Extraer CIDs de streams de contenido

```python
# Buscar streams comprimidos con BT/ET
for m in re.finditer(rb'stream\n', data):
    start = m.end()
    end = data.find(b'\nendstream', start)
    if end == -1: end = data.find(b'endstream', start)
    if end == -1: continue
    raw = data[start:end]
    try:
        decoded = zlib.decompress(raw)
    except:
        continue
    if b'BT' not in decoded:
        continue

    # Extraer hex strings de TJ arrays: <XXXX> <number>
    hex_pattern = rb'<([0-9A-Fa-f]+)>\s*([-+]?\d+\.?\d*)'
    hex_ops = re.findall(hex_pattern, decoded)
    cids = [int(h, 16) for h, _ in hex_ops]
    unique_cids = set(cids)

    # Filtrar: necesita al menos 3 CIDs únicos
    if len(unique_cids) < 3:
        continue

    # Identity-UCS: CIDs son Unicode directos
    chars = []
    for cid in cids:
        if 0x20 <= cid <= 0x7E:
            chars.append(chr(cid))
        elif 0xA0 <= cid <= 0xFFFF:
            chars.append(chr(cid))
        elif cid == 3:
            chars.append(' ')
    result = ''.join(chars)
```

### Paso 3 — Detectar shift sistemático

Si el texto no es legible, probar shifts:

```python
# Probar shifts de -5 a +5
for shift in range(-10, 11):
    chars = []
    for cid in cids:
        if 0x20 <= cid <= 0x7E:
            decoded_char = chr(cid + shift)
            if decoded_char.isalpha() or decoded_char in 'áéíóúñü ':
                chars.append(decoded_char)
            else:
                chars.append('?')
    result = ''.join(chars)
    # Verificar legibilidad
    alpha_ratio = sum(1 for c in result if c.isalpha()) / len(result)
    if alpha_ratio > 0.7 and len(result) > 20:
        print(f"Shift {shift:+d}: {result[:100]}")
```

### Paso 4 — Decodificación final

```python
def decode_pdf_text(cids, shift=0, skip_control=True):
    """Decode PDF CIDs to text with optional shift."""
    chars = []
    for cid in cids:
        if skip_control and cid < 0x20:
            if cid == 3:  # space
                chars.append(' ')
            continue
        if 0x20 <= cid <= 0x7E:
            chars.append(chr(cid - shift))
        elif 0xA0 <= cid <= 0xFFFF:
            chars.append(chr(cid - shift))
        else:
            chars.append('?')
    return ''.join(chars)
```

## Casos reales

### Caso: CCAA 2025 — TETUAN RESIDENCES SCM

- **PDF:** Informes de cuentas de cooperativa
- **Problema:** CMap TTF corrupto (443 subtables con datos basura)
- **ToUnicode:** Solo mapea CID 3 → espacio (0x0020)
- **CIDs encontrados:** 37 únicos, mayoría en rango ASCII (0x20-0x79)
- **Pattern descubierto:** Shift de -3 para mayúsculas (A-Z)
  - CID 72 (H) → E (69), CID 70 (F) → C (67), CID 82 (R) → O (79)
  - CID 68 (D) → A (65), CID 83 (S) → P (80)
- **Excepciones:** 
  - CID 54 (6) → S (83) en "SOCIEDAD" (dígito codificado diferente)
  - CID 38 (&) → C (67) en "COOPERATIVA"
  - Caracteres acentuados: mapeo especial (y→Ó, p→é)
  - Control chars: 0x000F, 0x0010, 0x0011, 0x001D → ignorar

### Verificación

Si el texto decodificado contiene palabras reconocibles en el idioma esperado → mapeo correcto.
