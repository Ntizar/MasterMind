# Diagnóstico de deploy Kaniko exitoso pero contenedor no arranca

## Síntoma

- Build Kaniko: **SUCCEEDED** (imagen empujada al registry)
- URL de NaN: **404 de Cloudflare** (no 502, no timeout)
- Logs del build muestran: `Pushed registry.nan.builders/...`
- El contenedor **no se está desplegando** después del build exitoso

## Causas posibles

### 1. Espacio NaN no creado o mal configurado
El espacio existe en la URL (por eso Cloudflare responde 404) pero **no está conectado al repo correcto** o **no tiene el container port configurado**.

**Verificación:**
- Ir a cloud.nan.builders → abrir el espacio → verificar:
  - Repo linked: `Ntizar/pdf-to-landing` (correcto)
  - Container port: `3000` (debe coincidir con EXPOSE del Dockerfile)
  - Build status: debe mostrar el último commit

### 2. Contenedor crash al arrancar
El build funciona pero el server.js crash al iniciar dentro del contenedor.

**Causas típicas:**
- ESM/CJS mismatch: `"type": "module"` en package.json + `require()` en server.js
- Token NAN_API inválido → el server arranca pero algún módulo crítico falla
- Puerto incorrecto: server escucha en puerto distinto al EXPOSE

**Verificación:** Ver logs del contenedor en cloud.nan.builders → pestaña Logs

### 3. `.env` no se copia al contenedor
El `.env` con NAN_API está en `.dockerignore` → no llega al contenedor → el server arranca pero la IA no funciona.

**Fix:** Quitar `.env` de `.dockerignore`. El `.env` debe estar en el contenedor para el fallback `fs.readFileSync('.env')`.

### 4. `package.json` sin `"type": "module"` + server.js con `import`
Node ejecuta como CommonJS → `import` no existe → crash silencioso.

**Fix:** Añadir `"type": "module"` a package.json.

### 5. `pdf-parse` sin `createRequire` en ESM
`import pdfParse from 'pdf-parse'` → `SyntaxError: does not provide an export named 'default'`

**Fix:** Usar `createRequire` como workaround ESM.

## Flujo de diagnóstico

```bash
# 1. Verificar si el build fue exitoso (mirar logs de NaN)
# 2. Verificar si el contenedor responde
curl -s https://<app>.apps.nan.builders/healthz
# 3. Si 404 de Cloudflare → espacio no provisionado o build fallido
# 4. Si 502 → contenedor crash al arrancar
# 5. Si 200 → todo OK

# 6. Verificar que el Dockerfile es correcto
grep "USER" Dockerfile  # debe tener USER appuser
grep "EXPOSE" Dockerfile  # debe coincidir con container port

# 7. Verificar package.json
grep '"type"' package.json  # debe tener "type": "module" si usa ESM

# 8. Verificar .dockerignore
cat .dockerignore  # NO debe incluir .env
```

## Trigger redeploy

Si el build fue exitoso pero el contenedor no arranca:
1. Hacer commit vacío: `git commit --allow-empty -m "redeploy trigger"`
2. Push: `git push`
3. Esperar 3-5 min (polling de NaN)
4. Verificar: `curl -s https://<app>.apps.nan.builders/healthz`

Si sigue sin funcionar, revisar los logs del contenedor en cloud.nan.builders.
