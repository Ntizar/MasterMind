#!/usr/bin/env node
/**
 * validate-llm.js — Valida que los archivos LLM estén consistentes.
 * 
 * Checks:
 * 1. LLM.md existe y tiene contenido
 * 2. components.json es JSON válido
 * 3. components.json tiene todos los packs
 * 4. Los ejemplos existen
 * 5. INDEX.md referencia a LLM.md
 * 6. AGENTS.md referencia a LLM.md
 */

const fs = require('fs');
const path = require('path');

const ROOT = __dirname + '/..';
let errors = 0;
let warnings = 0;

function check(name, condition, errorMsg, warnOnly = false) {
  if (condition) {
    console.log(`  ✓ ${name}`);
  } else {
    if (warnOnly) {
      console.log(`  ⚠ ${name}: ${errorMsg}`);
      warnings++;
    } else {
      console.log(`  ✗ ${name}: ${errorMsg}`);
      errors++;
    }
  }
}

console.log('🔍 Validando Aurora LLM setup...\n');

// 1. LLM.md
const llmPath = path.join(ROOT, 'LLM.md');
check('LLM.md existe', fs.existsSync(llmPath), 'No se encontró LLM.md');
if (fs.existsSync(llmPath)) {
  const content = fs.readFileSync(llmPath, 'utf8');
  check('LLM.md tiene contenido (>1KB)', content.length > 1000, 
    `Solo ${content.length} bytes (mínimo 1000)`);
  check('LLM.md tiene tabla de packs', content.includes('Packs a cargar') || content.includes('packs'),
    'No se encontró tabla de packs');
  check('LLM.md tiene anti-patrones', content.includes('❌') || content.includes('Anti'),
    'No se encontraron anti-patrones');
}

// 2. components.json
const compPath = path.join(ROOT, 'components.json');
check('components.json existe', fs.existsSync(compPath), 'No se encontró components.json');
if (fs.existsSync(compPath)) {
  try {
    const comp = JSON.parse(fs.readFileSync(compPath, 'utf8'));
    check('components.json es JSON válido', true, 'JSON inválido');
    check('components.json tiene name', !!comp.name, 'Falta campo "name"');
    check('components.json tiene packs', !!comp.packs, 'Falta campo "packs"');
    check('components.json tiene components', !!comp.components, 'Falta campo "components"');
    
    const packNames = Object.keys(comp.packs || {});
    const expectedPacks = ['core', 'themes', 'data', 'charts', 'maps', 'viz', 'motion', 'forms', 'ui', 'patterns', 'next'];
    const missingPacks = expectedPacks.filter(p => !packNames.includes(p));
    check('components.json tiene todos los packs', missingPacks.length === 0,
      `Faltan: ${missingPacks.join(', ')}`);
    
    const compCount = Object.keys(comp.components || {}).length;
    check(`components.json tiene componentes (${compCount})`, compCount > 50,
      `Solo ${compCount} componentes (esperado >50)`);
  } catch (e) {
    check('components.json es JSON válido', false, `Error: ${e.message}`);
  }
}

// 3. Examples
const examplesDir = path.join(ROOT, 'examples');
check('examples/ existe', fs.existsSync(examplesDir), 'No se encontró examples/');
if (fs.existsSync(examplesDir)) {
  const examples = fs.readdirSync(examplesDir).filter(f => f.endsWith('.html'));
  check(`examples/ tiene archivos HTML (${examples.length})`, examples.length >= 3,
    `Solo ${examples.length} ejemplos (esperado >=3)`);
  const expectedExamples = ['login.html', 'dashboard.html', 'landing.html', 'forms.html', 'ui-components.html'];
  const missingExamples = expectedExamples.filter(e => !examples.includes(e));
  if (missingExamples.length > 0) {
    console.log(`  ⚠ Ejemplos faltantes: ${missingExamples.join(', ')}`);
    warnings++;
  }
}

// 4. INDEX.md references LLM.md
const indexPath = path.join(ROOT, 'INDEX.md');
if (fs.existsSync(indexPath)) {
  const indexContent = fs.readFileSync(indexPath, 'utf8');
  check('INDEX.md referencia a LLM.md', 
    indexContent.includes('LLM.md') || indexContent.includes('llm.md'),
    'INDEX.md no menciona LLM.md');
}

// 5. AGENTS.md references LLM.md
const agentsPath = path.join(ROOT, 'AGENTS.md');
if (fs.existsSync(agentsPath)) {
  const agentsContent = fs.readFileSync(agentsPath, 'utf8');
  check('AGENTS.md referencia a LLM.md',
    agentsContent.includes('LLM.md') || agentsContent.includes('llm.md'),
    'AGENTS.md no menciona LLM.md');
}

// 6. package.json includes new files
const pkgPath = path.join(ROOT, 'package.json');
if (fs.existsSync(pkgPath)) {
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  check('package.json incluye components.json en files',
    (pkg.files || []).includes('components.json'),
    'components.json no está en package.json files');
  check('package.json incluye LLM.md en files',
    (pkg.files || []).includes('LLM.md'),
    'LLM.md no está en package.json files');
  check('package.json incluye examples/ en files',
    (pkg.files || []).includes('examples/'),
    'examples/ no está en package.json files');
  check('package.json tiene script validate:llm',
    !!pkg.scripts?.['validate:llm'],
    'Falta script validate:llm');
}

console.log(`\n${'='.repeat(50)}`);
if (errors === 0 && warnings === 0) {
  console.log('✅ Todo válido. Aurora está listo para LLMs.');
} else {
  console.log(`${errors} error(es), ${warnings} advertencia(s)`);
  if (errors > 0) process.exit(1);
}
