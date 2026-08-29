# 03 — Operación diaria

## Comandos clave

```bash
cd C:/Users/d_ant/Projects/MasterMind
python scripts/consultar-skills.py "consulta" --json   # búsqueda semántica de skills
python scripts/indexar-skills.py [--reset]             # reindexar tras crear skills
python scripts/doctor.py                               # health check del sistema
python scripts/test-doctor.py                          # tests del doctor (bug-inyección)
bash scripts/run-stars-explorer.sh --batch 3 --json    # explorar stars manual
```

## El doctor

`doctor.py` verifica 5 cosas: gateway vivo, crons con runs recientes (<25h),
ChromaDB sincronizada con los SKILL.md en disco, stars-registry fresco y git limpio.
`--json` para consumo por cron.

`test-doctor.py` valida al doctor con el patrón bug-inyección (inspirado en
javierpa95/harness): inyecta cada bug REAL en sandboxes aislados bajo `%TEMP%` y
verifica que el doctor lo detecta. Ejecutar tras tocar `doctor.py`.

## Gateway y crons

El gateway autoarranca al login (`Hermes_Gateway.vbs` en Startup). Comprobar:
`hermes gateway status`. Los crons (scout de stars cada 6h, digest semanal los
lunes, doctor diario) viven si el gateway está vivo.

## Reglas de git

- El scout pushea cada 6h: si un push propio se rechaza con "fetch first",
  resolver SIEMPRE con `git pull --rebase origin master && git push` (nunca merge, nunca force).
- Commits atómicos, mensajes en castellano.
