# -*- coding: utf-8 -*-
"""Auditaría de consumo real de tokens desde state.db de Hermes.

Uso:
    python auditar-tokens.py            # hoy
    python auditar-tokens.py 2026-08-31 # día concreto (YYYY-MM-DD)

Imprime tabla de sesiones del día, totales, desglose por perfil y coste
estimado con precios NaN. Solo lectura (mode=ro) — seguro con gateway activo.

Hecho con ❤️ por David Antizar
"""
import sqlite3, sys, os, datetime, collections

# Precio por 1M tokens en NaN (actualizar si cambian las tarifas)
PRECIOS = {  # (input, output) USD por 1M
    "qwen3.8-flash": (0.50, 0.50),
    "deepseek-v4-flash": (0.50, 0.50),
    "qwen3.6": (0.50, 0.50),
    "glm5.3-flash": (1.00, 1.00),
}
PRECIO_DEFAULT = (0.50, 0.50)


def db_path():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/.hermes")
    return os.path.join(base, "hermes", "state.db")


def ts(x):
    """unix float -> datetime (tolera None/str basura)."""
    try:
        return datetime.datetime.fromtimestamp(float(x))
    except (TypeError, ValueError):
        return None


def main():
    dia = None
    if len(sys.argv) > 1:
        dia = datetime.date.fromisoformat(sys.argv[1])
    else:
        dia = datetime.date.today()

    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    rows = con.execute(
        "SELECT id, profile_name, model, started_at, last_activity_at,"
        " input_tokens, output_tokens, cache_read_tokens, reasoning_tokens,"
        " api_call_count, tool_call_count, estimated_cost_usd, title"
        " FROM sessions"
    ).fetchall()

    day = [r for r in rows
           if (ts(r[4]) or ts(r[3])) and (ts(r[4]) or ts(r[3])).date() == dia]

    print(f"=== Consumo {dia} — {len(day)} sesiones ===")
    tot = collections.Counter()
    prof = collections.Counter()
    for r in sorted(day, key=lambda x: -((x[5] or 0) + (x[6] or 0))):
        (sid, p, m, s, l, i, o, cr, rt, api, tc, ec, title) = r
        i, o, cr, rt, api = i or 0, o or 0, cr or 0, rt or 0, api or 0
        pin, pout = PRECIOS.get(m or "", PRECIO_DEFAULT)
        coste = i / 1e6 * pin + o / 1e6 * pout
        ctx_medio = f"{i // max(api,1):,}" if api else "?"
        prof[p or "default"] += i + o
        tot["in"] += i; tot["out"] += o; tot["cache"] += cr
        tot["reason"] += rt; tot["api"] += api; tot["cost"] += coste
        print(f"{(ts(s).strftime('%H:%M') if ts(s) else '?'):<6} "
              f"{(p or 'default'):<12} in={i:>10,} out={o:>8,} "
              f"cache={cr:>10,} api={api:>4} ctx/llamada={ctx_medio:>9} "
              f"${coste:>6.3f}  {str(title or '')[:48]}")

    print("---")
    print(f"TOTAL: in={tot['in']:,} out={tot['out']:,} "
          f"cacheRead={tot['cache']:,} reasoning={tot['reason']:,} "
          f"apiCalls={tot['api']:,} coste≈${tot['cost']:.2f}")
    for k, v in prof.most_common():
        print(f"  perfil {k:<16} {v:>12,} tokens")


if __name__ == "__main__":
    main()
