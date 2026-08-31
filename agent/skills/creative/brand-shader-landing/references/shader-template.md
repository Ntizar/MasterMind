# Plantilla: shader GLSL fullscreen vivo para landings de marca

Código extraído del GlamourSurf v3 en producción (https://ntizar.github.io/glamoursurf/).
Adaptar: URL de la textura (imagen de marca), paleta de la luz (vec3 dorado), línea de espuma.

## Fragment shader (WebGL2)

```glsl
#version 300 es
precision highp float;
uniform vec2  uRes;
uniform float uTime;
uniform vec2  uMouse;      // -1..1, suavizado en JS (lerp 0.06)
uniform sampler2D uTex;
out vec4 fragColor;

// flujo de agua: domain-warp (adáptalo: olas→humo→niebla cambiando frecuencias)
vec2 flow(vec2 uv, float t){
  uv.x += sin(uv.y*3.0 + t*0.7)*0.028 + sin(uv.y*9.0 - t*1.3)*0.010;
  uv.y += cos(uv.x*2.5 - t*0.5)*0.022;
  return uv;
}

void main(){
  vec2 uv = gl_FragCoord.xy / uRes;
  vec2 p  = (gl_FragCoord.xy - 0.5*uRes) / min(uRes.x, uRes.y) * 2.0;
  vec2 tuv = flow(uv, uTime);

  // ripples al tocar el agua con el ratón/touch
  vec2 m = uMouse; vec2 pp = p;
  m.x *= uRes.x/uRes.y; pp.x *= uRes.x/uRes.y;
  float d = length(pp - m);
  float ripple = sin(d*22.0 - uTime*4.0) * exp(-d*3.5) * 0.012;
  tuv += normalize(pp - m + 1e-4) * ripple;

  vec3 base = texture(uTex, clamp(tuv, 0.001, 0.999)).rgb;
  // doble capa: reflejo desplazado = sensación de superficie
  vec2 refl = clamp(tuv + vec2(0.0, 0.06 + 0.04*sin(uTime*0.8 + tuv.x*4.0)), 0.001, 0.999);
  base = mix(base, texture(uTex, refl).rgb*0.85, 0.35);

  // espuma animada (banda superior)
  float lip = smoothstep(0.28, 0.62, tuv.y + tuv.x*0.18 - 0.25);
  float foam = 0.5 + 0.5*sin(tuv.x*40.0 + uTime*2.0)*sin(tuv.y*35.0 - uTime*1.5);
  base = mix(base, vec3(1.0,0.98,0.94), lip * smoothstep(0.4,0.9,foam) * 0.35);

  // luz cálida siguiendo el puntero
  base += vec3(1.0,0.72,0.35) * exp(-d*2.2) * 0.16;

  // vignette cinematográfico para que el texto respire
  base *= mix(1.0, smoothstep(1.9, 0.4, length(p))*0.75+0.25, 0.55);

  // grano de película
  float grain = (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898,78.233)) + uTime)*43758.5453)-0.5)*0.035;
  fragColor = vec4(base + grain, 1.0);
}
```

## Scaffolding JS (esqueleto completo)

```javascript
const canvas = document.getElementById('gl');
const gl = canvas.getContext('webgl2', {antialias:true});
// VS mínimo: in vec2 p; void main(){ gl_Position = vec4(p,0.,1.); }
// ... compilar/link (chequear COMPILE_STATUS y LINK_STATUS) ...
// Triángulo gigante (cubre pantalla con 3 vértices):
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
// Textura: MIRRORED_REPEAT en S y T (clave: el warp nunca muestra bordes), LINEAR min filter.
// cargar con Image() y texImage2D cuando onload; flag texReady antes de drawArrays.
// Uniforms cada frame: uRes (canvas.width/height con dpr≤2), uTime, uMouse suavizado (lerp 0.06).
// Loop: requestAnimationFrame; gl.clear + drawArrays(TRIANGLES, 0, 3) solo si texReady.
```

## Checklist de verificación (sin navegador)

```bash
# 1. balance de llaves del shader + sintaxis JS con vm.Script
node -e "
const fs=require('fs'); const html=fs.readFileSync('index.html','utf8');
const s=html.match(/const FS = \`([\s\S]*?)\`;/)[1]; let b=0;
for(const c of s){if(c==='{')b++;if(c==='}')b--}
console.log('shader:', b===0?'OK':'ERROR');
new (require('vm').Script)(html.match(/<script>([\s\S]*?)<\/script>/)[1]);
console.log('JS OK');"
# 2. deploy y curl producción esperando ~40s; grep de contenido característico
```
