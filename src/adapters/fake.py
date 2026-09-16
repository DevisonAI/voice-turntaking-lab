from __future__ import annotations

import time
from pathlib import Path


class FakeSTT:
    """Simulated STT. No API keys."""

    def __init__(self, fail: bool = False, delay_s: float = 0.08):
        self.fail = fail
        self.delay_s = delay_s

    def transcribe_file(self, path: str) -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise TimeoutError("STT timeout (injected)")
        label = Path(path).name if path else "utterance"
        return f"[stt] fake transcript of {label}"


class FakeAgent:
    def __init__(self, fail: bool = False, delay_s: float = 0.12):
        self.fail = fail
        self.delay_s = delay_s

    def reply(self, text: str) -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise TimeoutError("LLM timeout (injected)")
        return f"[agent] heard: {text}"


class FakeTTS:
    def __init__(self, fail: bool = False, delay_s: float = 0.10):
        self.fail = fail
        self.delay_s = delay_s

    def synthesize(self, text: str) -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise RuntimeError("TTS failure (injected)")
        return f"[tts-audio] {len(text)} chars"
