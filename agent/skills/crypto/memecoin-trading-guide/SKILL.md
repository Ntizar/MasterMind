---
name: memecoin-trading-guide
version: "1.0.0"
description: "Guía completa de trading de memecoins: fundamentos, plataformas, costes, análisis on-chain, psicología y seguridad"
tags: [crypto, memecoin, solana, trading, defi, blockchain]
author: "Basado en guía de @spyzer (x.com/@spyzer)"
---

# Guía Completa de Memecoins

## Fuente Original
- Autor: @spyzer (x.com/@spyzer)
- 132 páginas de contenido educativo
- Gratis para siempre (si pagaste, te estafaron)

---

## PART I — FUNDAMENTOS

### 1. Conceptos Técnicos Core

**Blockchain:**
- Base de datos pública que registra todas las transacciones
- Cada blockchain tiene su token nativo (SOL para Solana, ETH para Ethereum)
- Validadores verifican bloques colectivamente

**Wallet (Billetera):**
- Tu cuenta de crypto
- Secured por seed phrase (12-24 palabras)
- SIEMPRE guardar seed en papel/metal, NUNCA digital
- Si alguien obtiene tu seed phrase → roba todo

**Token/Coin:**
- Activo digital creado en una blockchain
- SPL tokens = tokens en Solana

**Gas Fee:**
- Costo por transacción
- En Solana es extremadamente bajo (<$0.01)

**Liquidity Pool (LP):**
- Caja con dos departamentos: token + SOL
- Permite comprar/vender tokens
- El precio se deriva de la ecuación entre activos en el pool
- Ejemplo: 100 MEME + 1 SOL → 1 MEME = 0.01 SOL

### 2. Métricas Clave

**Market Cap (MCap):**
- Total supply × precio actual
- Mide el valor total de todos los tokens en circulación

**Total Value Locked (TVL):**
- Liquidez dentro del liquidity pool
- Alto TVL = más estabilidad, menos slippage

**Slippage:**
- Diferencia de precio entre orders
- Normal en monedas de alto volumen y bajo market cap
- Mínimo en monedas con alto TVL

**Contract Address (CA):**
- String de letras/números que identifica un pool de liquidez
- Ejemplo: `EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm`

---

## PART II — PLATAFORMAS Y HERRAMIENTAS

### 1. Plataformas de Trading

**FOMO (Recomendado por la guía):**
- App móvil + web terminal
- Código de referido: spyzer (10% descuento en fees)
- Link: fomo.family/r/spyzer
- Características:
  - Trading en múltiples chains sin bridge manual
  - Social layer (ver qué compran otros)
  - UI amigable para principiantes
  - Auto-bridge entre chains
  - Wallet exportable (private keys)

**Alternativas:**
- Axiom
- Trojan
- GMGN
- Dexscreener (para charts/analytics)

### 2. Herramientas de Análisis

**Bubblemaps:**
- Visualiza holders como burbujas
- Muestra clusters (bundling)
- Burbujas amarillas = wallets vinculadas

**Rugcheck.xyz:**
- Verifica seguridad de tokens
- LP Locked %: debe ser >95%
- Mint Authority: debe estar DISABLED
- Freeze Authority: debe estar DISABLED

**Solscan:**
- Scanner de blockchain Solana
- Balance changes, transfers, holders
- Para investigar wallets

**Dexscreener:**
- Charts y analytics
- Muestra holders
- Ranking de coins

**Phantom Wallet:**
- Wallet principal para Solana
- Multi-chain support
- Exportar private keys por wallet

### 3. Launchpads

**PumpFun:**
- Lanzar memecoin gratis o por ~$1
- Bonding curve hasta graduation (~$60K mcap)
- LP lock automático
- Mint/freeze authority automático

**Bonkfun, Moonshot, Launchlab:**
- Alternativas a PumpFun
- Similar funcionalidad

---

## PART III — TIPOS DE COINS Y VALOR

### 1. Memecoins (Atención pura)
- Sin utility, sin producto
- Valor = atención viral
- Ejemplos: DOGE, WIF, PNUT, MOODENG
- Riesgo: pueden ir a 0 en horas
- Potencial: 100X en días

