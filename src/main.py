from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .adapters.fake import FakeAgent, FakeSTT, FakeTTS
from .timing import HopTimer, SessionMetrics
from .turn_controller import TurnPolicy


def run_session(fail_at: str | None = None) -> SessionMetrics:
    metrics = SessionMetrics()
    policy = TurnPolicy(max_hop_failures=1)
    failures = 0

    stt = FakeSTT(fail=(fail_at == "stt"))
    agent = FakeAgent(fail=(fail_at == "llm"))
    tts = FakeTTS(fail=(fail_at == "tts"))

    # Hop 1: STT
    hop = HopTimer("end_utt→stt_final")
    try:
        text = stt.transcribe("dry-run")
        hop.stop(ok=True, note="fake-stt")
        metrics.add(hop)
    except Exception as e:
        hop.stop(ok=False, note=str(e))
        metrics.add(hop)
        failures += 1
        stop, reason = policy.should_stop(failures, "stt")
        if stop:
            metrics.stop_reason = reason
            return metrics
        text = ""

    # Hop 2: Agent
    hop = HopTimer("stt→llm_first_token")
    try:
        reply = agent.reply(text)
        hop.stop(ok=True, note="fake-llm")
        metrics.add(hop)
    except Exception as e:
        hop.stop(ok=False, note=str(e))
        metrics.add(hop)
        failures += 1
        stop, reason = policy.should_stop(failures, "llm")
        if stop:
            metrics.stop_reason = reason
            return metrics
        reply = ""

    # Hop 3: TTS
    hop = HopTimer("llm→tts_first_audio")
    try:
        audio = tts.synthesize(reply)
        hop.stop(ok=True, note=audio)
        metrics.add(hop)
    except Exception as e:
        hop.stop(ok=False, note=str(e))
        metrics.add(hop)
        failures += 1
        stop, reason = policy.should_stop(failures, "tts")
        if stop:
            metrics.stop_reason = reason
            return metrics

    metrics.stop_reason = "complete"
    return metrics


def write_session_jsonl(metrics: SessionMetrics, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"session_{stamp}.jsonl"
    record = {
        "ts": stamp,
        "stop_reason": metrics.stop_reason,
        "e2e_ms": round(metrics.e2e_ms(), 2),
        "hops": [
            {"name": h.name, "ms": round(h.ms, 2), "ok": h.ok, "note": h.note}
            for h in metrics.hops
        ],
    }
    path.write_text(json.dumps(record) + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="voice-turntaking-lab")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run fake STT/LLM/TTS adapters (no API keys).",
    )
    parser.add_argument(
        "--fail-at",
        choices=["stt", "llm", "tts"],
        default=None,
        help="Inject a hop failure to demo stop rules.",
    )
    parser.add_argument(
        "--write-session",
        action="store_true",
        help="Write metrics/sessions/*.jsonl",
    )
    args = parser.parse_args()

    if not args.dry_run:
        print("Use --dry-run for the no-key lab loop. Live adapters: coming next.")
        return 2

    metrics = run_session(fail_at=args.fail_at)
    print(metrics.table())
    if args.write_session:
        root = Path(__file__).resolve().parents[1]
        path = write_session_jsonl(metrics, root / "metrics" / "sessions")
        print(f"wrote {path}")
    return 0 if metrics.stop_reason in ("complete",) or metrics.stop_reason.startswith("stop:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
