# Cross-Boundary Data Sync Pattern

Cuando un dashboard corre en un contenedor aislado (NaN) y necesita datos del host (VM), usar **Git como transport**:

## Patrón

```
Host → script genera JSON → git push → contenedor lee JSON local
```

## collect-status.py (referencia)

Script que ejecuta el **host** (VM) para recolectar datos y generar `status.json`:

```python
# Datos que recolecta:
# 1. Cron jobs: lee /hermes-home/cron/jobs.json
# 2. Skills: cuenta /hermes-home/skills/*/SKILL.md
# 3. Procesos: ps aux --sort=-%mem
# 4. Sesiones: ls -lt /hermes-home/sessions/*.json
# 5. Notas: ls -lt /root/workspace/Mastermind/notes/*.md
# 6. Logs: tail -5 /hermes-home/logs/agent.log
# 7. Sistema: /proc/uptime, /proc/meminfo, df -h /
```

Script completo: `/root/workspace/Mastermind-Dashboard/scripts/collect-status.py`

## Cron Hermes job

```json
{
  "name": "dashboard-status-sync",
  "schedule": "every 30m",
  "prompt": "Ejecuta collect-status.py y push status.json a GitHub"
}
```

## Server.js (contenedor)

```javascript
// Endpoint que sirve el status.json local
app.get('/api/vm-status', (req, res) => {
  const data = JSON.parse(fs.readFileSync('public/status.json'));
  res.json(data);
});
```

## Frontend

```javascript
// Lee datos reales del VM
const res = await fetch('/api/vm-status');
const { crons, skills, processes, activity } = await res.json();
```

## Ventajas

- Sin exponer puertos del host
- Sin VPN ni tunnels
- Datos actualizados cada 30min (suficiente para dashboards de monitoreo)
- GitHub actúa como "base de datos" distribuida
- NaN redeploya automáticamente al hacer push

## Limitaciones

- Delay de 30min (no es tiempo real)
- Requiere que el host tenga git push acceso
- status.json se versiona en el repo (crece el histórico)
