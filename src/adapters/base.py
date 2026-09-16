from __future__ import annotations

from typing import Protocol


class STT(Protocol):
    def transcribe(self, audio_label: str = "utterance") -> str: ...


class Agent(Protocol):
    def reply(self, text: str) -> str: ...


class TTS(Protocol):
    def synthesize(self, text: str) -> str: ...
