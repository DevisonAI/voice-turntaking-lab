# voice-turntaking-lab

Realtime voice turn-taking lab for a **remote Voice-AI / agents** portfolio.

**Goal:** Measure and harden a duplex loop — mic → STT → agent/LLM → TTS → speaker — with explicit latency budgets and failure degrade (not a demo that only works on the happy path).

## Why this exists

Voice-AI hiring screens for production instincts: end-of-utterance → first audio latency, barge-in / turn-taking, and explainable failures. This repo is the practice ground and the proof.

## Status

Scaffold. First runnable loop and `metrics.md` from real sessions come next.

## Target loop

```
mic → STT (streaming) → agent (LLM + tools) → TTS (streaming) → speaker
         ↑____ VAD / endpointing / barge-in ____↑
```

## Latency budget (fill with measured numbers)

| Hop | Budget (ms) | Measured p50 | Measured p95 |
| --- | --- | --- | --- |
| End of utterance → STT final | TBD | — | — |
| STT → LLM first token | TBD | — | — |
| LLM → TTS first audio | TBD | — | — |
| **E2E end-of-utterance → first audio** | TBD | — | — |

## Failure modes (must demonstrate)

- STT timeout / hang
- LLM timeout
- TTS failure
- Clear **stop rule** (human or automatic) — no silent “best judgment”

## Stack (v0 intent)

- Python 3.11+
- One STT provider + one TTS provider (swappable)
- Optional: LiveKit / WebRTC path after local loop works
- No claim of training speech models

## Layout

```
src/          # loop + timing
metrics/      # session exports → metrics.md
evals/        # later (Flagship 2)
docs/         # architecture notes
```

## Run

Coming with first skeleton (`pip install` + `.env.example`).

## Author

[Devison Kuhlmann](https://github.com/DevisonAI) · [LinkedIn](https://www.linkedin.com/in/david-kuhlmann-b1a2894b/)
