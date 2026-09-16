from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TurnPolicy:
    """Explicit stop rules — no silent best judgment."""

    max_hop_failures: int = 1
    label: str = "default"

    def should_stop(self, failures: int, reason: str) -> tuple[bool, str]:
        if failures >= self.max_hop_failures:
            return True, f"stop: {reason} (failures={failures})"
        return False, ""
