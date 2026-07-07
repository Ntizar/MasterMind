---
name: webui-csrf-origin
description: Fix CSRF origin mismatch when Hermes WebUI is proxied through NaN.builders or other reverse proxies.
---

# WebUI CSRF Origin Mismatch

## Cuándo aplicar

Si el WebUI de Hermes (puerto 8787) funciona por Telegram pero da **server error / 500 / "Cross-origin mismatch"** desde la web de NaN.builders (`https://webui-ntizar-ntizar.apps.nan.builders/`), el problema es CSRF.

## Causa

El WebUI valida `Origin`/`Referer` contra `Host` en cada POST. Cuando NaN.builders hace proxy, el Origin del navegador es `https://webui-ntizar-ntizar.apps.nan.builders` pero el Host interno del contenedor es diferente → el WebUI rechaza la petición.

## Diagnóstico

```bash
# Verificar si HERMES_WEBUI_ALLOWED_ORIGINS está configurado
cat /proc/199/environ 2>/dev/null | tr '\0' '\n' | grep -i ALLOWED_ORIGINS
# Si no devuelve nada → ese es el problema
```

## Solución

```bash
# Añadir la variable de entorno al contenedor
# En Kubernetes, actualizar el deployment con:
kubectl set env deployment/ntizar-agent \
  HERMES_WEBUI_ALLOWED_ORIGINS=https://webui-ntizar-ntizar.apps.nan.builders

# O editar el deployment directamente:
kubectl edit deployment ntizar-agent
# Añadir en spec.template.spec.containers[0].env:
# - name: HERMES_WEBUI_ALLOWED_ORIGINS
#   value: "https://webui-ntizar-ntizar.apps.nan.builders"
```

Después de cambiar la variable, el contenedor se reinicia automáticamente (rolling update).

## Notas

- El valor debe incluir el esquema (`https://`), no solo el dominio.
- Si se usan múltiples dominios, separar por comas: `https://a.com,https://b.com`.
- El WebUI también respeta `X-Forwarded-Host` y `X-Real-Host` como fallback para proxies reverso.
- Esta protección existe para prevenir CSRF en despliegues públicos.
