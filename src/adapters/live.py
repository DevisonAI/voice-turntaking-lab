from __future__ import annotations

from ..http_util import ProviderHTTPError
from .deepgram_stt import DeepgramSTT
from .elevenlabs_tts import ElevenLabsTTS
from .llm import build_llm


class MissingKeyError(RuntimeError):
    """Loud stop — never invent a silent fake success for live mode."""


def build_live_stack():
    """Hire-signal default: Deepgram STT → swappable LLM → ElevenLabs TTS.

    OpenAI is NOT the voice stack. It may only appear as an optional LLM_PROVIDER.
    """
    try:
        stt = DeepgramSTT()
        agent = build_llm()
        tts = ElevenLabsTTS()
        return stt, agent, tts
    except ProviderHTTPError as e:
        raise MissingKeyError(str(e)) from e
