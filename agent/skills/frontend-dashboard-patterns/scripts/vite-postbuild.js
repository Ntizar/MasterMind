// vite-postbuild.js — Copia scripts JS/CSS al dist/ y transforma referencias en HTML
// Vite no transforma scripts IIFE (sin type="module"), así que los copiamos manualmente.
// Uso: node scripts/vite-postbuild.js

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.dirname(__dirname);
const distDir = path.join(projectRoot, 'dist');
const srcJsDir = path.join(projectRoot, 'js');
const srcCssDir = path.join(projectRoot, 'css');

// Leer el HTML generado por Vite
const htmlPath = path.join(distDir, 'index.html');
if (!fs.existsSync(htmlPath)) {
    console.error('Error: dist/index.html no existe. Ejecuta "vite build" primero.');
    process.exit(1);
}

let html = fs.readFileSync(htmlPath, 'utf-8');

// Lista de scripts JS a copiar (actualizar según los archivos del proyecto)
const jsFiles = [
    'constants.js', 'theme.js', 'nuclear.js', 'weather.js',
    'demand.js', 'storage.js', 'policy.js', 'scenarios.js',
    'simulator.js', 'montecarlo.js', 'trajectory.js',
    'charts.js', 'ree-data.js', 'app.js',
];

// Copiar JS a dist/js/
fs.mkdirSync(path.join(distDir, 'js'), { recursive: true });
for (const jsFile of jsFiles) {
    const src = path.join(srcJsDir, jsFile);
    const dest = path.join(distDir, 'js', jsFile);
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
        console.log(`  ✓ Copiado: js/${jsFile}`);
    } else {
        console.warn(`  ✗ No encontrado: js/${jsFile}`);
    }
}

// Copiar CSS a dist/css/
fs.mkdirSync(path.join(distDir, 'css'), { recursive: true });
const cssFiles = ['ntizar.css', 'app.css', 'ree-data.css'];
for (const cssFile of cssFiles) {
    const src = path.join(srcCssDir, cssFile);
    const dest = path.join(distDir, 'css', cssFile);
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
        console.log(`  ✓ Copiado: css/${cssFile}`);
    } else {
        console.warn(`  ✗ No encontrado: css/${cssFile}`);
    }
}

// Transformar las referencias en el HTML
// Vite deja las referencias como src="/js/..." y href="/css/..."
// El deploy necesita src="js/..." (sin barra inicial)
html = html.replace(/src="\/js\//g, 'src="js/');
html = html.replace(/href="\/css\//g, 'href="css/');

fs.writeFileSync(htmlPath, html);
console.log('✓ Post-build completado: referencias transformadas en index.html');
