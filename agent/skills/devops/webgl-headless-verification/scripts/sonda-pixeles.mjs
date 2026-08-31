// Sonda de píxeles: mide el contenido real del buffer WebGL de una app Three.js
// en puppeteer+SwiftShader. Uso: node sonda-pixeles.mjs [url] 
// Adaptar la URL y los selectores window.App.* a tu proyecto.
import puppeteer from 'puppeteer';

const URL = process.argv[2] || 'http://localhost:5199/demo.html';

const browser = await puppeteer.launch({ headless: 'new',
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, isMobile: true });
await page.goto(URL, { waitUntil: 'networkidle0' });
await new Promise(r => setTimeout(r, 2000));

// --- adaptar: aplicar el estado que quieras medir ---
// await page.evaluate(() => window.Water3J.aplicarEscena('huracan'));
// await page.evaluate(() => window.Water3J.setCamara({ angX: 0.5, dist: 70, auto: false }));
await new Promise(r => setTimeout(r, 12000)); // margen generoso para SwiftShader

function muestrear(franja) {
  return page.evaluate((f) => {
    const cv = document.querySelector('#escena canvas');
    const gl = cv.getContext('webgl2') || cv.getContext('webgl');
    if (!gl) return { error: 'sin contexto GL' };
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    const px = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let mn = 999, mx = 0, s = 0, n = 0;
    const y0 = Math.floor(h * f[0]), y1 = Math.floor(h * f[1]);
    for (let y = y0; y < y1; y += 4)
      for (let x = 0; x < w; x += 4) {
        const i = (y * w + x) * 4;
        const l = 0.3 * px[i] + 0.6 * px[i + 1] + 0.1 * px[i + 2];
        mn = Math.min(mn, l); mx = Math.max(mx, l); s += l; n++;
      }
    return { min: +mn.toFixed(0), max: +mx.toFixed(0), rango: +(mx - mn).toFixed(0), media: +(s / n).toFixed(0) };
  }, franja);
}

const tercios = [[0.3, 0.45], [0.45, 0.6], [0.6, 0.75]];
for (let i = 0; i < 3; i++) {
  const m = await muestrear(tercios[i]);
  console.log(`franja ${tercios[i][0]}-${tercios[i][1]}:`, JSON.stringify(m));
}

// animación: segunda muestra 2 s después, comparar
const a = await muestrear([0.35, 0.7]);
await new Promise(r => setTimeout(r, 2000));
const b = await muestrear([0.35, 0.7]);
const dif = Math.abs(a.media - b.media);
console.log('variación de media entre frames:', dif.toFixed(1), dif > 2 ? '→ ANIMANDO' : '→ CONGELADO/frame caído');

await browser.close();
