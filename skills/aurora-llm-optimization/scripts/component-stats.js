#!/usr/bin/env node
/**
 * component-stats.js — Muestra estadísticas del diseño Aurora.
 * 
 * Usage: npm run stats
 */

const fs = require('fs');
const path = require('path');

const ROOT = __dirname + '/..';
const compPath = path.join(ROOT, 'components.json');

try {
  const spec = JSON.parse(fs.readFileSync(compPath, 'utf8'));
  
  console.log('📊 Aurora Design System — Component Stats\n');
  console.log(`  Versión: ${spec.version}`);
  console.log(`  Tipo: ${spec.type}`);
  console.log(`  Scope: ${spec.scope}`);
  
  // Components by category
  const byCat = spec.by_category || {};
  const totalComps = Object.keys(spec.components).length;
  
  console.log(`\n  Componentes totales: ${totalComps}`);
  console.log(`  Categorías: ${Object.keys(byCat).length}`);
  
  console.log('\n  Por categoría:');
  const sorted = Object.entries(byCat).sort((a, b) => b[1].length - a[1].length);
  for (const [cat, items] of sorted) {
    const bar = '█'.repeat(Math.min(items.length, 30));
    console.log(`    ${cat.padEnd(18)} ${items.length.toString().padStart(3)} ${bar}`);
  }
  
  // Top components by selector count
  console.log('\n  Top 10 por selectores:');
  const top = Object.entries(spec.components)
    .sort((a, b) => (b[1].selector_count || 0) - (a[1].selector_count || 0))
    .slice(0, 10);
  for (const [name, comp] of top) {
    const mods = (comp.modifiers || []).length;
    const parts = (comp.parts || []).length;
    console.log(`    .nz-${name.padEnd(20)} ${String(comp.selector_count).padStart(3)} selectors, ${mods} mods, ${parts} parts`);
  }
  
  // Packs summary
  console.log('\n  Packs:');
  for (const [name, pack] of Object.entries(spec.packs)) {
    const mandatory = pack.mandatory ? ' ★' : '';
    console.log(`    ${name.padEnd(12)} ${pack.file.padEnd(22)} ${mandatory} ${pack.description.substring(0, 60)}`);
  }
  
  // Token families
  const cssPath = path.join(ROOT, 'ntizar.css');
  if (fs.existsSync(cssPath)) {
    const css = fs.readFileSync(cssPath, 'utf8');
    const tokens = css.match(/--nz-[\w-]+:/g) || [];
    console.log(`\n  Tokens CSS: ${tokens.length}`);
  }
  
  console.log('\n  Archivos LLM:');
  console.log(`    LLM.md: ${fs.readFileSync(path.join(ROOT, 'LLM.md'), 'utf8').length} bytes`);
  console.log(`    components.json: ${fs.readFileSync(compPath, 'utf8').length} bytes`);
  console.log(`    AGENTS.md: ${fs.readFileSync(path.join(ROOT, 'AGENTS.md'), 'utf8').length} bytes`);
  console.log(`    INDEX.md: ${fs.readFileSync(path.join(ROOT, 'INDEX.md'), 'utf8').length} bytes`);
  
  const examples = fs.readdirSync(path.join(ROOT, 'examples')).filter(f => f.endsWith('.html'));
  console.log(`    examples/: ${examples.length} archivos`);
  
} catch (e) {
  console.error('Error:', e.message);
  process.exit(1);
}
