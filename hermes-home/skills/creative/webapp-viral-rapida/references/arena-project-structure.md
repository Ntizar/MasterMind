# Estructura de proyecto ARENA ( referencia para webapps virales)

## Archivos

```
arena/
├── index.html          ← Layout principal (header + visual 3D + info + pagos)
├── css/style.css       ← Estilo (mármol griego, responsive)
├── js/
│   ├── arena.js        ← Three.js scene + partículas + UI + pagos
│   └── countries.js    ← Datos estáticos (países, colores, flags)
├── public/
│   └── countries.json  ← Datos como JSON (para API)
├── server.js           ← Express + SQLite + WebSocket
├── package.json        ← Deps: express, better-sqlite3, ws
├── Dockerfile          ← node:20-alpine, no-root, HEALTHCHECK
├── .dockerignore       ← Excluir node_modules, .env, .git
├── .env.example        ← Template de variables
└── README.md           ← Descripción + cómo correr
```

## Puerto: 3000 (o el que configure NaN)

## Dependencias npm
- express
- better-sqlite3
- ws

## CDN
- Three.js r128: `cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- Google Fonts: Cormorant Garamond (para look elegante)

## Variables de entorno
- PORT (default 3000)
- PAYPAL_CLIENT_ID
- PAYPAL_SECRET
- ADMIN_PASSWORD
