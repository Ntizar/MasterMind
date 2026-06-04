---
fecha: 2026-03-20
tarea: montecarlo-github-pages-subdirectory
tipo: software
complejidad: baja
clusters: [github]
proyecto: montecarlo
patron: static-site-subdirectory-deploy
---

# GitHub Pages con archivos en subdirectorio /public

## Decisión clave
GitHub Pages no puede servir desde una carpeta arbitraria como /public — hay que usar GitHub Actions para copiar el contenido a la rama gh-pages.

## Patrón reutilizable
sí → static-site-subdirectory-deploy

Cuando un repo tiene los archivos estáticos en /public (o cualquier subcarpeta que no sea /docs), usar peaceiris/actions-gh-pages con publish_dir apuntando a esa carpeta. GitHub Pages entonces sirve desde gh-pages branch / (root).

```yaml
- uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./public
    publish_branch: gh-pages
    force_orphan: true
```

## Qué funcionó
- El workflow crea y actualiza la rama gh-pages automáticamente en cada push a main
- force_orphan: true evita acumulación de historial en gh-pages
- .nojekyll se añade solo por peaceiris — necesario para que GitHub Pages sirva archivos JS con rutas que empiezan por _

## Qué evitar
- No asumir que Pages puede configurarse para servir desde /public directamente — no existe esa opción
- No commitear index.html en la raíz del repo como workaround (chapuza)
- No olvidar cambiar Pages settings manualmente en GitHub UI después de que el Action cree gh-pages por primera vez: Settings → Pages → Branch: gh-pages / (root)

## Skills usados
- software-dev.md

## Tests/criterios que validaron esto
- Rama gh-pages creada con index.html, css/, js/ en la raíz
- GitHub Actions run con conclusion: success
- Site live en ntizar.github.io/MonteCarloInversion cargando contenido actualizado

## Conexiones
**Cluster:** #github
**Proyecto:** [[montecarlo]]
**Aprendizajes relacionados:** [[2026-03-20-montecarlo-deploy-sin-verificar]] · [[2026-03-20-montecarlo-v35-context-pdf-screener]]
