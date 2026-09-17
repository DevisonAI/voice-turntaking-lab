from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path | None = None) -> Path | None:
    """Load KEY=VALUE from .env into os.environ.

    Within the file, later lines win. Keys already set in the real process
    environment before load are left alone (so you can override in the shell).
    """
    root = Path(__file__).resolve().parents[1]
    env_path = path or (root / ".env")
    if not env_path.exists():
        return None
    preset = set(os.environ.keys())
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if not key:
            continue
        if key in preset:
            continue  # real process env wins
        os.environ[key] = val  # later .env lines overwrite earlier .env lines
    return env_path
