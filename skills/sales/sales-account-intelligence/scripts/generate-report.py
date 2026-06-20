#!/usr/bin/env python3
"""generate-report.py — Genera informes HTML/PDF de Account Intelligence para Control-M."""
import json
import os
import sys
import re
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
REPORTS_DIR = os.path.join(SCRIPT_DIR, 'reports')
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, 'template.html')
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')

def get_verdict(tier, score, notes):
    if 'EN CURSO' in notes.upper() or 'en curso' in notes.lower():
        return "OPORTUNIDAD EN CURSO — Coordinar con comercial asignado"
    if tier.startswith('A') and score >= 9:
        return "OPORTUNIDAD HIGH PRIORITY — Prioridad máxima de acción"
    if tier.startswith('A') and score >= 7:
        return "OPORTUNIDAD ALTA PRIORIDAD — Contactar en próximas 2 semanas"
    if tier.startswith('B') and score >= 8:
        return "OPORTUNIDAD MEDIA-ALTA — Seguimiento activo recomendado"
    if tier.startswith('B'):
        return "OPORTUNIDAD MEDIA — Nurturing + señales de compra"
    return "OPORTUNIDAD NURTURING — Monitoreo continuo"

def get_wallet(tier, score, subsegment):
    if subsegment in ('Banking', 'Insurance'):
        if tier.startswith('A'): return "300-600K€/año"
        if tier.startswith('B'): return "150-400K€/año"
        return "100-250K€/año"
    if subsegment in ('Retail', 'Wholesale Trade'):
        if tier.startswith('A'): return "250-500K€/año"
        if tier.startswith('B'): return "100-300K€/año"
        return "80-200K€/año"
    if subsegment in ('Pharmaceuticals', 'Chemicals'):
        if tier.startswith('A'): return "200-400K€/año"
        if tier.startswith('B'): return "100-250K€/año"
        return "80-180K€/año"
    if tier.startswith('A'): return "200-400K€/año"
    if tier.startswith('B'): return "100-250K€/año"
    return "80-200K€/año"

def get_urgency(tier, score, notes):
    if 'EN CURSO' in notes.upper(): return "ALTA"
    if tier.startswith('A') and score >= 9: return "ALTA"
    if tier.startswith('A'): return "ALTA"
    if tier.startswith('B') and score >= 8: return "MEDIA-ALTA"
    if tier.startswith('B'): return "MEDIA"
    return "BAJA-MEDIA"

def get_fit_score(tier, score, fit):
    fit_num = int(fit) if fit.isdigit() else 3
    if fit_num >= 4: return "Muy alto"
    if fit_num >= 3: return "Alto"
    return "Medio"

def get_probability(tier, score, notes):
    if 'EN CURSO' in notes.upper(): return "70-80% (comercial asignado)"
    if tier.startswith('A') and score >= 9: return "60-70%"
    if tier.startswith('A'): return "50-60%"
    if tier.startswith('B') and score >= 8: return "40-50%"
    if tier.startswith('B'): return "30-40%"
    return "20-30%"

def sanitize(name):
    return name.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def generate_report(acct, output_dir):
    name = acct['account']
    tier = acct['tier']
    score = float(acct['score']) if acct.get('score') else 0
    segment = acct.get('segment', '')
    subsegment = acct.get('subsegment', '')
    fit = acct.get('fit_subsegmento', '')
    top_ent = acct.get('top_enterprise', '')
    cliente = acct.get('cliente_actual', '')
    notas = acct.get('aproximacion_notas', '')
    
    wallet = get_wallet(tier, score, subsegment)
    urgency = get_urgency(tier, score, notas)
    fit_score = get_fit_score(tier, score, fit)
    prob = get_probability(tier, score, notas)
    verdict = get_verdict(tier, score, notas)
    
    safe_name = sanitize(name)
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    replacements = {
        '{{TITLE}}': f'Account Intelligence — {safe_name}',
        '{{ACCOUNT_NAME}}': safe_name,
        '{{SEGMENT}}': segment,
        '{{SUBSEGMENT}}': subsegment,
        '{{TIER}}': tier,
        '{{SCORE}}': str(acct.get('score', '')),
        '{{NOTES}}': sanitize(notas)[:200] if notas else 'Sin notas en CRM',
        '{{FIT}}': fit if fit else '3',
        '{{TOP_ENT}}': top_ent if top_ent else '0',
        '{{CLIENTE_ACTUAL}}': cliente if cliente else '0',
        '{{WALLET_SIZE}}': wallet,
        '{{URGENCY}}': urgency,
        '{{FIT_SCORE}}': fit_score,
        '{{PROBABILITY}}': prob,
        '{{VERDICT}}': verdict,
    }
    for k, v in replacements.items():
        html = html.replace(k, v)
    
    short_name = re.sub(r'[^a-z0-9]', '-', name.lower())[:60]
    filename = f"control-m-{subsegment.lower().replace(' ', '-')}-{short_name}.html"
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

