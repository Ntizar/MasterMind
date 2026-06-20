# Node.js Multi-User App — Patrones de Auditoría

## Contexto

Este documento captura patrones específicos de apps Node.js + Express + SQLite (sql.js) con autenticación multiusuario, detectados durante auditorías reales del proyecto MasterFit (dieta-masterfit).

Se aplica a: apps Express con sql.js, auth por token, vanilla JS frontend, y onboarding por pasos.

---

## Patrón 1: `sql_run` vs `sql_all` — el antipattern invisible

### Síntoma

Un endpoint devuelve `{"ok": true}` sin los datos esperados. No hay error, simplemente faltan campos.

### Causa

En proyectos con sql.js es común tener helpers:

```js
function sql_run(sql, params) { db.run(sql, params || []); }        // No devuelve nada
function sql_all(sql, params) { /* prepara, itera, devuelve rows */ } // Devuelve array
```

Si un endpoint usa `sql_run()` para una consulta SELECT, la variable destino será `undefined` y `JSON.stringify` lo omite silenciosamente.

```js
// 🔴 MAL
const users = sql_run("SELECT * FROM usuarios");  // undefined
res.json({ ok: true, usuarios: users });          // → {"ok": true}

// ✅ BIEN
const users = sql_all("SELECT * FROM usuarios");  // [{id:1, nombre:"X"}, ...]
res.json({ ok: true, usuarios: users });          // → {"ok": true, "usuarios": [...]}
```

### Detección automática

```bash
# Buscar SELECTs ejecutados con sql_run en vez de sql_all
grep -n "sql_run.*SELECT" server.js

# Buscar endpoints que devuelvan el resultado sin verificar
grep -nB2 "res.json.*{.*ok.*true" server.js | grep -v "sql_all\|sql_get"
```

### Verificación funcional

```bash
# Para cada endpoint GET que lista datos, curl directo:
curl -s URL | python3 -c "import sys,json; d=json.load(sys.stdin); print('keys:', list(d.keys()))"
```

- Si el endpoint debería devolver `usuarios` pero no aparece → sospechar `sql_run` en vez de `sql_all`
- Si devuelve array vacío `[]` pero hay datos en DB → revisar filtro WHERE (usuario_id incorrecto, fechas, etc.)

### Lección

**En Node.js con sql.js, `sql_run` solo ejecuta (INSERT/UPDATE/DELETE). Para SELECTs usar `sql_all` (array) o `sql_get` (único).** No hay error si usas el equivocado — el cliente recibe JSON incompleto sin enterarse.

---

## Patrón 2: `getMeta()` global vs datos por usuario

### Síntoma

Amadeo (o cualquier IA) se dirige al usuario por un nombre incorrecto. Todos los usuarios reciben el mismo nombre en el prompt de IA.

### Causa

La función `getMeta(key)` lee de una tabla `meta` key-value **global**. Si el nombre del usuario se guarda con `getMeta('nombre')` en vez de desde la tabla `usuarios.nombre`, TODOS los usuarios ven el nombre del primero que se registró.

```js
// 🔴 MAL — global, siempre devuelve el mismo nombre
function perfilUsuario(userId) {
  return {
    nombre: getMeta('nombre') || 'Usuario',  // ← tabla META (global)
    ...
  };
}

// ✅ BIEN — específico del usuario
function perfilUsuario(userId) {
  const user = sql_get("SELECT nombre FROM usuarios WHERE id = ?", [userId]);
  return {
    nombre: user?.nombre || 'Usuario',
    ...
  };
}
```

### Detección automática

```bash
# Buscar getMeta() dentro de funciones perfilUsuario o contextoPerfil
grep -n "getMeta" server.js

# Buscar si perfilUsuario usa getMeta en vez de la tabla usuarios
grep -n "nombre.*getMeta\|getMeta.*nombre" server.js
```

### Verificación

```bash
# Crear dos sesiones como usuarios distintos y verificar qué nombre recibe la IA
curl -X POST URL/api/auth/login -H "Content-Type: application/json" -d '{"nombre":"Test1"}'  # → obtener session_id
curl URL/api/datos -H "X-Session-Id: <session1>" | python3 -c "import sys,json; print(json.load(sys.stdin)['meta']['nombre'])"
```

### Lección

**En apps multi-usuario, `meta` key-value es para configuración global (fecha_inicio, versión). Datos del usuario (nombre, edad, etc.) van en tabla `usuarios` o `perfil` con `usuario_id`.** No mezclar capas.

---

## Patrón 3: Auth por token en header, no cookie

### Estructura observada (correcta)

```
Frontend:
  localStorage.setItem('mf_session', token)
  headers['X-Session-Id'] = token

Backend:
  function getSessionUserId(req) {
    const token = req.headers['x-session-id'] || req.query.session_id;
    const row = sql_get("SELECT usuario_id FROM sesiones WHERE token = ? AND expires_at > datetime('now')", [token]);
    return row ? row.usuario_id : null;
  }
```

### Ventajas de este patrón
- Sin cookies → sin CSRF
- Sin dependencias de sesión de Express → funciona en entornos serverless
- El frontend controla explícitamente el envío
- Fácil de depurar (curl con `-H "X-Session-Id: X"`)

