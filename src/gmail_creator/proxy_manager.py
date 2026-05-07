from __future__ import annotations

from src.gmail_creator.config import CONFIG


def get_proxy_options() -> dict[str, str | dict[str, str]] | None:
    if not CONFIG.PROXY_ENABLED:
        return None
    try:
        from fp.fp import FreeProxy

        proxy = FreeProxy(country_id=["US", "GB", "DE"], rand=True).get()
        if proxy:
            return {"proxy": {"http": proxy, "https": proxy}}
    except Exception:
        pass
    return None
