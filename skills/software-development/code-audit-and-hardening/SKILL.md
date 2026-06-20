---
name: code-audit-and-hardening
description: Systematic procedure for auditing, debugging, and hardening web applications (Node.js/SQLite/Vanilla JS).
---

# Code Audit and Hardening

A structured approach to identify security vulnerabilities, logic errors, and architectural fragility in web applications.

## Workflow

1.  **Static Analysis (Code Review):**
    *   Scan for SQL concatenation in database queries.
    *   Check for missing `try-catch` blocks in asynchronous operations (especially AI/Fetch calls).
    *   Audit CORS configurations and authentication middleware.
    *   Verify input validation and type casting (e.g., `parseInt`, `parseFloat`).
2.  **Security Audit:**
    *   **SQL Injection:** Ensure all queries use parameterized statements (`?`).
    *   **XSS:** Check if user-generated content is escaped before being injected into the DOM.
    *   **Broken Auth:** Validate session token handling and `requireAuth` middleware.
3.  **Logic & Robustness Audit:**
    *   **Math Safety:** Check for potential division by zero or `NaN` in calculation-heavy components (charts, projections).
    *   **Schema Consistency:** Ensure backend JSON structures match frontend expectations.
    *   **Error Handling:** Ensure API responses are consistent (e.g., `{ ok: true }` vs `{ success: true }`).
4.  **Hardening (Implementation):**
    *   Apply targeted patches.
    *   Verify with manual/automated tests.

## Pitfalls

*   **Partial Patching:** When fixing a bug, ensure all related instances (e.g., both `GET` and `POST` endpoints) are updated.
*   **Silent Failures:** Avoid catching errors and doing nothing (`catch(e) {}`). At minimum, log the error.
*   **JSON Fragility:** When using LLMs, always assume the output might be malformed and wrap `JSON.parse` in a `try-catch`.
