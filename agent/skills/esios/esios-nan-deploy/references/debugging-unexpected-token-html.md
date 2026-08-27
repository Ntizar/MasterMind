# Debugging: "Unexpected token '<'" en IA / API endpoints

## Síntoma

El frontend de un dashboard recibe `Unexpected token '<', "<html>...` al hacer fetch a un endpoint interno (ej: `/api/ia/consejo`).

## Causa

El servidor devuelve **HTML de error** (500, 401, 404) en vez de JSON. Esto pasa cuando:
1. **Token API inválido o faltante** → la API externa devuelve 401 HTML
2. **Servidor crash al arrancar** → nginx/Cloudflare devuelve su página de error HTML
3. **Endpoint mal configurado** → el router no enruta a la función correcta

## Diagnóstico

```bash
# ¿Devuelve HTML o JSON?
curl -s https://app.apps.nan.builders/api/ia/consejo \
  -H 'Content-Type: application/json' \
  -d '{"mensaje":"test"}' | head -c 200

# Si devuelve "<!DOCTYPE html>" o "<html>" → es error HTML, no JSON
# Si devuelve "{"consejo":"..." → funciona

# Verificar si el token está disponible en el contenedor
docker exec <container> node -e "console.log(process.env.NAN_API)"
```

## Fix por capa

### Capa 1: Token no configurado en NaN Env
- Ir a [cloud.nan.builders](https://cloud.nan.builders) → espacio → pestaña **Env**
- Añadir `NAN_API` con el token real
- Redeploy

### Capa 2: Token no disponible en contenedor (no en NaN Env)
- Crear `.env` en el proyecto con el token
- Añadir `.env` a `.gitignore` (no a `.dockerignore`)
- El server.js debe leer el `.env` como fallback (ver patrón en `esios-nan-deploy`)

### Capa 3: Error en la API externa
- Probar el token directamente:
  ```bash
  curl -s -H "Authorization: Bearer $NAN_API" https://api.nan.builders/v1/models
  ```
- Si devuelve error → el token es inválido o expirado

### Capa 4: Servidor crash
- Verificar logs del contenedor
- Comprobar ESM/CJS mismatch (`"type": "module"` + `require()`)
- Verificar que el usuario no-root tiene permisos de lectura en `.env`

## Prevención

- Siempre añadir `try/catch` en endpoints que llaman a APIs externas
- Siempre devolver JSON válido incluso en error: `{ consejo: "error msg", fallback: true }`
- Nunca mostrar stack traces o detalles técnicos al frontend
- Frontend debe verificar `r.ok` y `r.headers.get('content-type')` antes de parsear JSON
