from __future__ import annotations

import wave
from pathlib import Path


def frame_energies(path: str, frame_ms: int = 30) -> list[tuple[int, float]]:
    """Return (t_ms, rms) for mono PCM wav. Crude energy VAD input — not a production VAD."""
    with wave.open(path, "rb") as w:
        if w.getnchannels() != 1:
            raise ValueError("vad_energy expects mono wav")
        rate = w.getframerate()
        width = w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if width != 2:
        raise ValueError("vad_energy expects 16-bit PCM")
    import array

    samples = array.array("h")
    samples.frombytes(raw)
    frame = max(1, int(rate * frame_ms / 1000))
    out: list[tuple[int, float]] = []
    for i in range(0, len(samples) - frame + 1, frame):
        chunk = samples[i : i + frame]
        acc = sum(int(s) * int(s) for s in chunk) / len(chunk)
        rms = acc**0.5
        t_ms = int(1000 * i / rate)
        out.append((t_ms, rms))
    return out


def energies_to_vad_events(
    energies: list[tuple[int, float]],
    *,
    speech_rms: float = 200.0,
    hangover_frames: int = 3,
) -> list[tuple[str, int]]:
    """Map energy frames to coarse vad_speech / vad_silence events."""
    events: list[tuple[str, int]] = []
    speaking = False
    hang = 0
    for t_ms, rms in energies:
        if rms >= speech_rms:
            hang = hangover_frames
            if not speaking:
                speaking = True
                events.append(("vad_speech", t_ms))
        else:
            if speaking:
                hang -= 1
                if hang <= 0:
                    speaking = False
                    events.append(("vad_silence", t_ms))
    if speaking and energies:
        events.append(("vad_silence", energies[-1][0]))
    return events
