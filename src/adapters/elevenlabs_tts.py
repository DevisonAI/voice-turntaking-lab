from __future__ import annotations

import os
from pathlib import Path

from ..http_util import ProviderHTTPError, http_request


class ElevenLabsTTS:
    """ElevenLabs text-to-speech — the hire-signal TTS hop."""

    def __init__(self):
        key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not key:
            raise ProviderHTTPError(
                "missing ELEVENLABS_API_KEY — required for live TTS (default stack)"
            )
        self.api_key = key
        # Rachel is a common public default voice id; override via env.
        self.voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.model_id = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

    def synthesize(self, text: str) -> str:
        if not (text or "").strip():
            raise ProviderHTTPError("TTS refused empty text")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        import json

        raw = http_request(
            "POST",
            url,
            headers={
                "xi-api-key": self.api_key,
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "text": text.strip(),
                    "model_id": self.model_id,
                    "voice_settings": {"stability": 0.4, "similarity_boost": 0.75},
                }
            ).encode(),
            timeout=120.0,
        )
        out_dir = Path(__file__).resolve().parents[2] / "metrics" / "tmp"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "last_tts.mp3"
        out.write_bytes(raw)
        return f"[elevenlabs] {out.name} {len(raw)} bytes voice={self.voice_id}"
