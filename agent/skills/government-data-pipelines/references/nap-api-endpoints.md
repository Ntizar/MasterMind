# NAP API — Endpoints y patrones de uso

## Endpoints verificados (2026-06-23)

### ✅ Funcionando

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/v2/conjunto-dato` | GET | Lista TODOS los conjuntos (161 datasets) |
| `/api/v2/conjunto-dato/{id}` | GET | Metadatos de un conjunto específico |
| `/api/v2/fichero/{id}/descarga` | GET | URL de descarga S3 temporal (900s) |
| `/api/swagger/v2/swagger.json` | GET | Definición OpenAPI completa |

### ❌ No funciona

| Endpoint | Método | Error |
|---|---|---|
| `/api/v2/conjunto-dato/{id}/ficheros` | GET | 404 |
| `/` (root) | GET | 404 |

## Autenticación

```
Header: ApiKey: <NAP_API_KEY>
```

La API key está en `.env` (variable `NAP_API_KEY`).

## Respuesta de /conjunto-dato

```json
[
  {
    "id": "896",
    "nombre": "Autobús urbano de Madrid",
    "tipo": "Autobús urbano",
    "regionId": "028",
    "tamaño": 16887040,
    "versiones": [
      {
        "id": "2060",
        "fechaActualizacion": "2026-06-22T00:00:00Z",
        "tamaño": 16887040,
        "ficheros": [
          {
            "id": "2061",
            "nombre": "GTFS-ZIP",
            "nombreTipoFichero": "GTFS",
            "tipo": "GTFS-ZIP"
          }
        ]
      }
    ]
  }
]
```

## Respuesta de /fichero/{id}/descarga

```json
{
  "success": true,
  "data": {
    "enlaceDescarga": "https://naptransportes.blob.core.windows.net/gtfs/.../GTFS.zip?X-Amz-Signed..."
  }
}
```

**⚠️ El enlace caduca en 900 segundos.**

## Tipos de fichero

| `nombreTipoFichero` | `tipo` | Descargable |
|---|---|---|
| GTFS | GTFS-ZIP | ✅ Sí |
| GTFS-RT | GTFS-RT | ❌ No (tiempo real) |
| NetEx | NetEx | ❌ No (formato diferente) |
| SIRI | SIRI | ❌ No (tiempo real) |

## Ejemplo de curl

```bash
# Listar conjuntos
curl -s -H "ApiKey: $NAP_API_KEY" \
  "https://nap.transportes.gob.es/api/v2/conjunto-dato" | \
  python3 -c "import sys,json; data=json.load(sys.stdin); [print(f'{d[\"id\"]}: {d[\"nombre\"]} ({d[\"tamaño\"]/1024/1024:.1f} MB)') for d in data]"

# Metadatos de un conjunto
curl -s -H "ApiKey: $NAP_API_KEY" \
  "https://nap.transportes.gob.es/api/v2/conjunto-dato/896"

# URL de descarga
curl -s -H "ApiKey: $NAP_API_KEY" \
  "https://nap.transportes.gob.es/api/v2/fichero/2061/descarga"

# Descargar ZIP (enlace temporal)
curl -L -o GTFS.zip "https://naptransportes.blob.core.windows.net/gtfs/.../GTFS.zip?X-Amz-Signed..."
```

## Referencias

- API oficial: https://nap.transportes.gob.es/api/index.html?url=/swagger/v2/swagger.json