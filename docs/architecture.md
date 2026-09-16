# Architecture (v0.2 hire-signal)

```
--dry-run:  FakeSTT → FakeAgent → FakeTTS
--live:     DeepgramSTT → LLM (openai|anthropic) → ElevenLabsTTS
                 │                │                      │
                 └──────── HopTimer + SessionMetrics ────┘
                                   │
                            TurnPolicy (stop)
                                   │
              metrics/sessions/*.jsonl → python3 -m src.rollup
```

### Design rules

1. Voice hops (STT/TTS) are specialist providers — not “one OpenAI key for everything.”
2. Live mode never falls back to fake adapters.
3. Live STT requires a real audio file (`--audio`). No silence WAV shortcut.
4. `fixtures/hello.wav` is synthetic (espeak) for smoke tests; portfolio latency claims should prefer your own capture and say so in `metrics.md`.

## Turn-taking (v0.2.1)

`src/turn_taking.py` owns duplex policy as an explicit state machine:

`idle → user_speaking → endpointing → agent_speaking ⇄ barge_in → stopped`

It does **not** call providers. The loop asks `should_start_agent()` / `should_cancel_agent()` after VAD events. Wire real VAD next; until then, tests prove the policy.
