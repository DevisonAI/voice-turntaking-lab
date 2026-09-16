from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class HopTimer:
    name: str
    started: float = field(default_factory=time.perf_counter)
    ended: float | None = None
    ok: bool = True
    note: str = ""

    def stop(self, ok: bool = True, note: str = "") -> float:
        self.ended = time.perf_counter()
        self.ok = ok
        self.note = note
        return self.ms

    @property
    def ms(self) -> float:
        end = self.ended if self.ended is not None else time.perf_counter()
        return (end - self.started) * 1000.0


@dataclass
class SessionMetrics:
    hops: list[HopTimer] = field(default_factory=list)
    stop_reason: str = ""

    def add(self, hop: HopTimer) -> None:
        self.hops.append(hop)

    def e2e_ms(self) -> float:
        if not self.hops:
            return 0.0
        return sum(h.ms for h in self.hops)

    def table(self) -> str:
        lines = [
            f"{'hop':<28} {'ms':>8} {'ok':>4}  note",
            f"{'-'*28} {'-'*8} {'-'*4}  ----",
        ]
        for h in self.hops:
            lines.append(f"{h.name:<28} {h.ms:8.1f} {str(h.ok):>4}  {h.note}")
        lines.append(f"{'E2E (sum of hops)':<28} {self.e2e_ms():8.1f}")
        if self.stop_reason:
            lines.append(f"stop_reason: {self.stop_reason}")
        return "\n".join(lines)
