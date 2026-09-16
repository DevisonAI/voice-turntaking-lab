# Architecture (Working)

## Principles

1. **Measure before optimize** — every hop gets a timestamp.
2. **Degrade visibly** — if a hop dies, the loop announces and stops or falls back; it does not hang.
3. **Stop rules are explicit** — timeout, error count, or human interrupt.
4. **Providers are adapters** — STT/TTS behind interfaces so logos can change without rewriting the lab.

## Components (v0)

- `AudioIn` — mic capture / file input for reproducible tests
- `STTAdapter` — streaming partials + final
- `AgentAdapter` — LLM turn with optional tools
- `TTSAdapter` — streaming audio out
- `TurnController` — VAD/endpointing/barge-in policy
- `MetricsSink` — JSONL per session → rollup in `metrics/`

## Non-goals (v0)

- Training TTS/STT models
- Multi-tenant production SaaS
- Onsite telephony truck rolls
