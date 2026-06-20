# Control-M Account Intelligence — Quick Reference

## Para Gandarillas: Cómo usar este skill

### Lo que tienes

- **614 cuentas españolas** de Salesforce clasificadas por tier y score
- **63 Tier A** (Atacar primero)
- **199 Tier B** (Alta prioridad)
- **135 Tier C** (Media)
- **211 Tier D** (Nurturing)

### Comandos rápidos

```bash
# Generar informe de cuenta #1 (la de mayor score)
python3 /hermes-home/scripts/control-m/generate-report.py 1 --pdf

# Generar informe de cuenta #5
python3 /hermes-home/scripts/control-m/generate-report.py 5 --pdf

# Generar informe de múltiples cuentas
python3 /hermes-home/scripts/control-m/generate-report.py 1 5 12 20 --pdf

# Generar TODAS las Tier A con PDF
python3 /hermes-home/scripts/control-m/generate-report.py --tier "A – Atacar primero" --pdf

# Generar las primeras 20 cuentas
python3 /hermes-home/scripts/control-m/generate-report.py --limit 20 --pdf

# Generar informe de un sector específico
python3 /hermes-home/scripts/control-m/generate-report.py --segment "Banking" --pdf

# Generar informe de una cuenta por nombre
python3 /hermes-home/scripts/control-m/generate-report.py --name "Ibercaja" --pdf
```

### Dónde están los informes

- **HTML:** `/hermes-home/scripts/control-m/reports/*.html`
- **PDF:** `/hermes-home/scripts/control-m/reports/*.pdf`

### Estructura del informe

Cada informe tiene 6 fases:
1. **Portada** — Datos de la cuenta
2. **Fase 0** — Contexto de Control-M (qué vendes)
3. **Fase 1** — Intelligence de cuenta (trigger events, señales de compra)
4. **Fase 2** — Tech Stack y automatización (qué usan, qué les falta)
5. **Fase 3** — Pains por sector (problemas que Control-M resuelve)
6. **Fase 4** — Oportunidades comerciales (quick wins, land & expand, ROI)
7. **Fase 5** — Stakeholders y plan de acción (quién contactar, cómo, cuándo)

### Notas importantes

- Los datos de CRM (tier, score, notas) son fuente de verdad
- Los análisis de tech stack son inferencias por sector (marcadas como tal)
- Las oportunidades reales se validan en reuniones con la cuenta
- Los informes Tier A★ están "en curso" con comercial asignado
