---
name: pin-auth-nodejs-sqlite
description: >
  Patrón completo de autenticación con PIN para apps Node.js + SQLite (sql.js).
  Migración de BD existente, login con creación de usuario, PIN siempre visible,
  endpoint de set/change PIN, frontend con modal de setup.
version: "2.0.0"
tags:
  - auth
  - security
  - nodejs
  - sqlite
  - pin
---

# PIN Auth — Node.js + SQLite

Patrón de autenticación con PIN de 4-6 dígitos para apps multi-usuario.

## Backend (server.js)

### 1. Schema + Migración (CRÍTICO)

```sql
CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT UNIQUE NOT NULL,
  pin TEXT,  -- nullable: usuarios existentes sin PIN
  activo INTEGER DEFAULT 1,
  created_at TEXT DEFAULT (datetime('now'))
)
```

**⚠️ PITFALL: `CREATE TABLE IF NOT EXISTS` NO añade columnas nuevas a tablas existentes.**
Si la tabla ya existe sin `pin`, el `CREATE TABLE` no hace nada y el `SELECT pin` falla con `no such column`.

**Solución: ALTER TABLE con try-catch después del CREATE TABLE:**
```javascript
db.run(`CREATE TABLE IF NOT EXISTS usuarios (...)`);
// Migración: añadir columna pin si no existe (BDs viejas)
try { db.run("ALTER TABLE usuarios ADD COLUMN pin TEXT"); } catch(e) { /* ya existe */ }
```

El `ALTER TABLE` lanza excepción si la columna ya existe — por eso el try-catch silencioso.

### 2. Login: crear usuario con PIN en primer acceso

```javascript
app.post('/api/auth/login', (req, res) => {
  const { nombre, pin } = req.body;
  let user = sql_get('SELECT id, nombre, pin FROM usuarios WHERE nombre = ?', [cleanName]);
  
  if (user) {
    // Usuario existente — PIN requerido si está configurado
    if (user.pin) {
      if (!pin) return res.status(400).json({ error: 'PIN requerido', pin_required: true });
      if (String(pin).trim() !== user.pin) return res.status(400).json({ error: 'PIN incorrecto' });
    }
  } else {
    // Usuario nuevo — crear CON el PIN que introduce
    const pinValue = (pin && /^\d{4,6}$/.test(String(pin).trim())) ? String(pin).trim() : null;
    sql_run('INSERT INTO usuarios (nombre, pin) VALUES (?, ?)', [cleanName, pinValue]);
    user = { id: lastId(), nombre: cleanName, pin: pinValue };
    sql_run("INSERT INTO perfil (usuario_id, genero, notas) VALUES (?, 'no definido', '')", [user.id]);
  }
  
  const token = crypto.randomBytes(32).toString('hex');
  res.json({ ok: true, sessionId: token, user: { id, nombre }, needs_pin: !user.pin });
});
```

**Flujo:**
- Nuevo + PIN → crea usuario CON PIN → entra
- Nuevo sin PIN → crea usuario SIN PIN → `needs_pin: true` → modal setup
- Existente + tiene PIN + PIN correcto → entra
- Existente + tiene PIN + sin PIN/error → `pin_required: true`
- Existente + sin PIN → entra directo (backward compat)

### 3. Endpoint set/change PIN

```javascript
app.post('/api/auth/set-pin', requireAuth, (req, res) => {
  const { pin } = req.body;
  if (!pin || !/^\d{4,6}$/.test(String(pin).trim())) {
    return res.status(400).json({ error: 'PIN debe ser de 4 a 6 dígitos' });
  }
  sql_run('UPDATE usuarios SET pin = ? WHERE id = ?', [String(pin).trim(), req.userId]);
  saveDB();
  res.json({ ok: true });
});
```

### 4. Usuarios con has_pin

```javascript
app.get('/api/auth/usuarios', (req, res) => {
  const users = sql_all("SELECT id, nombre, pin IS NOT NULL as has_pin FROM usuarios WHERE activo = 1");
  res.json({ ok: true, usuarios: users });
});
```

## Frontend (dashboard.html)

### 5. PIN siempre visible

El input de PIN **NUNCA** se oculta. Siempre está visible debajo del nombre.

```html
<input type="text" id="auth-name" placeholder="Tu nombre" autocomplete="name" autofocus>
<input type="password" id="auth-pin" placeholder="PIN (4-6 dígitos)"
       pattern="[0-9]*" maxlength="6" inputmode="numeric" style="margin-top:12px">
<button class="btn-primary" onclick="doLogin()">Entrar</button>
```

**No usar `display:none` en el PIN.** El usuario debe ver que hay un campo PIN siempre.

### 6. Selector de usuario → foco en PIN

```javascript
data.usuarios.forEach(function(u) {
  var btn = document.createElement('button');
  btn.className = 'user-btn';
  btn.textContent = (u.has_pin ? '🔒 ' : '👤 ') + u.nombre;
  btn.onclick = function() {
    document.getElementById('auth-name').value = u.nombre;
    document.getElementById('auth-pin').value = '';
    document.getElementById('auth-pin').focus();
  };
});
```

Al clicar un perfil: rellena nombre, limpia PIN, foco en PIN. Simple.

### 7. doLogin envía PIN siempre

```javascript
var pin = document.getElementById('auth-pin').value.trim();
var body = { nombre: name };
if (pin) body.pin = pin;
var data = await api('/api/auth/login', { method: 'POST', body });
if (data.ok) {
  document.getElementById('auth-pin').value = '';
  enterApp();
  if (data.needs_pin) setTimeout(showPinSetup, 800);
} else {
  document.getElementById('auth-pin').value = '';
  document.getElementById('auth-pin').focus();
}
```

### 8. Modal setup de PIN (para usuarios sin PIN)

```javascript
function showPinSetup() {
  // Overlay con input password + botones "Configurar" y "Ahora no"
  // POST /api/auth/set-pin con el PIN
}
```

## Pitfalls

1. **`CREATE TABLE IF NOT EXISTS` no migra columnas.** Si la tabla existe sin `pin`, el SELECT falla. Siempre hacer `ALTER TABLE ... ADD COLUMN` con try-catch después del CREATE.
2. **PIN en texto plano** es suficiente para apps de fitness. No usar bcrypt para 4-6 dígitos (overkill + sql.js no soporta native).
3. **Usuarios existentes** quedan sin PIN (nullable). Son compatibles con el sistema nuevo.
4. **`needs_pin: true`** se envía si el usuario NO tiene PIN configurado.
5. **`pin_required: true`** en error response indica que el usuario tiene PIN pero no se proporcionó.
6. **PIN input SIEMPRE visible.** No ocultarlo con display:none. El usuario debe ver que hay seguridad.
7. **No guardar PIN** en localStorage. Solo el sessionId.
8. **sql.js** `pin IS NOT NULL as has_pin` funciona como SQL estándar. Verificar con `node -c`.
