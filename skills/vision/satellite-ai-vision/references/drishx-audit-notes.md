# DRISH-X — Technical Audit (2026-06-24)

## Resumen Ejecutivo
Proyecto legítimo con base científica sólida (paper peer-reviewed), implementado por desarrollador junior. Pipeline fiel a referencia académica. Código funcional pero amateur.

## Problemas de Seguridad Encontrados
- Sin autenticación en APIs (CORS `*`)
- Credenciales Copernicus en memoria del proceso, sin persistencia segura
- `engine.history` en memoria RAM → datos perdidos al reiniciar
- `CONFIG.save()` escribe TOML en disco con secrets — riesgo de dump accidental

## Problemas de Código
- Proxy classifier usa heurísticas con pesos arbitrarios (no científicos)
- `window.dashboard` global asumido sin declaración (bug potencial en JS)
- requirements.txt sin versions pinned excepto scikit-learn
- 1132 líneas en un solo archivo — sin separación en módulos
- Sin tests unitarios, sin CI/CD, sin Dockerfile

## Branding/UX
- Lenguaje "tactical military" excesivo: "Threat Index", "WARNING" para cada camión
- Dark mode con cyan neón (#00f2ff) — patrón genérico IA
- Frontend funcional pero con terminología militar innecesaria para producto legítimo

## Comparativa con DRISH-X de David
- Este DRISH-X: RF en servidor, Sentinel-2 real, smear spectral
- DRISH-X de David: WebGPU + ONNX en navegador, detección multi-clase
- Enfoques complementarios: servidor vs edge, científico vs práctico

## Archivos Clave
- `/drishx.py` — Backend completo (1132 líneas)
- `/rf_model.pickle` — Modelo Random Forest entrenado
- `/frontend/index.html` — Dashboard Leaflet + Chart.js
- `/frontend/app.js` — Lógica frontend (685 líneas)
- `/frontend/styles.css` — Tema tactical dark (955 líneas)
