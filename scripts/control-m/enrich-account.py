#!/usr/bin/env python3
"""
enrich-account.py — Busca datos de tamaño y noticias recientes IT de una empresa.

Uso:
    python3 enrich-account.py "Banco Sabadell"
    python3 enrich-account.py "Ibercaja"

Busca en Google:
- Facturación, empleados, oficinas, sede
- Noticias recientes IT, estrategia, transformacion digital, cloud

Salida:
    JSON con datos enriquecidos o muestra directa en consola.
"""
import sys
import subprocess
import re
import json
import time

def search_google(query, max_results=5):
    """Buscar en Google via DuckDuckGo HTML."""
    try:
        cmd = ['curl', '-s', '-L', '--max-time', '15',
               '--user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36']
        url = f'https://html.duckduckgo.com/html/?q={query}'
        cmd.append(url)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            return []
        
        html = result.stdout
        results = []
        for block in re.finditer(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL):
            href = block.group(1)
            title = re.sub(r'<[^>]+>', '', block.group(2)).strip()
            
            snippet_match = re.search(r'class="result__snippet">(.*?)</span>', html[block.start():], re.DOTALL)
            snippet = ''
            if snippet_match:
                snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()
            
            results.append({
                'title': title,
                'url': href,
                'snippet': snippet[:300],
            })
        
        return results[:max_results]
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        return []

def extract_company_size(text):
    """Extraer empleados, facturación, oficinas del texto."""
    data = {}
    
    # Empleados
    emp_match = re.search(r'(\d[\d\s.]*)\s*(?:empleados?|workers?|colaboradores?|personal|headcount)', text, re.IGNORECASE)
    if emp_match:
        data['empleados'] = emp_match.group(1).replace(' ', '').replace('.', '')
    
    # Facturación
    rev_match = re.search(r'(\d[\d\s.]*)\s*(?:M€|millones?|million|EUR|€|euros)', text, re.IGNORECASE)
    if rev_match:
        data['facturacion'] = rev_match.group(1).replace(' ', '').replace('.', '') + 'M€'
    
    # Oficinas/sedes
    off_match = re.search(r'(\d[\d\s.]*)\s*(?:oficinas?|sedes?|branches?|agencias?|centros?|locations?)', text, re.IGNORECASE)
    if off_match:
        data['oficinas'] = off_match.group(1).replace(' ', '').replace('.', '')
    
    return data

def enrich_company(company):
    """Buscar datos de tamaño y noticias IT de una empresa."""
    print(f"🔍 Enriching: {company}\n")
    
    results = {}
    
    # 1. Datos de tamaño
    print("  📊 Buscando datos de tamaño...")
    size_queries = [
        f'"{company}" empleados facturación oficinas sede',
        f'"{company}" employees revenue headquarters',
        f'"{company}" annual report 2024 2025',
    ]
    
    size_data = {}
    for q in size_queries:
        print(f"    Query: {q}")
        r = search_google(q, max_results=5)
        for item in r:
            extracted = extract_company_size(item['title'] + ' ' + item['snippet'])
            size_data.update(extracted)
            print(f"    → {item['title'][:80]}")
            print(f"      Extraído: {extracted}")
        time.sleep(0.3)
    
    results['size'] = size_data
    
    # 2. Noticias IT recientes
    print("\n  📰 Buscando noticias IT/estrategia...")
    it_queries = [
        f'"{company}" IT transformación digital 2025 2026',
        f'"{company}" cloud data AI estrategia 2025',
        f'"{company}" tecnología innovación digital',
        f'"{company}" SAP Microsoft AWS Google 2025',
    ]
    
    news = []
    for q in it_queries:
        print(f"    Query: {q}")
        r = search_google(q, max_results=5)
        for item in r:
            if item['snippet']:
                news.append({
                    'title': item['title'],
                    'url': item['url'],
                    'snippet': item['snippet'][:250],
                })
                print(f"    → {item['title'][:80]}")
        time.sleep(0.3)
    
    results['news'] = news
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 enrich-account.py 'Nombre Empresa'")
        sys.exit(1)
    
    company = ' '.join(sys.argv[1:])
    
    results = enrich_company(company)
    
    print("\n" + "="*60)
    print("RESULTADOS:")
    print("="*60)
    
    size = results.get('size', {})
    if size:
        print(f"\n📊 Tamaño:")
        if 'empleados' in size:
            print(f"   👥 Empleados: {size['empleados']}")
        if 'facturacion' in size:
            print(f"   💰 Facturación: {size['facturacion']}")
        if 'oficinas' in size:
            print(f"   🏢 Oficinas: {size['oficinas']}")
    else:
        print("\n⚠ No se encontraron datos de tamaño.")
    
    news = results.get('news', [])
    if news:
        print(f"\n📰 Noticias IT/estrategia ({len(news)} encontradas):")
        for i, n in enumerate(news[:5]):
            print(f"\n   {i+1}. {n['title']}")
            print(f"      {n['snippet'][:200]}")
            print(f"      🔗 {n['url']}")
    else:
        print("\n⚠ No se encontraron noticias IT recientes.")
    
    # Output JSON
    print("\n" + "="*60)
    print("JSON output:")
    print("="*60)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
