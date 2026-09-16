# voice-turntaking-lab

Realtime voice turn-taking lab for a **remote Voice-AI / agents** portfolio aimed at **ElevenLabs-class** employers.

**Goal:** Measure and harden a duplex loop — audio → STT → agent/LLM → TTS — with explicit latency budgets and failure degrade (not a demo that only works on the happy path).

## Stack (intentional)

| Hop | Default live provider | Why |
| --- | --- | --- |
| STT | **Deepgram** | Industry voice STT; not bundled into a single LLM vendor |
| LLM | Swappable (`openai` / `anthropic`) | Commodity middle hop — not the hire differentiator |
| TTS | **ElevenLabs** | Matches target employer class |

Dry-run uses fake adapters (no keys). Live **never** silently falls back to fakes.

## Status

**v0.2** — hire-signal live path: Deepgram → LLM → ElevenLabs, real `--audio`, hop timers, stop rules, session JSONL + rollup.

**v0.2.1** — `TurnTakingController` (endpointing + barge-in) + offline tests.

**v0.2.2** — energy-VAD stub + `python3 -m src.simulate_turns` feeding the turn machine (endpoint → agent → barge-in demo).

## Verify

```bash
# no keys
python3 -m src.main --dry-run --audio fixtures/hello.wav
python3 -m src.main --dry-run --fail-at tts
python3 -m src.main --dry-run --write-session
./scripts/make_fixture.sh

# turn-taking
python3 tests/test_turn_taking.py
python3 -m src.simulate_turns --audio fixtures/hello.wav

# live (requires .env)
cp .env.example .env
python3 -m src.main --live --audio fixtures/hello.wav --write-session
python3 -m src.rollup
```

**Do not invent numbers** in `metrics.md` — fill from `metrics/sessions/` only.

## Author

[Devison Kuhlmann](https://github.com/DevisonAI) · [LinkedIn](https://www.linkedin.com/in/david-kuhlmann-b1a2894b/)
