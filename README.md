GetFreeProxy Python client
=================================

Install
-------

```bash
pip install .
```

Usage (sync)
------------

```py
from getfreeproxy import FreeProxyClient

client = FreeProxyClient(api_key="YOUR_API_KEY")
proxies = client.query(country="US", protocol="https")
for p in proxies:
    print(p.proxy_url)
client.close()
```

Usage (async)
-------------

```py
import asyncio
from getfreeproxy import AsyncFreeProxyClient

async def main():
    client = AsyncFreeProxyClient(api_key="YOUR_API_KEY")
    proxies = await client.query(country="US")
    for p in proxies:
        print(p.proxy_url)
    await client.aclose()

asyncio.run(main())
```

Tests
-----

Install dev dependencies and run tests:

```bash
pip install -e .[dev]
pytest -q
```

Publishing
----------

This repository uses a GitHub Actions workflow to publish to PyPI when a tag matching `vX.Y.Z` is pushed.

Preparation (one-time):
- Create a PyPI API token at https://pypi.org/ (Account > API tokens).
- Add the token to GitHub repository secrets as `PYPI_API_TOKEN` (Repository Settings > Secrets).

Release steps (recommended via CI):

1. Bump `version` in `pyproject.toml` to the new release version (for example `0.0.2`).
2. Create a signed or annotated tag and push it:

```bash
git tag -a v0.0.2 -m "Release v0.0.2"
git push origin v0.0.2
```

When the tag is pushed, GitHub Actions will run `.github/workflows/release.yml` and publish the built distributions to PyPI using the `PYPI_API_TOKEN` secret.

You can also build and upload locally (useful for dry-run checks):

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
# then upload (will require PyPI credentials or token):
python -m twine upload dist/*
```

