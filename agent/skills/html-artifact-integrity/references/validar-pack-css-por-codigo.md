# Validar un pack CSS de design system por código (sin navegador)

Contexto (2026-09-07, pack `ntizar.ai.css` de Aurora, 20 primitivos AI-native de
Beautiful UI). El navegador pidió permiso de depuración remota y el usuario no
respondió, así que la verificación se hizo 100% por código. Es una verificación
**complementaria** al `audit-aurora.py` (que cuenta clases únicas pero NO valida
que existan) y a la captura visual (que no se pudo hacer). Da una señal objetiva
de integridad sin abrir el navegador.

## Las 4 comprobaciones

1. **Balance de llaves CSS** — para cada `.css` del repo: `css.count("{") == css.count("}")`.
   Detecta bloques sin cerrar (un fichero "balanceado" a ojo no basta).

2. **Existencia de clases** — toda clase `nz-*` usada en el HTML debe existir como
   selector en algún `.css` del repo. Caza clases inventadas/typos que el
   `audit-aurora.py` no ve.

3. **Existencia de tokens** — todo `var(--nz-*)` usado debe estar definido.
   Caza renders rotos por variable inexistente (el color/sombra se resetea a nada).

4. **Well-formedness del HTML** — `html.parser` que registre etiquetas sin cerrar
   y cierres huérfanos.

## PITFALL crítico: el regex BEM

```python
# ✗ MAL — el guion bajo _ y el doble guion -- quedan fuera, reporta falsos faltantes
re.findall(r'\.([a-z0-9-]+)', css)

# ✓ BIEN — incluye _ (__body) y -- (--primary)
re.findall(r'\.(nz-[a-zA-Z0-9_\-]+)', css)
```

En la sesión, el regex `[a-z0-9-]` reportó **195** clases "faltantes" falsas
(todas las `nz-card__body`, `nz-btn--primary`...). Al corregirlo a
`[a-zA-Z0-9_\-]` dio **0**. La clase base `.nz-approval` se capturaba pero el
modificador `.nz-approval__body` no, por eso el falso "missing".

## Script

`scripts/validate-aurora-css.py` (en este skill) hace las comprobaciones 1-3.
Uso: `python validate-aurora-css.py <archivo.html> [dir_repo]`.

```python
import os, re
# clases usadas en el HTML (split de cada class="")
used = set()
for m in re.findall(r'\bclass="([^"]+)"', html):
    used |= set(m.split())
nz_used = {c for c in used if c.startswith('nz-')}
# clases definidas en el CSS (regex BEM-safe)
defs = set()
for fn in os.listdir(repo):
    if fn.endswith('.css'):
        defs |= set(re.findall(r'\.(nz-[a-zA-Z0-9_\-]+)', open(os.path.join(repo,fn),encoding='utf-8').read()))
missing = sorted(nz_used - defs)
```

## Regla de monocromo a nivel de componente (extiende el ERROR #14 de Aurora)

David no solo rechaza el **gradiente** azul→naranja; también rechaza mezclar el
azul brand y el naranja accent **dentro de un mismo componente pequeño**
(badge + meter, icono + pill). Al construir packs/componentes nuevos:
- **Default monocromo azul** — usa `--nz-color-brand` para identidad/estado.
- Las variantes `--accent` (naranja) se dejan como **opt-in** en el CSS, pero
  NO se muestran en el demo/galería por defecto.
- Los colores de **estado semántico** (verde/rojo/ámbar vía `--nz-status-*`) sí
  están permitidos — son estados, no marca.

En la sesión, el pack `ntizar.ai.css` inicial usaba `--nz-color-accent` en el
badge de entidad, el meter de confidence y el icono de condición del flowchart;
se cambiaron todos a `--nz-color-brand` (y el demo quitó las barras/tags
`--accent`) para presentar un look monocromo limpio.
