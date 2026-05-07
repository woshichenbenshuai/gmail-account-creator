from __future__ import annotations

from typing import TYPE_CHECKING

from src.gmail_creator.config import CONFIG

if TYPE_CHECKING:
    from src.gmail_creator.phone.base import SMSProvider


_registry: dict[str, type[SMSProvider]] = {}


def register_provider(name: str, cls: type[SMSProvider]) -> None:
    _registry[name] = cls


def get_provider(name: str | None = None) -> SMSProvider | None:
    provider_name = name or CONFIG.SMS_PROVIDER
    if not provider_name:
        return None
    cls = _registry.get(provider_name)
    if cls is None:
        msg = f"Unknown SMS provider: {provider_name}. Available: {list(_registry)}"
        raise ValueError(msg)
    return cls()


def list_providers() -> list[str]:
    return list(_registry)


class ProviderRegistry:
    @staticmethod
    def register(name: str, cls: type[SMSProvider]) -> None:
        register_provider(name, cls)

    @staticmethod
    def get(name: str | None = None) -> SMSProvider | None:
        return get_provider(name)

    @staticmethod
    def available() -> list[str]:
        return list_providers()
