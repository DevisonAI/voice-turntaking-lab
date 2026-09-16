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

**v0.2.1** — `TurnTakingController` (endpointing + barge-in state machine) with offline tests — the hard duplex part, no keys required.

## Verify

```bash
# no keys
python3 -m src.main --dry-run --audio fixtures/hello.wav
python3 -m src.main --dry-run --fail-at tts
python3 -m src.main --dry-run --write-session

# regenerate synthetic smoke audio if needed
./scripts/make_fixture.sh

# live (requires .env — see .env.example)
cp .env.example .env   # then fill DEEPGRAM_API_KEY, ELEVENLABS_API_KEY, LLM_API_KEY
python3 -m src.main --live --audio fixtures/hello.wav --write-session
python3 -m src.rollup

# turn-taking / barge-in (no keys)
python3 tests/test_turn_taking.py
```

Expect a hop latency table. Failures print `stop_reason` and exit cleanly. **Do not invent numbers** in `metrics.md` — fill from `metrics/sessions/` only. Label whether audio was `fixtures/hello.wav` (synthetic) or your own mic capture.

## Failure modes

- Missing keys → loud `stop_reason` (no fake success)
- STT / LLM / TTS errors → `TurnPolicy` stop
- `--fail-at stt|llm|tts` on dry-run to demo stop rules

## Layout

```
src/adapters/   # fake + deepgram + elevenlabs + llm
src/turn_taking.py  # endpointing + barge-in state machine
tests/          # offline policy tests
fixtures/       # hello.wav via scripts/make_fixture.sh
metrics/        # session JSONL (gitignored)
metrics.md      # human rollup — empty until measured
docs/           # architecture
```

## Author

[Devison Kuhlmann](https://github.com/DevisonAI) · [LinkedIn](https://www.linkedin.com/in/david-kuhlmann-b1a2894b/)
