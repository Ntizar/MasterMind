# GitHub Pages en repos privados — Workaround

## Problema

GitHub Pages en repositorios privados solo está disponible con cuentas Pro (de pago).
Las cuentas free solo permiten Pages en repos públicos.

## Solución

Crear un repositorio público dedicado solo para Pages, con un nombre relacionado:

```bash
# 1. Crear repo público vía API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"name":"<proyecto>-web","description":"<proyecto> — Dashboard","public":true}' \
  https://api.github.com/user/repos

# 2. Clonar, copiar index.html, push
git clone https://$GITHUB_TOKEN@github.com/Ntizar/<proyecto>-web.git
cp index.html <proyecto>-web/
cd <proyecto>-web
git add . && git commit -m "Initial dashboard" && git push

# 3. Activar Pages vía API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"source":{"branch":"main","path":"/"}}' \
  https://api.github.com/repos/Ntizar/<proyecto>-web/pages

# URL resultante: https://ntizar.github.io/<proyecto>-web/
```

## Ejemplo: Nogal 9

- Datos privados: `Ntizar/nogal9` (presupuestos, comparaciones)
- Pages público: `Ntizar/nogal9-web` (solo index.html)
- URL: https://ntizar.github.io/nogal9-web/
