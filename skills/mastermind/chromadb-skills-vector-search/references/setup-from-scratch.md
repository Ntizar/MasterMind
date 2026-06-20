# Setup de ChromaDB desde cero en Hermes VM

Procedimiento validado el 2026-06-11 en MicroVM NaN.builders (Debian, Python 3.13.5).

## Problemas encontrados y soluciones

### 1. pip no disponible en Python del sistema

```bash
# python3 -m pip --version → ModuleNotFoundError
# El paquete python3-pip está instalado pero los binarios no funcionan
# Solución: crear venv dedicado
python3 -m venv /hermes-home/chromadb-venv
```

### 2. pip install chromadb bloqueado por detector de servidores

El detector de procesos largos de Hermes confunde `pip install` con un servidor:

```bash
# ESTO FALLA:
pip install chromadb
# → "This foreground command appears to start a long-lived server/watch process"

# SOLUCIÓN: ejecutar en background
terminal(background=true, command="/hermes-home/chromadb-venv/bin/pip install chromadb")
# Luego esperar con process(action="wait", session_id=...)
```

### 3. Dependencia faltante: opentelemetry-instrumentation-fastapi

ChromaDB 1.5.9 importa `opentelemetry.instrumentation.fastapi` al arrancar el servidor FastAPI, pero no lo declara como dependencia:

```bash
# Error al arrancar:
# ModuleNotFoundError: No module named 'opentelemetry.instrumentation'

# Solución:
/hermes-home/chromadb-venv/bin/pip install opentelemetry-instrumentation-fastapi
```

### 4. El indexador no produce output visible

El script original imprimía a stdout pero cuando se ejecuta en background el output no se capturaba:

```bash
# Solución: logging a archivo
# El indexador v2 escribe a /tmp/indexar-skills.log
tail -f /tmp/indexar-skills.log
```

### 5. Arranque del servidor

```bash
# Script de arranque con health check:
bash /hermes-home/scripts/start-chromadb.sh

# Verificar:
curl http://localhost:8000/api/v1/collections
```

### 6. Indexación completa

```bash
cd /hermes-home/scripts
NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python indexar-skills.py --reset
# Tarda ~5-6 minutos para 199 skills (1.5s entre embeddings)
```

## Orden correcto de instalación

```bash
# 1. Crear venv
python3 -m venv /hermes-home/chromadb-venv

# 2. Instalar chromadb (en background)
/hermes-home/chromadb-venv/bin/pip install chromadb

# 3. Instalar dependencia faltante
/hermes-home/chromadb-venv/bin/pip install opentelemetry-instrumentation-fastapi

# 4. Arrancar servidor
bash /hermes-home/scripts/start-chromadb.sh

# 5. Indexar skills
cd /hermes-home/scripts
NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python indexar-skills.py --reset
```