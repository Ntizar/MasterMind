# CSP Helmet Fix — Google Fonts + CDN (2026-05-26)

## Problema
CSP con helmet bloqueaba:
1. Google Fonts CSS → `styleSrc` no tenía `fonts.googleapis.com`
2. Google Fonts (gstatic) → `fontSrc` no tenía `fonts.gstatic.com`
3. Sourcemaps jsDelivr → `connectSrc` no existía
4. `scriptSrcAttr` mal formado → `'unsafe-inline"` (falta comilla simple)

## Solución (helmet config)
```js
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
      styleSrcElem: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://cdn.jsdelivr.net", "https://fonts.gstatic.com"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      scriptSrcAttr: ["'unsafe-inline'"],
      scriptSrcElem: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://cdn.jsdelivr.net"],
    },
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

## Verificación
```bash
curl -s -D- http://localhost:4000/ | grep Content-Security-Policy
# Debe incluir: fonts.googleapis.com, fonts.gstatic.com, connect-src
```

## Regla
Cada recurso externo necesita su propia directiva CSP:
- CSS de CDN → `styleSrc` + `styleSrcElem`
- Fuentes → `fontSrc`
- JS de CDN → `scriptSrc` + `scriptSrcElem`
- Fetch/XHR a CDN → `connectSrc`
- Atributos inline → `scriptSrcAttr`
