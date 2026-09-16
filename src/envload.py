from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path | None = None) -> Path | None:
    """Load KEY=VALUE from .env into os.environ (does not override existing)."""
    root = Path(__file__).resolve().parents[1]
    env_path = path or (root / ".env")
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val
    return env_path
