from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlencode

from ..http_util import ProviderHTTPError, http_request


class DeepgramSTT:
    """Deepgram prerecorded transcription — hire-relevant STT hop."""

    def __init__(self):
        key = os.environ.get("DEEPGRAM_API_KEY", "").strip()
        if not key:
            raise ProviderHTTPError(
                "missing DEEPGRAM_API_KEY — required for live STT (not optional in default stack)"
            )
        self.api_key = key
        self.model = os.environ.get("DEEPGRAM_MODEL", "nova-2")

    def transcribe_file(self, path: str) -> str:
        audio = Path(path)
        if not audio.is_file():
            raise FileNotFoundError(f"audio not found: {path}")
        params = urlencode({"model": self.model, "smart_format": "true"})
        url = f"https://api.deepgram.com/v1/listen?{params}"
        suffix = audio.suffix.lower()
        ctype = {
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
            ".webm": "audio/webm",
        }.get(suffix, "application/octet-stream")
        raw = http_request(
            "POST",
            url,
            headers={
                "Authorization": f"Token {self.api_key}",
                "Content-Type": ctype,
            },
            data=audio.read_bytes(),
            timeout=120.0,
        )
        data = json.loads(raw.decode())
        try:
            text = data["results"]["channels"][0]["alternatives"][0]["transcript"]
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderHTTPError(f"unexpected Deepgram response: {data!r}") from e
        text = (text or "").strip()
        if not text:
            raise ProviderHTTPError("Deepgram returned empty transcript")
        return text
