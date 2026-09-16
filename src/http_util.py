from __future__ import annotations

import json
import urllib.error
import urllib.request


class ProviderHTTPError(RuntimeError):
    pass


def http_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str],
    data: bytes | None = None,
    timeout: float = 90.0,
) -> bytes:
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:800]
        raise ProviderHTTPError(f"HTTP {e.code} {url}: {body}") from e
    except urllib.error.URLError as e:
        raise ProviderHTTPError(f"network error {url}: {e}") from e


def http_json(method: str, url: str, *, headers: dict[str, str], payload: dict, timeout: float = 90.0) -> dict:
    raw = http_request(
        method,
        url,
        headers={**headers, "Content-Type": "application/json"},
        data=json.dumps(payload).encode(),
        timeout=timeout,
    )
    return json.loads(raw.decode())
