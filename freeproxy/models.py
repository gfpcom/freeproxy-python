from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Proxy:
    id: str
    protocol: str
    ip: str
    port: int
    user: Optional[str]
    passwd: Optional[str]
    country_code: str
    region: Optional[str]
    asn_number: Optional[str]
    asn_name: Optional[str]
    anonymity: str
    uptime: int
    response_time: float
    last_alive_at: str
    proxy_url: str
    https: bool
    google: bool

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Proxy":
        return cls(
            id=str(d.get("id")),
            protocol=d.get("protocol"),
            ip=d.get("ip"),
            port=int(d.get("port")),
            user=d.get("user"),
            passwd=d.get("passwd"),
            country_code=d.get("countryCode") or d.get("country_code") or "",
            region=d.get("region"),
            asn_number=d.get("asnNumber") or d.get("asn_number"),
            asn_name=d.get("asnName") or d.get("asn_name"),
            anonymity=d.get("anonymity"),
            uptime=int(d.get("uptime") or 0),
            response_time=float(d.get("responseTime") or d.get("response_time") or 0.0),
            last_alive_at=d.get("lastAliveAt") or d.get("last_alive_at") or "",
            proxy_url=d.get("proxyUrl") or d.get("proxy_url") or "",
            https=bool(d.get("https") or False),
            google=bool(d.get("google") or False),
        )

    def to_url(self) -> str:
        if self.proxy_url:
            return self.proxy_url
        auth = f"{self.user}:{self.passwd}@" if self.user and self.passwd else ""
        return f"{self.protocol}://{auth}{self.ip}:{self.port}"
