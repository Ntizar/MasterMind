# Auditoría SPA+Backend: MasterFit v3 (Caso Real)

Este documento recoge los hallazgos y fixes de la auditoría del proyecto MasterFit v3
(`dieta-masterfit`), un SPA con Express backend, persistencia en JSON + GitHub y
visualización con Chart.js + Three.js.

## Stack auditado

| Componente | Tecnología |
|---|---|
| Backend | Express (1 servidor, 12 endpoints REST) |
| Frontend | HTML+CSS+JS vanilla, 5 tabs |
| Charts | Chart.js (peso, pasos, tendencias) |
| 3D | Three.js (cuerpo humano en tab Progreso) |
| Persistencia | JSON file + GitHub Contents API |
| Deploy | NaN.builders (Docker + Kaniko) |
| Auth | Basic Auth (admin/$Nan603060) |

## Hallazgos y fixes

### 🔴 Crítico: borrar ejercicios no funciona

**Causa:** Frontend llama `borrarRegistro('deporte', idx)` que hace fetch a `/api/deporte/${idx}`, pero el backend solo tiene `app.delete('/api/entrenamientos/:index', ...)`.

**Fix:** Cambiar `borrarRegistro('deporte',` → `borrarRegistro('entrenamientos',` en dashboard.html.

**Detección:** `grep -n "fetch.*'/api/" dashboard.html | grep delete` vs `grep "app.delete" server.js`.

### 🔴 Importante: indexOf con duplicados

**Causa:** Tras hacer `.reverse()` en listas de entrenamientos/comidas, se usa `list.indexOf(item)` para encontrar el índice. Si hay dos ejercicios con el mismo nombre, `indexOf` devuelve el PRIMER match, no el seleccionado.

**Fix:** Usar `findIndex()` con callback que compare por timestamp o ID único.

**Patrón incorrecto:**
```javascript
const idx = entrenos.indexOf(entreno); // ❌ bug con duplicados
```

**Patrón correcto:**
```javascript
const idx = entrenos.findIndex(e => e.fecha === entreno.fecha); // ✅
```

### ⚠️ Importante: Tab Progreso no responsive

**Causa:** KPIs en grid fijo de 2 columnas, canvas Three.js a 500px fijo, contenedores sin media queries.

**Fix:** Media queries para 768px y 480px:
- Grids: `grid-template-columns: 1fr` en móvil
- Canvas 3D: 350px (768px) / 280px (480px)
- Labels 3D sprites: reducidas con `scale.set(0.5)`
- Tabs: `overflow-x: auto` + `flex-wrap: nowrap`

### ⚠️ Importante: Tabs no scrollables en móvil

**Causa:** `.mf-tabs-row` con `flex-wrap: wrap` en móvil → los tabs se apilan verticalmente.

**Fix:** `flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch`

### 💡 Mejora: Falta botón editar para entrenamientos

Similar a editar comida: añadir función `editarEntreno()` que rellene formulario y establezca `_editandoEntrenoIdx`.

### 💡 Mejora: Sin loading state para Three.js

**Causa:** El canvas 3D se renderiza con WebGLRenderer que puede tardar. Sin spinner mientras carga.

**Fix:** Añadir overlay con spinner CSS, ocultarlo en `initThreeScene()`.

## Verificación de sincronización GitHub

Pasos para confirmar que la persistencia funciona:

1. **SHA match:** `sha256sum data/database.json` local vs GitHub API
2. **Conteo de registros:** mismo número de pesos, comidas, entrenos, pasos, InBody
3. **Timestamp:** `updated` field coincide entre local y remoto
4. **Prueba DELETE:** `curl -X DELETE .../api/entrenamientos/0` → `{"ok":true}`
5. **Re-verificación:** nuevo GET a `/api/datos` confirma que el registro desapareció

## Carpetas huérfanas

Se detectaron dos carpetas locales apuntando al mismo remoto:

| Carpeta | Commit más reciente | ¿Desplegada? |
|---|---|---|
| `dieta-masterfit/` | `57e510b` (MasterFit v3 auto-sync) | ✅ Sí |
| `dieta/` | `c58820b` (3 commits atrás) | ❌ No |

Ambas apuntan a `origin https://github.com/Ntizar/dieta.git`. El servidor en NaN usa el remoto, no el local, así que la inconsistencia local no afecta producción pero confunde.