from __future__ import annotations

import os


class MissingKeyError(RuntimeError):
    """Loud stop — never invent a silent fake success for live mode."""


def _require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise MissingKeyError(f"missing env {name} — copy .env.example → .env and set keys")
    return val


class EnvSTT:
    """Placeholder live STT. Fails loudly until a real provider is wired."""

    def __init__(self, provider: str = "deepgram"):
        self.provider = provider
        self.api_key = _require("STT_API_KEY")

    def transcribe(self, audio_label: str = "utterance") -> str:
        raise NotImplementedError(
            f"live STT ({self.provider}) not wired yet — key present, adapter stub only"
        )


class EnvAgent:
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = _require("LLM_API_KEY")

    def reply(self, text: str) -> str:
        raise NotImplementedError(
            f"live LLM ({self.provider}) not wired yet — key present, adapter stub only"
        )


class EnvTTS:
    def __init__(self, provider: str = "elevenlabs"):
        self.provider = provider
        self.api_key = _require("TTS_API_KEY")

    def synthesize(self, text: str) -> str:
        raise NotImplementedError(
            f"live TTS ({self.provider}) not wired yet — key present, adapter stub only"
        )
