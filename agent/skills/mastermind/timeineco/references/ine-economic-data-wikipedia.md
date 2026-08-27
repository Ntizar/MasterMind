# Escrapear datos económicos del INE vía Wikipedia

## Problema recurrente

El INE bloquea acceso directo a sus datos:
- **CSV endpoints** (jaxiT3/files/t/csvbase/*) → 599/404
- **datos.gob.es** → 403 sin session/cookie
- **API REST** → bloquea sin auth
- **JAXI endpoints** → 404/599

## Solución: Wikipedia como proxy de datos oficiales

Wikipedia referencia datos del INE en sus tablas y es accesible vía `curl` normal.

### Fuentes Wikipedia útiles para datos económicos españoles

| Dato | URL | Tabla clave |
|------|-----|-------------|
| Renta per cápita por CA | `Economía de España` | "Renta per cápita por comunidad autónoma" (2019-2024) |
| Tasa de desempleo por CA | `Desempleo en España` | "Tasa de desempleo por comunidad autónoma" (2005-2025) |
| Salario medio histórico | `Salario en España` | Sección "Salario medio y distribución salarial" |

### Patrón de scraping

```python
# 1. Descargar página
result = subprocess.run(['curl', '-s', '-L', '-m', '15', '-A', 'Mozilla/5.0', url], capture_output=True, text=True)

# 2. Extraer tablas wikitable
tables = re.findall(r'<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>(.*?)</table>', content, re.DOTALL)

# 3. Extraer filas
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)

# 4. Extraer celdas
cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
texts = [re.sub(r'<[^>]+>', ' ', c).replace('\n', ' ') for c in cells]
texts = [t.strip() for t in texts if t.strip() and len(t) > 2]
```

### Pitfalls

- **Encoding:** Wikipedia usa UTF-8, pero algunos caracteres especiales pueden causar problemas. Usar `errors='replace'` en `open()`.
- **Nombres de comunidades:** Wikipedia usa nombres largos ("Asturias, Principado de", "Navarra, Comunidad Foral de"). Mapear a nombres cortos.
- **Tablas múltiples:** Algunas páginas tienen varias tablas. Identificar la correcta por el header o el contexto.
- **Valores numéricos:** Wikipedia usa puntos como separadores de miles y comas como decimales (formato español). Limpiar con `re.sub(r'[^\d.,]', '', val)`.
- **Años disponibles:** Los años no son consecutivos en todas las tablas. Verificar qué años están disponibles antes de parsear.
- **Wikipedia API:** Si el HTML no tiene tablas (página con contenido dinámico), usar `https://es.wikipedia.org/w/api.php?action=parse&format=json&page=TÍTULO&prop=wikitext` para obtener wikitext raw.

### Datos obtenidos en sesión 2026-06-22

**Renta per cápita 2024 por CA:**
- Madrid: 44.749€ (más alto)
- País Vasco: 41.010€
- Navarra: 39.096€
- Cataluña: 37.477€
- Aragón: 36.699€
- Total nacional: 32.633€
- Melilla: 21.118€ (más bajo)

**Tasa de desempleo 2024 por CA:**
- Navarra: 6.6% (más bajo)
- Cataluña: 7.9%
- Aragón: 7.6%
- Madrid: 7.0%
- Total nacional: 9.9%
- Melilla: 23.0% (más alto)
- Ceuta: 22.2%

### Mapeo provincia → comunidad autónoma

Necesario porque los datos económicos están por CA pero los CPs están por provincia. Ver mapeo en `salarios-por-cp.json` enrichment script.
