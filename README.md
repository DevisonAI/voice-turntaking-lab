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

**v0.2** — hire-signal live path: Deepgram → LLM → ElevenLabs, real `--audio` file, hop timers, stop rules, session JSONL + rollup.

## Verify

```bash
# no keys
python3 -m src.main --dry-run --audio fixtures/hello.wav
python3 -m src.main --dry-run --fail-at tts
python3 -m src.main --dry-run --write-session

# live (requires .env — see .env.example)
cp .env.example .env   # then fill DEEPGRAM_API_KEY, ELEVENLABS_API_KEY, LLM_API_KEY
python3 -m src.main --live --audio fixtures/hello.wav --write-session
python3 -m src.rollup
```

Expect a hop latency table. Failures print `stop_reason` and exit cleanly. **Do not invent numbers** in `metrics.md` — fill from `metrics/sessions/` only. Label whether audio was `fixtures/hello.wav` (synthetic) or your own mic capture.

## Failure modes

- Missing keys → loud `stop_reason` (no fake success)
- STT / LLM / TTS errors → `TurnPolicy` stop
- `--fail-at stt|llm|tts` on dry-run to demo stop rules

## Layout

```
src/adapters/   # fake + deepgram + elevenlabs + llm
fixtures/       # hello.wav (espeak synthetic smoke audio)
metrics/        # session JSONL (gitignored)
metrics.md      # human rollup — empty until measured
docs/           # architecture
```

## Author

[Devison Kuhlmann](https://github.com/DevisonAI) · [LinkedIn](https://www.linkedin.com/in/david-kuhlmann-b1a2894b/)
