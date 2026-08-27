#!/usr/bin/env python3
"""extract-accounts.py — Convierte Excel de Salesforce (XLSX) a JSON para Control-M Account Intelligence."""
import zipfile
import xml.etree.ElementTree as ET
import json
import sys
import os

def extract_strings(xf):
    try:
        ss_xml = xf.read('xl/sharedStrings.xml').decode('utf-8')
        root = ET.fromstring(ss_xml)
        ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        strings = {}
        for i, e in enumerate(root.findall('.//ss:t', ns)):
            if e.text:
                strings[i] = e.text.strip()
        return strings
    except Exception as e:
        print(f"⚠ Warning: No se pudo leer sharedStrings: {e}", file=sys.stderr)
        return {}

def read_sheet(xf, sheet_name='sheet1'):
    try:
        sheet_path = f'xl/worksheets/{sheet_name}.xml'
        s1_xml = xf.read(sheet_path).decode('utf-8')
        root = ET.fromstring(s1_xml)
        ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        rows = []
        for row in root.findall('.//ss:row', ns):
            cells = []
            for c in row.findall('ss:c', ns):
                v_elem = c.find('ss:v', ns)
                t = c.get('t', '')
                val = v_elem.text if v_elem is not None else ''
                if t == 's' and val.isdigit():
                    idx = int(val)
                    val = strings.get(idx, val)
                cells.append(val)
            if cells:
                rows.append(cells)
        return rows
    except Exception as e:
        print(f"⚠ Error leyendo {sheet_name}: {e}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 extract-accounts.py <archivo.xlsx> [--output output.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    if not os.path.exists(input_file):
        print(f"⚠ Error: {input_file} no existe")
        sys.exit(1)
    
    if output_file is None:
        output_file = os.path.join(
            os.path.dirname(os.path.abspath(input_file)),
            os.path.basename(input_file).replace('.xlsx', '.json')
        )
    
    print(f"📂 Leyendo: {input_file}")
    
    with zipfile.ZipFile(input_file, 'r') as xf:
        global strings
        strings = extract_strings(xf)
        print(f"📝 Strings compartidos: {len(strings)}")
        
        rows = read_sheet(xf, 'sheet1')
        print(f"📊 Filas totales: {len(rows)}")
    
    if not rows:
        print("⚠ Error: No se leyeron filas. Verifica que el Excel tenga datos.")
        sys.exit(1)
    
    headers = rows[0]
    print(f"📋 Headers: {headers}")
    
    accounts = []
    seen_names = set()
    for row in rows[1:]:
        vals = row + [''] * (len(headers) - len(row))
        acct = dict(zip(headers, vals))
        name = acct.get('Account', '').strip().upper()
        if not name or name in seen_names:
            continue
        seen_names.add(name)
        accounts.append(acct)
    
    print(f"\n✅ Cuentas únicas: {len(accounts)}")
    
    prospectable = [a for a in accounts if a.get('Tier', '').startswith(('A', 'B', 'C', 'D'))]
    spain = [a for a in prospectable if a.get('Country', '') == 'Spain']
    spain.sort(key=lambda x: float(x.get('Score', 0)), reverse=True)
    
    print(f"🎯 Prospectables: {len(prospectable)}")
    print(f"🇪🇸 España: {len(spain)}")
    
    from collections import Counter
    tier_counts = Counter(a.get('Tier', '') for a in spain)
    print("\n📊 Por Tier:")
    for tier, cnt in sorted(tier_counts.items()):
        print(f"   {tier}: {cnt}")
    
    output = []
    for a in spain:
        output.append({
            'tier': a.get('Tier', ''),
            'score': a.get('Score', ''),
            'account': a.get('Account', ''),
            'country': a.get('Country', ''),
            'segment': a.get('Segment', ''),
            'subsegment': a.get('SubSegment', ''),
            'fit_subsegmento': a.get('Fit_SubSegmento', ''),
            'top_enterprise': a.get('Top_Enterprise', ''),
            'cliente_actual': a.get('Cliente_Actual', ''),
            'en_curso': a.get('En_Curso', ''),
            'aproximacion_notas': a.get('Aproximación / Notas', ''),
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado: {output_file}")
    print(f"📊 Cuentas España escritas: {len(output)}")

if __name__ == '__main__':
    main()
