---
name: nan-builder-troubleshooting
description: "Troubleshooting para deployments en NaN.builders — OOMKill, proxy CSRF, API keys caducadas, reinicios en cadena, puerto 8787 WebUI, puerto 8765 file server."
version: 1.0.0
author: Ntizar
---

# NaN.builders — Troubleshooting

Guía de diagnóstico y resolución de problemas para instancias de Hermes Agent en NaN.builders.

## 🔍 Diagnóstico Rápido

### Paso 1: ¿El contenedor está vivo?
```bash
ps -p 1 -o pid,comm,args
cat /proc/1/status | grep State
```
PID 1 = `hermes gateway run`. Si está zombie (Z state), el contenedor se reinició por OOMKill.

### Paso 2: ¿WebUI responde?
```bash
curl -sI http://127.0.0.1:8787/ | head -5
```
Debería devolver `302` (redirect a login). Si `Connection refused`, el WebUI no está corriendo.

### Paso 3: ¿Gateway responde?
```bash
/opt/hermes/.venv/bin/hermes gateway status
```
Debería decir "Gateway is running (PID: 1)".

### Paso 4: ¿API key de NaN funciona?
```bash
curl -s "https://api.nan.builders/v1/models" -H "Authorization: Bearer $NAN_API" | head -5
```
Si devuelve 401 `token_not_found_in_db` → la key está caducada/borrada.

## 🚨 Problemas Comunes

### OOMKill (exit 137)
**Síntomas:**
- Contenedor se reinicia frecuentemente
- Logs perdidos ("OOM kill leaves no logs")
- API keys se pierden o caducan
- Sesiones de WebUI se pierden

**Diagnóstico:**
```bash
cat /proc/1/status | grep State
# Si dice "Z (zombie)" → el proceso hijo murió
```

**Solución:** Aumentar memoria del contenedor en NaN.builders dashboard.

### WebUI no accesible desde NaN.proxy (401/403 CSRF)
**Síntomas:** 
- WebUI funciona en `127.0.0.1:8787` pero da error desde `webui-ntizar-ntizar.apps.nan.builders`
- Login no funciona o da 401

**Causa:** El proxy de NaN.builders cambia el `Origin` header pero el WebUI lo valida contra el `Host` interno.

**Solución:**
```bash
# Añadir a las env vars del contenedor
HERMES_WEBUI_ALLOWED_ORIGINS=https://webui-ntizar-ntizar.apps.nan.builders
# Reiniciar el WebUI
kill -9 <webui_pid>
cd /usr/share/hermes-webui && HERMES_WEBUI_ALLOWED_ORIGINS="..." /opt/hermes/.venv/bin/python server.py &
```

### API key NAN_API inválida (401 LiteLLM)
**Síntomas:**
```
Authentication Error, LiteLLM Virtual Key expected. Received=no-key-provided
```

**Causa:** La key en `NAN_API` no existe en la base de datos de LiteLLM de NaN.builders.

**Solución:**
1. Ir a panel de usuario en nan.builders
2. Regenerar API key
3. Actualizar env var `NAN_API` en el contenedor
4. Reiniciar gateway

### WebUI no inicia tras reinicio
**Síntomas:** Puerto 8787 no responde.

**Causa:** El WebUI (PID 199 o similar) no se reinicia automáticamente con el gateway.

**Solución:**
```bash
# Verificar si hay procesos zombies
ps aux | grep defunct
# Reiniciar manualmente
cd /usr/share/hermes-webui && HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8787 /opt/hermes/.venv/bin/python server.py &
```

### Procesos zombie
**Síntomas:** `ps aux` muestra procesos `<defunct>` o `<zombie>`.

**Causa:** El proceso padre (gateway PID 1) no reaprovechó hijos muertos.

**Acción:** No se pueden matar (ya están muertos). Solo se limpian al reiniciar el padre o el contenedor.

## 🔧 Comandos Útiles

```bash
# Ver todas las env vars del gateway
cat /proc/1/environ | tr '\0' '\n'

# Ver memoria disponible
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable"

# Ver procesos escuchando puertos
cat /proc/net/tcp | awk '{print $2}' | grep "0A" | while read addr; do
  port=$((16#${addr##*:}))
  [ $port -lt 10000 ] && echo "Port $port listening"
done | sort -un

# Ver logs del contenedor (si hay)
# NaN.builders no guarda logs tras OOMKill
```

## 📊 Puertos por Defecto

| Puerto | Proceso |
|--------|---------|
| 8765 | Server de archivos del workspace |
| 8787 | Hermes WebUI |
| 8642 | Gateway API (raramente usado directamente) |

## ⚠️ Reglas

1. **Siempre verificar RAM antes de asumir otros problemas.** OOMKill es la causa raíz del 80% de fallos en NaN.
2. **Las env vars se leen al arrancar.** Cambiarlas sin reiniciar el proceso no tiene efecto.
3. **Los logs de NaN.builders se pierden tras OOMKill.** No confiar en ellos para diagnósticos post-reinicio.
4. **El WebUI necesita reinicio manual tras cambios de env vars.** No se reinicia solo.
