# Multi-usuario + Onboarding IA — Sesión 2026-06-13

## Resumen

Se implementó soporte multi-usuario y onboarding IA conversacional para MasterFit.

## Endpoints añadidos

### GET /api/auth/usuarios
```
Response: { ok: true, usuarios: [{ id: 1, nombre: "David" }, { id: 2, nombre: "Feli" }] }
```
Lista usuarios activos ordenados por created_at. Usado por frontend para mostrar botones de selector.

### GET /api/onboarding/status
```
Response: { ok: true, completo: false, siguiente: { campo: 'edad', pregunta: '¿Cuántos años tienes?', tipo: 'numero', tabla: 'perfil' } }
Response: { ok: true, completo: true }
```
Verifica si el perfil del usuario actual está completo. Si no, devuelve el siguiente paso pendiente.

### POST /api/onboarding/step
```
Body: { paso: 0, respuesta: "28" }
Response: { ok: true, completo: false, siguiente: { campo: 'altura_cm', ... } }
Response: { ok: true, completo: true, siguiente: null }
```
Guarda la respuesta del usuario. Si paso=2 (peso_actual_kg), INSERT en tabla `peso`. Si no, UPDATE en tabla `perfil`.

## Flujos de prueba

### Onboarding completo (curl)
```bash
TOKEN=$(curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/auth/login -H 'Content-Type: application/json' -d '{"nombre":"Feli"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['sessionId'])")

# Paso 1: edad
curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/step \
  -H "X-Session-Id: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"paso":0,"respuesta":"28"}'

# Paso 2: altura
curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/step \
  -H "X-Session-Id: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"paso":1,"respuesta":"165"}'

# Paso 3: peso actual (va en tabla peso)
curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/step \
  -H "X-Session-Id: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"paso":2,"respuesta":"72"}'

# Paso 4: peso objetivo
curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/step \
  -H "X-Session-Id: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"paso":3,"respuesta":"62"}'

# Paso 5: nivel actividad
curl -s -X POST https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/step \
  -H "X-Session-Id: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"paso":4,"respuesta":"activo"}'

# Verificar completo
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/api/onboarding/status \
  -H "X-Session-Id: $TOKEN"
```

### Verificar deploy
```bash
curl -s https://dieta-ntizar-ntizar.apps.nan.builders/ | grep -o 'onboarding\|loadUsers\|checkOnboarding' | sort -u
```

## Errores encontrados y corregidos

1. **peso_actual_kg en tabla perfil**: El primer intento usaba `UPDATE perfil SET peso_actual_kg = ?` pero la columna no existe. Corregido: paso 3 INSERT en tabla `peso`.
2. **Valores por defecto al crear usuario**: El login creaba perfil con `edad=30, genero='masculino', altura=174` → `perfilCompleto()` devolvía true y se saltaba el onboarding. Corregido: perfil se crea con `genero='no definido'` y todo lo demás NULL.
3. **Conflicto git en rebase**: La DB binaria (`masterfit.db`) tenía conflicto porque local tenía a Feli creada y el remote no. Solución: `git checkout --theirs data/masterfit.db` (aceptar versión remota, la DB se sincroniza por server).
