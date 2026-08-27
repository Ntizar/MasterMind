# NaN Deploy Cache — Patrones de Verificación

## Problema

NaN.builders tiene un CDN con cache agresivo (Cloudflare). Los cambios en el HTML no se reflejan inmediatamente en la URL pública.

## Síntomas

- `curl` al deploy sirve versión vieja
- El browser tool muestra versión vieja
- `git log` muestra commit nuevo pero la URL no lo refleja
- El HTML local está bien pero el deploy no

## Patrón de verificación

```bash
# 1. Verificar que el commit está en GitHub
cd /root/workspace/dieta-masterfit
git log --oneline -3

# 2. Esperar y verificar deploy
sleep 30
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep "heroQuickStatus"

# 3. Si no aparece, esperar más
sleep 30
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep "heroQuickStatus"

# 4. Si sigue sin aparecer, forzar con version query
# (añadir ?v=3.4 al script tag en el HTML)
```

## Tiempo típico

- Primer deploy: 1-2 minutos
- Deployes posteriores: 30-60 segundos
- En raras ocasiones: hasta 2 minutos

## Forzar recache

Si el deploy no se actualiza tras 2 minutos:

1. **Version query en script tags** (ya implementado):
   ```html
   <script src="chart.js?v=3.4"></script>
   ```
2. **Commit empty** (si es necesario):
   ```bash
   git commit --allow-empty -m "chore: trigger redeploy" && git push
   ```

## Verificar que el deploy tiene los cambios correctos

```bash
# Verificar elementos clave
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep -c "heroQuickStatus"
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep "switchTab('registrar')"
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep -c "toggleDarkMode"  # debe ser 0

# Verificar que database.json es accesible
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/data/database.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Peso: {len(d[\"peso\"])}')"
```

## Pitfall

**NUNCA asumir que el deploy tiene los cambios solo porque el commit está en GitHub.** Siempre verificar con `curl` a la URL del deploy. El HTML local puede estar perfecto pero el deploy puede tener la versión vieja.

## Debugging "no cargan datos"

Si el usuario dice "no cargan los datos":

1. Verificar que `loadData()` está definida Y llamada (no solo definida)
2. Verificar que `renderDashboard(db)` se llama con los datos
3. Verificar que `database.json` es accesible y tiene datos
4. Verificar que no hay código residual que rompa el JS (dark mode, IIFEs abiertos)
5. Verificar que los tabs tienen `display:none` por defecto
