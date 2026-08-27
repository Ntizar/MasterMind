# Caso: NtizarBrainMasterMind v4.0 — Merge master/main

## Contexto

El repo tenía dos ramas:
- **master** = v3.1 (OpenCode + Obsidian), mejor diseño de README y index.html
- **main** = v4.0 (Hermes + GitHub + NaN.builders), mejor contenido pero peor diseño

## Problema

El usuario dijo: "el master está mejor estructurado, el diseño del readme es mejor, pero en el main es donde está realmente la chicha de nan.builders"

## Solución

1. **README.md**: Tomar master como base + reemplazar secciones técnicas por contenido v4.0 de main. Limpiar obsidian/opencode.
2. **index.html**: Tomar master + limpiar obsidian/opencode + CDN → @latest.
3. **SOUL.md, AGENTS.md, CHANGELOG.md**: Mantener de main (v4.0).
4. **vercel.json**: Recrear para learning-platform.
5. **GitHub description**: Actualizar vía API REST.
6. **Branch master remoto**: Eliminar.

## Lecciones

- `git merge` directo no funciona con archivos comunes y diferentes contenidos
- Patrón: inventario → clasificación → fusión manual → verificación
- Escanear referencias residuales post-fusión con `search_files` (obsidian, opencode, etc.)
- GitHub description no está en el repo, se actualiza vía API REST: `PATCH /repos/{owner}/{repo}`
- Eliminar el description default que GitHub genera automáticamente
- Si un branch remoto (`origin/master`) sigue existiendo, recuperarlo con `git checkout -b master origin/master`
- **Después del merge, verificar CDN Aurora** → `@latest`, no `@master`
- **Poda de legacy:** después de migrar, analizar skills/archivos en 3 categorías (personales, mixtos, genéricos) y presentar tabla al humano antes de eliminar
- **v4.0 resultante:** 40 archivos (vs 137), solo `legacy/skills/` con 9 patrones genéricos, y `learning-platform/vercel.json` restaurado
