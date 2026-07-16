# DCEE Naming Convention — Reference

## Format

```
[ClaveProyecto]_[NaturalezaDoc]_[AlcanceContenido]_[InfoComplementaria]_[Descripcion].[ext]
```

### Example

```
33-BA-4320_ACT_AO_06.0055-01.pdf
│           │    │   │           └── Descripción (finca 01)
│           │    │   └────────────── Info complementaria (municipio 06.0055 = La Albuera)
│           │    └────────────────── Alcance/Contenido (Acta de Ocupación)
│           └─────────────────────── Tipo de documento (Acta)
└─────────────────────────────────── Código de proyecto (33-BA-4320)
```

## Naturaleza de Documento (Tipos principales)

| Código | Descripción |
|--------|-------------|
| ACT | Acta |
| AC | Acta de Comprobación |
| ADI | Aditivo |
| ADJ | Adjudicación |
| ANT | Anteproyecto |
| APR | Aprobación |
| AX | Anexo |
| CO | Contrato |
| CT | Cuaderno de Técnico |
| EC | Ejecución de Contrato |
| EP | Estudio Previo |
| ES | Estudio de Seguridad |
| ET | Especificaciones Técnicas |
| EX | Expediente |
| IN | Informe |
| MO | Modificación |
| PE | Presupuesto |
| PR | Proyecto |
| SO | Solicitud |
| TR | Trámite |
| VA | Valoración |

## Alcance/Contenido (Códigos habituales)

| Código | Descripción |
|--------|-------------|
| AO | Acta de Ocupación |
| AI | Acta de Inicio |
| AC | Acta de Comprobación |
| AD | Acta de Defectos |
| AT | Acta de Terminación |
| AP | Acta de Recepción |
| AR | Acta de Replanteo |
| AX | Anexo |
| CO | Contrato |
| CT | Cuaderno de Técnico |
| EC | Ejecución de Contrato |
| EP | Estudio Previo |
| ES | Estudio de Seguridad |
| ET | Especificaciones Técnicas |
| EX | Expediente |
| IN | Informe |
| MO | Modificación |
| OB | Obra |
| OR | Orden de Inicio |
| PC | Pliego de Condiciones |
| PE | Presupuesto |
| PR | Proyecto |
| RE | Recurso |
| SO | Solicitud |
| TR | Trámite |
| VA | Valoración |

## INE Municipality Codes

Format: `CC.MMMM` where CC = province code (2 digits), MMMM = municipality code (4 digits).

Example: `06.0055` = Badajoz, La Albuera

Full glossary of 388 municipalities available in `glossary.py` of PDFtoMeta Python version.

## Source

Based on DCEE (Dirección de Carreteras del Estado de Extremadura) coding procedure document.
