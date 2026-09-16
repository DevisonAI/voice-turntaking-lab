from __future__ import annotations

from typing import Protocol


class STT(Protocol):
    def transcribe_file(self, path: str) -> str: ...


class Agent(Protocol):
    def reply(self, text: str) -> str: ...


class TTS(Protocol):
    def synthesize(self, text: str) -> str: ...
