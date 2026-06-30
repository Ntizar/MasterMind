# CIAF-data Embedded JSON Extraction — Session Details

## Date: 2026-06-24

### Problem: 38 reports embedded in `js/app.js` via `const CIAF_DATA = { reports: [...] }`

### Symptoms
- `json.loads()` fails with "Extra data: line 2 column 12 (char 12)"
- `demjson3.decode()` fails with "Unknown identifier: oard"
- Bracket counter finds wrong closing bracket (first `]` inside `"trenes": []`)

### Root cause analysis

**Issue 1: Bracket counter failure**
The naive bracket counter found `"trenes": []` as the array close instead of the real closing `]` after the last report object. The `]` inside a string value decremented the depth counter incorrectly.

**Fix:** Use regex to find the specific closing pattern `}\n]\n  ];\n//` — the `]` followed by `\n  ];` is unique to the CIAF_DATA structure.

**Issue 2: demjson3 "Unknown identifier: oard"**
The script was reading content from AFTER the reports array (Leaflet map initialization code) instead of the array itself. The bracket counter was off by hundreds of characters because it was including JS code after `];`.

**Issue 3: Double-escaped newlines in strings**
The JSON contained `\\\\n` (double backslash + n) in string values like the resumen field. This is a literal backslash + letter n, NOT a newline. JSON parser sees this as valid, but it confuses string inspection.

### Verification approach
After rewriting app.js:
1. Extract array between `[` and the `]` before `;\n// === Estado ===`
2. Wrap in `[]` and call `json.loads()`
3. Verify each report: danos_materiales is boolean, tags unique, no conclusion headers
4. Write to `/tmp/ciaf_verified.json` as source of truth

### Files involved
- `/root/workspace/ciaf-data/js/app.js` — 89KB, 38 reports embedded in CIAF_DATA
- `/root/workspace/ciaf-data/dashboard/data/reports.json` — standalone JSON, updated to v2.1
- `/root/workspace/ciaf-data/js/app.js.bak` — backup before changes

### Key regexes for boundary detection
```python
# Find reports array opening
reports_pos = content.find('"reports":')
arr_start = content.find('[', reports_pos)

# Find closing pattern: } ] \n ]; \n //
import re
pattern = re.search(r'\n\]\n\s*\]', content[footer_pos-500:footer_pos])
```
