# Quick Start — Control-M Account Intelligence

## En 3 pasos

### Paso 1: Generar informe de una cuenta

```bash
python3 scripts/control-m/generate-report.py 1 --pdf
```

Esto genera un dossier completo de 8 páginas para la cuenta #1 (la de mayor score).

### Paso 2: Ver el informe

Los PDFs se guardan en:
```
scripts/control-m/reports/
```

### Paso 3: Generar más

```bash
# Top 10 Tier A
python3 scripts/control-m/generate-report.py --tier "A – Atacar primero" --pdf

# Sector Banking
python3 scripts/control-m/generate-report.py --segment "Banking" --pdf

# Cuentas específicas
python3 scripts/control-m/generate-report.py 1 5 10 15 20 --pdf
```

## ¿Qué incluye cada informe?

1. **Portada** profesional con datos de la cuenta
2. **Contexto de Control-M** — qué vendes, competencia, diferenciadores
3. **Intelligence de cuenta** — trigger events, señales de compra
4. **Tech Stack** — cloud, SAP, legacy, automatización actual
5. **Pains** — tabla de problemas con impacto y solución Control-M
6. **Oportunidades** — quick wins, land & expand, ROI estimado
7. **Stakeholders** — quién contactar, cómo, cuándo
8. **Veredicto** — prioridad y probabilidad de cierre

## Estructura de directorios

```
scripts/control-m/
├── README.md                    ← Este archivo
├── SKILL.md                     ← Skill completo
├── extract-accounts.py          ← Convierte Excel → JSON
├── generate-report.py           ← Genera HTML/PDF
├── template.html                ← Plantilla del informe
├── data/
│   └── accounts.json            ← 614 cuentas España
└── reports/
    ├── control-m-banking-aviva-plc.pdf
    ├── control-m-banking-eroski.pdf
    └── ...
```
