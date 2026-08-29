# 06 — Recuperación desde cero

Si se pierde el PC, el sistema se reconstruye desde el repo. Orden exacto:

1. **Instalar Hermes Agent** (desktop) y clonar el repo:
   `git clone https://github.com/Ntizar/MasterMind.git C:/Users/d_ant/Projects/MasterMind`
2. **Instalar Python del sistema + chromadb**:
   usar `C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe`
   (el python del PATH de Hermes no tiene pip) → `pip install chromadb`
3. **Sincronizar identidad y memorias**: copiar `agent/skills/` →
   `%LOCALAPPDATA%\hermes\skills\` y `agent/MEMORY.md` / `agent/USER.md` →
   `%LOCALAPPDATA%\hermes\memories\`
4. **Configurar .env** de Hermes con `OPENAI_API_KEY` / `OPENAI_BASE_URL` de NaN
   (los secrets NO viven en el repo, por diseño).
5. **Indexar skills**: `python scripts/indexar-skills.py --reset`
6. **Gateway**: `hermes gateway install` (activa los crons) y arrancar
   `Hermes_Gateway.vbs` como startup item.
7. **Verificar**: `python scripts/doctor.py` y `python scripts/test-doctor.py`.

Con eso el sistema queda idéntico: skills, memorias de especialistas (van dentro
del repo), crons y búsqueda semántica operativos.

## Qué NO se recupera del repo (y es intencional)

- Secrets (`.env`) — regenerar a mano.
- Caches locales (`~/.mastermind/chromadb` se regenera con `--reset`).
- Estado efímero de sesiones.
