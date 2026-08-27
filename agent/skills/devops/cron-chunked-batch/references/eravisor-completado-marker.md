# ERAVisor — Incidente del marcador `.completado`

## Contexto

ERAVisor descarga informes de accidentes ferroviarios de la ERA (European Railway Agency) por país. El cron `eravisor-descarga-paises` (cada 20 min) ejecuta `eravisor-wrapper.sh` que procesa 1 país por ejecución.

## Problema original

El usuario descargó países AT→HU (14 países) y movió las carpetas de PDFs a almacenamiento local. El script determina si un país está completo contando PDFs en `Data/PAIS/`. Al ver 0 PDFs (porque se movieron), reiniciaba desde AT y volvía a descargar todo.

El usuario detectó el problema dos veces:
1. Primera vez: "ha vuelto a empezar por AT" — se parcheó el script y se crearon marcadores para AT→HU
2. Segunda vez: "OTRA VEZ POR LA AT" — resultó que IE también estaba ya en local pero no se había marcado

## Fix aplicado

### 1. Parche en `descargar_siguiente_pais.py` — función `pais_completo()`

```python
def pais_completo(pais, indice):
    if pais not in indice:
        return False
    # Marcador explícito: si existe Data/PAIS/.completado, el país ya fue
    # descargado y movido a otro destino. No necesita re-descarga.
    marcador = DATA_DIR / pais / ".completado"
    if marcador.exists():
        return True
    # ... verificación normal por conteo de archivos ...
```

### 2. Creación de marcadores para los países ya procesados

```bash
cd /root/workspace/ERAVisor/Data
for pais in AT BE BG CH CZ DE DK EE EL ES FI FR HR HU IE; do
  mkdir -p "$pais"
  echo "movido a local" > "$pais/.completado"
done
```

### 3. Limpieza

- Matar proceso activo que estaba descargando AT (`kill PID`)
- Eliminar lock (`descarga_activa.lock`)
- Eliminar carpeta AT parcial descargada erróneamente

## Segundo incidente (2026-07-10) — 7 países más en local

El usuario informó que de la cola pendiente (IT LT LU LV NL NO PL PT RO SE SI SK Serbia UK), los primeros 7 (IT LT LU LV NL NO PL) también estaban ya en local. Solo quedaban PT RO SE SI SK Serbia UK.

### Fix aplicado

1. **Crear marcadores `.completado`** para IT LT LU LV NL NO PL (igual que antes)
2. **Actualizar `eravisor_progress.json`** con `actual: 22` — esto es CRÍTICO porque el wrapper bash (`eravisor-wrapper.sh`) NO comprueba `.completado`, solo el script Python (`descargar_siguiente_pais.py`) lo hace. El wrapper usa el índice `actual` del progress file para decidir qué país procesar.

```bash
# Marcadores
for pais in IT LT LU LV NL NO PL; do
  mkdir -p "$pais"
  echo "movido a local" > "$pais/.completado"
done

# Progress file
cat > eravisor_progress.json <<'EOF'
{
  "países": ["AT","BE","BG","CH","CZ","DE","DK","EE","EL","ES","FI","FR","HR","HU","IE","IT","LT","LU","LV","NL","NO","PL","PT","RO","SE","SI","SK","Serbia","UK"],
  "actual": 22,
  "completado": false,
  "ultima_ejecucion": "2026-07-10 09:45 UTC",
  "pais_procesado": "PL (saltado — en local)",
  "status": "Actualizado: 22 países en local, quedan PT→RO→SE→SI→SK→Serbia→UK"
}
EOF
```

## Lecciones

1. **Parchear TODOS los scripts de entrada:** Había dos scripts (`eravisor-wrapper.sh` bash y `descargar_siguiente_pais.py` Python) con lógica de completitud independiente. El parche `.completado` solo se aplicó al Python. El wrapper bash sigue sin comprobar `.completado` — solo cuenta PDFs vs índice.
2. **Doble red de seguridad:** Para que un chunk "movido a local" no se re-procese, se necesitan DOS cosas:
   - `.completado` marker en el directorio del chunk (protege si el script Python gestiona el flujo)
   - `actual` index actualizado en el progress file (protege si el wrapper bash gestiona el flujo)
   Si solo se hace una, el otro script puede reiniciar desde cero.
3. **Pedir lista completa de chunks ya procesados:** El usuario dijo "ya descargué hasta HU" pero IE también estaba hecho. Preguntar explícitamente antes de crear marcadores.
4. **El usuario puede dar la lista RESTANTE en vez de la completada:** "PT → RO → SE → SI → SK → Serbia → UK" — más fiable porque es más corta y fácil de verificar. Calcular los completados por diferencia.
5. **El marcador `.completado` sobrevive a reinicios:** A diferencia de `batch_progress.json`, el marcador vive en el directorio del chunk y no se ve afectado por reinicios del cron o limpieza de progreso.

## Estado actual (2026-07-10)

- 22 países marcados `.completado`: AT BE BG CH CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV NL NO PL
- Cola pendiente: PT RO SE SI SK Serbia UK (7 países, ~1230 PDFs)
- Cron: `eravisor-descarga-paises` cada 20 min, `actual: 22` → empieza en PT
- PDFs totales en índice: 4715 (29 países)
