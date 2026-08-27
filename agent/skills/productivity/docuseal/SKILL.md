---
name: docuseal
description: Generación de documentos con IA — crear PDFs, contratos, formularios desde templates con contenido generado por IA.
version: "1.0.0"
tags: [document, PDF, generation, AI, contract, form]
---

# Docuseal — Document Generation con IA

## Resumen

Plataforma open-source para generación de documentos con IA — crear PDFs, contratos, formularios desde templates. 17k⭐.

## Repo de referencia

- **GitHub:** `github.com/docusealco/docuseal`
- **Lenguaje:** TypeScript/Node.js
- **Licencia:** AGPL-3.0

## Instalación

```bash
# Docker (recomendado)
docker compose up -d

# O desde source
git clone https://github.com/docusealco/docuseal.git
cd docuseal && npm install && npm run build
```

## Uso Básico

```javascript
// Crear documento desde template
const doc = await docuseal.createDocument({
  template: "contrato-base",
  data: {
    nombre: "Juan Pérez",
    fecha: "2026-07-13",
    importe: 1500,
    // ... campos dinámicos
  }
});

// Generar PDF
const pdf = await doc.generate();
pdf.download("contrato.pdf");

// Signatura electrónica
const signature = await doc.addSignature("firmante@email.com");
```

## Patrones Clave

1. **Templates:** Crear plantillas con campos dinámicos
2. **Datos variables:** Insertar datos desde APIs o bases de datos
3. **Signatura:** Flujo de signatura electrónica integrado
4. **API REST:** Control programático completo
5. **Multi-formato:** PDF, DOCX, XLSX

## Integración con Mastermind

- Útil para generar informes automáticos en PDF
- Complementa `markdown` → PDF pipeline
- Ideal para generation de contratos, facturas, reportes
- Reemplaza `WeasyPrint` o `pdfkit` con template engine

## Pitfalls

- **Licencia AGPL:** Uso comercial requiere abrir código
- **Server-side:** Requiere servidor (no browser-only)
- **Templates:** Curva de aprendizaje para crear templates complejos
- **Memory:** Generación de PDFs grandes puede consumir memoria

## Referencias

- [GitHub: docusealco/docuseal](https://github.com/docusealco/docuseal)
