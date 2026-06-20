# NaN Spaces Deploy — Patrón (2026-05-26)

## Contexto
Proyectos Node.js deployados en NaN Spaces (https://*.apps.nan.builders/).

## Limitaciones
- **No hay CLI de NaN Spaces instalada** en el entorno de trabajo
- `npx @nan/spaces` no existe en el registry npm
- No hay scripts de deploy automatizado (`deploy.sh`, `Makefile`, hooks)
- No hay contenedores Docker corriendo localmente

## Proceso
1. Commit + push a GitHub (`origin/main`)
2. Deploy automático desde UI de NaN Spaces (auto-deploy desde main branch)
3. **No se puede verificar remotamente** qué versión está desplegada
4. Para confirmar versión en producción:
   - Verificar commit SHA en la UI de NaN Spaces
   - O hacer un deploy manual desde la UI

## Pitfall
Si el deploy falla o no refleja los últimos cambios, puede ser:
- Auto-deploy de NaN Spaces con delay (no instantáneo)
- Cache del navegador (hard refresh: Ctrl+Shift+R)
- El CSP bloqueando recursos externos (ver `csp-helmet-fix.md`)
