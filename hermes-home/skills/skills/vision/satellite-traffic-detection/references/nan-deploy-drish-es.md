# Deploy DRISH-ES en NaN Builders

## URL objetivo
`https://drish-es-ntizar-ntizar.apps.nan.builders`

## Configuración en dashboard NaN

- **Repo:** Ntizar/drish-es (privado)
- **Branch:** main
- **Container Port:** 4000

### Variables de entorno (pestaña Env)

```
COPERNICUS_CLIENT_ID=3081b7b8-40cd-4873-9b2d-9870bd02ec51
COPERNICUS_CLIENT_SECRET=sh-5f8b630b-b083-49ed-b340-b8f01ecb81c4
```

## Pitfall: .env no llega al contenedor

El `.env` del proyecto DrishX/ contiene las credenciales para desarrollo local.
En NaN, el `.env` NO está en el repo (gitignore) → NO se copia al contenedor.
Las credenciales se pasan como env vars en el dashboard de NaN.

El código usa `os.getenv()` que funciona tanto con .env (local) como con env vars (NaN).

## Verificación post-deploy

```bash
# Healthcheck
curl -s https://drish-es-ntizar-ntizar.apps.nan.builders/api/sites | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'{len(d)} sites cargados')
for s in d[:3]: print(f'  {s[\"name\"]}')
"

# Análisis de prueba (M-30 Madrid)
curl -s -X POST https://drish-es-ntizar-ntizar.apps.nan.builders/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"bbox":[40.420,-3.720,40.470,-3.640],"label":"Test M-30","months":1,"max_frames":2}'
```
