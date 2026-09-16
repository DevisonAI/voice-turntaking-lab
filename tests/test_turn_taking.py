from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.turn_taking import TurnEvent, TurnState, TurnTakingConfig, TurnTakingController


def test_endpoint_after_silence():
    c = TurnTakingController(TurnTakingConfig(silence_endpoint_ms=600, min_utterance_ms=250))
    c.on_event(TurnEvent("vad_speech", 0))
    c.on_event(TurnEvent("vad_silence", 300))
    assert c.state == TurnState.USER_SPEAKING
    c.on_event(TurnEvent("vad_silence", 950))
    assert c.state == TurnState.ENDPOINTING
    assert c.should_start_agent()


def test_no_endpoint_short_utterance():
    c = TurnTakingController(TurnTakingConfig(silence_endpoint_ms=600, min_utterance_ms=250))
    c.on_event(TurnEvent("vad_speech", 0))
    c.on_event(TurnEvent("vad_silence", 100))
    c.on_event(TurnEvent("vad_silence", 800))
    assert c.state == TurnState.USER_SPEAKING
    assert not c.should_start_agent()


def test_barge_in_cancels_agent():
    c = TurnTakingController()
    c.on_event(TurnEvent("agent_audio_start", 0))
    assert c.state == TurnState.AGENT_SPEAKING
    c.on_event(TurnEvent("vad_speech", 50))
    assert c.state == TurnState.BARGE_IN
    assert c.should_cancel_agent()


def test_stop_is_terminal():
    c = TurnTakingController()
    c.on_event(TurnEvent("vad_speech", 0))
    c.on_event(TurnEvent("stop", 10))
    assert c.state == TurnState.STOPPED
    c.on_event(TurnEvent("vad_speech", 20))
    assert c.state == TurnState.STOPPED


def test_turn_policy_stop():
    from src.turn_controller import TurnPolicy

    p = TurnPolicy(max_hop_failures=1)
    stop, reason = p.should_stop(1, "tts")
    assert stop and "tts" in reason


if __name__ == "__main__":
    test_endpoint_after_silence()
    test_no_endpoint_short_utterance()
    test_barge_in_cancels_agent()
    test_stop_is_terminal()
    test_turn_policy_stop()
    print("5/5 passed")
