# Caso: DietaNan → Template para comunidad NaN.builders

**Fecha:** 2026-06-11
**Proyecto original:** `/root/workspace/dieta-masterfit/` (DietaNan personal)
**Repositorio público:** https://github.com/Ntizar/DietaNan

## Qué se hizo

1. Crear copia en `/root/workspace/dieta-template/` (sin tocar original)
2. Sanitizar `server.js` — quitar referencias a "David", "Amadeo Llados", repo `Ntizar/dieta` hardcodeado en `syncGitHub()`
3. Sanitizar `dashboard.html` — reemplazar "MasterFit"→"FitTrack", "Amadeo"→"Coach", "David"→"Usuario", footer genérico
4. Crear `database.json` vacío — estructura con campos placeholder, arrays vacíos
5. Reescribir `README.md` como guía de instalación de 10 pasos
6. Crear `.env.example` con instrucciones (sin tokens)
7. Verificación de seguridad con regex por nombres, tokens, emails
8. Crear repo público vía GitHub API
9. Subir todos los archivos con API REST (11 commits)
10. Squash a 1 commit limpio con `git reset --soft $(git rev-list --max-parents=0 HEAD)`
11. Captura del dashboard para presentación

## Datos sensibles identificados y limpiados

| Archivo | Dato | Acción |
|---------|------|--------|
| `.env` | `NAN_API=sk-oej...4dRg` | No copiado al template |
| `database.json` | Nombre "David Antizar", peso real, comidas reales | Estructura vacía con placeholder |
| `server.js` | Referencias a "David", "Amadeo Llados", repo `Ntizar/dieta` | Genérico, configurable via env vars |
| `dashboard.html` | "MasterFit", "Amadeo Llados", "David", "KoldoFit" | "FitTrack", "Coach IA", "Usuario" |
| `README.md` | Datos personales, progreso real | Guía genérica de instalación |

## Falsos positivos aceptados (NO son fugas)

- `Ntizar/Aurora` en CDN CSS del dashboard → es un repo público, no dato personal
- `NTIZAR_API` como nombre de variable en server.js → es un nombre de variable, no contiene el token
- Referencia a "David Antizar" en créditos del README → atribución, no fuga de datos

## Comandos clave

```bash
# Escaneo de seguridad
grep -rn -i -E '(David|Ntizar|Amadeo|Koldo|ntizar)' /path/to/template

# Squash de commits
git reset --soft $(git rev-list --max-parents=0 HEAD)
git commit -m "FitTrack — Dashboard de seguimiento de dieta con IA"
git push --force origin main
```

## Lecciones

- El dashboard.html es grande (~54KB) — usar `patch` en vez de reescribir
- Los scripts de shell (`.sh`) no se copian automáticamente con `cp -r` si el script los crea después
- La API de GitHub Contents API requiere rutas completas (`data/database.json`, no `database.json` dentro de `data/`)
- El squash a 1 commit es importante para que el repo se vea limpio al público
