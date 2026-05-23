from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from src.gmail_creator.config import CONFIG

HOSTING_KEYWORDS = (
    "amazon",
    "aws",
    "azure",
    "cloud",
    "data center",
    "datacenter",
    "digitalocean",
    "google",
    "hetzner",
    "hosting",
    "linode",
    "microsoft",
    "oracle",
    "ovh",
    "proxy",
    "server",
    "tencent",
    "vps",
    "vpn",
)


@dataclass(frozen=True)
class IpCheckResult:
    ok: bool
    ip: str
    country: str
    city: str
    region: str
    org: str
    timezone: str
    source: str
    warnings: list[str]
    error: str = ""


def _proxy_config() -> dict[str, str] | None:
    if not CONFIG.PROXY_ENABLED or not CONFIG.PROXY_SERVER:
        return None
    return {
        "http": CONFIG.PROXY_SERVER,
        "https": CONFIG.PROXY_SERVER,
    }


def _looks_like_hosting(org: str) -> bool:
    normalized = org.lower()
    return any(keyword in normalized for keyword in HOSTING_KEYWORDS)


def check_current_ip(timeout: int = 12) -> IpCheckResult:
    proxies = _proxy_config()
    source = "proxy" if proxies else "direct"

    try:
        response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=timeout)
        response.raise_for_status()
        data: dict[str, Any] = response.json()
    except Exception as exc:
        return IpCheckResult(
            ok=False,
            ip="",
            country="",
            city="",
            region="",
            org="",
            timezone="",
            source=source,
            warnings=[],
            error=str(exc),
        )

    country = str(data.get("country", "")).upper()
    org = str(data.get("org", ""))
    warnings: list[str] = []

    expected = [country_code.upper() for country_code in CONFIG.IP_CHECK_EXPECTED_COUNTRIES]
    if expected and country not in expected:
        warnings.append(f"Country mismatch: expected {', '.join(expected)}, got {country or 'unknown'}.")

    if _looks_like_hosting(org):
        warnings.append("Network owner looks like hosting/proxy/VPN infrastructure.")

    return IpCheckResult(
        ok=not warnings,
        ip=str(data.get("ip", "")),
        country=country,
        city=str(data.get("city", "")),
        region=str(data.get("region", "")),
        org=org,
        timezone=str(data.get("timezone", "")),
        source=source,
        warnings=warnings,
    )