### Riesgos a auditar
- **Token en URL** (`req.query.session_id`): Puede quedar en logs del servidor. Preferir solo header.
- **Limpieza de sesiones expiradas**: Verificar que hay un `DELETE FROM sesiones WHERE expires_at < datetime('now')` periódico (cada hora o al crear nueva sesión).
- **Token en localStorage**: Persiste aunque el usuario cierre sesión. Asegurar que `doLogout()` borra localStorage + backend.

### Verificación

```bash
# Verificar que 401 funciona
curl -s URL/api/datos | python3 -c "import sys,json; print(json.load(sys.stdin))['error']"  # → "No autenticado"

# Verificar limpieza de sesiones vencidas
sqlite3 data/masterfit.db "SELECT COUNT(*) FROM sesiones WHERE expires_at < datetime('now');"
```

---

## Patrón 4: Onboarding como formulario vs conversación

### El problema

Muchas apps multiusuario implementan onboarding como una secuencia fija de pasos:

```js
const ONBOARDING_STEPS = [
  { campo: 'edad', pregunta: '¿Cuántos años tienes?', tipo: 'numero' },
  { campo: 'altura_cm', pregunta: '¿Cuánto mides (en cm)?', tipo: 'numero' },
  // ... pasos fijos
];
```

Esto tiene limitaciones:
- **No es natural**: No hay personalidad ni calidez. Parece un formulario, no una conversación.
- **No se adapta**: Si el usuario responde con matices ("tengo 36, pero entreno desde los 20"), el onboarding no lo captura.
- **No hay follow-up**: Una vez completo, el sistema no pregunta "¿cuál es tu experiencia?" o "¿lesiones?".
- **No hay relación**: Amadeo no construye una relación con el usuario — solo recoge datos fríos.

### Patrón deseado (conversacional con IA)

1. **Amadeo saluda y pregunta abiertamente** → "¡Hola! Soy Amadeo, tu coach. Cuéntame de ti, ¿cuántos años tienes, qué entrenas, cuál es tu objetivo?"
2. **El usuario responde con lenguaje natural** → "Tengo 36, mido 174, quiero bajar de 98 a 88 kg"
3. **Amadeo extrae los datos vía IA** → La IA parsea la respuesta y registra en DB
4. **Amadeo confirma y sigue** → "Genial, 36 años, 174 cm, objetivo 88 kg. ¿Y tu nivel de actividad?"
5. **Repetir hasta perfil completo**

### Implementación sugerida

```js
app.post('/api/ia/onboarding', requireAuth, async (req, res) => {
  const { mensaje, paso } = req.body;
  const uid = req.userId;
  
  const respuesta = await llamarIA({
    system: "Eres Amadeo Llados, coach de fitness. Tu objetivo es conocer al usuario. Del usuario: " + ...,
    user: "Mensaje del usuario: " + mensaje + "\n\nExtrae en JSON los campos que puedas identificar..."
  });
  
  // Registrar lo que la IA extrajo
  if (respuesta.edad) sql_run("UPDATE perfil SET edad = ? WHERE usuario_id = ?", [respuesta.edad, uid]);
  // ...
  
  res.json({ ok: true, registrado: respuesta, siguiente_pregunta: respuesta.siguiente });
});
```

### Verificación de onboarding

```bash
# Verificar que un usuario nuevo tiene onboarding pendiente
curl URL/api/onboarding/status -H "X-Session-Id: <token>" | python3 -m json.tool

# Verificar que al completar, perfil está completo
sqlite3 data/masterfit.db "SELECT * FROM perfil WHERE usuario_id = 1;"
```

---

## Patrón 5: Chat persistente vs localStorage

### El problema

Cuando el chat de IA se guarda solo en `localStorage` por día:

```js
var key = 'mf_chat_' + today();
localStorage.setItem(key, JSON.stringify(appState.chatMessages));
```

Implicaciones:
- **No hay memoria entre sesiones** del usuario (Amadeo no recuerda conversaciones previas)
- **No hay sync entre dispositivos** (móvil vs escritorio)
- **Se pierde al borrar localStorage** (mantenimiento del navegador)
- **No hay historial de IA** para análisis o mejora

### Patrón deseado

```sql
CREATE TABLE IF NOT EXISTS chat_mensajes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL,
  fecha TEXT NOT NULL,
  rol TEXT NOT NULL,  -- 'user' | 'assistant'
  contenido TEXT NOT NULL,
  metadata TEXT,      -- JSON con pasos de onboarding, etc.
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

### Verificación de persistencia

```bash
# Verificar si hay tabla de chat
sqlite3 data/masterfit.db ".tables" | grep -c chat

# Verificar mensajes por usuario
sqlite3 data/masterfit.db "SELECT COUNT(*), usuario_id FROM chat_mensajes GROUP BY usuario_id;"
```

---

## Índice de detección rápida

| Síntoma | Patrón sospechoso | Cómo confirmar |
|---------|-------------------|----------------|
| Endpoint devuelve `{}` sin datos esperados | `sql_run()` para SELECT | `grep -n "sql_run.*SELECT" server.js` |
| Todos los usuarios se llaman igual en la IA | `getMeta('nombre')` | `grep -n "getMeta" server.js` |
| Chat se pierde al cambiar de navegador | Solo en `localStorage` | Buscar `localStorage.getItem` + `chat` |
| Usuario nuevo no recibe onboarding | Sin endpoint `onboarding/status` | `grep -rn "onboarding" server.js` |