def convert_html_to_pdf(html_path):
    pdf_path = html_path.replace('.html', '.pdf')
    js_code = f"""
const {{ chromium }} = require('/opt/hermes/node_modules/playwright-core');
(async () => {{
  const browser = await chromium.launch({{ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'] }});
  const page = await browser.newPage();
  await page.goto('file://' + require('path').resolve('{html_path}'), {{ waitUntil: 'networkidle0', timeout: 30000 }});
  await page.pdf({{ path: '{pdf_path}', format: 'A4', printBackground: true, margin: {{ top: '15mm', bottom: '15mm', left: '15mm', right: '15mm' }} }});
  await browser.close();
}})();
"""
    js_file = html_path + '.convert.js'
    with open(js_file, 'w') as f:
        f.write(js_code)
    try:
        subprocess.run(['node', js_file], check=True, capture_output=True, timeout=60)
        os.remove(js_file)
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"⚠ Error PDF: {e}", file=sys.stderr)
        os.remove(js_file)
        return None
    except subprocess.TimeoutExpired:
        print(f"⚠ Timeout PDF", file=sys.stderr)
        os.remove(js_file)
        return None

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"⚠ Error: {ACCOUNTS_FILE} no existe.")
        print("   Ejecuta: python3 extract-accounts.py <archivo.xlsx>")
        sys.exit(1)
    with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    accounts = load_accounts()
    print(f"📊 Cuentas cargadas: {len(accounts)}")
    
    indices = []
    names = []
    tier_filter = None
    segment_filter = None
    limit = None
    generate_pdf = '--pdf' in sys.argv
    all_flag = '--all' in sys.argv
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--name' and i + 1 < len(args):
            names.append(args[i + 1])
            i += 2
        elif arg == '--tier':
            tier_filter = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif arg == '--segment':
            segment_filter = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif arg == '--limit':
            limit = int(args[i + 1]) if i + 1 < len(args) else 10
            i += 2
        elif arg == '--pdf':
            generate_pdf = True
            i += 1
        elif arg == '--all':
            all_flag = True
            i += 1
        elif arg.isdigit():
            indices.append(int(arg) - 1)
            i += 1
        else:
            i += 1
    
    selected = []
    if all_flag:
        selected = accounts[:]
    elif tier_filter:
        selected = [a for a in accounts if a.get('tier', '') == tier_filter]
    elif segment_filter:
        selected = [a for a in accounts if segment_filter.lower() in a.get('subsegment', '').lower()]
    elif names:
        for n in names:
            for a in accounts:
                if n.lower() in a.get('account', '').lower():
                    selected.append(a)
                    break
    elif indices:
        for idx in indices:
            if 0 <= idx < len(accounts):
                selected.append(accounts[idx])
            else:
                print(f"⚠ Índice {idx + 1} fuera de rango (1-{len(accounts)})")
    else:
        selected = accounts[:10]
    
    print(f"🎯 Cuentas seleccionadas: {len(selected)}")
    
    generated = 0
    for i, acct in enumerate(selected):
        try:
            path = generate_report(acct, REPORTS_DIR)
            print(f"[{i+1}/{len(selected)}] {acct['account'][:50]:50s} → {os.path.basename(path)}")
            generated += 1
            if generate_pdf:
                pdf_path = convert_html_to_pdf(path)
                if pdf_path:
                    print(f"   📄 PDF: {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"   ✗ Error con {acct['account']}: {e}")
    
    print(f"\n✅ Generados: {generated}")
    print(f"📁 Directorio: {REPORTS_DIR}")
    if generate_pdf:
        pdfs = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.pdf')]
        print(f"📄 PDFs: {len(pdfs)}")

if __name__ == '__main__':
    main()
