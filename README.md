GetFreeProxy — Python client
===========================

This is a small, typed Python client for the GetFreeProxy API (https://developer.getfreeproxy.com).

About the API
-------------
The GetFreeProxy API exposes a simple endpoint to fetch public proxy servers:

- GET /v1/proxies — returns a JSON array of proxy objects. Optional query parameters include `country`, `protocol`, and `page`.

Each proxy object contains fields such as `ip`, `port`, `protocol`, `proxyUrl`, `countryCode`, `anonymity`, `uptime`, and timestamps like `lastAliveAt`.

Key behaviours of this client
----------------------------
- Minimal runtime dependency (`httpx`).
- Synchronous `Client` and asynchronous `AsyncClient` classes with simple `query(...)` methods.
- Returns a list of `Proxy` dataclasses (fields mapped to Pythonic names, e.g. `country_code`).
- Raises typed exceptions on errors: `APIError`, `InvalidAPIKey`, `NetworkError`, `TimeoutError`, `ParseError`.

Installation
------------

Install from PyPI (when published) or locally in editable mode during development:

```bash
pip install freeproxy-python
# or local editable install for development:
pip install -e .[dev]
```

Quick examples
--------------

Sync example:

```py
from freeproxy import Client

client = Client(api_key="YOUR_API_KEY")
proxies = client.query(country="US", protocol="https")
for p in proxies:
    print(p.to_url())
client.close()
```

Async example:

```py
import asyncio
from freeproxy import AsyncClient

async def main():
    client = AsyncClient(api_key="YOUR_API_KEY")
    proxies = await client.query(country="US")
    for p in proxies:
        print(p.to_url())
    await client.aclose()

asyncio.run(main())
```

Authentication
--------------
Provide your API key to the client constructor. The client sends `Authorization: Bearer <API_KEY>` in requests.

Query parameters
----------------
- `country`: ISO 3166-1 alpha-2 country code (e.g. `US`).
- `protocol`: proxy protocol filter like `http`, `https`, `socks5`.
- `page`: pagination page index (integer).

Errors and exceptions
---------------------
- `APIError` is raised for non-2xx HTTP responses. The message attempts to surface the API `error` field when present, otherwise it falls back to the response body.
- `InvalidAPIKey` is a subclass used when the API returns HTTP 401.
- `NetworkError` and `TimeoutError` wrap transport-level failures.

Notes and limitations
---------------------
- This client intentionally keeps runtime dependencies minimal and does not implement automatic retries. It also does not stream responses — responses are small (up to ~10 proxies per request).

Testing
-------
Run the test suite locally with:

```bash
pip install -e .[dev]
pytest -q
```

License
-------
MIT


