# Nota: Verify System — De existencia a funcionalidad

**Fecha:** 2026-06-04  
**Lección:** Un check de "existe" no es lo mismo que un check de "funciona".

## Evolución

| Versión | Checks | Qué verifica |
|---------|--------|-------------|
| v1 | 11 | Solo existencia de archivos y directorios |
| v2 | 27 | Existencia + contenido + consistencia + JSON válido |

## Checks añadidos en v2

1. **Contenido** — SOUL.md contiene "Koldo", "Hermes Agent", "David Antizar"
2. **Contenido** — README.md contiene "143 skills", "git clone"
3. **Contenido** — index.html contiene "nz-btn", "og:title", "og:image"
4. **Negativo** — index.html NO contiene "innerHTML" (XSS seguro)
5. **Negativo** — pages.yml NO contiene "verify-system.bat" (limpio)
6. **Consistencia** — Aurora CDN usa "@latest"
7. **Validación** — tokens-log.json es JSON válido

## Patrón reutilizable

```bash
check_content "archivo" "texto esperado"    # Verifica que un archivo contiene algo
check_no_content "archivo" "texto prohibido" # Verifica que un archivo NO contiene algo
```

## Aplicable a

Cualquier proyecto con CI/CD. Los checks de consistencia son más valiosos que los de existencia porque detectan regresiones sutiles.
