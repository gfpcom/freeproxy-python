import respx
import httpx
import pytest

from freeproxy.async_client import AsyncClient


@pytest.mark.asyncio
@respx.mock
async def test_async_query_parses_proxies():
    url = "https://api.getfreeproxy.com/v1/proxies"
    sample = [
        {
            "id": "1",
            "protocol": "socks5",
            "ip": "1.2.3.4",
            "port": 1080,
            "user": None,
            "passwd": None,
            "countryCode": "US",
            "region": "",
            "asnNumber": "AS123",
            "asnName": "ASN",
            "anonymity": "Elite",
            "uptime": 99,
            "responseTime": 0.5,
            "lastAliveAt": "2025-11-18T10:00:00Z",
            "proxyUrl": "socks5://1.2.3.4:1080",
            "https": True,
            "google": True,
        }
    ]

    respx.get(url).mock(return_value=httpx.Response(200, json=sample))

    client = AsyncClient(api_key="KEY")
    out = await client.query()
    assert len(out) == 1
    p = out[0]
    assert p.ip == "1.2.3.4"
    assert p.country_code == "US"
    await client.aclose()
