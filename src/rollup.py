from __future__ import annotations

import json
import statistics
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "metrics" / "sessions"
    files = sorted(root.glob("session_*.jsonl")) if root.exists() else []
    if not files:
        print("no sessions under metrics/sessions/ — run with --write-session first")
        return 2
    e2e = []
    by_hop: dict[str, list[float]] = {}
    for path in files:
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            e2e.append(float(rec.get("e2e_ms") or 0))
            for h in rec.get("hops") or []:
                by_hop.setdefault(h["name"], []).append(float(h["ms"]))
    def pct(xs, p):
        if not xs:
            return None
        xs = sorted(xs)
        k = (len(xs) - 1) * p / 100.0
        f = int(k)
        c = min(f + 1, len(xs) - 1)
        if f == c:
            return xs[f]
        return xs[f] + (xs[c] - xs[f]) * (k - f)
    print(f"sessions: {len(e2e)}")
    print(f"{'metric':<28} {'n':>4} {'p50':>8} {'p95':>8}")
    print(f"{'-'*28} {'-'*4} {'-'*8} {'-'*8}")
    print(f"{'E2E':<28} {len(e2e):>4} {pct(e2e,50):8.1f} {pct(e2e,95):8.1f}")
    for name, xs in by_hop.items():
        print(f"{name:<28} {len(xs):>4} {pct(xs,50):8.1f} {pct(xs,95):8.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
