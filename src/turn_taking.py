from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TurnState(str, Enum):
    IDLE = "idle"
    USER_SPEAKING = "user_speaking"
    ENDPOINTING = "endpointing"
    AGENT_SPEAKING = "agent_speaking"
    BARGE_IN = "barge_in"
    STOPPED = "stopped"


@dataclass
class TurnTakingConfig:
    """Endpointing + barge-in knobs. Numbers are policy defaults, not measured latency."""

    silence_endpoint_ms: int = 600
    min_utterance_ms: int = 250
    barge_in_enabled: bool = True
    barge_in_min_user_ms: int = 180


@dataclass
class TurnEvent:
    kind: str  # vad_speech | vad_silence | agent_audio_start | agent_audio_end | stop
    t_ms: int


class TurnTakingController:
    """Explicit turn machine — no silent best judgment.

    Does not call STT/TTS. Owns *when* the loop may start/stop agent audio.
    """

    def __init__(self, config: TurnTakingConfig | None = None):
        self.config = config or TurnTakingConfig()
        self.state = TurnState.IDLE
        self._speech_started_ms: int | None = None
        self._silence_started_ms: int | None = None
        self.stop_reason: str = ""

    def on_event(self, event: TurnEvent) -> TurnState:
        if self.state == TurnState.STOPPED:
            return self.state

        if event.kind == "stop":
            self.state = TurnState.STOPPED
            self.stop_reason = "stop event"
            return self.state

        if event.kind == "vad_speech":
            return self._on_speech(event.t_ms)
        if event.kind == "vad_silence":
            return self._on_silence(event.t_ms)
        if event.kind == "agent_audio_start":
            if self.state != TurnState.BARGE_IN:
                self.state = TurnState.AGENT_SPEAKING
            return self.state
        if event.kind == "agent_audio_end":
            if self.state == TurnState.AGENT_SPEAKING:
                self.state = TurnState.IDLE
            return self.state

        self.stop_reason = f"unknown event: {event.kind}"
        self.state = TurnState.STOPPED
        return self.state

    def should_start_agent(self) -> bool:
        return self.state == TurnState.ENDPOINTING

    def should_cancel_agent(self) -> bool:
        return self.state == TurnState.BARGE_IN

    def _on_speech(self, t_ms: int) -> TurnState:
        if self.state in (TurnState.IDLE, TurnState.ENDPOINTING):
            self.state = TurnState.USER_SPEAKING
            self._speech_started_ms = t_ms
            self._silence_started_ms = None
            return self.state

        if self.state == TurnState.AGENT_SPEAKING and self.config.barge_in_enabled:
            self.state = TurnState.BARGE_IN
            self._speech_started_ms = t_ms
            self._silence_started_ms = None
            return self.state

        if self.state == TurnState.USER_SPEAKING:
            self._silence_started_ms = None
            return self.state

        return self.state

    def _on_silence(self, t_ms: int) -> TurnState:
        if self.state != TurnState.USER_SPEAKING:
            return self.state

        if self._silence_started_ms is None:
            self._silence_started_ms = t_ms
            return self.state

        silence_ms = t_ms - self._silence_started_ms
        uttered = 0
        if self._speech_started_ms is not None:
            uttered = self._silence_started_ms - self._speech_started_ms

        if uttered < self.config.min_utterance_ms:
            return self.state

        if silence_ms >= self.config.silence_endpoint_ms:
            self.state = TurnState.ENDPOINTING
        return self.state