### 2. Utility Coins
- Team construyendo producto
- Value accrual: buybacks, burns, revenue
- Ejemplo: $HYPE (Hyperliquid)
- Más estable que memecoins
- Menor potencial a corto plazo

### 3. Ownership Coins (Nuevos)
- Token representa equity/debt de empresa
- Valor atado a valuación de empresa
- Ejemplo: $CPT en Soar
- Más parecido a inversión tradicional

---

## PART IV — CÓMO ENCONTRAR BUENAS OPERACIONES

### 1. Fuentes de Información

**Telegram:**
- Grupos privados de traders (el valor real)
- Canales públicos: solo como streams de info
- Bot Rick: información de tokens en tiempo real

**X (Twitter):**
- Narrativas se forman aquí
- Seguir traders con track record
- Buscar posts humanos, no bots

**FOMO App:**
- Feed de compras/ventas de traders seguidos
- Notas explicativas de por qué compraron

### 2. Señales de Alerta (Red Flags)

**Bundling:**
- Top holder >3.5% del supply
- Múltiples fresh wallets
- Wallets funding from same source
- Patrón de escalera en chart
- Volumen < Market Cap

**Honeypots:**
- Chart solo sube con bajo volumen
- Pocos holders
- LP no locked
- Mint authority enabled

**Bots:**
- Velas idénticas en tamaño
- Grandes velas instantáneas
- Patrón de escalera

### 3. Checklist de Compra

1. **Narrativa:** ¿Puedo explicar en 1 oración por qué existe?
2. **Dev:** ¿Tiene track record? ¿X account no está hacked?
3. **Volumen/MCap ratio:** Volumen debe ser >80% de MCap
4. **Holders:** Top holder <3.5%?
5. **Fresh wallets:** ¿Múltiples?
6. **Fees:** ¿Proporcional al MCap? (15K MCap >0.5 SOL fees)
7. **Comunidad:** ¿Está creciendo?

---

## PART V — ANÁLISIS DE CHARTS

### 1. Estructura de Mercado

**Uptrend:**
- Higher highs, higher lows
- Compra en retracements

**Downtrend:**
- Lower lows, lower highs
- No intentar atrapar bottom

**Break of Structure:**
- Cambio de tendencia
- Señal para entrar/salir

### 2. Fibonacci Retracement

**Niveles clave:**
- 0.5 = pullback fuerte
- 0.618 = zona dorada (mejor entrada)
- 0.786 = último soporte antes de invalidación

**Reglas:**
- Dibujar body-to-body (no wick-to-wick) en memecoins
- Solo en movimientos direccionales claros
- Confluence = múltiples señales en mismo nivel

### 3. Lecciones Clave

1. No intentar atrapar el bottom
2. Zoom out cuando entres en pánico
3. Ser "tarde" está bien (confirmación > timing perfecto)

---

## PART VI — EJECUCIÓN DE TRADING

### 1. Position Sizing

**Regla de oro:**
- Si pierdes, ¿puedes seguir operando mañana?
- Si no → tamaño demasiado grande

**Por convicción:**
- Alta convicción (info que nadie tiene) → tamaño grande
- Info pública → tamaño pequeño

**Errores comunes:**
- Demasiado en monedas malas → wipeout
- Muy poco en monedas buenas → win no mueve portfolio
- Spreading en 20 monedas → diluye returns

### 2. Entry Strategy

**Evitar FOMO:**
- Definir entry antes de la emoción
- Comprar cuando hay tesis, no cuando sube
- Un solo candle verde ≠ razón para entrar

**Dollar Cost Averaging (DCA):**
- Entrar gradualmente
- Reducir riesgo de timing malo

### 3. Taking Profits

**Regla práctica:**
- Cuando piensas "un poco más" → vender algo
- Escalar out en subidas
- Nunca intentar vender en el top

**Pregunta clave:**
- "Si no tuviera esta moneda y la viera a este precio, ¿la compraría?"
- Si NO → vender parte

### 4. Cutting Losses

**Señales de salida:**
- Thesis invalidada
- Nuevo info bearish
- Precio cruza nivel de invalidación

**Revenge trading:**
- NUNCA intentar recuperar pérdidas rápido
- Esperar, ser paciente
- Oportunidades son abundantes

---

## PART VII — PSICOLOGÍA

