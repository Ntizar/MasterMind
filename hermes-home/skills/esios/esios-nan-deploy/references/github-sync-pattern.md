# GitHub Contents API Sync Pattern (2026-06-11)

## Problema

NaN containers pierden filesystem en redeploy. Si una app escribe datos (JSON, SQLite, etc.), se pierden al siguiente deploy.

## Solución: GitHub Contents API

Usar la API de Contents de GitHub para mantener un archivo en el repo sincronizado con los datos del contenedor. **No necesita git CLI en el contenedor.**

### Flujo

1. Mutación en el contenedor → `writeDB(db)` (guarda local)
2. `syncGitHub(db)` (async, background) → actualiza el archivo en GitHub
3. En redeploy → el Dockerfile `COPY . .` trae el último `database.json` desde GitHub

### Implementación (Node.js)

```javascript
async function syncGitHub(db) {
  const token = getNanToken(); // process.env.NAN_API o .env
  if (!token) return;

  // 1. Obtener SHA actual del archivo
  const getRes = await fetch('https://api.github.com/repos/OWNER/REPO/contents/data/database.json', {
    headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/vnd.github.v3+json' }
  });
  if (!getRes.ok) return;
  const { sha } = await getRes.json();

  // 2. Subir contenido actualizado (base64)
  const content = JSON.stringify(db, null, 2);
  const b64 = Buffer.from(content).toString('base64');

  await fetch('https://api.github.com/repos/OWNER/REPO/contents/data/database.json', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json'
    },
    body: JSON.stringify({
      message: `App: actualización ${new Date().toISOString().slice(0,19)}`,
      content: b64,
      sha
    })
  });
}
```

### Dónde llamarlo

En **TODOS** los endpoints de mutación (POST, PUT, DELETE). No esperar a que termine — fire and forget:

```javascript
writeDB(db);
syncGitHub(db); // async, no bloquea la respuesta
res.json({ ok: true });
```

### Requisitos

- Token GitHub con permisos de escritura (Contents: Read and write)
- El archivo DEBE existir previamente en el repo (el sync actualiza, no crea)
- El Dockerfile debe `COPY . .` para que el archivo esté en el contenedor

### Pitfalls

- **Token sin permisos:** el sync falla silenciosamente (solo `console.error`). Verificar: `curl -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/OWNER/REPO`
- **Archivo no existe en GitHub:** el PUT falla con 422. Asegurar que el archivo está en el repo antes del primer sync
- **Race condition:** si dos mutaciones pasan casi simultáneamente, la segunda puede leer un SHA obsoleto. Para apps con poco tráfico no es problema. Para alto tráfico, usar un lock o queue
- **syncGitHub es fire-and-forget:** si falla, el dato se guarda localmente pero no en GitHub. El usuario puede no darse cuenta hasta el próximo redeploy
