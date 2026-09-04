# Caso ejecutado: corrupcion-por-partido.netlify.app (2026-09-02)

Auditoría "ver la realidad de los números" de un sitio Netlify de una sola página (~29 KB, `index.html` con datos embebidos, sin backend, generado con netlify.new).

## Estructura del dato embebido

- `const SEED = [ ["Caso X","PARTIDO",123456], ... ]` — 389 entradas `["nombre","partido",importe_entero_euros]`
- `const P = {...}` — 34 partidos (PP, PSOE, CDC, CiU, coaliciones "PP-PSOE", …)
- `const ORGS = {...}` — 11 agentes no-partido (Bancos, Cajas de Ahorros, Empresas, UGT, Casa Real, …)
- `const COAL` — mapeo de coaliciones para el toggle "split" (reparte el importe entre componentes)
- `const MACRO = ["Caso Amnistía Fiscal","Caso Rescate Bancario"]` — excluidos por defecto vía checkbox `noMacro`
- `parsePaste()` + `reset` — loader que admite pegar datos de la fuente; el tweet precargado dice "124.235 millones de euros en 591 casos de corrupción"

## Extracción (Python, execute_code)

```python
html = open(base + r"\index.html", encoding="utf-8").read()
seed_block = html.split("const SEED = [",1)[1].split("];",1)[0]
seed = {n:(p,int(c)) for n,p,c in re.findall(r'\["([^"]+)","([^"]+)",(\d+)\]', seed_block)}
P_parties   = set(k.strip('"') for k in re.findall(r'("[\w\- ]+"|[\w\-]{2,14})\s*:\s*\{', html.split("const P = {",1)[1].split("};",1)[0]))
ORG_parties = set(re.findall(r'"([^"]+)":\{', html.split("const ORGS = {",1)[1].split("};",1)[0]))
```

Resultado: **389 entradas, suma 124.235.185.826 € EXACTA** = el claim del header. ✔

## Diff contra la fuente

Fuente: `https://casos-aislados.com/tramas.php` (descargada con curl, 804 KB). Parseo por bloques:

```python
blocks = re.split(r'<div class="bloc_title"><a href="Caso-Aislado\.php\?Caso=', src)
# nombre = hasta el '&'; partido = regex r'Partido/Org:.*?>([^<]+)</a>'
# coste = regex r'Coste:\s*<span class="red count">([\d.,\s]+)</span>' | None si "N/A"
```

- Fuente: **591 casos, 389 con importe, 202 sin importe** — coincide con el claim del header.
- ⚠️ **Trampa encontrada:** la primera comparación dio `Comunes: 0` con 389 "solo en SEED" y 389 "solo en fuente" — porque muchos nombres reales son `CASO COOPERACIÓN/PIEZA 1` y el site los capitaliza a `Caso Cooperación...`. Al normalizar `re.sub(r'^caso\s+','Caso ', raw, flags=re.I)` + match por `.lower()` → **0 discrepancias de partido, 0 de importe, 0 ausencias en ambos sentidos. Copia 100 % fiel.**

## Desglose del titular (la auditoría real)

| Capa | € | % del 124.235 M |
|---|---:|---:|
| MACRO (Amnistía fiscal 38.809 M + Rescate bancario 58.948 M) | 97.757 M | **78,7 %** |
| ORGS (bancos, cajas, empresas, sindicatos…) | 7.752 M | 6,2 % |
| **Casos por partido = vista por defecto (327 casos)** | **18.726 M** | **15,1 %** |

- Vista por defecto: PP 9.618 M (51,4 %) con 135 casos; la torre se apoya en importes INVESTIGADOS no sentenciados (Castor 1.700 M, Taula 1.300 M, Caballo de Troya 1.200 M, RTVV 1.200 M). PSOE 1.897 M (111 casos), CDC 1.906 M, UCOR 2.600 M (Malaya).
- Toggle "amnistía" ON → PP pasa a 48.427 M (39 % del total) con un clic.
- **El tweet precargado usa los 124.235 M** (la escala que la propia web oculta) → asimetría compartir-vs-ver.

## Spot-checks externos (web_search)

- Gürtel 201 M € en SEED ≈ "200 millones defraudados, 94 condenados, 22 sentencias" (El Plural / TS 2020) ✔
- Rescate bancario 58.948 M ≈ Banco de España "60.613 M perdidos" — razonable, pero es rescate financiero, no trama judicial
- Amnistía fiscal 38.809 M = lo **declarado** al regularizar (recaudado ~885 M); contar como "coste" es un techo interpretativo ✗
- 3 % CDC 1.800 M = estimación, no sentencia firme; Malaya 2.600 M = lo manejado, no defraudado probado

## Formato del informe entregado

5 secciones: ① Integridad técnica ✅ (tabla checks) · ② Realidad del titular ⚠️ (tabla capas) · ③ Vista por defecto (tabla torres) · ④ Calidad de la fuente (mezcla de naturalezas de importe) · ⑤ Lo bien hecho + resumen con veredicto de una línea: "El código no miente; el titular estira."