### 1. Fish vs Monkey

**Fish (Pez):**
- Consistente, paciente, métodico
- Wins steady, lower risk
- Suitable para: personas metódicas

**Monkey (Mono):**
- High risk, high reward
- Moonshots o nada
- Suitable para: personas aventureras

**Regla:** No intentar ser lo que no eres

### 2. Scarcity Brain (Mentalidad de Escasez)

**Síntomas:**
- Holding winners too long
- Selling too early
- Tratar cada trade como "única oportunidad"
- Holding posiciones muertas por meses

**Solución:**
- Crear safety net financiero fuera de crypto
- Creer que más oportunidades vendrán
- Cortar pérdidas limpiamente

### 3. Revenge Trading

**El cycle:**
1. Pérdida grande
2. Urgencia de recuperar
3. Entries malos
4. Más pérdidas
5. Repeat

**Solución:**
- Parar
- Identificar la falla específica
- Crear regla concreta
- Desapegarse y empezar de nuevo

---

## PART VIII — SEGURIDAD

### 1. Amenazas Comunes

- **Phishing links:** URLs falsas idénticas
- **Fake support:** Nunca dar seed phrase
- **Discord/Telegram DMs:** No clicar links
- **Hacked X accounts:** Verificar por múltiples canales
- **Honeypots:** Chart bello pero no puedes vender
- **Fake airdrops:** No interactuar con tokens no solicitados

### 2. Hot Wallets vs Cold Wallets

**Hot Wallets (online):**
- Para trading diario
- Solo mantener lo necesario
- Phishing vulnerable

**Cold Wallets (hardware):**
- Para holdings significativos
- Ledger, Trezor, Tangem
- Comprar SOLO del fabricante oficial
- Private key nunca expuesto a internet

### 3. Seed Phrase Security

**Reglas:**
- NUNCA almacenar digital
- Guardar en papel/metal
- Múltiples copias en diferentes ubicaciones
- Codificar (steganography, numbering)
- No guardar en la misma casa que el dispositivo

### 4. Diversificación

- Trading wallet ≠ blockchain navigation wallet ≠ cold storage
- No confiar en un solo método
- Multisig para cantidades grandes
- Nunca hablar de cuánto tienes

---

## PART IX — COSTES Y ECONOMÍA

### 1. Costes de Transacción

- **Gas fee Solana:** <\$0.01 por transacción
- **Trading fees FOMO:** ~1-2% (10% descuento con código)
- **Bridge fees:** Variables (FOMO hace automático)
- **Token account rent:** ~0.002 SOL (recuperable con Sol Incinerator)

### 2. Capital Inicial Recomendado

- **Mínimo para empezar:** $50-100
- **Comfortable:** $500-1000
- **NUNCA invertir más de lo que puedas perder completamente**

### 3. Costes Ocultos

- Slippage en trades de bajo TVL
- Fees de exchange (CEX) para comprar SOL
- Coste de oportunidad de capital muerto
- Impuestos (varía por jurisdicción)

---

## PART X — PRIMEROS PASOS

1. **Descargar FOMO** → usar código 'spyzer'
2. **Exportar private keys** → guardar en papel
3. **Crear Phantom wallet** → separada de FOMO
4. **Comprar crypto** → tarjeta en FOMO o CEX (Kraken)
5. **Empezar pequeño** → lo que puedas perder
6. **Crear cuenta X** → seguir traders, construir feed
7. **Crear grupo Telegram** → con bot Rick
8. **Aprender leyendo** → no saltar secciones

---

## Referencias

- Canal original: x.com/@spyzer
- Canal de contribuciones: ver guía original
- Lee la guía completa: drive.google.com (enlace original)
- Lee las referencias al final de la guía para profundizar

---

## Pitfalls Críticos

1. **NUNCA compartir seed phrase** → robo total
2. **NUNCA hacer revenge trading** → destruye portfolios
3. **NUNCA invertir dinero que necesites** → presión emocional
4. **NUNCA seguir calls ciegamente** → DYOR siempre
5. **NUNCA guardar seed digital** → hacking
6. **SIEMPRE verificar URLs** → phishing
7. **SIEMPRE check LP lock + mint authority** → honeypots
8. **SIEMPRE empezar pequeño** → learning curve
