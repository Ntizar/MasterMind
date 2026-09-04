---
name: computational-science-agent-methodology
version: "1.0.0"
description: "Usa para ciencia computacional con agentes y pre-registro."
tags: [science, agents, methodology, research, skills]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [science, agents, methodology, research, skills]
    related_skills: [hermes-agent]
---
# Science Superpowers — Metodología de ciencia computacional para agentes

## Resumen
`Science Superpowers` (K-Dense AI) es una metodología completa de ciencia computacional para agentes de investigación, construida sobre skills componibles + instrucciones iniciales que aseguran que el agente realmente las use. Cero dependencias de terceros: solo el harness del agente y un shell POSIX. Reimplementación de `Superpowers` para ciencia con datos: skills auto-trigger via bootstrap de inicio de sesión, disciplina central = **pre-registration** (en vez de TDD).

## Uso (comandos reales del README)
Sin CLI propio: es una colección de skills + instrucciones iniciales para el agente que se auto-triggeran al inicio de sesión. Contiene 16 skills.

## Patrones / Arquitectura
- Skills componibles que auto-trigger via session-start bootstrap.
- El ciclo de trabajo es el *research lifecycle*.
- Disciplina central: **pre-registration** de hipótesis antes de ejecutar (equivalente a test-driven development en software).
- Dependencia cero: funciona solo con el harness del agente y un shell POSIX.
- Modelo: skills + instrucciones iniciales que fuerzan su uso.

## Pitfalls
- No añadir dependencias de terceros: mantener el "zero third-party dependencies".
- Verificar que el agente efectivamente utiliza las skills (bootstrap al iniciar sesión).
- El bootstrap se basa en auto-trigger: si el agente no carga la skill, el flujo de pre-registro no se activa.

## Verificación
- Confirmar que las 16 skills están presentes y que el bootstrap de inicio de sesión las carga.
- Verificar el pre-registro de hipótesis al iniciar cada experimento.

## Referencia
README de https://github.com/K-Dense-AI/science-superpowers (MIT, 16 skills, v1.0.0). Blog: k-dense.ai/blog/introducing-science-superpowers.
