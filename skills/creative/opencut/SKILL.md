---
name: opencut
description: Editor de documentos y texto con IA — alternativa open-source a herramientas SaaS de edición.
version: "1.0.0"
tags: [editor, document, text, AI, open-source, SaaS]
---

# OpenCut — Editor de Documentos con IA

## Resumen

Editor de documentos y texto con IA — alternativa open-source a herramientas SaaS. 57k⭐.

## Repo de referencia

- **GitHub:** `github.com/OpenCut-app/OpenCut`
- **Lenguaje:** TypeScript/React
- **Licencia:** MIT

## Instalación

```bash
git clone https://github.com/OpenCut-app/OpenCut.git
cd OpenCut && npm install && npm run build
```

## Uso Básico

```javascript
import { OpenCut } from 'opencut';

const editor = new OpenCut({
  container: '#editor',
  ai: {
    provider: 'openai',
    apiKey: process.env.OPENAI_API_KEY,
  }
});

// Editar texto con IA
editor.ai.summarize();
editor.ai.translate('es');
editor.ai.rewrite({ tone: 'professional' });

// Exportar
editor.export('pdf');
editor.export('html');
```

## Funcionalidades

1. **Editor rich text:** Edición visual de documentos
2. **AI assistance:** Resumir, traducir, reescribir con IA
3. **Templates:** Plantillas predefinidas
4. **Export:** PDF, HTML, Markdown
5. **Collaborative:** Edición colaborativa en tiempo real

## Integración con Mastermind

- Complementa `docuseal` — edición vs generación
- Útil para `ppt-master` — edición de documentos
- Ideal para `claude-design` — edición de artefactos
- Reemplaza Google Docs para flujos open-source

## Pitfalls

- **Licencia:** Verificar licencia para uso comercial
- **IA:** Requiere API key de proveedor de IA
- **Server:** Requiere backend para algunas funciones
- **Performance:** Editor pesado en recursos

## Referencias

- [GitHub: OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut)
