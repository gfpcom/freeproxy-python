from typing import List, Optional, Dict
import httpx

from .models import Proxy
from .exceptions import APIError, InvalidAPIKey, NetworkError, TimeoutError, ParseError
from ._utils import build_headers, extract_error_message


class Client:
    def __init__(self, api_key: str, *, base_url: str = "https://api.getfreeproxy.com", timeout: float = 30.0, user_agent: Optional[str] = None, session: Optional[httpx.Client] = None):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent
        self._own_session = session is None
        self.session = session or httpx.Client(timeout=timeout)

    def _handle_error_response(self, response: httpx.Response):
        status = response.status_code
        text = response.text
        try:
            j = response.json()
        except Exception:
            j = None

        msg = extract_error_message(text, j)
        if status == 401:
            raise InvalidAPIKey(status, msg, raw_body=text)
        raise APIError(status, msg, raw_body=text)

    def query(self, country: Optional[str] = None, protocol: Optional[str] = None, page: Optional[int] = None) -> List[Proxy]:
        url = f"{self.base_url}/v1/proxies"
        params: Dict[str, str] = {}
        if country:
            params["country"] = country
        if protocol:
            params["protocol"] = protocol
        if page is not None:
            params["page"] = str(page)

        headers = build_headers(self.api_key, self.user_agent)
        try:
            resp = self.session.get(url, headers=headers, params=params)
        except httpx.ReadTimeout:
            raise TimeoutError("request timed out")
        except httpx.RequestError as e:
            raise NetworkError(str(e))

        if resp.status_code < 200 or resp.status_code >= 300:
            self._handle_error_response(resp)

        try:
            data = resp.json()
        except Exception as e:
            raise ParseError(f"failed to parse JSON response: {e}")

        if not isinstance(data, list):
            raise ParseError("expected JSON array of proxies")

        proxies = [Proxy.from_dict(item) for item in data]
        return proxies

    def query_country(self, country: str) -> List[Proxy]:
        return self.query(country=country)

    def query_protocol(self, protocol: str) -> List[Proxy]:
        return self.query(protocol=protocol)

    def query_page(self, page: int) -> List[Proxy]:
        return self.query(page=page)

    def iter_pages(self, *, start: int = 1):
        page = start
        while True:
            items = self.query(page=page)
            yield items
            if not items:
                break
            page += 1

    def raw_request(self, method: str, path: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = kwargs.pop("headers", None) or build_headers(self.api_key, self.user_agent)
        return self.session.request(method, url, headers=headers, timeout=self.timeout, **kwargs)

    def close(self) -> None:
        if self._own_session:
            self.session.close()
