# Architecture (v0.1)

```
audio_in → FakeSTT → FakeAgent → FakeTTS → audio_out (label)
              │           │          │
              └──── HopTimer + SessionMetrics ────┘
                         │
                   TurnPolicy (stop)
```

Live adapters replace Fake* behind the same call shapes. Metrics are hop-sum only until multi-session p50/p95 is added.
