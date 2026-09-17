from __future__ import annotations

import os

from ..http_util import ProviderHTTPError, http_json


class OpenAIChatAgent:
    """Swappable LLM hop (not the Voice-AI differentiator)."""

    def __init__(self):
        key = (
            os.environ.get("LLM_API_KEY", "").strip()
            or os.environ.get("OPENAI_API_KEY", "").strip()
        )
        if not key:
            raise ProviderHTTPError(
                "missing LLM_API_KEY (or OPENAI_API_KEY) — required for live agent hop"
            )
        self.api_key = key
        self.model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
        self.base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    def reply(self, text: str) -> str:
        data = http_json(
            "POST",
            f"{self.base}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            payload={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a concise voice agent. One short spoken sentence.",
                    },
                    {"role": "user", "content": text or "Say hello briefly."},
                ],
                "max_tokens": 80,
            },
        )
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderHTTPError(f"unexpected LLM response: {data!r}") from e


class AnthropicChatAgent:
    def __init__(self):
        key = (
            os.environ.get("LLM_API_KEY", "").strip()
            or os.environ.get("ANTHROPIC_API_KEY", "").strip()
        )
        if not key:
            raise ProviderHTTPError(
                "missing LLM_API_KEY (or ANTHROPIC_API_KEY) — required for live agent hop"
            )
        self.api_key = key
        self.model = os.environ.get("LLM_MODEL", "claude-3-5-haiku-latest")

    def reply(self, text: str) -> str:
        data = http_json(
            "POST",
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            payload={
                "model": self.model,
                "max_tokens": 80,
                "messages": [{"role": "user", "content": text or "Say hello briefly."}],
                "system": "You are a concise voice agent. One short spoken sentence.",
            },
        )
        try:
            parts = data["content"]
            return "".join(p.get("text", "") for p in parts if p.get("type") == "text").strip()
        except (KeyError, TypeError) as e:
            raise ProviderHTTPError(f"unexpected Anthropic response: {data!r}") from e


def _resolve_llm_key() -> str:
    return (
        os.environ.get("LLM_API_KEY", "").strip()
        or os.environ.get("ANTHROPIC_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )


def build_llm():
    provider = os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()
    key = _resolve_llm_key()
    # Never send an Anthropic key to OpenAI (common .env mix-up).
    if key.startswith("sk-ant-"):
        provider = "anthropic"
    if provider in ("openai", "openai_compatible"):
        return OpenAIChatAgent()
    if provider in ("anthropic", "claude"):
        return AnthropicChatAgent()
    raise ProviderHTTPError(f"unsupported LLM_PROVIDER={provider!r} (openai|anthropic)")
