# LladosApp (MasterFit) Audit & Hardening Case Study

## Context
Audit of LladosApp v5.0.0 (MasterFit). A fitness tracking web app using Node.js, SQLite, and Vanilla JS.

## Vulnerabilities Identified
- **SQL Injection:** Risk in `DELETE` and `PUT` endpoints due to dynamic table name concatenation.
- **Broken Auth:** User enumeration via `/api/auth/usuarios`.
- **XSS Risk:** Potential for unescaped content in chat/descriptions.

## Logic Errors & Fixes
- **AI Robustness:** `JSON.parse` on LLM responses was prone to crashing the server. Fixed with `try-catch`.
- **Math Stability:** Division by zero in projection calculations (`semanasRest`).
- **Schema Mismatch:** Inconsistency between InBody data stored in SQLite and keys expected by the Chart.js frontend.

## Hardening Techniques Applied
- **Parameterized Queries:** Moved all dynamic SQL to strict parameterization.
- **Safe Parsing:** Wrapped all external AI data parsing in error-handling blocks.
- **Context-Aware AI:** Enhanced the system prompt to include real-time user metrics, turning the agent from a passive logger into an active coach.
