#!/usr/bin/env python3
"""Vigia de cron: alerta SOLO ante fallos nuevos. Salida vacia = silencio (no_agent).

Instalar en ~/.hermes/scripts/ (en David: %LOCALAPPDATA%/hermes/scripts/vigia-cron.py)
y crear el job:
  hermes cron create "*/30 * * * *" --name vigia-cron --no-agent \
      --script vigia-cron.py --deliver telegram
(logra absoluta a --script falla: exige ruta relativa a ~/.hermes/scripts/)

Estado en ~/.hermes/cron/vigia-estado.json para dedup: solo avisa de un fallo
la PRIMERA vez que lo ve (hash nombre|last_run_at); al arreglarlo y volver a
fallar con otro run, avisara otra vez.
"""
import json, os

P = os.path.join(os.environ['LOCALAPPDATA'], 'hermes', 'cron', 'jobs.json')
STATE = os.path.join(os.environ['LOCALAPPDATA'], 'hermes', 'cron', 'vigia-estado.json')

try:
    d = json.load(open(P, encoding='utf-8'))
    jobs = d if isinstance(d, list) else d.get('jobs', [])
except Exception as e:
    print("🚨 Vigia de cron: no puedo leer jobs.json (%s)" % e)
    raise SystemExit

prev = json.load(open(STATE, encoding='utf-8')) if os.path.exists(STATE) else {}
alertas = []
for j in jobs:
    if not j.get('enabled', True) or j.get('name') == 'vigia-cron':
        continue  # el vigía no se vigila a sí mismo
    st = j.get('last_status')
    fs = j.get('failure_streak') or 0
    key = "%s|%s" % (j['name'], j.get('last_run_at'))
    if st not in ('ok', None, 'running', 'scheduled') and prev.get(j['id']) != key:
        alertas.append("❌ %s — estado %s, racha %d fallos. Ultimo error: %s" % (
            j['name'], st, fs, (j.get('last_error') or '')[:160].replace('\n', ' ')))
        prev[j['id']] = key

json.dump(prev, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False)
if alertas:
    print("🚨 Vigia de cron — fallos nuevos detectados:")
    print("\n".join(alertas))
    print("Arreglar: hermes cron list | revisar output en ~/AppData/Local/hermes/cron/output/")
# sin fallos nuevos -> stdout vacio -> sin entrega (patron watchdog no_agent)
