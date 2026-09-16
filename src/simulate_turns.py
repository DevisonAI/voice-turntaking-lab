from __future__ import annotations

import argparse
from pathlib import Path

from .turn_taking import TurnEvent, TurnTakingController, TurnTakingConfig
from .vad_energy import energies_to_vad_events, frame_energies


def main() -> int:
    p = argparse.ArgumentParser(description="Feed energy-VAD events into TurnTakingController")
    p.add_argument("--audio", default="fixtures/hello.wav")
    p.add_argument("--speech-rms", type=float, default=200.0)
    args = p.parse_args()
    path = Path(args.audio)
    if not path.is_file():
        print(f"stop_reason: audio not found: {path}")
        return 2
    energies = frame_energies(str(path))
    events = energies_to_vad_events(energies, speech_rms=args.speech_rms)
    ctrl = TurnTakingController(TurnTakingConfig())
    print(f"frames={len(energies)} vad_events={len(events)}")
    last_t = 0
    for kind, t in events:
        last_t = t
        state = ctrl.on_event(TurnEvent(kind, t))
        print(f"t={t:5d}  {kind:<12} → {state.value}")
        if kind == "vad_silence":
            for tick in (t + 200, t + 400, t + 650):
                state = ctrl.on_event(TurnEvent("vad_silence", tick))
                print(f"t={tick:5d}  vad_silence  → {state.value}")
                last_t = tick
                if ctrl.should_start_agent():
                    break
        if ctrl.should_start_agent():
            print("  ⇒ should_start_agent")
            ctrl.on_event(TurnEvent("agent_audio_start", last_t + 1))
            print(f"t={last_t+1:5d}  agent_start  → {ctrl.state.value}")
            ctrl.on_event(TurnEvent("vad_speech", last_t + 100))
            print(f"t={last_t+100:5d}  vad_speech   → {ctrl.state.value} cancel={ctrl.should_cancel_agent()}")
            ctrl.on_event(TurnEvent("stop", last_t + 101))
            break
    print(f"final_state={ctrl.state.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
