from __future__ import annotations

import time


class FakeSTT:
    """Simulated streaming STT. No API keys."""

    def __init__(self, fail: bool = False, delay_s: float = 0.08):
        self.fail = fail
        self.delay_s = delay_s

    def transcribe(self, audio_label: str = "utterance") -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise TimeoutError("STT timeout (injected)")
        return f"[stt] hello from {audio_label}"


class FakeAgent:
    """Simulated LLM turn. No API keys."""

    def __init__(self, fail: bool = False, delay_s: float = 0.12):
        self.fail = fail
        self.delay_s = delay_s

    def reply(self, text: str) -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise TimeoutError("LLM timeout (injected)")
        return f"[agent] heard: {text}"


class FakeTTS:
    """Simulated streaming TTS. No API keys."""

    def __init__(self, fail: bool = False, delay_s: float = 0.10):
        self.fail = fail
        self.delay_s = delay_s

    def synthesize(self, text: str) -> str:
        time.sleep(self.delay_s)
        if self.fail:
            raise RuntimeError("TTS failure (injected)")
        return f"[tts-audio] {len(text)} chars"
