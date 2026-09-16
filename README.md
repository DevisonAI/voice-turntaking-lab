# voice-turntaking-lab

Realtime voice turn-taking lab for a **remote Voice-AI / agents** portfolio.

**Goal:** Measure and harden a duplex loop — mic → STT → agent/LLM → TTS → speaker — with explicit latency budgets and failure degrade (not a demo that only works on the happy path).

## Status

**v0.1 dry-run:** fake STT / LLM / TTS adapters + hop timers + stop rules. No API keys required.

**v0.1.1 live stubs:** `--live` requires env keys and fails loudly if missing (no fake success).

## Verify (done metric)

```bash
python3 -m src.main --dry-run
python3 -m src.main --dry-run --fail-at tts
python3 -m src.main --dry-run --write-session
python3 -m src.main --live   # requires .env keys; fails loudly if missing
```

Expect a hop latency table. Injected failures print `stop_reason` and exit cleanly.

## Target loop

```
mic → STT (streaming) → agent (LLM + tools) → TTS (streaming) → speaker
         ↑____ VAD / endpointing / barge-in ____↑
```

## Latency budget

See `metrics.md` — fill from session JSONL only. Do not invent numbers.

## Failure modes

- STT timeout / hang (`--fail-at stt`)
- LLM timeout (`--fail-at llm`)
- TTS failure (`--fail-at tts`)
- Explicit **stop rule** via `TurnPolicy` — no silent best judgment
- Missing live keys → loud `stop_reason` (not a quiet fake path)

## Layout

```
src/          # loop + timing + fake/live adapters
metrics/      # session JSONL
metrics.md    # human rollup (empty until measured)
docs/         # architecture notes
```

## Live adapters

Live stubs: `--live` requires `STT_API_KEY` / `LLM_API_KEY` / `TTS_API_KEY` (see `.env.example`). Missing keys → loud `stop_reason`, not a fake success. Real provider calls: next.

## Author

[Devison Kuhlmann](https://github.com/DevisonAI) · [LinkedIn](https://www.linkedin.com/in/david-kuhlmann-b1a2894b/)
