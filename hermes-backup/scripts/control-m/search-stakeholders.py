#!/usr/bin/env python3
"""
search-stakeholders.py — Busca personas clave de una empresa en Google/DuckDuckGo vía curl.

Uso:
    python3 search-stakeholders.py "Nombre Empresa"
    python3 search-stakeholders.py "Banco Sabadell"

Salida:
    Lista de nombres y cargos encontrados en fuentes públicas.
"""
import sys
import subprocess
import re
import json
import time

def search_ddg(query, max_results=5):
    """Buscar en DuckDuckGo vía curl (sin dependencias)."""
    try:
        cmd = ['curl', '-s', '-L', 
               '--max-time', '15',
               '--user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36']
        # DuckDuckGo HTML search
        url = f'https://html.duckduckgo.com/html/?q={query}'
        cmd.append(url)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            return []
        
        html = result.stdout
        # Parsear resultados
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
                'snippet': snippet[:250],
            })
        
        return results[:max_results]
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        return []

def extract_names(text):
    """Extraer posibles nombres de personas del texto."""
    # Nombres españoles comunes: capitalizada, 2-4 palabras
    names = set()
    # Patrón: palabras capitalizadas consecutivas (2-4)
    matches = re.findall(r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})', text)
    for m in matches:
        # Filtrar falsos positivos
        skip_words = {'Spain', 'Spain.', 'Banco', 'SA', 'SL', 'S.A.', 'S.L.', 'Corp', 'Inc',
                      'Ltd', 'Plc', 'The', 'And', 'For', 'From', 'With', 'This', 'That',
                      'Also', 'More', 'New', 'Also Known', 'Known As'}
        words = m.split()
        if len(words) >= 2 and len(words) <= 4:
            # Al menos una palabra no debe ser solo mayúsculas
            if not all(w.isupper() for w in words):
                names.add(m)
    return names

def search_stakeholders(company, roles=None):
    """Buscar stakeholders de una empresa."""
    if roles is None:
        roles = [
            'CTO', 'CIO', 'Chief Technology Officer', 'Chief Information Officer',
            'Head of IT', 'Director de IT', 'Director de Tecnología',
            'Head of Infrastructure', 'Director de Infraestructura',
            'Head of Data', 'Director de Datos', 'Head of Digital',
            'SAP Manager', 'Director de Operaciones IT',
        ]
    
    all_results = []
    seen_urls = set()
    
    for role in roles:
        query = f'"{company}" "{role}" 2025 2026'
        print(f"  🔍 {role}...")
        
        results = search_ddg(query, max_results=5)
        for r in results:
            url = r.get('url', '')
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            text = f"{r['title']} {r['snippet']}"
            names = extract_names(text)
            
            all_results.append({
                'role': role,
                'title': r['title'],
                'url': url,
                'names': list(names),
                'snippet': r['snippet'][:200],
            })
        
        time.sleep(0.3)
    
    return all_results

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 search-stakeholders.py 'Nombre Empresa'")
        sys.exit(1)
    
    company = ' '.join(sys.argv[1:])
    print(f"🔍 Buscando stakeholders de: {company}\n")
    
    results = search_stakeholders(company)
    
    if not results:
        print("❌ No se encontraron resultados con Google.")
        print("\n💡 Para encontrar stakeholders reales:")
        print("   1. Busca manualmente en LinkedIn: site:linkedin.com 'Empresa' 'CTO'")
        print("   2. Busca en Twitter/X: site:x.com 'Empresa' CTO")
        print("   3. Busca en conferencias: site:eventbrite.com 'Empresa' technology")
        print("   4. Busca en prensa: 'Empresa' 'nuevo CTO' o 'Empresa' 'contrata'")
        return
    
    print(f"✅ {len(results)} resultados encontrados:\n")
    
    for r in results:
        print(f"📌 {r['role']}")
        print(f"   {r['title']}")
        if r['names']:
            print(f"   👤 {', '.join(r['names'])}")
        print(f"   🔗 {r['url']}")
        print(f"   💬 {r['snippet'][:150]}")
        print()

if __name__ == '__main__':
    main()
