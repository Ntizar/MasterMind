# Three.js Engine Pitfalls — Quaternion, Materials, Game Loop

> Pitfalls de Three.js r128+ descubiertos en DronRacer (2026-07-08). Aplicables a cualquier proyecto Three.js con física, animación o game loop.

## 1. Quaternion.multiply() NO chaining en r128

**Error:** `_tmpQ.copy(...).multiply(...).multiplyScalar is not a function`

**Causa:** En Three.js r128, `Quaternion.multiply(q)` **no retorna `this`** para chaining — retorna `undefined`. A diferencia de `Vector3.add()` que sí retorna `this`, Quaternion rompe el patrón. Esto causa 1000+ errores/frame silenciosos en game loops.

```javascript
// ❌ ROTO — multiply() retorna undefined en r128
const dq = _tmpQ.copy(S.quat).multiply(omegaQuat).multiplyScalar(0.5);

// ✅ CORRECTO — operaciones separadas
const dq = new THREE.Quaternion().copy(S.quat).multiply(omegaQuat);
dq.x *= 0.5; dq.y *= 0.5; dq.z *= 0.5; dq.w *= 0.5;
```

**Verificación:** En r128, verificar qué métodos de Quaternion soportan chaining:
```javascript
const q = new THREE.Quaternion();
console.log(q.multiply(new THREE.Quaternion()) instanceof THREE.Quaternion); // false en r128
```

**Nota:** Three.js r150+ restaura el chaining. Si se usa una versión reciente, el código chained funciona. Verificar la versión con `THREE.REVISION`.

## 2. MeshStandardMaterial — propiedades custom no validadas

**Warning:** `THREE.MeshStandardMaterial: 'eColor' is not a property of this material.`

**Causa:** Three.js valida propiedades del material y genera warnings para propiedades que no reconoce. No rompe la renderización pero llena la consola.

```javascript
// ❌ Warning — eColor no es una propiedad válida
new THREE.MeshStandardMaterial({ color, eColor, emissive: eColor, ... });

// ✅ Correcto — solo usar propiedades known
const { color, emissive } = powerupData;
new THREE.MeshStandardMaterial({ color, emissive });
```

## 3. Object.assign en Position/Rotation (read-only)

**Error silencioso:** `Object.assign(sceneObject.position, {x: 10, y: 5, z: 0})` no lanza error pero no mueve el objeto.

**Causa:** `Object.assign` llama a los setters, pero `position` es un `Vector3` que no soporta `Object.assign` correctamente.

```javascript
// ❌ ROTO
Object.assign(light.position, { x: 100, y: 200, z: 100 });

// ✅ Correcto
light.position.set(100, 200, 100);
```

## 4. Game Loop Error Debugging — RAF Wrapper Pattern

Cuando hay errores en requestAnimationFrame, el browser los reporta como "exception" sin mensaje útil. Para capturar el error real:

```javascript
let errorCount = 0;
let lastError = '';
const origRAF = window.requestAnimationFrame;
window.requestAnimationFrame = function(cb) {
  return origRAF.call(window, function(time) {
    try { cb(time); }
    catch(e) {
      errorCount++;
      if(errorCount <= 5) {
        lastError = e.message + ' | ' + (e.stack||'').split('\n').slice(0,3).join(' | ');
      }
    }
  });
};

// Verificar después:
JSON.stringify({ errorCount, lastError })

// Restaurar:
window.requestAnimationFrame = origRAF;
```

## 5. Embedded Single-File Deployment (GitHub Pages Legacy)

Cuando GitHub Pages legacy no sirve ES modules, embeber TODO en un solo `<script>` inline:

```html
<script src="https://cdn.jsdelivr.net/npm/three@r128/build/three.min.js"></script>
<script>
  // TODO el JS inline, sin imports, sin exports
  let scene, camera, renderer;
  // ... toda la app
</script>
```

**Verificar syntax del script inline antes de push:**
```bash
node -e "
const fs = require('fs');
const html = fs.readFileSync('index.html','utf8');
const scriptMatch = html.match(/<script>[\\s\\S]*?<\\/script>/g);
if(scriptMatch) {
  const s = scriptMatch[scriptMatch.length-1].replace(/<\\/?script>/g,'');
  try { new Function(s); console.log('✅ OK'); }
  catch(e) { console.log('❌', e.message); }
}
"
```